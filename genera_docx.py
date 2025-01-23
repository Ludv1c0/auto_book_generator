import os
import json
import pypandoc

# Funzione per creare un file .txt con metadati DOCX
def create_metadata_txt(data, metadata_file):
    print("Creating metadata file for DOCX...")

    with open(metadata_file, 'w') as f:
        f.write(f'title: {data["titolo"]}\n')
        f.write(f'author: {data["autore"]}\n')
        if "sottotitolo" in data:
            f.write(f'subtitle: {data["sottotitolo"]}\n')

    print(f"Metadata file created: {metadata_file}")

# Funzione per creare un DOCX da markdown e metadati
def convert_markdown_to_docx(markdown_file, output_docx, metadata_file):
    print("Converting Markdown to DOCX using Pandoc...")

    # Comandi per Pandoc
    pandoc_args = [
        "--metadata-file", metadata_file,
        "--toc"  # Aggiunge automaticamente l'indice dei contenuti
    ]
    
    output = pypandoc.convert_file(markdown_file, 'docx', outputfile=output_docx, extra_args=pandoc_args)
    assert output == "", "Error in converting markdown to DOCX"
    print(f"Conversion complete: {output_docx}")

# Funzione principale
def create_print_ready_docx(markdown_file, json_data_file):
    # Nome del DOCX finale
    final_docx = "final_bookV2.docx"
    metadata_file = "metadata.txt"

    # Carica i dati dal file JSON
    with open(json_data_file, 'r') as f:
        data = json.load(f)

    # Crea il file di metadati
    create_metadata_txt(data, metadata_file)

    # Converti markdown in DOCX con metadati
    convert_markdown_to_docx(markdown_file, final_docx, metadata_file)

    # Rimuovi file temporanei
    os.remove(metadata_file)
    print(f"Cleaned up temporary metadata file.")

if __name__ == "__main__":
    # Specifica i file necessari
    markdown_file = "bookV2.md"
    json_data_file = "dati_libro.json"

    # Verifica che tutti i file esistano
    if os.path.exists(markdown_file) and os.path.exists(json_data_file):
        create_print_ready_docx(markdown_file, json_data_file)
    else:
        print("Error: Ensure that the markdown file and JSON data file exist in the same directory!")
