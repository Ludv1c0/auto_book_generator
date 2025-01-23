import json
import openai  # Importazione corretta del modulo openai

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

def generate_chapters():
    # Carica i segreti e il file di configurazione
    secrets = load_secrets()
    config = load_config()

    if secrets is None or config is None:
        return

    # Imposta la chiave API direttamente
    openai.api_key = secrets['OPENAI_API_KEY']

    prompt = f'''
Genera un elenco di capitoli per un libro con il titolo "{config['title']}".
- Numero di capitoli: {config['number_of_chapters']}
- Lunghezza dei capitoli: {config['chapter_length']}
- Informazioni aggiuntive: {config['additional_info_chapters']}
Fornisci unicamente il risultato in formato JSON con "title" e "description" per ogni capitolo.
    '''

    try:
        # Utilizzo di GPT-4o per generare i capitoli
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )


        print ("📝 risposta capitoli = ", response)

        chapters_text = response['choices'][0]['message']['content'].strip()

        # Assicurarsi che il testo sia un JSON valido
        try:
            chapters = json.loads(chapters_text)
        except json.JSONDecodeError:
            print("Errore nel parsing del JSON. Assicurati che il modello risponda con un JSON valido.")
            return

        # Salva il risultato in un file
        with open('chapters.json', 'w', encoding='utf-8') as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)

        print('Capitoli generati e salvati in chapters.json')

    except Exception as e:
        print(f"Errore nella chiamata API: {str(e)}")

if __name__ == '__main__':
    generate_chapters()
