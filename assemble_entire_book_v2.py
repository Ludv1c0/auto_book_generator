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
            # Supporta vari formati: array diretto o dizionari incasellati
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                for key in ['chapters', 'Capitoli', 'ChapterList']:
                    if key in data:
                        return data[key]
            print("Errore: Il file chapters.json non contiene un formato valido.")
            return None
    except FileNotFoundError:
        print("Errore: Il file chapters.json non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print("Errore: Il file chapters.json non è formattato correttamente.")
        return None

def load_subchapters(chapter_number):
    """Carica i sottocapitoli per un dato capitolo dal file JSON, gestendo diversi formati JSON."""
    try:
        with open(f'subchapters_chapter_{chapter_number}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Supporta vari formati: array diretto o dizionari incasellati
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                for key in ['subchapters', 'SubchapterList', 'sottocapitoli']:
                    if key in data:
                        return data[key]
            print(f"Errore: Il file subchapters_chapter_{chapter_number}.json non contiene un formato valido.")
            return None
    except FileNotFoundError:
        print(f"Avviso: Il file subchapters_chapter_{chapter_number}.json non è stato trovato. Verranno usati file .txt.")
        return None
    except json.JSONDecodeError:
        print(f"Errore: Il file subchapters_chapter_{chapter_number}.json non è formattato correttamente.")
        return None

def assemble_book():
    """Assembla il libro con capitoli e sottocapitoli in un file markdown."""
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
        chapter_content = f'# Capitolo {i+1}: {chapter.get("title", f"Capitolo {i+1}")}\n\n{chapter.get("description", "")}\n\n'

        # Carica i sottocapitoli dal file JSON
        subchapters = load_subchapters(i+1)
        
        if subchapters is not None:
            # Usa i sottocapitoli dal file JSON
            for subchapter_index, subchapter in enumerate(subchapters, start=1):
                # Prova a leggere il file di testo relativo al sottocapitolo
                try:
                    with open(f'subchapter_{i+1}_{subchapter_index}.txt', 'r', encoding='utf-8') as f:
                        subchapter_content = f.read()
                        # Aggiungi titolo dal JSON, con fallback al titolo generico
                        chapter_content += f'## {i+1}.{subchapter_index} {subchapter.get("title", f"Sottocapitolo {subchapter_index}")}\n\n{subchapter_content}\n\n'
                except FileNotFoundError:
                    print(f"Errore: Il file subchapter_{i+1}_{subchapter_index}.txt non è stato trovato.")
        else:
            # Se il file JSON non esiste, usa i file .txt con titoli generici
            subchapter_index = 1
            while True:
                try:
                    with open(f'subchapter_{i+1}_{subchapter_index}.txt', 'r', encoding='utf-8') as f:
                        subchapter_content = f.read()
                        chapter_content += f'## {i+1}.{subchapter_index} Sottocapitolo {subchapter_index}\n\n{subchapter_content}\n\n'
                    subchapter_index += 1
                except FileNotFoundError:
                    break

        # Aggiungi il contenuto del capitolo al libro
        book_content += chapter_content

    # Salva il libro completo in un file markdown
    with open('bookV2.md', 'w', encoding='utf-8') as f:
        f.write(book_content)

    print('Libro completo salvato in book.md')

if __name__ == '__main__':
    assemble_book()
