# Automatic Book Generator

## About the Project

This program is a **personal project**, developed for **passion and hobby**, and was never intended for public release. It is maintained sporadically, may contain **bugs**, and has been developed in **Italian**. Below is a detailed description of how to use the program, along with the necessary disclaimers and usage restrictions.

---

## **Important Disclaimers and Legal Notices**

### Disclaimer (English)

- This program is provided as-is, without any guarantees of correctness, functionality, or fitness for any particular purpose.
- **I do not accept any responsibility** for how this program is used, any issues that may arise, or any consequences of using this software.
- **This program must only be used for personal purposes**. Commercial use of any kind is strictly prohibited.
- It is forbidden to use this program to **generate content intended for sale on online stores** or other commercial platforms.
- The program **may contain errors** and is provided as a learning tool or for entertainment purposes only.

---

### **Important Note on Automatic Content Generation**

⚠️ **Using this program to generate content can have serious legal and ethical consequences.**

- **Violations of copyright**: Automatically generated content may infringe on intellectual property laws if it includes protected materials.
- **Legal and financial risks**: Using automatically generated content without proper consideration for copyright can lead to lawsuits and financial penalties.
- **Harm to creativity and quality**: Automatic content generation can harm human creativity, reduce the quality of online content, and contribute to an unethical and less authentic digital ecosystem.

### Moral and Ethical Obligations:

- You **must cite the original author** when using this program.
- Always verify that the generated content does not infringe on copyright or violate intellectual property laws.

---

### **Disclaimer (Italian)**

- Questo programma è fornito così com'è, senza alcuna garanzia di correttezza, funzionalità o idoneità per uno scopo particolare.
- **Non mi assumo alcuna responsabilità** per l'uso di questo programma, eventuali problemi derivanti o conseguenze derivanti dall'utilizzo di questo software.
- **Questo programma deve essere usato solo per scopi personali**. È severamente vietato qualsiasi utilizzo commerciale.
- È proibito utilizzare questo programma per **generare contenuti destinati alla vendita su store online** o altre piattaforme commerciali.
- Il programma **potrebbe contenere errori** ed è fornito come strumento educativo o per scopi di intrattenimento.

---

### **Nota importante sulla generazione automatica di contenuti**

⚠️ **Utilizzare questo programma per generare contenuti può avere gravi conseguenze legali ed etiche.**

- **Violazione del diritto d'autore**: I contenuti generati automaticamente potrebbero violare le leggi sulla proprietà intellettuale se contengono materiali protetti.
- **Rischi legali ed economici**: Chi utilizza contenuti generati automaticamente senza considerare i diritti d'autore può incorrere in azioni legali e sanzioni economiche.
- **Danno alla creatività e alla qualità**: La generazione automatica di contenuti danneggia la creatività umana, riduce la qualità dei contenuti online e contribuisce a un ecosistema digitale meno etico e autentico.

### Obblighi morali ed etici:

- È obbligatorio **citare l'autore originale** quando si utilizza questo programma.
- Verificare sempre che i contenuti generati non violino i diritti d'autore o le leggi sulla proprietà intellettuale.

---

## **How It Works**

The program generates complete books automatically by leveraging OpenAI APIs. It includes several components, which are described below.

### **Required Files**

1. **`secrets.json`**
   - Stores the OpenAI API key. The user must provide their own API key in this file.
   - Example format:
     ```json
     {
         "OPENAI_API_KEY": "your-openai-api-key"
     }
     ```

2. **`book_config.json`**
   - Contains configuration data for the book generation process.
   - Specifies the number of chapters, their length, and additional metadata.
   - Example format:
     ```json
     {
         "title": "Your Book Title",
         "number_of_chapters": "Number of chapters to generate",
         "chapter_length": "Length of each chapter",
         "subchapter_length": "Length of subchapters",
         "number_of_subchapters_per_chapter": "Number of subchapters",
         "content_length": "Length of content per subchapter",
         "additional_info_chapters": "Description of the chapters' purpose",
         "additional_info_summary": "Summary to include in the book",
         "additional_info_content": "Style and content details"
     }
     ```

3. **`dati_libro.json`**
   - Contains additional book metadata such as the title, author, subtitle, dedication, and index settings.
   - Example format:
     ```json
     {
         "titolo": "Book Title",
         "autore": "Author Name",
         "sottotitolo": "Subtitle of the book",
         "dedica": "Dedication text",
         "indice": true
     }
     ```

4. **`cover.jpeg`**
   - The cover image for the book in JPEG format.

   
     Please note that some prompts that are sent to OpenAi may contain deprecated api calls, deprecated models, or a prompt that is not exactly suitable for the content you want to generate. Make sure to modify it accordingly
---

### **Program Components**

The project contains the following Python scripts:

1. **`esegui_tutto.py`**
   - Acts as a master script to execute all other scripts in sequence to generate the final book.
   - Prompts the user to confirm that all necessary files are prepared before proceeding.
   - Outputs the final book in `.md`, `.epub`, and `.docx` formats.

2. **`generate_chapters.py`**
   - Generates a list of chapters based on the configuration in `book_config.json`.
   - Uses OpenAI APIs to create chapter titles and descriptions.

3. **`generate_subchapters.py`**
   - Generates subchapters for each chapter using the details from `chapters.json`.
   - Saves each subchapter in a dedicated JSON file.

4. **`generate_content.py`**
   - Generates detailed content for each subchapter using OpenAI APIs.
   - Outputs the content in `.txt` files, one for each subchapter.

5. **`assemble_entire_book.py` and `assemble_entire_book_v2.py`**
   - Combines chapters and subchapters into a complete book.
   - Saves the final book in `book.md` for subsequent conversion.

6. **`genera_docx.py`**
   - Converts the markdown file (`book.md`) into a `.docx` format using `pypandoc`.

7. **`genera_epub.py`**
   - Converts the markdown file (`book.md`) into an `.epub` format using `pypandoc`.
   - Includes metadata and a cover image.

8. **`interfaccia.py`**
   - A GUI prototype built with Tkinter.
   - Allows users to edit JSON files (`book_config.json`, `dati_libro.json`, `secrets.json`) and execute scripts from a graphical interface.
   - This interface is incomplete and open to suggestions for improvement.

9. **`suono_avviso.py`**
   - Plays a system sound upon completion of tasks (designed for macOS).


---

### **How to Use**

1. ***Prepare the following files in the program directory***:
   - `secrets.json` (with your OpenAI API key)
   - `book_config.json`
   - `dati_libro.json`
   - `cover.jpeg`

2. ***Install the required libraries and dependencies***:
   To ensure the program works correctly, you need to install the following Python libraries. Run this command in your terminal:

     ```bash
     pip install openai pypandoc tkinter
     ```
****Details of the libraries:****

- **`openai`**: Used to access OpenAI's APIs for generating book content.
- **`pypandoc`**: Converts the generated Markdown (`book.md`) into EPUB and DOCX formats.
- **`tkinter`**: Provides the GUI for editing JSON files and managing the process. *(Note: `tkinter` is included with most Python installations but may require additional system setup on some platforms.)*

**System dependencies for `pypandoc`:**
The `pypandoc` library requires Pandoc to be installed on your system. Follow the instructions below based on your operating system:

- **Ubuntu/Debian**:
  ```bash
  sudo apt install pandoc
  ```

- **macOS**:
  Install using Homebrew:
  ```bash
  brew install pandoc
  ```

- **Windows**:
  Download Pandoc from the official website: [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

**Acknowledgments**:
Special thanks to the creators and maintainers of these libraries for their incredible tools and contributions. This project has no affiliation with OpenAI, Pandoc, or any other software/library mentioned above or in the code.

3. ***Run the `esegui_tutto.py` script***:
```bash
python esegui_tutto.py
```
*(sometimes you should use python3 instead)*

Follow the on-screen instructions to generate the book.


### **Outputs**

The program generates the following files:
- A markdown file: `book.md`
- An EPUB file: `final_bookV2.epub`
- A DOCX file: `final_bookV2.docx`

---

### **Notes on Versions**

- Multiple versions of some scripts (e.g., `assemble_entire_book.py` and `assemble_entire_book_v2.py`) are included for reference. These earlier versions may be useful for understanding the development process.
- The GUI (`interfaccia.py`) is in a **prototype stage** and is incomplete.

---

### **Acknowledgments**

- This program was created by **Ludv1c0 @ GitHub**.
- Please ensure that any use of this program includes proper attribution to the original author.

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
