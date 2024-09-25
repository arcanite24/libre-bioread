import sys
import os
import re
import zipfile
import tempfile
import subprocess
from bs4 import BeautifulSoup


def apply_bionic_reading_to_node(text_node, soup):
    word_pattern = re.compile(r"\b\w+\b", re.UNICODE)

    new_contents = []
    last_end = 0
    text = text_node.string

    for match in word_pattern.finditer(text):
        start, end = match.span()
        word = match.group()

        if start > last_end:
            new_contents.append(text[last_end:start])

        length = len(word)
        bold_chars = max(1, int(round(length * 0.5)))
        bold_part = word[:bold_chars]
        normal_part = word[bold_chars:]

        # Create a <strong> tag using the soup object
        bold_tag = soup.new_tag("strong")
        bold_tag.string = bold_part
        new_contents.append(bold_tag)

        # Append the normal part as text
        new_contents.append(normal_part)

        last_end = end

    if last_end < len(text):
        new_contents.append(text[last_end:])

    # Replace the original text node with the new contents
    text_node.replace_with(*new_contents)


def process_htmlz(input_file, output_file, original_format):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Convert ebook to HTMLZ format
        htmlz_file = os.path.join(tmpdir, "book.htmlz")
        cmd_convert_to_htmlz = ["ebook-convert", input_file, htmlz_file]
        subprocess.run(cmd_convert_to_htmlz, check=True)

        # Extract HTMLZ contents
        with zipfile.ZipFile(htmlz_file, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        # Apply Bionic Reading effect to all HTML files
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                if file.endswith(".html") or file.endswith(".htm"):
                    html_path = os.path.join(root, file)
                    with open(html_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f, "html.parser")
                    # Process text nodes
                    for text_node in soup.find_all(string=True):
                        parent = text_node.parent.name if text_node.parent else None
                        if parent in ["style", "script", "[document]", "head", "title"]:
                            continue
                        if text_node.strip():
                            apply_bionic_reading_to_node(text_node, soup)
                    # Save modified HTML
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(str(soup))

        # Rezip contents into HTMLZ
        with zipfile.ZipFile(htmlz_file, "w") as zip_ref:
            for folder_name, subfolders, filenames in os.walk(tmpdir):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    # Avoid including the HTMLZ file itself
                    if file_path == htmlz_file:
                        continue
                    arcname = os.path.relpath(file_path, tmpdir)
                    zip_ref.write(file_path, arcname=arcname)

        # Convert HTMLZ back to the original format
        cmd_convert_back = [
            "ebook-convert",
            htmlz_file,
            output_file,
            "--output-profile=default",
        ]
        subprocess.run(cmd_convert_back, check=True)


def main():
    if len(sys.argv) != 2:
        print("Usage: python bionic_reader.py input_file")
        sys.exit(1)
    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print("File not found.")
        sys.exit(1)
    file_name, file_ext = os.path.splitext(input_file)
    supported_formats = [".epub", ".mobi", ".azw3"]
    if file_ext.lower() not in supported_formats:
        print("Supported input formats are .epub, .mobi, and .azw3.")
        sys.exit(1)
    output_file = f"{file_name}_fastread{file_ext}"
    process_htmlz(input_file, output_file, file_ext.lower()[1:])
    print(f"Processed file saved as {output_file}")


if __name__ == "__main__":
    main()
