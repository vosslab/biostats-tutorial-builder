#!/usr/bin/env python3
"""Compile single-source Markdown tutorials and student workbooks."""

# Standard library
import sys
import pathlib
import argparse

# Local modules
import tutorial_lib.build
import tutorial_lib.compiler
import tutorial_lib.workbook
import tutorial_lib.worksheet_edit


#============================================
def main(argv: list[str] | None = None) -> int:
	"""Run lint, staged build, or one-time workbook import."""
	parser = argparse.ArgumentParser(description=__doc__)
	commands = parser.add_subparsers(dest="command", required=True)
	lint = commands.add_parser("lint", help="Validate without writing deliverables")
	lint.add_argument("source", type=pathlib.Path)
	build = commands.add_parser("build", help="Generate a verified output bundle")
	build.add_argument("sources", nargs="+", type=pathlib.Path,
		help="One or more Markdown tutorials sharing a workbook")
	build.add_argument("--format", "-f", choices=tutorial_lib.build.FORMATS, default="all")
	build.add_argument("--output-dir", "-o", type=pathlib.Path)
	build.add_argument("--workbook-name", help="Name the generated shared workbook")
	importer = commands.add_parser("import-xlsx", help="Create a Markdown draft from an XLSX")
	importer.add_argument("source", type=pathlib.Path)
	importer.add_argument("--output", "-o", type=pathlib.Path, required=True)
	editor = commands.add_parser("worksheet-edit",
		help="Preview a coordinated worksheet-coordinate maintenance edit")
	editor.add_argument("source", type=pathlib.Path)
	editor.add_argument("--sheet", required=True, help="Declared worksheet name")
	editor.add_argument("--write", action="store_true", help="Atomically write the compiled preview")
	edit_commands = editor.add_subparsers(dest="worksheet_edit", required=True)
	insert_rows = edit_commands.add_parser("insert-rows", help="Insert worksheet rows")
	insert_rows.add_argument("--at", type=int, required=True)
	insert_rows.add_argument("--count", type=int, required=True)
	insert_columns = edit_commands.add_parser("insert-columns", help="Insert worksheet columns")
	insert_columns.add_argument("--at", required=True, help="Column letter or number")
	insert_columns.add_argument("--count", type=int, required=True)
	move_range = edit_commands.add_parser("move-range", help="Move a worksheet rectangle")
	move_range.add_argument("--range", dest="source_range", required=True)
	move_range.add_argument("--destination", required=True)
	resize = edit_commands.add_parser("resize-observations", help="Resize a supplied data table")
	resize.add_argument("--data-range", required=True)
	resize.add_argument("--rows", type=int, required=True)
	# Authors naturally append the confirmation flag after the operation.  Keep
	# the parent spelling too, so both command orders are accepted.
	for command in (insert_rows, insert_columns, move_range, resize):
		command.add_argument("--write", action="store_true", default=argparse.SUPPRESS,
			help=argparse.SUPPRESS)
	args = parser.parse_args(argv)
	if args.command == "import-xlsx":
		if args.output.exists() or args.output.is_symlink():
			raise FileExistsError(f"Import destination already exists: {args.output}")
		draft = tutorial_lib.workbook.import_workbook(args.source)
		with args.output.open("x", encoding="utf-8") as handle:
			handle.write(draft)
		print(f"Wrote draft {args.output}; author the Tutorial scaffold before building.")
		return 0
	if args.command == "worksheet-edit":
		try:
			at = getattr(args, "at", None)
			if args.worksheet_edit == "insert-columns":
				at = tutorial_lib.worksheet_edit.column_number(args.at)
			request = tutorial_lib.worksheet_edit.WorksheetEdit(args.worksheet_edit, args.sheet,
				at=at, count=getattr(args, "count", None),
				source_range=getattr(args, "source_range", None),
				destination=getattr(args, "destination", None),
				data_range=getattr(args, "data_range", None), rows=getattr(args, "rows", None))
			result = tutorial_lib.worksheet_edit.prepare_edit(args.source, request)
		except tutorial_lib.worksheet_edit.WorksheetEditError as error:
			print(f"worksheet-edit: {error}", file=sys.stderr)
			return 1
		print(result.diff, end="")
		for notice in result.notices:
			print(f"Review: {notice}", file=sys.stderr)
		if args.write:
			tutorial_lib.worksheet_edit.write_edit(args.source, result)
			print(f"Updated {args.source}")
		else:
			print("Preview only; rerun with --write to replace the source.", file=sys.stderr)
		return 0
	documents = ([tutorial_lib.compiler.compile_document(source) for source in args.sources]
		if args.command == "build" else [tutorial_lib.compiler.compile_document(args.source)])
	for document in documents:
		for item in document.diagnostics:
			location = f"{item.span.path}:{item.span.start_line}"
			print(f"{location}: {item.severity} [{item.category}] {item.message}", file=sys.stderr)
			print(f"  Correction: {item.correction}", file=sys.stderr)
	if any(document.has_errors for document in documents):
		return 1
	if args.command == "build":
		destination = args.output_dir
		if destination is None:
			destination = pathlib.Path("tutorial_output") / args.sources[0].stem
		published = tutorial_lib.build.build_documents(documents, destination, args.format,
			workbook_name=args.workbook_name)
		print(f"Published {published}")
	else:
		print("Offline lint passed; Google import, navigation, and calculation are unchecked.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
