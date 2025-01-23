import json
import openai

# Funzione per caricare i segreti dal file secrets.json
def load_secrets():
    try:
        with open('secrets.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Errore: Il file secrets.json non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print("Errore: Il file secrets.json non è formattato correttamente.")
        return None

# Funzione per caricare il file di configurazione del libro
def load_config():
    try:
        with open('book_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Errore: Il file book_config.json non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print("Errore: Il file book_config.json non è formattato correttamente.")
        return None

# Funzione per caricare il file chapters.json e contare il numero di capitoli
def count_chapters(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Conta quante volte compare la chiave 'title' nel file
            number_of_chapters = sum(1 for item in data if 'title' in item)
            return number_of_chapters
    except FileNotFoundError:
        print(f"Errore: Il file {file_path} non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print(f"Errore: Il file {file_path} non è formattato correttamente.")
        return None

# Funzione per caricare e contare i sottocapitoli nel file JSON
def count_subchapters(file_path):
    """Restituisce il numero di sottocapitoli basato sul numero di 'title' nel file JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Conta quante volte compare la chiave 'title' nel file
            number_of_subchapters = sum(1 for item in data if 'title' in item)
            return number_of_subchapters
    except FileNotFoundError:
        print(f"Errore: Il file {file_path} non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print(f"Errore: Il file {file_path} non è formattato correttamente.")
        return None

def load_subchapters(file_path):
    """Funzione per caricare i sottocapitoli da un file JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data  # Assumi che il file contenga un array di sottocapitoli
    except FileNotFoundError:
        print(f"Errore: Il file {file_path} non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print(f"Errore: Il file {file_path} non è formattato correttamente.")
        return None

def generate_content():
    # Carica i segreti e il file di configurazione
    secrets = load_secrets()
    config = load_config()

    if secrets is None or config is None:
        return

    # Imposta la chiave API direttamente
    openai.api_key = secrets['OPENAI_API_KEY']

    # Conta il numero di capitoli nel file chapters.json
    number_of_chapters = count_chapters('chapters.json')

    if number_of_chapters is None:
        print("Errore: Impossibile determinare il numero di capitoli.")
        return

    print(f"Numero di capitoli trovati: {number_of_chapters}")

    # Loop sui capitoli
    for i in range(1, number_of_chapters + 1):
        # Carica i sottocapitoli per il capitolo corrente
        subchapters = load_subchapters(f'subchapters_chapter_{i}.json')

        if subchapters is None:
            print(f"Errore: Impossibile caricare i sottocapitoli per il capitolo {i}.")
            continue

        # Conta il numero di sottocapitoli
        number_of_subchapters = count_subchapters(f'subchapters_chapter_{i}.json')

        if number_of_subchapters is None:
            print(f"Errore: Impossibile determinare il numero di sottocapitoli per il capitolo {i}.")
            continue

        print(f"Numero di sottocapitoli trovati per il capitolo {i}: {number_of_subchapters}")

        for j, subchapter in enumerate(subchapters):
            # Controlla che ogni sottocapitolo sia un dizionario
            if isinstance(subchapter, dict):
                title = subchapter.get('title', 'Senza titolo')
                description = subchapter.get('description', 'Senza descrizione')
            else:
                print(f"Errore: Il sottocapitolo {j+1} nel capitolo {i} non è un oggetto JSON valido.")
                print(f"Contenuto del sottocapitolo non valido: {subchapter}")
                continue

            prompt = f'''
Tieni conto delle preferenze: "{config['additional_info_content']}". Genera il contenuto dettagliato per il sottocapitolo "{title}" con la descrizione "{description}". Evita le introduzioni e vai direttamente al contenuto. Evita anche i saluti e i convenevoli poiché il testo sarà inserito in un contesto più ampio.
Fornisci un testo completo di lunghezza: {config['content_length']}. Utilizza, se necessario, il formato markdown per i formati.
            '''

            try:
                # Utilizza GPT-4o per generare il contenuto dei sottocapitoli
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )

                print ("📝 Risposta contenuto = ", response)

                subchapter_content = response['choices'][0]['message']['content'].strip()

                # Salva il contenuto del sottocapitolo in un file
                with open(f'subchapter_{i}_{j+1}.txt', 'w', encoding='utf-8') as f:
                    f.write(subchapter_content)

                print(f'Contenuto per il sottocapitolo {i}.{j+1} salvato in subchapter_{i}_{j+1}.txt')

            except Exception as e:
                print(f"Errore nella chiamata API per il sottocapitolo {i}.{j+1}: {str(e)}")

if __name__ == '__main__':
    generate_content()
