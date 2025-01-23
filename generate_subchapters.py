import json
import openai  # Importa correttamente il modulo openai

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

def load_chapters():
    """Funzione per caricare i capitoli da chapters.json, supportando sia il formato array diretto che quello con la chiave 'chapters', 'Capitoli', ecc."""
    try:
        with open('chapters.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Verifica se il file contiene direttamente un array o è racchiuso in una chiave (ad es. "chapters", "Capitoli")
            if isinstance(data, list):
                return data  # Formato diretto: l'array JSON è già a livello principale
            elif isinstance(data, dict):
                for key in ['chapters', 'Capitoli', 'ChapterList']:  # Aggiungi altre chiavi se necessario
                    if key in data:
                        return data[key]  # Restituisce l'array sotto la chiave trovata
            print("Errore: Il file chapters.json non è in un formato valido.")
            return None
    except FileNotFoundError:
        print("Errore: Il file chapters.json non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print("Errore: Il file chapters.json non è formattato correttamente.")
        return None

def generate_subchapters():
    # Carica i segreti e il file di configurazione
    secrets = load_secrets()
    config = load_config()

    if secrets is None or config is None:
        return

    # Imposta la chiave API direttamente
    openai.api_key = secrets['OPENAI_API_KEY']

    # Carica i capitoli dal file chapters.json
    chapters = load_chapters()

    if chapters is None:
        return

    for i, chapter in enumerate(chapters):
        # Verifica che ogni capitolo sia un dizionario
        if not isinstance(chapter, dict):
            print(f"Errore: Il capitolo {i+1} non è un oggetto JSON valido.")
            continue

        prompt = f'''
        Per il capitolo "{chapter['title']}" ({chapter['description']}), genera un elenco di sottocapitoli.
        - Numero di sottocapitoli: {config['number_of_subchapters_per_chapter']}
        - Lunghezza dei sottocapitoli: {config['subchapter_length']}
        Fornisci il risultato in formato JSON come un array, con ciascun sottocapitolo contenente le chiavi "title" e "description".
        Esempio:
        [
          {{
            "title": "Titolo del sottocapitolo 1",
            "description": "Descrizione del sottocapitolo 1"
          }},
          {{
            "title": "Titolo del sottocapitolo 2",
            "description": "Descrizione del sottocapitolo 2"
          }}
        ]
        '''

        try:
            # Utilizza GPT-4o per generare i sottocapitoli
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            print("📝 Risposta sottocapitoli = ", response)

            subchapters_text = response['choices'][0]['message']['content'].strip()

            # Assicurarsi che il testo sia un JSON valido
            try:
                subchapters = json.loads(subchapters_text)
            except json.JSONDecodeError:
                print(f"Errore nel parsing del JSON per il capitolo {i+1}.")
                continue

            # Salva i sottocapitoli in un file
            with open(f'subchapters_chapter_{i+1}.json', 'w', encoding='utf-8') as f:
                json.dump(subchapters, f, ensure_ascii=False, indent=2)

            print(f'Sottocapitoli per il capitolo {i+1} salvati in subchapters_chapter_{i+1}.json')

        except Exception as e:
            print(f"Errore nella chiamata API per il capitolo {i+1}: {str(e)}")

if __name__ == '__main__':
    generate_subchapters()
