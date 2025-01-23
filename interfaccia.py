import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
import os
import subprocess
import sys
import shutil

# Funzione per caricare e visualizzare i campi di un file JSON
def load_json_file(json_file_path, frame):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    for key, value in data.items():
        tk.Label(frame, text=key).pack(anchor='w')
        entry = tk.Entry(frame, width=100)
        entry.insert(0, str(value))  # Inserisci il valore attuale
        entry.pack(pady=5)
        # Salva l'entry per usarla in seguito per salvare i valori modificati
        frame.entries[key] = entry

# Funzione per salvare le modifiche in un file JSON e caricare il successivo
def save_json_file(json_file_path, frame, next_json_file=None, next_frame=None):
    data = {}
    for key, entry in frame.entries.items():
        data[key] = entry.get()  # Ottieni il valore modificato dall'utente
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Salvato", f"Il file {json_file_path} è stato salvato con successo!")

    # Mostra il frame successivo (il prossimo file JSON) se disponibile
    if next_frame is not None:
        next_frame.pack(pady=20)

# Funzione per eseguire i vari script e mostrare l'output nella GUI
def run_all_scripts(output_text):
    script_list = ["generate_chapters.py", "generate_subchapters.py", "generate_content.py", 
                   "assemble_entire_book_v2.py", "genera_epub.py", "genera_docx.py"]
    
    for script in script_list:
        try:
            result = subprocess.run([sys.executable, script], check=True, capture_output=True, text=True)
            output_text.insert(tk.END, f"{script} eseguito con successo:\n{result.stdout}\n")
        except subprocess.CalledProcessError as e:
            output_text.insert(tk.END, f"Errore durante l'esecuzione di {script}:\n{e.stderr}\n")

# Funzione principale per gestire la GUI
def main():
    root = tk.Tk()
    root.title("Gestione Programma di Generazione Libro")

    # Creazione di un canvas con scrollbar per l'interfaccia scorrevole
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Ottieni la directory corrente in cui si trova lo script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Percorsi dei file JSON nella directory corrente
    book_config_path = os.path.join(current_directory, "book_config.json")
    dati_libro_path = os.path.join(current_directory, "dati_libro.json")
    secrets_path = os.path.join(current_directory, "secrets.json")

    # Creazione delle sezioni per i JSON
    sections = [
        {"name": "book_config.json", "path": book_config_path},
        {"name": "dati_libro.json", "path": dati_libro_path},
        {"name": "secrets.json", "path": secrets_path}
    ]

    # Frames per ciascun file JSON
    frames = []
    for i, section in enumerate(sections):
        frame = tk.Frame(scrollable_frame)
        frame.entries = {}
        tk.Label(frame, text=section["name"]).pack(anchor='w')
        load_json_file(section["path"], frame)
        frames.append(frame)

        if i == 0:
            # Mostra il primo frame
            frame.pack(pady=20)
        else:
            # Nascondi gli altri frame inizialmente
            frame.pack_forget()

    # Aggiungi un pulsante di salvataggio per ogni file JSON
    for i in range(len(frames)):
        if i < len(frames) - 1:
            save_button = tk.Button(frames[i], text=f"Salva {sections[i]['name']}", command=lambda p=sections[i]['path'], f=frames[i], nf=frames[i+1]: save_json_file(p, f, nf))
        else:
            # L'ultimo pulsante di salvataggio aprirà la sezione per eseguire il programma
            save_button = tk.Button(frames[i], text=f"Salva {sections[i]['name']}", command=lambda p=sections[i]['path'], f=frames[i]: save_json_file(p, f))
        save_button.pack(pady=10)

    # Sezione per eseguire il programma e mostrare l'output
    output_frame = tk.Frame(scrollable_frame)
    
    output_label = tk.Label(output_frame, text="Output del programma:")
    output_label.pack(anchor='w')

    output_text = scrolledtext.ScrolledText(output_frame, width=100, height=10)
    output_text.pack(pady=10)

    # Pulsante per eseguire il programma e mostrare l'output
    run_button = tk.Button(output_frame, text="Esegui Programma", command=lambda: run_all_scripts(output_text), bg="red", fg="white")
    run_button.pack(pady=10)

    # Quando l'ultimo JSON è salvato, mostra questa sezione
    save_button.config(command=lambda p=sections[-1]['path'], f=frames[-1]: [save_json_file(p, f), output_frame.pack(pady=20)])

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

if __name__ == '__main__':
    main()
