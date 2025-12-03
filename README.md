## DOC2MD (Version 1.0.0)

## Introduction
DOC2MD is a CLI tool that allows for the conversion of DOCX files to Markdown. The tool is specifically designed to handle DOCX files that contain citations and references, but ODT files are supported as well. The tool uses Pandoc to convert the DOCX files to Markdown and then cleans the Markdown files to ensure that they are ready for publication. The software was initially developed to support the typesetting of articles in the [Philosophy and the Mind Sciences](https://philosophymindscience.org/) journal.

## Installation
The tool is available as a Docker image. To use the tool, you need to have [Docker](https://docs.docker.com/engine/install/) installed on your system. You can either pull the image from the GitHub Container Registry or build the image yourself.

### Pull the image from the GitHub Container Registry
You can directly pull the image from the GitHub Container Registry by running the following command:

`docker pull ghcr.io/phimisci/doc2md-os:latest`

### Build the image yourself
If you want to build the image yourself, you can do so by cloning the repository and running the following command in the root directory of the repository:

`docker build --tag doc2md .`

## Usage
In the following steps, we assume that you have installed the Docker image as described above using the local build. If you have pulled the image from the GitHub Container Registry, you need to replace `doc2md` with the appropriate image name (which is `ghcr.io/phimisci/doc2md-os:latest`).

### DOCX/ODT files with citeproc citations and external BibTeX file
If you want to convert a DOCX/ODT file to Markdown and you have included citations in the DOCX file that use [pandoc's citeproc](https://pandoc.org/MANUAL.html#citation-syntax) citation style, you can use the following command:

`docker run --rm --volume "$(pwd):/app/files" doc2md <FILENAME>.<docx|odt>`

### DOCX files with included citations (e.g. using the Zotero plugin for Word)
If you want to convert a DOCX file to Markdown and you have included citations in the DOCX file using the Zotero plugin for Word, you can use the following command:

`docker run --rm --volume "$(pwd):/app/files" doc2md --zotero <FILENAME>.docx`

### Automatically generated bibliography from a BibTeX file
If you want to automatically generate citeproc citations in a document containing plain APA citations, such as Meyer 2020 or Meyer (2020), you can use the `--autobib` option. This option requires a path to a BibTeX file.

`docker run --rm --volume "$(pwd):/app/files" doc2md --autobib <FILENAME>.bib <FILENAME>.<docx|odt>`

The `--autobib` option uses a two-filter process to convert hand-written citations into formal pandoc citations:

1.  The first filter (`hand-written-citations.py`) parses the provided BibTeX file and tries to find hand-written citations in the document (e.g., `Author (2023)`, `(Author, 2023)`, etc.) and replaces them with proper pandoc citation markers using BibTeX IDs.

2.  The second filter (`find_citation_candidates.py`) runs after the first one and searches for any remaining citation-like patterns (e.g., a 4-digit year) that might have been missed. The list of these candidates is saved in `files/citation_candidates.txt` for your review. This file will only be created if there are any candidates found.

## About
The tool was developed by Thomas Jurczyk for [Philosophy and the Mind Sciences](https://philosophymindscience.org/) to support the typesetting of articles in the journal. The tool is open-source and licensed under the MIT license. The source code is available on [GitHub](https://github.com/phimisci/doc2md-os).

## Versions
### 1.0.1
- Bump Pandoc version to 3.6.4.0

### 1.0.0

- Initial release
