"""
A pandoc filter to search for citation candidates, understood as 4-digit strings
followed by an optional lowercase letter. Candidates are output to a text file
for further processing.
"""

import panflute as pf
import re

def find_remaining_citations(elem, doc):
    """
    Walk pandoc's AST and check all strings for occurrence of the typical APA
    citation pattern.

    Exclude strings that appear within Citations or Links.
    """
    if isinstance(elem, pf.Str) \
        and not isinstance(elem.parent, pf.Cite) \
        and not isinstance(elem.parent, pf.Link):
        result = re.search("(\\d{4}[a-z]*)", elem.text)
        if result:
            doc.remaining_citations.add(result.group(1))
            doc.citation_candidate_counter += 1
            
    return None


def prepare(doc):
    doc.remaining_citations = set()
    doc.citation_candidate_counter = 0
    return 


def finalize(doc):
    """
    Write the gathered information to an external file, citation_candidates.txt.
    """
    with open("files/citation_candidates.txt", "w") as f:
        f.write(f"I found {len(doc.remaining_citations)} possible citation")
        f.write(f"strings, with a total of {doc.citation_candidate_counter} ")
        f.write("occurrences:\n")
        f.write("\n".join(sorted(doc.remaining_citations)))

    del doc.remaining_citations
    del doc.citation_candidate_counter
    return 


def main(doc=None):
    return pf.run_filter(
        find_remaining_citations, 
        prepare=prepare, 
        finalize=finalize, 
        doc=doc
    ) 

if __name__ == '__main__':
    main()