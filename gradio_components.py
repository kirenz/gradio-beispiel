# Interface-Beispiel mit mehreren unterschiedlichen Komponenten (Textbox, Dropdown, Slider).
import gradio as gr


# Die zugrunde liegende Logik kombiniert die Eingaben zu Text und Score.
def compute(name: str, stimmung: str, intensitaet: int):
    """Funktion erzeugt eine kurze Nachricht basierend auf Name, Stimmung und Intensität."""
    message = f'{name} fühlt sich {stimmung}'
    score = intensitaet * 10
    return message, score

# Wie zuvor beschreibt Interface alles, was die App braucht.
# Mehrere Eingaben oder Ausgaben werden als Liste übergeben.
gr.Interface(
    fn=compute,
    inputs=[
        # Textbox für frei eingegebene Daten (Name)
        gr.Textbox(label="Name eingeben"),
        # Dropdown zwingt zur Auswahl aus vorgegebenen Optionen (validiert Eingaben automatisch)
        gr.Dropdown(choices=["glücklich", "traurig", "aufgeregt"], label="Stimmung auswählen"),
        # Slider eignet sich für Zahlenbereiche; min/max/step geben den erlaubten Bereich vor
        gr.Slider(minimum=1, maximum=10, step=1, label="Intensität der Stimmung")
    ],
    outputs=[
        # Ausgabe einer Zeichenkette
        gr.Textbox(label="Nachricht"),
        # Ausgabe einer Zahl; Gradio zeigt automatisch passende Formatierung
        gr.Number(label="Stimmungswert")
    ],
    title="Gradio Komponenten Beispiel",
    description="Geben Sie Ihren Namen, Ihre Stimmung und die Intensität ein."
).launch()
