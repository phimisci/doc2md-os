# Introduction
DOC2MD is a CLI tool that allows for the conversion of DOCX files to Markdown. The tool is specifically designed to handle DOCX files that contain citations and references, but ODT files are supported as well. The tool uses Pandoc to convert the DOCX files to Markdown and then cleans the Markdown files to ensure that they are ready for publication. The software was initially developed to support the typesetting of articles in the [Philosophy and the Mind Sciences](https://philosophymindscience.org/) journal.

# Installation
The tool is available as a Docker image. To use the tool, you need to have [Docker](https://docs.docker.com/engine/install/) installed on your system. You can either pull the image from the GitHub Container Registry or build the image yourself.

## Pull the image from the GitHub Container Registry
You can directly pull the image from the GitHub Container Registry by running the following command:

`docker pull ghcr.io/phimisci/doc2md:latest`

## Build the image yourself
If you want to build the image yourself, you can do so by cloning the repository and running the following command in the root directory of the repository:

`docker build --tag doc2md .`

# Usage
In the following steps, we assume that you have installed the Docker image as described above using the local build. If you have pulled the image from the GitHub Container Registry, you need to replace `doc2md` with the appropriate image name (which is `ghcr.io/phimisci/doc2md:latest`).

## DOCX/ODT files with citeproc citations and external BibTeX file
If you want to convert a DOCX/ODT file to Markdown and you have included citations in the DOCX file that use [pandoc's citeproc](https://pandoc.org/MANUAL.html#citation-syntax) citation style, you can use the following command:

`docker run --rm --volume "$(pwd):/app/files" doc2md <FILENAME>.<docx|odt>`

## DOCX files with included citations (e.g. using the Zotero plugin for Word)
If you want to convert a DOCX file to Markdown and you have included citations in the DOCX file using the Zotero plugin for Word, you can use the following command:

`docker run --rm --volume "$(pwd):/app/files" doc2md --zotero <FILENAME>.docx`

# About
The tool was developed by Thomas Jurczyk for [Philosophy and the Mind Sciences](https://philosophymindscience.org/) to support the typesetting of articles in the journal. The tool is open-source and licensed under the MIT license. The source code is available on [GitHub]().

# Versions

### 1.0.0

- Initial release