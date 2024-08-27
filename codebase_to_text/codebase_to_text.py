import os
import argparse
import git
import shutil
from docx import Document
import tempfile
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List, Optional, Literal


class CodebaseToText(BaseModel):
    input_path: str
    output_path: str
    output_type: Literal["txt", "docx"]
    verbose: bool = Field(default=False)
    exclude_hidden: bool = Field(default=False)
    file_extensions: List[str] = Field(default_factory=lambda: [".py"])
    temp_folder_path: Optional[str] = None

    @field_validator("input_path")
    def validate_input_path(cls, value):
        if not value:
            raise ValueError("Input path cannot be empty.")
        return value

    @field_validator("output_path")
    def validate_output_path(cls, value):
        if not value:
            raise ValueError("Input path cannot be empty.")
        return value

    @field_validator("output_type")
    def validate_output_type(cls, value):
        if value not in ["txt", "docx"]:
            raise ValueError("Invalid output type. Supported types: txt, docx")
        return value

    def _parse_folder(self, folder_path: str) -> str:
        tree = ""
        for root, dirs, files in os.walk(folder_path):
            level = root.replace(folder_path, "").count(os.sep)
            indent = " " * 4 * (level)
            tree += "{}{}/\n".format(indent, os.path.basename(root))
            subindent = " " * 4 * (level + 1)
            for f in files:
                tree += "{}{}\n".format(subindent, f)

        if self.verbose:
            print(f"The file tree to be processed:\n {tree}")

        return tree

    def _get_file_contents(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()

    def _is_hidden_file(self, file_path: str) -> bool:
        components = os.path.normpath(file_path).split(os.sep)
        for c in components:
            if c.startswith((".", "__")):
                return True
        return False

    def _process_files(self, path: str) -> str:
        content = ""
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.exclude_hidden and self._is_hidden_file(
                    os.path.abspath(file_path)
                ):
                    if self.verbose:
                        print(f"Ignoring hidden file {file_path}")
                    continue

                if not any(file.endswith(ext) for ext in self.file_extensions):
                    if self.verbose:
                        print(f"Skipping file {file_path} due to unmatched extension")
                    continue

                try:
                    if self.verbose:
                        print(f"Processing: {file_path}")
                    file_content = self._get_file_contents(file_path)
                    content += f"\n\n{file_path}\n"
                    content += f"File type: {os.path.splitext(file_path)[1]}\n"
                    content += f"{file_content}"
                    content += f"\n\n{'-' * 50}\nFile End\n{'-' * 50}\n"
                except Exception as e:
                    print(f"Couldn't process {file_path}: {e}")
        return content

    def get_text(self) -> str:
        folder_structure = ""
        file_contents = ""
        if self.is_github_repo():
            self._clone_github_repo()
            folder_structure = self._parse_folder(self.temp_folder_path)
            file_contents = self._process_files(self.temp_folder_path)
        else:
            folder_structure = self._parse_folder(self.input_path)
            file_contents = self._process_files(self.input_path)

        folder_structure_header = "Folder Structure"
        file_contents_header = "File Contents"
        delimiter = "-" * 50

        final_text = f"{folder_structure_header}\n{delimiter}\n{folder_structure}\n\n{file_contents_header}\n{delimiter}\n{file_contents}"

        return final_text

    def get_file(self) -> None:
        text = self.get_text()
        if self.output_type == "txt":
            with open(self.output_path, "w") as file:
                file.write(text)
        elif self.output_type == "docx":
            doc = Document()
            doc.add_paragraph(text)
            doc.save(self.output_path)

    def _clone_github_repo(self) -> None:
        try:
            self.temp_folder_path = tempfile.mkdtemp(prefix="github_repo_")
            git.Repo.clone_from(self.input_path, self.temp_folder_path)
            if self.verbose:
                print("GitHub repository cloned successfully.")
        except Exception as e:
            print(f"Error cloning GitHub repository: {e}")

    def is_github_repo(self) -> bool:
        return self.input_path.startswith(
            "https://github.com/"
        ) or self.input_path.startswith("git@github.com:")

    def is_temp_folder_used(self) -> bool:
        return self.temp_folder_path is not None

    def clean_up_temp_folder(self) -> None:
        if self.temp_folder_path:
            shutil.rmtree(self.temp_folder_path)


def main():
    parser = argparse.ArgumentParser(description="Generate text from codebase.")
    parser.add_argument(
        "--input", help="Input path (folder or GitHub URL)", required=True
    )
    parser.add_argument("--output", help="Output file path", required=True)
    parser.add_argument(
        "--output_type", help="Output file type (txt or docx)", required=True
    )
    parser.add_argument(
        "--exclude_hidden",
        help="Exclude hidden files",
        required=False,
        type=bool,
        default=False,
    )
    parser.add_argument(
        "--verbose",
        help="Show useful information",
        required=False,
        type=bool,
        default=False,
    )
    args = parser.parse_args()

    try:
        code_to_text = CodebaseToText(
            input_path=args.input,
            output_path=args.output,
            output_type=args.output_type,
            verbose=args.verbose,
            exclude_hidden=args.exclude_hidden,
        )
        code_to_text.get_file()
    except ValidationError as e:
        print(f"Validation Error: {e}")

    if code_to_text.is_temp_folder_used():
        code_to_text.clean_up_temp_folder()


if __name__ == "__main__":
    main()
