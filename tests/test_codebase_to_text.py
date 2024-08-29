import unittest
import os
import sys
import shutil
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from codebase_to_text.codebase_to_text import CodebaseToText


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
        with open(os.path.join(self.test_folder_path, ".hidden_file.py"), "w") as file:
            file.write("Hidden file content")

        self.maxDiff = None

    def test_get_text(self):
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path="output.txt",
            output_type="txt",
            file_extensions=[".txt", ".py"],
        )

        text = code_to_text.get_text()
        expected_text = f"""Folder Structure
--------------------------------------------------
{self.test_folder_path}/
    test_file1.py
    test_file2.txt
    .hidden_file.py
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


test_folder/.hidden_file.py
File type: .py
Hidden file content

--------------------------------------------------
File End
--------------------------------------------------
"""
        self.assertEqual(text, expected_text)

    def test_exclude_hidden_files(self):
        code_to_text = CodebaseToText(
            input_path=self.test_folder_path,
            output_path="output.txt",
            output_type="txt",
            exclude_hidden=True,
            file_extensions=[".txt", ".py"],
        )

        text = code_to_text.get_text()
        expected_text = f"""Folder Structure
--------------------------------------------------
{self.test_folder_path}/
    test_file1.py
    test_file2.txt
    .hidden_file.py
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

    def test_cli(self):
        # Test the command-line interface
        output_path = "cli_output.txt"
        result = subprocess.run(
            [
                "python",
                "codebase_to_text/codebase_to_text.py",
                "--input",
                self.test_folder_path,
                "--output",
                output_path,
                "--output_type",
                "txt",
                "--exclude_hidden",
                "True",
                "--file_extensions",
                ".py",
                ".txt",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        print(result)

        # Ensure the process completed successfully
        self.assertEqual(result.returncode, 0)

        # Verify the output file content
        with open(output_path, "r", encoding="utf-8") as file:
            cli_output = file.read()

        cli_expected_output = f"""Folder Structure
--------------------------------------------------
{self.test_folder_path}/
    test_file1.py
    test_file2.txt
    .hidden_file.py
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
        self.assertEqual(cli_output, cli_expected_output)

        # Clean up CLI test output
        os.remove(output_path)

    def tearDown(self):
        # Clean up temporary folder
        if os.path.exists(self.test_folder_path):
            shutil.rmtree(self.test_folder_path)


if __name__ == "__main__":
    unittest.main()
