# DOC2MD

## Description

Transforming PhiMiSci submissions (.docx) to (clean) Markdown using Pandoc. The output also includes a doc2md.log file with the Pandoc output (if any problems occur during the conversion).

1. DOCX -> Raw MD (pandoc)
2. Cleaning MD
3. Output

## Usage

### docx/odt files with citeproc citations and external BibTeX file
`docker run --rm --volume "$(pwd):/app/files" --user $(id -u):$(id -g) registry.git.noc.ruhr-uni-bochum.de/phimisci/doc2md/0.0.1:latest <FILENAME>.<docx|odt>`

### docx files with included citations (e.g. using the Zotero plugin for Word)
`docker run --rm --volume "$(pwd):/app/files" --user $(id -u):$(id -g) registry.git.noc.ruhr-uni-bochum.de/phimisci/doc2md/0.0.1:latest --zotero <FILENAME>.docx`

## Versions

### 0.1.0

- Bump Pandoc to 3.4.0.0; this allows for better handling of citations and references when using Zotero plugins in Word