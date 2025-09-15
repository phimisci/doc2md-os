"""
A pandoc filter to detect hand-coded citations based on a supplied bibliography
database.
"""

import json
import panflute as pf
import re
import subprocess

def parse_input_bibliography(bibliography_file):
    """
    Obtain the JSON representation of a bibliography database stored in 
    `bibliography_file`.

    This function uses the `subprocess` library to call `pandoc`.
    """
    return json.loads(
        subprocess.check_output(
            ["pandoc", "-t", "csljson", bibliography_file]
        )
    )

def connect_two_names(name1, name2, *, connectives=[" & ", " and "]):
    """
    Return the strings that could possibly occur given two input names and some
    `connectives`.
    """
    return [f"{name1}{connective}{name2}" for connective in connectives]

def find_name_components(name):
    """
    In a first step, detect "von" particles. These are stored separately from
    the family name in the JSON.

    For authors that have a family name, return that family name. 
    For other authors, such as anonymous, authors from antiquity, authors with
    a pen name, organisations, etc., return the literal name.
    """
    try:
        von_particle = name["dropping-particle"] + " "
    except KeyError:
        von_particle = ""
    
    try:
        return von_particle + name["family"]
    except KeyError:
        # A literal name does not contain "von" particles.
        return name["literal"]

def parse_json_author_names(author_input, *, and_others_string=" et al."):
    """
    Parse author data stored in a JSON object and return expected APA citation
    name.
    """
    if len(author_input) == 1:
        return [find_name_components(author_input[0])]
    
    if len(author_input) == 2:
        n1 = find_name_components(author_input[0])
        n2 = find_name_components(author_input[1])
        
        if n2 == "others":
            # Catch the case "author = {Author 1 and others}", where "others"
            # would usually be interpreted a name.
            return [f"{n1}{and_others_string}"]
        else:
            return connect_two_names(n1, n2)
        
    if len(author_input) > 2:
        return [f"{find_name_components(author_input[0])}{and_others_string}"]

def compose_narrative_citation(*, name, date):
    """
    In a narrative or “in-text” citation, the `name` is followed by the 
    publication year in parentheses.

    Example: Name (Year)
    """
    return [f"{name} ({date}"]

def compose_plain_citation(*, name, date, connectives=[" ", ", "]):
    """
    In a plain citation, the date follows the name(s) separated by any of the
    `connectives`. As far as this filter is concerned, parenthetical citations
    are plain citations surrounded by parentheses.

    Examples: (Name, Year); Name Year; Name, Year
    """
    return [f"{name}{connective}{date}" for connective in connectives]

def compose_parenthetical_citation(*, name, date, connectives=[" ", ", "]):
    """
    Placeholder function that might be useful in the future but is not used now.
    """
    return [f"({name}{connective}{date})" for connective in connectives]

def compose_possessive_citation(*, name, date, 
                                connectives=["' ", "'s ", "’s "]):
    """
    Possessive citations add a genitive -s to `name` and parentheses around
    `year`.

    In contrast to the other composition function, possessive citations return
    a list of dictionaries instead of a list of strings. This is because the 
    returned `citestring` needs to be replaced in the document, but the author
    names(s) need to be printed like `authors`. See the details of
    `parse_author_names()` below.

    Examples: Name's (Year); Name' (Year); Name’s (Year)
    """
    return [{"citestring": f"{name}{connective}({date})",
             "authors": f"{name}{connective}"} for connective in connectives]
    
def parse_author_names(bibliography_file):
    """
    Build and return a mapping ...
      - from: the citation strings we expect to appear in the document based on 
              the supplied bibliography.
      - to:   the citation keys in the bibliography.

    Example: {"Wiese & Fink, 2020": "wiese_fink_2020"}, where “Wiese & Fink, 
             2020” is a string typed manually in the submission and 
             `wiese_fink_2020` is a citation key stored in the submitted 
             bibliography database.
    """
    d = dict()
    r = parse_input_bibliography(bibliography_file)
    for work in r:
        
        # We first check whether a work is identified by its author or editor
        try:
            author_or_editor = work["author"]
        except KeyError:
            try:
                author_or_editor = work["editor"]
            except KeyError:
                continue

        # Next, we check whether the entry has a publication year or a 
        # publication state.
        try:
            publication_date_or_status = work["issued"]["date-parts"][0][0]
        except:
            # Expected errors: KeyError, IndexError (depending on supplied info)
            try:
                publication_date_or_status = work["status"]
            except:
                # The entry does not even have a date or state field. In this 
                # case, assume the string contains “forthcoming”
                publication_date_or_status = "forthcoming"

        
        if author_or_editor:
            # We skip entries that have neither author nor editor
            for name in parse_json_author_names(author_or_editor):
                
                # Add all expected narrative citations.
                for string in compose_narrative_citation(
                    name=name, date=publication_date_or_status
                ):
                    d[string] = {"id": work["id"], 
                                "type": "narrative",
                                "authors": name
                                } 

                # Add all expected plain citations. 
                # This also covers parenthetical citations, which we treat as
                # a special case of plain citations.
                for string in compose_plain_citation(
                    name=name, date=publication_date_or_status
                ):
                    d[string] = {"id": work["id"], 
                                "type": "plain",
                                "authors": name
                                } 
                    
                # Add all expected possessive citations.
                # Treatment here is a bit different so we can properly print
                # the possessive markers like “'s”
                for result in compose_possessive_citation(
                    name=name, date=publication_date_or_status
                ):
                    d[result["citestring"]] = {"id": work["id"],
                                               "type": "possessive",
                                               "authors": result["authors"]
                                              } 

    return d

def compose_regex_search_string(input_iterable):
    """
    From a dictionary, compose a RegEx search string that matches either of
    the dictionary's keys. In reality, this will be a quite long expression
    consisting of all the possible citation strings that we can expect to be 
    typed in a document.

    First we escape all regex metacharacters in the input dictionary (re.escape).
    We then build a string separating each key from the iterable, separating 
    each entry by a logical or (|).

    Next, we compile a regex pattern. The expected citation string...
      - can be preceeded by: (
      - can be followed by: ; , . or )
      - is delimited by ^ and $ to protect against over-matching.

    If a match is found, the pattern will return three groups:
      - \1: If present, a ( preceeding the citation string 
            (in parenthetical citations)
      - \2: The citation string
      - \3: The post-citation elements like a semicolon or comma.

    \1 and \3 can be empty groups.
    """
    names = "|".join(map(re.escape, input_iterable))
    pattern = re.compile(r"^([\(]*)"+"("+names+")"+"([;,\\.\\)]*)$")

    return pattern

def determine_unique_length_of_bib_strings(d):
    """
    There is a danger of short-circuiting our search. For example, if both 
    “Wiese 2020” and “Fink & Wiese 2020” are present in the bibliography, 
    looking for “Wiese 2020” before “Fink & Wiese 2020” could lead to wrong
    citations.

    Our solution is to look for the longest citation strings first, and work
    down from this. Later in the filter, we iterate over the possible lenghts
    of citation strings in *descending* order (`reverse=True`).

    If an entry has n words separated by spaces, it has 2n-1 elements in total.

    Typical values are 3 and 7:
     - “Wiese 2020“ has three components (Wiese, Space, and 2020)
     - “Wiese & Fink 2020“ has seven components (Wiese, Space, &, Space, Fink, 
       Space, 2020)
    """
    return sorted({2 * len(entry.split()) - 1 for entry in d}, reverse=True)

def filter_pandoc_objects(elem, doc): 
    """
    The actual filter function. We parse the document iteratively from the last
    to the first element. Parsing backwards allows us to do in-place operations.
    The in-place operations we perform a deletion of a matched manually typed
    citation and appropriate replacement by a pandoc Citation object.

    We parse the document n times, where n is the unique length of expected 
    citation strings. Usually, the document is parsed for lengths 7 and then 3
    (see `determine_unique_length_of_bib_strings()`).

    As we traverse the tree backwards, new elements are also inserted last-to-
    first.
    """
    if isinstance(elem, pf.Para): #or type(elem) == pf.Plain:
        for d in doc.tmp_distances:
            for i in range(len(elem.content)-1, -1, -1):
                current_element = pf.stringify(elem.content[i:i+d])
                result = re.search(doc.tmp_searchstring, current_element)

                if result:
                    # We found something! 
                    del elem.content[i:i+d]
                    bib_string = result.group(2)

                    if result.group(3) != "":
                        # We insert the last group first, but only if it is
                        # non-empty. For example, this could be a closing ).
                        elem.content.insert(
                            i, pf.Str(result.group(3))
                        )

                    if bib_string in doc.tmp_bibliography:
                        # The second group of our match contains the actual 
                        # citation string. The replacement depends on the type
                        # of citation.

                        if doc.tmp_bibliography[bib_string]["type"] == "narrative":
                            
                            elem.content.insert(i, pf.Cite(
                                citations=[pf.Citation(
                                    id=doc.tmp_bibliography[bib_string]["id"],
                                    mode="SuppressAuthor"
                                    )]
                                )
                            )
                            elem.content.insert(i, pf.Str("("))
                            elem.content.insert(i, pf.Space())
                            elem.content.insert(i, pf.Str(
                                doc.tmp_bibliography[bib_string]["authors"]
                                )
                            )

                        if doc.tmp_bibliography[bib_string]["type"] == "plain":
                            
                            elem.content.insert(i, pf.Cite(
                                citations=[pf.Citation(
                                    id=doc.tmp_bibliography[bib_string]["id"],
                                    mode="NormalCitation"
                                    )]
                                )
                            )

                        if doc.tmp_bibliography[bib_string]["type"] == "possessive":
                            
                            elem.content.insert(i, pf.Str(")"))
                            elem.content.insert(i, pf.Cite(
                                citations=[pf.Citation(
                                    id=doc.tmp_bibliography[bib_string]["id"],
                                    mode="SuppressAuthor"
                                    )]
                                )
                            )
                            elem.content.insert(i, pf.Str(
                                doc.tmp_bibliography[bib_string]["authors"] + "(")
                            )
                    else:
                        # This should never happen. A serious malfunction.
                        raise IndexError(
                            f"Bibliography entry {bib_string} missing."
                            )

                    if result.group(1) != "":
                        # The first group of our match is input last, in line
                        # with our backwards processing. It usually contains a
                        # (, but is often empty (in which case nothing is done).
                        elem.content.insert(
                            i, pf.Str(result.group(1))
                        )
        return 

def preprocess_bibliography(doc):
    """
    Before running the filter, we prepare some data so that it is not processed
    at each iteration of the fitler. Please see the documentation for the 
    individual functions to see which data is processed here.
    """
    bibliography = parse_author_names(doc.get_metadata("bibliography"))
    distances = determine_unique_length_of_bib_strings(bibliography)
    doc.tmp_bibliography = bibliography
    doc.tmp_distances = distances
    doc.tmp_searchstring = compose_regex_search_string(bibliography)

    # We need a customised APA citation pattern, which we indicate here.
    if doc.format == "html":
        doc.metadata["csl"] = "./csl/apa7-manual-parentheses.csl"
    
    # We also need to direct LaTeX \autocite and \autocite* to *not* output
    # parentheses.
    if doc.format == "latex":
        doc.metadata["biblatex"] = "true"
        doc.metadata["biblatexoptions"] = ["autocite=plain, style=apa"]
    
    return

def cleanup(doc):
    """
    We're not exactly sure whether this is necessary, but before writing the
    document, we clean up the temporary objects we have created in the pandoc
    document.
    """
    del doc.tmp_bibliography
    del doc.tmp_distances
    del doc.tmp_searchstring
    return 

def main(doc=None):
    """
    This function merely initialises the filter.
    """
    return pf.run_filter(
        filter_pandoc_objects, 
        doc=doc,
        prepare=preprocess_bibliography,
        finalize=cleanup
        ) 

if __name__ == '__main__':
    main()
