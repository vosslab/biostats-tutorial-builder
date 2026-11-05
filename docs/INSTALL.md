# Install

The converter runs on Python 3 with the packages in `pip_requirements.txt`. The default build also
uses LibreOffice Writer to export PDF; the `docx,xlsx` build does not need LibreOffice.
Dollar-delimited TeX equations use Pandoc to create editable mathematics in Word output.

Generated DOCX files use Google Docs paragraph styles and PT Sans, PT Sans Narrow, and Roboto Mono.
PDF export requires these fonts to be installed locally and visible to LibreOffice. Setup does not
install fonts or download fallback fonts.

Download [PT Sans](https://fonts.google.com/specimen/PT+Sans),
[PT Sans Narrow](https://fonts.google.com/specimen/PT+Sans+Narrow), and
[Roboto Mono](https://fonts.google.com/specimen/Roboto+Mono) from Google Fonts. Extract each
download, open its font files in Font Book on macOS, and choose **Install**. Restart LibreOffice
after installing the fonts. On other systems, install these same families with your font manager.

## macOS setup

1. Install [Homebrew](https://brew.sh/) using its instructions. Follow the installer's **Next
   steps** to make the `brew` command available, then return to this setup.
2. Open Terminal and download a working project copy with Git:

   ```bash
   git clone https://github.com/vosslab/biostats-tutorial-builder.git
   cd biostats-tutorial-builder
   ```

   This downloads the project into a folder named `biostats-tutorial-builder`. You do not need to know
   Git to follow these commands. Run the setup commands below from this folder; it contains
   `make_tutorial.py`, `source_me.sh`, and `pip_requirements.txt`.

Install Python 3.12, Pandoc, LibreOffice, and the Python packages:

```bash
brew install python@3.12 pandoc
brew install --cask libreoffice
python3 --version
```

Check that the last command reports Python 3.12. If it reports another version, use the local
package folder steps below, which select Python 3.12 explicitly. Otherwise, install the packages:

```bash
python3 -m pip install -r pip_requirements.txt
```

### If pip reports externally-managed-environment

[Homebrew protects its Python installation](https://docs.brew.sh/Language-Runtimes-and-Packages#python)
from direct package changes. If the package command above reports `externally-managed-environment`,
or `python3 --version` reported a different Python version, create a local package folder for
this project:

```bash
bash
source source_me.sh
python3.12 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r pip_requirements.txt
```

In each new Bash shell, run `source source_me.sh` first, then `source .venv/bin/activate` before
running Python commands. Keep using this same shell after installation.

For other systems, install Python 3, Pandoc, LibreOffice, and the same Python requirements with that
system's package tools. Keep LibreOffice available on `PATH` for PDF builds.

Before running a repository command, start Bash and load the shell environment. The setup script
requires Bash; macOS terminals often start in Zsh.

```bash
bash
source source_me.sh
```

If you created `.venv` above, also run `source .venv/bin/activate` in this shell.

Run subsequent repository commands in this same Bash shell.

## Verify install

```bash
python3 make_tutorial.py lint docs/examples/authoring_features.md
```

The command should finish without errors. Building this example additionally verifies the local
Pandoc, fonts, and LibreOffice setup.

See [USAGE.md](USAGE.md) for lint, build, and import commands. See
[AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) for the Markdown format.

## Optional screenshot tooling

Authors who refresh documentation screenshots also need Poppler (`pdftotext`, `pdftoppm`),
WebP (`cwebp`), and librsvg (`rsvg-convert`). Install these tools and the existing Python dependency
with the repository's [Brewfile](../Brewfile):

```bash
brew bundle
```

Pillow is included in [pip_requirements.txt](../pip_requirements.txt). LibreOffice and the PT Sans,
PT Sans Narrow, and Roboto Mono fonts described above are also required for capture. These extra
command-line tools are optional for normal tutorial builds.

Refresh all documentation artifacts and screenshots from the repository root:

```bash
source source_me.sh && python3 devel/refresh_documentation.py
```

See [screenshots/README.md](screenshots/README.md) for capture
provenance and the distinction between starter workbooks and completed demonstrations.
