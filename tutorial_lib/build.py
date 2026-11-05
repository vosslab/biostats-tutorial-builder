"""Staged tutorial bundles and fingerprint-based publication protection."""

# Standard library
import json
import shutil
import hashlib
import pathlib
import zipfile
import tempfile
import dataclasses
import collections.abc

# PIP modules
import defusedxml.ElementTree

# Local modules
import tutorial_lib.model
import tutorial_lib.workbook
import tutorial_lib.pdf_export
import tutorial_lib.docx_renderer
import tutorial_lib.reflections


OWNER = "markdown-to-tutorial"
FORMATS = {"all": ("docx", "xlsx", "pdf"), "docx,xlsx": ("docx", "xlsx"),
	"docx": ("docx",), "xlsx": ("xlsx",)}


#============================================
def fingerprint(path: pathlib.Path) -> str:
	"""Return a streaming SHA256 fingerprint of one file."""
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(65536), b""):
			digest.update(chunk)
	return digest.hexdigest()


#============================================
def run_stage(name: str, operation: collections.abc.Callable, *parameters: object) -> None:
	"""Attach build context while preserving the original exception and cause."""
	try:
		operation(*parameters)
	except Exception as error:
		error.add_note(f"Tutorial build failed during {name}; previous bundle was preserved.")
		raise


#============================================
def verify_docx(path: pathlib.Path) -> None:
	"""Reopen the DOCX package and parse its document and relationship XML."""
	with zipfile.ZipFile(path) as package:
		if package.testzip() is not None:
			raise ValueError("Generated DOCX contains a corrupt ZIP member.")
		defusedxml.ElementTree.fromstring(package.read("word/document.xml"))
		defusedxml.ElementTree.fromstring(package.read("[Content_Types].xml"))
		for name in package.namelist():
			if name.endswith(".rels"):
				defusedxml.ElementTree.fromstring(package.read(name))


#============================================
def check_destination(destination: pathlib.Path, inputs: list[pathlib.Path]) -> None:
	"""Refuse input destruction, foreign directories, and edited generated files."""
	if destination.is_symlink():
		raise ValueError(f"Bundle destination cannot be a symlink: {destination}")
	for source in inputs:
		if source.resolve().is_relative_to(destination.resolve()):
			raise ValueError(f"Bundle destination contains an input: {source}")
	if not destination.exists():
		return
	manifest_path = destination / "validation.json"
	if not destination.is_dir() or not manifest_path.is_file() or manifest_path.is_symlink():
		raise ValueError(f"Destination is not an owned tutorial bundle: {destination}")
	manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
	if manifest.get("owner") != OWNER or manifest.get("schema_version") != 1:
		raise ValueError(f"Destination has no supported ownership manifest: {destination}")
	outputs = manifest["outputs"]
	expected = set(outputs) | {"validation.json"}
	if set(item.name for item in destination.iterdir()) != expected:
		raise ValueError(f"Bundle has added or removed files; preserve edits first: {destination}")
	for name, record in outputs.items():
		path = destination / name
		if pathlib.Path(name).name != name or path.is_symlink() or not path.is_file():
			raise ValueError(f"Unsafe generated artifact in ownership manifest: {name}")
		if fingerprint(path) != record["sha256"]:
			raise ValueError(f"Generated artifact was modified; preserve edits first: {path}")


#============================================
def validation_report(document: tutorial_lib.model.Document) -> dict:
	"""Describe offline coverage without implying external acceptance."""
	report = {
		"owner": OWNER, "schema_version": 1,
		"source": {"path": str(document.path.resolve()),
			"sha256": fingerprint(document.path)},
		"assets": [{"path": str(path.resolve()), "sha256": fingerprint(path)}
			for path in document.assets],
		"diagnostics": [dataclasses.asdict(item) for item in document.diagnostics],
		"reference_coverage": {
			"formula_checks": [dataclasses.asdict(item) for item in document.formula_checks],
			"scope": "Offline structure, references, and instruction consistency only",
		},
		"external_behavior": {
			"google_import": "unchecked", "link_navigation": "unchecked",
			"formula_calculation": "unchecked", "pdf_visual_review": "unchecked",
		},
		"outputs": {},
	}
	return report


#============================================
def _reference_key(reference: tutorial_lib.model.CellReference) -> tuple:
	"""Return the authored identity of a worksheet reference without its span."""
	return (reference.sheet, reference.start_row, reference.start_column,
		reference.end_row, reference.end_column, reference.address)


#============================================
def _action_groups(actions: list[tutorial_lib.model.Action]) -> set[int]:
	"""Collect source-local alternative identifiers, including generated fills."""
	groups = set()
	for action in actions:
		if action.alternative_group is not None:
			groups.add(action.alternative_group)
		groups.update(_action_groups(action.generated_actions))
	return groups


#============================================
def _rebase_action(action: tutorial_lib.model.Action, groups: dict[int, int]) -> tutorial_lib.model.Action:
	"""Copy one action into bundle-wide alternative-group numbering."""
	children = [_rebase_action(item, groups) for item in action.generated_actions]
	group = action.alternative_group
	return dataclasses.replace(action, alternative_group=groups.get(group, group),
		generated_actions=children)


#============================================
def _references_overlap(left: tutorial_lib.model.CellReference,
	right: tutorial_lib.model.CellReference) -> bool:
	"""Return whether two rectangle references share at least one cell."""
	return (left.start_row <= right.end_row and right.start_row <= left.end_row
		and left.start_column <= right.end_column and right.start_column <= left.end_column)


#============================================
def merge_documents(documents: list[tutorial_lib.model.Document]) -> tutorial_lib.model.Document:
	"""Combine compatible worksheet declarations for one shared workbook."""
	if not documents:
		raise ValueError("At least one compiled tutorial is required.")
	documents = tutorial_lib.reflections.resolve_documents(documents)
	worksheets = []
	by_name = {}
	actions = []
	next_group = 1
	for document in documents:
		group_map = {group: next_group + offset
			for offset, group in enumerate(sorted(_action_groups(document.actions)))}
		next_group += len(group_map)
		for action in (_rebase_action(item, group_map) for item in document.actions):
			actions.append(action)
		for source in document.worksheets:
			key = source.name.casefold()
			target = by_name.get(key)
			if target is None:
				target = tutorial_lib.model.Worksheet(source.name, source.span,
					cells=dict(source.cells), regions=list(source.regions),
					entry_cells=set(source.entry_cells), google=source.google,
					role_regions=list(source.role_regions))
				target.is_reflection = source.is_reflection
				by_name[key] = target
				worksheets.append(target)
				continue
			if target.name != source.name:
				raise ValueError(f"Worksheet names differ only by case: {target.name!r}, {source.name!r}")
			if target.is_reflection or source.is_reflection:
				raise ValueError(f"Generated reflection worksheet name collision: {source.name}")
			if target.google != source.google and target.google is not None and source.google is not None:
				raise ValueError(f"Conflicting Google mapping for worksheet {source.name!r}")
			if target.google is None:
				target.google = source.google
			for address, seed in source.cells.items():
				existing = target.cells.get(address)
				if existing is not None and existing.scalar != seed.scalar:
					row, column = address
					raise ValueError(f"Conflicting values for {source.name}!R{row}C{column}")
				target.cells.setdefault(address, seed)
			target.entry_cells.update(source.entry_cells)
			for region in source.regions:
				if not any((item.start_row, item.start_column, item.end_row, item.end_column)
					== (region.start_row, region.start_column, region.end_row, region.end_column)
					for item in target.regions):
					target.regions.append(region)
			for region in source.role_regions:
				if any(item.role != region.role and _references_overlap(item.reference,
					region.reference) for item in target.role_regions):
					raise ValueError(f"Conflicting roles for worksheet {source.name!r}")
				if not any(item.role == region.role and _reference_key(item.reference)
					== _reference_key(region.reference) for item in target.role_regions):
					target.role_regions.append(region)
	# Shared data leads; each lesson's action targets precede its reflection tab.
	work_sheets = [{action.target.sheet.casefold() for action in document.actions
		if action.target is not None} for document in documents]
	owned = set().union(*work_sheets)
	ordered = [sheet for sheet in worksheets
		if not sheet.is_reflection and sheet.name.casefold() not in owned]
	for document, names in zip(documents, work_sheets):
		for sheet in document.worksheets:
			if sheet.is_reflection or sheet.name.casefold() in names:
				target = by_name[sheet.name.casefold()]
				if target not in ordered:
					ordered.append(target)
	return dataclasses.replace(documents[0], worksheets=ordered, actions=actions)


#============================================
def _record_output(report: dict, path: pathlib.Path, extension: str) -> None:
	"""Record one verified output in the ownership manifest."""
	if not path.is_file() or path.stat().st_size == 0:
		raise RuntimeError(f"Exporter produced no {extension.upper()} artifact.")
	report["outputs"][path.name] = {
		"sha256": fingerprint(path), "status": "generated",
		"verification": "serialized values and types" if extension == "xlsx"
		else "conversion and PDF page-tree parse" if extension == "pdf"
		else "ZIP integrity and document/relationship XML parse",
	}


#============================================
def publish(staging: pathlib.Path, destination: pathlib.Path) -> None:
	"""Swap a verified bundle, rolling back if the final rename fails."""
	if not destination.exists():
		staging.rename(destination)
		return
	backup = pathlib.Path(tempfile.mkdtemp(prefix=".tutorial-backup-", dir=destination.parent))
	previous = backup / "bundle"
	destination.rename(previous)
	try:
		staging.rename(destination)
	except OSError:
		# If rollback itself fails, retain the backup for explicit recovery.
		previous.rename(destination)
		backup.rmdir()
		raise
	shutil.rmtree(backup)


#============================================
def build_document(document: tutorial_lib.model.Document, destination: pathlib.Path,
	formats: str = "all") -> pathlib.Path:
	"""Verify every requested format before publishing any of them."""
	return build_documents([document], destination, formats)


#============================================
def build_documents(documents: list[tutorial_lib.model.Document], destination: pathlib.Path,
	formats: str = "all", workbook_name: str | None = None) -> pathlib.Path:
	"""Publish separate tutorial documents and one compatible shared workbook."""
	if not documents:
		raise ValueError("At least one compiled tutorial is required.")
	if any(document.has_errors for document in documents):
		raise ValueError("Validation errors prevent artifact publication.")
	requested = FORMATS[formats]
	stems = [document.path.stem for document in documents]
	if len(stems) != len(set(stems)):
		raise ValueError("Tutorial source basenames must be unique in a shared bundle.")
	inputs = [path for document in documents for path in [document.path, *document.assets]]
	for document in documents:
		if document.path.read_text(encoding="utf-8") != document.source:
			raise ValueError("Source changed after compilation; retry the build.")
	workbook_document = merge_documents(documents)
	documents = tutorial_lib.reflections.resolve_documents(documents)
	report = validation_report(documents[0])
	if len(documents) > 1:
		report["diagnostics"] = [dataclasses.asdict(item)
			for document in documents for item in document.diagnostics]
		report["reference_coverage"]["formula_checks"] = [dataclasses.asdict(item)
			for document in documents for item in document.formula_checks]
		report["sources"] = [{"path": str(document.path.resolve()),
			"sha256": fingerprint(document.path)} for document in documents]
		report["assets"] = [{"path": str(path.resolve()), "sha256": fingerprint(path)}
			for document in documents for path in document.assets]
	destination = pathlib.Path(destination).absolute()
	check_destination(destination, inputs)
	destination.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory(prefix=".tutorial-stage-", dir=destination.parent) as temporary:
		staging = pathlib.Path(temporary) / "bundle"
		staging.mkdir()
		if "docx" in requested:
			for document in documents:
				docx_path = staging / f"{document.path.stem}.docx"
				run_stage("DOCX rendering", tutorial_lib.docx_renderer.write_document,
					document, docx_path)
				run_stage("DOCX package verification", verify_docx, docx_path)
		if "xlsx" in requested:
			workbook_name = workbook_name or ("workbook.xlsx" if len(documents) > 1
				else f"{documents[0].path.stem}.xlsx")
			if pathlib.Path(workbook_name).name != workbook_name or not workbook_name.endswith(".xlsx"):
				raise ValueError("Workbook name must be a plain .xlsx filename.")
			workbook_path = staging / workbook_name
			run_stage("XLSX rendering", tutorial_lib.workbook.write_workbook,
				workbook_document, workbook_path)
			run_stage("XLSX verification", tutorial_lib.workbook.verify_workbook,
				workbook_document, workbook_path)
		if "pdf" in requested:
			for document in documents:
				run_stage("LibreOffice PDF conversion", tutorial_lib.pdf_export.export_pdf,
					staging / f"{document.path.stem}.docx",
					staging / f"{document.path.stem}.pdf")
		for document in documents:
			if "docx" in requested:
				_record_output(report, staging / f"{document.path.stem}.docx", "docx")
			if "pdf" in requested:
				_record_output(report, staging / f"{document.path.stem}.pdf", "pdf")
		if "xlsx" in requested:
			_record_output(report, workbook_path, "xlsx")
		(staging / "validation.json").write_text(
			json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
		)
		# Recheck after rendering so edits made while building cannot be overwritten.
		check_destination(destination, inputs)
		for path in inputs:
			if not path.is_file():
				raise ValueError(f"Input changed while building: {path}; retry the build.")
		for source in report["assets"] + [report["source"]]:
			if fingerprint(pathlib.Path(source["path"])) != source["sha256"]:
				raise ValueError(f"Input changed while building: {source['path']}; retry the build.")
		if len(documents) > 1:
			for source in report["sources"]:
				if fingerprint(pathlib.Path(source["path"])) != source["sha256"]:
					raise ValueError(f"Input changed while building: {source['path']}; retry the build.")
		publish(staging, destination)
	return destination
