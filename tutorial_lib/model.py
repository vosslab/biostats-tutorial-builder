"""Shared semantic contracts for tutorial compilation and exporters."""

import pathlib
import dataclasses


@dataclasses.dataclass(frozen=True)
class SourceSpan:
	path: str
	start_line: int
	end_line: int


@dataclasses.dataclass(frozen=True)
class Diagnostic:
	severity: str
	category: str
	span: SourceSpan
	message: str
	correction: str
	worksheet: str | None = None
	address: str | None = None
	related: SourceSpan | None = None


@dataclasses.dataclass(frozen=True)
class Scalar:
	kind: str
	value: str | int | float | bool | None


@dataclasses.dataclass(frozen=True)
class CellReference:
	sheet: str
	start_row: int
	start_column: int
	end_row: int
	end_column: int
	address: str


@dataclasses.dataclass(frozen=True)
class CellSeed:
	row: int
	column: int
	scalar: Scalar
	span: SourceSpan


@dataclasses.dataclass(frozen=True)
class TableRegion:
	start_row: int
	start_column: int
	end_row: int
	end_column: int
	span: SourceSpan


@dataclasses.dataclass(frozen=True)
class GoogleMapping:
	url: str
	spreadsheet_id: str
	gid: str | None


@dataclasses.dataclass(frozen=True)
class RoleRegion:
	role: str
	reference: CellReference
	span: SourceSpan


@dataclasses.dataclass
class Worksheet:
	name: str
	span: SourceSpan
	cells: dict[tuple[int, int], CellSeed] = dataclasses.field(default_factory=dict)
	regions: list[TableRegion] = dataclasses.field(default_factory=list)
	entry_cells: set[tuple[int, int]] = dataclasses.field(default_factory=set)
	google: GoogleMapping | None = None
	role_regions: list[RoleRegion] = dataclasses.field(default_factory=list)
	is_reflection: bool = False


@dataclasses.dataclass(frozen=True)
class ReflectionQuestion:
	text: str
	span: SourceSpan
	children: list


@dataclasses.dataclass
class Action:
	kind: str
	span: SourceSpan
	token_index: int
	payload: str
	target: CellReference | None = None
	scalar: Scalar | None = None
	menu: list[str] = dataclasses.field(default_factory=list)
	worksheet: str | None = None
	alternative_group: int | None = None
	alternative_branch: int | None = None
	generated_actions: list["Action"] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(frozen=True)
class Heading:
	level: int
	title: str
	display: str
	slug: str
	span: SourceSpan
	token_index: int
	kind: str = "informational"
	number: str | None = None
	prefix_length: int = 0


@dataclasses.dataclass(frozen=True)
class FormulaCheck:
	formula: str
	span: SourceSpan
	status: str
	references: tuple[CellReference, ...]
	limitations: tuple[str, ...]


@dataclasses.dataclass
class Document:
	path: pathlib.Path
	source: str
	title: str = ""
	tokens: list = dataclasses.field(default_factory=list)
	worksheets: list[Worksheet] = dataclasses.field(default_factory=list)
	actions: list[Action] = dataclasses.field(default_factory=list)
	headings: list[Heading] = dataclasses.field(default_factory=list)
	diagnostics: list[Diagnostic] = dataclasses.field(default_factory=list)
	formula_checks: list[FormulaCheck] = dataclasses.field(default_factory=list)
	assets: list[pathlib.Path] = dataclasses.field(default_factory=list)
	content_token_indices: list[int] = dataclasses.field(default_factory=list)
	reflection_questions: list[ReflectionQuestion] = dataclasses.field(default_factory=list)
	reflection_part_number: int | None = None

	@property
	def has_errors(self) -> bool:
		return any(item.severity == "error" for item in self.diagnostics)
