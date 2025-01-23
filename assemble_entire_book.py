import json

def load_secrets():
    """Funzione per caricare i segreti dal file secrets.json"""
    try:
        with open('secrets.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Errore: Il file secrets.json non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print("Errore: Il file secrets.json non è formattato correttamente.")
        return None

def load_config():
    """Funzione per caricare il file di configurazione del libro, gestendo diversi formati."""
    try:
        with open('book_config.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ritorna il titolo e altre informazioni se presenti
            return {
                "title": data.get("title", "Titolo del libro non trovato"),
                "additional_info_summary": data.get("additional_info_summary", "")
            }
    except FileNotFoundError:
        print("Errore: Il file book_config.json non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print("Errore: Il file book_config.json non è formattato correttamente.")
        return None

def load_chapters():
    """Funzione per caricare i capitoli da chapters.json, supportando diversi formati JSON."""
    try:
        with open('chapters.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Verifica se il file contiene un array di capitoli direttamente o se è incasellato sotto una chiave
            if isinstance(data, list):
                return data  # Formato diretto
            elif isinstance(data, dict):
                for key in ['chapters', 'Capitoli', 'ChapterList']:  # Supporta diverse chiavi
                    if key in data:
                        return data[key]  # Restituisci l'array sotto la chiave
            print("Errore: Il file chapters.json non contiene un formato valido.")
            return None
    except FileNotFoundError:
        print("Errore: Il file chapters.json non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print("Errore: Il file chapters.json non è formattato correttamente.")
        return None

def assemble_book():
    # Carica la configurazione e il titolo del libro
    config = load_config()
    if config is None:
        return
    
    title = config["title"]
    book_content = f'# {title}\n\n{config["additional_info_summary"]}\n\n'

    # Carica i capitoli dal file chapters.json
    chapters = load_chapters()
    if chapters is None:
        return

    for i, chapter in enumerate(chapters):
        # Prepara il contenuto del capitolo
        chapter_content = f'# Capitolo {i+1}: {chapter.get("title", f"Capitolo {i+1}")}\n\n{chapter.get("description", "")}\n\n'

        # Tentativo di aprire i file .txt dei sottocapitoli senza basarsi sul JSON
        subchapter_index = 1
        while True:
            try:
                # Prova a leggere i file dei sottocapitoli con la convenzione subchapter_{i+1}_{subchapter_index}.txt
                with open(f'subchapter_{i+1}_{subchapter_index}.txt', 'r', encoding='utf-8') as f:
                    subchapter_content = f.read()
                    # Aggiungi un titolo generico per il sottocapitolo se non esiste nel JSON
                    chapter_content += f'## {i+1}.{subchapter_index} Sottocapitolo {subchapter_index}\n\n{subchapter_content}\n\n'
                subchapter_index += 1
            except FileNotFoundError:
                # Quando non ci sono più file di sottocapitoli da leggere, esci dal ciclo
                break

        # Aggiungi il contenuto del capitolo al libro
        book_content += chapter_content

    # Salva il libro completo in un file markdown
    with open('book.md', 'w', encoding='utf-8') as f:
        f.write(book_content)

    print('Libro completo salvato in book.md')

if __name__ == '__main__':
    assemble_book()
