# LaurelLeaf

## HTML File Processing Tool

This Python program allows you to process HTML files within a selected folder, including:

- **Clean HTML Content**: The program can remove various elements from the HTML content such as scripts, links, meta tags, iframes, navigation tags, and more.

- **Filter URLs**: You can remove URLs from anchor tags in HTML files. Optionally, you can filter out GitHub repository links.

- **Convert to PDF**: The program provides an option to convert the cleaned HTML content to PDF using the wkhtmltopdf library.


## Prerequisites

Before using this program, make sure you have the following prerequisites:

- Python 3.x: The program is written in Python and requires a Python interpreter.

- Tkinter: Tkinter is used for creating the graphical user interface. It is typically included with Python, so you might not need to install it separately.

- wkhtmltopdf: To convert HTML content to PDF, you need to have the wkhtmltopdf library installed. Make sure it's available in your system's PATH or specify the path in the program.

- BeautifulSoup4: You can install BeautifulSoup4 using pip:

  ```bash
   python3 -m pip install beautifulsoup4
  ```

   ```sh
   pip install pdfkit
   ```

## Run the program:

```bash
python3 app.py
```



## How to Use

1. **Choose a Folder to Clean**:
   - Click the "Select a Folder" button.
   - Navigate to and select the folder containing HTML files to be cleaned.

2. **Apply Cleaning Options**:
   - You can select various cleaning options, including:
       - Removing links to external sources.
       - Removing GitHub links (if checked, the user will be prompted before deletion).
       - Skipping subfolders (if checked, you will be prompted before deletion).

3. **Convert to PDF (Optional)**:
   - Provide input and output folders for PDF conversion.
   - Click the "Browse" buttons to select these folders.
   - Click the "Convert to PDF" button to start the conversion process. The program will generate PDF files from the cleaned HTML content.

## Running the Program

- Execute the Python script to launch the GUI and start using the tool.
- The program will guide you through the process, and you can view the progress and results in the GUI itself.


3. You will see the processed subfolders and any subfolders that were deleted (if applicable) in the program's output.

## License

This program is available under the [MIT License](LICENSE).
