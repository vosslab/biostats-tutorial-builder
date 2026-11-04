# Caffeine shared release

## Delivered workflow

Three separate Caffeine Markdown sources remain canonical. The normal build accepts them in
sequence and publishes three DOCX/PDF pairs, one `workbook.xlsx`, and one validation manifest in
`tutorial_output/caffeine_release/`. There is no split-Part exporter or combined Caffeine source.

The existing staged publisher protects edited outputs and keeps the previous bundle if an exporter
fails. Shared sheets merge compatible declarations and reject conflicting values or roles. Ordered
student actions and source-local calculation alternatives remain distinct across documents.

## Content and numerical evidence

- All six original worksheet names are retained. Analysis sheets use the same 25 regression pairs;
  the warm-up's different frozen dataset is deliberately replaced for instructional continuity.
- Labels are supplied, student answer cells remain blank, and Part 3 uses Part 2's linear results.
- Explanatory prose and authored humor are retained with targeted instruction corrections.
- Independent expectations: 12 tutorials, 13 scenarios, 254 formula results.
- Actual shared-workbook LibreOffice Calc execution: 103 formula results passed. The generated
  evidence is `tutorial_output/validation/shared_caffeine_calc.json`.
- Final test run: 2,120 passed; one Podman disk-budget test cannot connect to the existing VM.
  The same failure occurred before implementation. No Podman tests were changed or skipped.
- Screenshot refresh completed through the existing capture script outside the sandbox.

## Review and boundaries

The [visual report](caffeine_release_visual.md) records page inspection and corrections. Local
rendering and actual Calc execution do not establish Google Docs/Sheets import acceptance.
Default Google Application Default Credentials were unavailable; no Google files were created.

Frozen inputs remain unchanged. SHA256 fingerprints checked before and after implementation:

| Frozen file suffix | SHA256 |
| --- | --- |
| Academy.pdf | 92df92c385c9dc461fa5673bc4a9a7844f74546b2398e7d305a757740353ed99 |
| Academy.xlsx | 550684a93ff8ea1411ec4cfb502b91e904ad13c5762fd59dd858e9b070a981bf |
| Tutorial.docx | 673844508c7acd5f146952d2b0b85ea64c17b30729bc7c74013072334cbd991b |
| Tutorial.md | 50fcd938b09a92a262d1103f3ed6513832d763a1d8543ccef92a935fecf38d09 |
| Tutorial.pdf | 1aa70ba0f9ede7c93fc71fe12b5cff95c30c15067a66f96359ecce5ea0909ce8 |
| Tutorial.rtf | 335c3b707c069b6006b3d435fe6fe38205ed991bb7484e93a0e1cb57790abdd9 |
