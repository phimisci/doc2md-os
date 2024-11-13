import argparse, os, subprocess, logging
from typing import Optional
from markdown_cleaner import remove_escapes, replace_comma_citation, remove_yaml_bib

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments and return the parsed arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('doc_file', type=str, help='Path to the input doc file.')
    parser.add_argument("-z", "--zotero", help="Indicate that a docx file has been created using Zotero Plugin.", action="store_true")
    args = parser.parse_args()

    return args

def convert_doc_to_md(doc_file_path: str) -> None:
            """Convert a docx file to markdown using pandoc.

            Arguments
            ---------
                doc_file_path (str):
                    Path to the input docx file.
                
            """
            # convert docx to md via pandoc
            pandoc_command = ["pandoc", "-s", doc_file_path, "-t", "markdown", "-o", "files/raw_markdown.md"]
            result = subprocess.run(pandoc_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # check if the command was successful
            if result.returncode == 0:
                # open raw markdown file
                with open("files/raw_markdown.md", "r", encoding="utf-8") as f:
                    md_file = f.read()

                # clean markdown
                md_file = remove_escapes(md_file)
                md_file = replace_comma_citation(md_file)

                # save clean markdown
                with open("files/clean_markdown.md", "w", encoding="utf-8") as f:
                    f.write(md_file)
            else:
                logging.error(f"Error occurred when converting docx->md: {result.stderr}")
                print("Error running pandoc")
                print("Error:", result.stderr)

def convert_doc_zotero_to_md(doc_file_path: str) -> None:
            """Convert a docx file with Zotero/Endnote plugin citations to markdown using pandoc.

            Arguments
            ---------
                doc_file_path (str):
                    Path to the input docx file.
                
            """
            ### FIRST STEP
            # convert docx to md via pandoc
            pandoc_command = ["pandoc", "-s", "--from", "docx+citations", doc_file_path, "-t", "markdown", "-o", "files/raw_markdown.md"]
            result = subprocess.run(pandoc_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # check if the command was successful
            if result.returncode != 0:
                logging.error(f"Error occurred when converting docx->md using Zotero inplace citations: {result.stderr}")
                return 1

            ### SECOND STEP
            # extract bibtex from bib-yaml in markdown file
            pandoc_command = ["pandoc", "-s", "files/raw_markdown.md", "--citeproc", "-o", "files/bibliography.bib"]
            result = subprocess.run(pandoc_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # check if the command was successful
            if result.returncode != 0:
                logging.error(f"Error occurred when extracting bib from md+yaml file when using Zotero inplace citations: {result.stderr}")
                return 1
 
            ### THIRD STEP
            # remove bib-yaml from markdown file
            remove_yaml_bib("files/raw_markdown.md")
            ### FOURTH STEP
            # open raw markdown file
            with open("files/raw_markdown.md", "r", encoding="utf-8") as f:
                md_file = f.read()
            # clean markdown
            md_file = remove_escapes(md_file)
            md_file = replace_comma_citation(md_file)
            # save clean markdown
            with open("files/clean_markdown.md", "w", encoding="utf-8") as f:
                f.write(md_file)


if __name__=="__main__":
    arguments = parse_arguments()
    doc_file_path = arguments.doc_file
    doc_file_path = f"files/{doc_file_path}"

    # init logging file
    logging.basicConfig(filename='files/doc2md.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    
    # check if path leads to a valid file
    if not os.path.isfile(doc_file_path):
        print(f"{doc_file_path} is not a valid file path. Exit.")
        exit()

    # check if docx file has been created using Zotero Plugin
    if arguments.zotero:
        convert_doc_zotero_to_md(doc_file_path)
    else:
        convert_doc_to_md(doc_file_path)
        