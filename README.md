# LaurelLeaf

## HTML File Processing Tool

This Python program allows you to process HTML files within a selected folder, including:

- Removing `<script>` tags from the header.
- Removing `<nav></nav>` tags from the HTML content.
- Removing a user-specified string from `<link>` and `<img>` tags.
- Copying files from subfolders to a central `_files` folder in the root directory.
- Optionally deleting subfolders after a successful copy.

## Prerequisites

- Python 3.x is required to run this program. If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

## Installation

1. Install the required Python libraries using pip:

```bash
python3 -m pip install beautifulsoup4
```

2. Run the program:

```bash
python3 your_program.py
```


## Usage

1. Run the program and select a folder from which you want to process HTML files.

2. The program will perform the following actions:

- Remove `<script>` tags from the header.
- Remove `<nav></nav>` tags from the HTML content.
- Remove a user-specified string from `<link>` and `<img>` tags.
- Copy files from subfolders to a central `_files` folder in the root directory.
- Optionally delete subfolders after successful copying (you will be prompted to confirm).

3. You will see the processed subfolders and any subfolders that were deleted (if applicable) in the program's output.

## License

This program is available under the [MIT License](LICENSE).
