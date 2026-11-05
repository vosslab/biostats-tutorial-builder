# Screenshot sources and refresh

The authoring guides pair copyable Markdown with actual Word and Excel output.
[../examples/authoring_features.md](../examples/authoring_features.md) is the shared runnable
source for the `authoring_*` captures. Roots supplies a few formatting values; there is no
example lesson students must complete.

## Authoring reference images

| Image group | Native source and view |
| --- | --- |
| Title, headings, text, table, image, and links | DOCX exported to PDF, cropped at the corresponding headings |
| Enter, Fill, Select, Replace, and alternatives | DOCX instruction crops from the same feature source |
| Workbook | Generated XLSX, A1:E6; supplied data and blank work cells |
| Results | Generated XLSX, D1:E3; supplied labels and blank result cells |
| Response | Generated XLSX, D8:E9; a separate response table below the data |
| Source/output comparison | Literal source beside the unchanged Enter instruction crop |
| Instructor excerpt | The Calculate the Z-Statistic step in [../../tutorial_data/microbes/microbes_1_z_test.md](../../tutorial_data/microbes/microbes_1_z_test.md) |

The workbook images show starter files, with learner calculations left blank. The screenshot
workflow prints disposable copies through LibreOffice Calc; it does not fill these answers.
Word images come from the project's actual DOCX-to-PDF export, not an HTML imitation.

[syntax_capture_receipt.json](syntax_capture_receipt.json) records source and image hashes,
crop anchors, native artifact paths, and renderer details. The source/output comparison records
the exact displayed source and the native crop used. Final images use WebP at quality 90.

## Other retained captures

The instructor gallery uses [capture_receipt.json](capture_receipt.json). Its completed ANOVA
image is explicitly a demonstration: the capture applies authored actions to a disposable
workbook and recalculates it. It is not a blank student starter.

The earlier Roots checkpoint illustrations and published example remain available with
[course_capture_receipt.json](course_capture_receipt.json). They are retained examples, not the
current three-part authoring path. Their standalone capture command remains available in
[../../devel/capture_authoring_course.py](../../devel/capture_authoring_course.py).

## Refresh the current guides

From the repository root:

```bash
source source_me.sh && python3 devel/refresh_documentation.py
```

The existing command rebuilds the instructor gallery, syntax/feature captures, and three guide
Parts. For guide export it combines the Markdown page with the feature example's workbook;
fenced snippets stay literal and are never executed. Guide exports are under
`tutorial_output/authoring_course/parts/`. The source pages remain ordinary GitHub Markdown.

For only the syntax and feature images, run
`source source_me.sh && python3 devel/capture_syntax_examples.py`.
Review the resulting images at reading size, then check the rendered GitHub pages separately
from the native guide PDFs. Local LibreOffice rendering does not prove Google import behavior.

This optional maintainer workflow needs the tools and fonts in [../INSTALL.md](../INSTALL.md).
On this macOS host, agents run all LibreOffice commands outside the sandbox.
