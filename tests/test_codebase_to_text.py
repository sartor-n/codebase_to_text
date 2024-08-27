import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from codebase_to_text.codebase_to_text import CodebaseToText
import shutil


class TestCodebaseToText(unittest.TestCase):
    def setUp(self):
        # Create a temporary folder with some test files
        self.test_folder_path = "test_folder"
        os.makedirs(self.test_folder_path, exist_ok=True)
        with open(os.path.join(self.test_folder_path, "test_file1.py"), "w") as file:
            file.write("Test file 1 content")
        with open(os.path.join(self.test_folder_path, "test_file2.txt"), "w") as file:
            file.write("Test file 2 content")
        with open(os.path.join(self.test_folder_path, "test_file3.csv"), "w") as file:
            file.write("Test file 3 content")
        self.maxDiff = None

    def test_get_text(self):
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path="output.txt",
            output_type="txt",
            file_extensions=[".txt", ".py"],
        )

        text = code_to_text.get_text()
        print(text)
        expected_text = f"""Folder Structure
--------------------------------------------------
{self.test_folder_path}/
    test_file1.py
    test_file2.txt
    test_file3.csv


File Contents
--------------------------------------------------


{self.test_folder_path}/test_file1.py
File type: .py
Test file 1 content

--------------------------------------------------
File End
--------------------------------------------------


{self.test_folder_path}/test_file2.txt
File type: .txt
Test file 2 content

--------------------------------------------------
File End
--------------------------------------------------
"""
        self.assertEqual(text, expected_text)

    def tearDown(self):
        # Clean up temporary folder
        if os.path.exists(self.test_folder_path):
            shutil.rmtree(self.test_folder_path)


if __name__ == "__main__":
    print(sys.path)
    unittest.main()
