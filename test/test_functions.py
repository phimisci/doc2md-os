import unittest
from markdown_cleaner import remove_escapes, replace_comma_citation, remove_yaml_bib

class TestRemoveEscapes(unittest.TestCase):
    def test_remove_escapes(self):
        # Test case 1: No escapes to remove
        md_file = "This is a test"
        expected_output = "This is a test"
        self.assertEqual(remove_escapes(md_file), expected_output)

        # Test case 2: Remove escapes for special characters
        md_file = r"This is a \[test\] with \#special\# characters"
        expected_output = "This is a [test] with #special# characters"
        self.assertEqual(remove_escapes(md_file), expected_output)

        # Test case 3: Remove multiple escapes in one step
        md_file = r"This is a \[test\] with \#special\# characters and \\backslashes\\"
        expected_output = "This is a [test] with #special# characters and \\backslashes\\"
        self.assertEqual(remove_escapes(md_file), expected_output)

        # Test case 4: Remove escapes for quotes
        md_file = r'This is a \"test\" with \'quotes\''
        expected_output = 'This is a "test" with \'quotes\''
        self.assertEqual(remove_escapes(md_file), expected_output)

        # Test case 5: Remove escapes for brackets
        md_file = r"This is a $\rbracktest$\lbrack with brackets"
        expected_output = "This is a ]test[ with brackets"
        self.assertEqual(remove_escapes(md_file), expected_output)

    def test_replace_comma_citation(self):
        # Test case 1: Replace comma in citeproc citation with semicolon
        md_file = "[@mueller21, @peter23]"
        expected_output = "[@mueller21; @peter23]"
        self.assertEqual(replace_comma_citation(md_file), expected_output)

        # Test case 2: No comma in citeproc citation
        md_file = "[@mueller21]"
        expected_output = "[@mueller21]"
        self.assertEqual(replace_comma_citation(md_file), expected_output)

        # Test case 3: Multiple citations with comma
        md_file = "[@mueller21, @peter23, @john45]"
        expected_output = "[@mueller21; @peter23; @john45]"
        self.assertEqual(replace_comma_citation(md_file), expected_output)
        
        # Test case 4: Multiple citations with comma and page numbers
        md_file = "[@mueller21, @peter23, @john45, 23-45]"
        expected_output = "[@mueller21; @peter23; @john45, 23-45]"
        self.assertEqual(replace_comma_citation(md_file), expected_output)

        # Test case 5: Multiple citations with comma and page numbers
        md_file = "[@mueller21, @peter23, 33-55, @john45, 23-45, 46-78]"
        expected_output = "[@mueller21; @peter23, 33-55; @john45, 23-45, 46-78]"
        self.assertEqual(replace_comma_citation(md_file), expected_output)

class TestRemoveYamlBib(unittest.TestCase):
    def test_remove_yaml_bib(self):
        # Test case 1: Remove YAML front matter and bibliography in --- ... block
        md_file_path = "test/test_file.md"
        expected_output = "\n# Introduction\n\nThis is the content of the Markdown file."
        
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write("---\nTitle: Test File\nAuthor: John Doe\n...\n\n# Introduction\n\nThis is the content of the Markdown file.")
        
        remove_yaml_bib(md_file_path)
        
        with open(md_file_path, "r", encoding="utf-8") as f:
            actual_output = f.read()
        
        self.assertEqual(actual_output, expected_output)

        # Test case 2: Remove YAML front matter and bibliography in --- --- block
        md_file_path = "test/test_file.md"
        expected_output = "\n# Introduction\n\nThis is the content of the Markdown file."

        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write("---\nTitle: Test File\nAuthor: John Doe\n---\n\n# Introduction\n\nThis is the content of the Markdown file.")

        remove_yaml_bib(md_file_path)
          
        with open(md_file_path, "r", encoding="utf-8") as f:
            actual_output = f.read()
        
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()