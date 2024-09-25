# Libre BioRead

A Python command-line interface (CLI) script that applies the Bionic Reading effect to .epub, .mobi, and .azw3 ebook files. The script processes the text within the ebook, bolding parts of words to enhance reading speed and comprehension.

## Features

- Supports .epub, .mobi, and .azw3 ebook formats.
- Preserves the original ebook formatting and structure.
- Utilizes Calibre's command-line tools for robust ebook conversion.
- Applies the Bionic Reading effect by bolding portions of words.

## Requirements

- **Python 3.x**: Ensure you have Python 3 installed on your system.
- **Calibre Command-Line Tools**: The script uses Calibre's ebook-convert utility.
  - Windows: Calibre's CLI tools are usually located at `C:\Program Files\Calibre2`. Add this directory to your system's PATH environment variable.
  - macOS: Install Calibre and create symbolic links to the CLI tools in `/usr/local/bin`.
  - Linux: Install Calibre via your package manager or from the Calibre website.
- **Python Libraries**:
  - BeautifulSoup4: Install using `pip install beautifulsoup4`.

## Installation

1. Clone the Repository:
```bash
git clone https://github.com/yourusername/bionic-reader-cli.git
```

2. Install Required Python Libraries:
```bash
pip install beautifulsoup4
```

3. Ensure Calibre CLI Tools Are Accessible:
- Add Calibre's installation directory to your system's PATH.
- Verify that `ebook-convert` is accessible by running:
```bash
ebook-convert --version
```

## Usage
```bash
python apply_bioread.py <input_file>
```

Replace `<input_file>` with the path to your .epub, .mobi, or .azw3 ebook file.
The processed ebook will be saved in the same directory with a `_fastread` suffix in the filename.

Example:
```bash
python apply_bioread.py "The Great Gatsby.epub"
```
This will create `The Great Gatsby_fastread.epub`.

## Rules Applied (Bionic Reading Effect)

The script enhances readability by applying the following rules to the text:

1. **Bolding Part of Each Word**:
   - For each word, the first half of the characters are bolded.
   - If the word has an odd number of characters, the number of bolded characters is rounded up.

2. **Preserving Original Formatting**:
   - The script only modifies text nodes, leaving the rest of the ebook's formatting intact.
   - It avoids processing text within certain HTML elements like `style`, `script`, `head`, and `title`.

3. **Proper HTML Manipulation**:
   - Uses BeautifulSoup to manipulate the HTML DOM safely.
   - Ensures that bold tags are correctly inserted without breaking the HTML structure.

## Limitations

- **DRM-Protected Ebooks**: The script cannot process DRM-protected ebooks.
- **Ebook Reader Compatibility**: Some ebook readers may not support the HTML tags or CSS styles used. The script attempts to maximize compatibility, but results may vary.
- **Unicode Support**: If using the Unicode bold character method, ensure your ebook reader's font supports these characters.

## Notes for Kindle users
- This is tested with .epub files, then converting them with Calibre to .azw3, they work great!
- You can select any font in your Kindle device, it will work. No extra settings needed on Calibre.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.