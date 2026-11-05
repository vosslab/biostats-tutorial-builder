# Use formulas

Use ordinary spreadsheet formulas in source and explain what they mean in your own tutorial. This
page documents compiler behavior; it does not choose a statistical method or research question.

Return to [../AUTHORING_GUIDE.md](../AUTHORING_GUIDE.md) or
[../FORMATTING_GUIDE.md](../FORMATTING_GUIDE.md).

## Put a formula in an instruction

Type this Markdown:

```markdown
#### Step: Enter a formula

1. In cell E2, enter:
   [`=AVERAGE(A2:A6)`](enter:E2)
```

The reader sees the cell and formula. The `enter:E2` target connects the visible instruction to
the blank workbook cell. It does not appear as a separate link in the document.

<!-- screenshots:begin (managed by screenshot-docs) -->
![Generated instruction to enter an AVERAGE formula in cell E2](../screenshots/authoring_enter.webp)
<!-- screenshots:end -->

A formula begins with `=`. Put one entry or replacement formula on its own line below its named
destination. The formula input range and the action target do different jobs:
`A2:A6` supplies values and `E2` receives the result.

## Fill a repeated formula

Type this Markdown:

```markdown
#### Step: Fill a column

1. In cell B2, enter:
   [`=A2^2`](enter:B2)
2. [Fill B2:B6](fill:B2:B6) down.
```

<!-- screenshots:begin (managed by screenshot-docs) -->
![Generated formula-entry and fill-down instructions](../screenshots/authoring_fill.webp)
<!-- screenshots:end -->

The first formula must exist before the fill. The range includes the formula cell and every target
row. Relative references change as a spreadsheet fills: the formula in B3 becomes `=A3^2`.

Use `$` only when a reference must stay fixed during copying, such as `=A2-$E$3`. The compiler
preserves formula text and checks supported static references; it does not calculate formulas.

## Keep formulas and values distinct

| Source in a Workbook cell or Enter/Replace payload | Meaning |
| --- | --- |
| `=AVERAGE(A2:A6)` | Formula |
| `AVERAGE(A2:A6)` | Text |
| `"=AVERAGE(A2:A6)"` | Literal text |
| `0` | Numeric zero |
| Empty table cell | Blank cell |

A formula in Workbook is prefilled. A formula in an `enter:` action stays blank in the starter
workbook. Use one choice deliberately.

Generated numeric, formula, and blank work cells display three decimal places. Percentages and
scientific notation require an explicit instructional choice. See [ACTIONS.md](ACTIONS.md) for
action syntax and [../TUTORIAL_SPEC.md](../TUTORIAL_SPEC.md) for formula limits.

## Display a formula without an action

Use a code span such as `=AVERAGE(A2:A6)` in prose when you only want to show the formula.
The compiler styles it without assigning a destination. A fenced `sheets` block can display a
longer formula on its own line:

````markdown
```sheets
=AVERAGE(A2:A6)
```
````

Keep one logical formula on one source line; Word handles visual wrapping. Quotes in ordinary
Tutorial prose do not invoke the Workbook's JSON scalar rules.

## Write explanatory mathematics

Use dollar-delimited TeX for an equation that students read rather than enter into a spreadsheet:

```markdown
$y = ax^2 + bx + c$
```

The DOCX contains editable Office Math. Keep spreadsheet formulas such as `=SLOPE(B2:B26,A2:A26)`
as ordinary formula text; dollar-delimited mathematics is for explanatory notation.

For example, `$y = ax^2 + bx + c$` explains a quadratic model, while
`=I2*7^2+I3*7+I4` is the literal spreadsheet formula for a prediction.

## Read validation limits

Static A1 references and declared worksheets can be checked without calculating results. Named
ranges, whole-column ranges, dynamic references such as `INDIRECT`, and array/spill expressions
are not fully validated. Unknown functions may be preserved without verified compatibility.
Read the diagnostic, then test the calculation in the spreadsheet application readers will use.
