import subprocess
import sys
import time


def play_system_sound():
    nv = 6
    while nv > 0:
        # Usa il comando "afplay" per riprodurre il suono di sistema
        subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
        nv = nv -1
    print("Suono di avviso riprodotto!")




def run_script(script_name):
    """
    Funzione per eseguire un singolo script Python.
    """
    try:
        print(f"Eseguendo {script_name}...")
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(result.stdout)  # Stampa l'output dello script
        print(f"{script_name} eseguito con successo.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione di {script_name}: {e.stderr}")
        sys.exit(1)  # Termina l'esecuzione se c'è un errore


def main():
    """
    Funzione principale per eseguire tutti gli script in serie.
    """
    scripts = [
        "generate_chapters.py",
        "generate_subchapters.py",
        "generate_content.py",
        "assemble_entire_book_v2.py",
        "genera_epub.py",
        "genera_docx.py",
    ]

    for script in scripts:
        run_script(script)

    print("Tutti gli script sono stati eseguiti con successo, il libro è stato generato.")

if __name__ == '__main__':
    print ("verifica di avere correttamente settato: \n - book_config.json \n - dati_libro.json \n - secrets.json (con la chiave api di openai. ricrodati poi di revocare la chiave) \n - cover.jpeg \n \n PREMI INVIO QUANDO HAI CONCLUSO ")
    input ("➡️ premi invio per iniziare a creare📝")
    time.sleep(5)
    print ("inizio a creare il tuo libro")
    main()
    play_system_sound()
