import subprocess


# Esegui il comando per riprodurre il suono di sistema
def play_system_sound():
    nv = 6
    while nv > 0:
        # Usa il comando "afplay" per riprodurre il suono di sistema
        subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
        nv = nv -1
    print("Suono di avviso riprodotto!")

# Chiamata alla funzione per far suonare la campanella
play_system_sound()
