import os
import json
import pypandoc

# Funzione per creare un file .txt con metadati EPUB
def create_metadata_txt(data, metadata_file):
    print("Creating metadata file for EPUB...")
    
    with open(metadata_file, 'w') as f:
        f.write(f'title: {data["titolo"]}\n')
        f.write(f'author: {data["autore"]}\n')
        if "sottotitolo" in data:
            f.write(f'subtitle: {data["sottotitolo"]}\n')

    print(f"Metadata file created: {metadata_file}")

# Funzione per creare un EPUB da markdown e metadati
def convert_markdown_to_epub(markdown_file, output_epub, metadata_file, cover_image):
    print("Converting Markdown to EPUB using Pandoc...")

    # Comandi per Pandoc
    pandoc_args = [
        "--metadata-file", metadata_file,
        "--epub-cover-image", cover_image,
        "--toc"  # Aggiunge automaticamente l'indice dei contenuti
    ]
    
    output = pypandoc.convert_file(markdown_file, 'epub', outputfile=output_epub, extra_args=pandoc_args)
    assert output == "", "Error in converting markdown to EPUB"
    print(f"Conversion complete: {output_epub}")

# Funzione principale
def create_print_ready_epub(markdown_file, cover_image, json_data_file):
    # Nome del EPUB finale
    final_epub = "final_bookV2.epub"
    metadata_file = "metadata.txt"

    # Carica i dati dal file JSON
    with open(json_data_file, 'r') as f:
        data = json.load(f)

    # Crea il file di metadati
    create_metadata_txt(data, metadata_file)

    # Converti markdown in EPUB con copertina e metadati
    convert_markdown_to_epub(markdown_file, final_epub, metadata_file, cover_image)

    # Rimuovi file temporanei
    os.remove(metadata_file)
    print(f"Cleaned up temporary metadata file.")

if __name__ == "__main__":
    # Specifica i file necessari
    markdown_file = "bookV2.md"
    cover_image = "cover.jpeg"
    json_data_file = "dati_libro.json"

    # Verifica che tutti i file esistano
    if os.path.exists(markdown_file) and os.path.exists(cover_image) and os.path.exists(json_data_file):
        create_print_ready_epub(markdown_file, cover_image, json_data_file)
    else:
        print("Error: Ensure that the markdown file, cover image, and JSON data file exist in the same directory!")
