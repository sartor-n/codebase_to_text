
# Codebase to Text

This tool allows you to convert a codebase into a text format, with options to include or exclude certain files based on their extensions. It supports both plain text and DOCX output formats. 

## Features

- Parse a directory and output its structure and contents to a text or DOCX file.
- Exclude hidden files from processing.
- Specify file extensions to include only certain types of files.
- Handle both local directories and GitHub repositories as input sources.

## Installation

Make sure you have Python 3.x installed. You also need to install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can use this tool either as a Python module or through the command line interface (CLI).

### Command Line Interface (CLI)

Use the following arguments:

- `--input`: The input path, which can be a local folder or a GitHub repository URL.
- `--output`: The path where the output file will be saved.
- `--output_type`: The format of the output file, either `txt` or `docx`. Defaults to `txt`.
- `--exclude_hidden`: Exclude hidden files and folders from processing. (Default: False)
- `--verbose`: Display detailed processing information. (Default: False)
- `--file_extensions`: Specify which file extensions to include in the output. Provide a comma-separated list of extensions. (Default: `[".py"]`)

#### Example CLI Usage

```bash
codebase_to_text --input your_folder_path --output output.txt --output_type txt --exclude_hidden True --file_extensions .py,.txt
```

This command will generate a text file `output.txt` from the specified folder, including only Python and text files, while excluding hidden files.

### Python Module

You can also use this tool directly as a Python module:

```python
from codebase_to_text import CodebaseToText

code_to_text = CodebaseToText(
    input_path="your_folder_path",
    output_path="output.txt",
    output_type="txt",
    exclude_hidden=True,
    file_extensions=[".py", ".txt"]
)

code_to_text.get_file()
```

## Testing

Unit tests are included to validate the functionality. To run the tests:

```bash
python -m unittest discover -s tests
```

This will execute the tests in the `tests` directory.


## License

This project is licensed under the MIT License.
