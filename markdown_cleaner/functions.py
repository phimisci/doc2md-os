import re

def remove_escapes(md_file: str) -> str:
    '''Function to remove unnecessary escapes resulting from DOCX->MD conversion.

    Parameters
    ----------
    md_file : str
        Content of the markdown file.

    Returns
    -------
    str
        A new string with removed escapes from certain characters.
    '''
    # for now, I remove each escape in an individual step; TODO: maybe create one final expression once everything works as expected
    md_file = md_file.replace(r"\[", r"[")
    md_file = md_file.replace(r"\]", r"]")
    md_file = md_file.replace(r"\@", r"@")
    md_file = md_file.replace(r"\#", r"#")
    md_file = md_file.replace(r"\$", r"$")
    md_file = md_file.replace(r"\[", r"[")
    md_file = md_file.replace("\\\\", "\\")
    md_file = md_file.replace(r"\^", r"^")
    md_file = md_file.replace(r'\"', r'"')
    md_file = md_file.replace(r"\'", r"'")
    md_file = md_file.replace(r"$\rbrack", r"]")
    md_file = md_file.replace(r"$\lbrack", r"[")

    return md_file

def replace_comma_citation(md_file: str) -> str:
    '''Function to replace comma in citeproc citation with semicolon: [@mueller21, @peter23] -> [@mueller21; @peter23]
        
        Parameters
        ----------
            md_file: str
                Content of the markdown file.

        Returns
        -------
            A new string with changed md content.
    '''
    pattern = re.compile(r"(@\w+\s?|@\w+\s?,\s?\d+-\d+\s?),\s?(?=@\w+)", re.UNICODE)
    md_file = re.sub(pattern, r"\1; ", md_file)
    
    return md_file

def remove_yaml_bib(md_file_path: str) -> None:
    """Removes YAML front matter and bibliography from a Markdown file.

    Arguments
    ----------
        md_file_path (str):
            The path to the Markdown file.

    Returns
    -------
        None
    """
    pattern = re.compile(r"^-{3}\n.*?(\.\.\.\n|---\n)", re.DOTALL)

    with open(md_file_path, "r", encoding="utf-8") as f:
        md_file = f.read()
    
    md_file = re.sub(pattern, "", md_file)
    
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_file)
        
        