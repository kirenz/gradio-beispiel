import gradio as gr

def compute(name: str, stimmung: str, intensitaet: int):
    """Funktion erzeugt eine kurze Nachricht basierend auf Name, Stimmung und Intensität."""
    message = f'{name} fühlt sich {stimmung}'
    score = intensitaet * 10
    return message, score

gr.Interface(
    fn=compute,
    inputs=[
        gr.Textbox(label="Name eingeben"),
        gr.Dropdown(choices=["glücklich", "traurig", "aufgeregt"], label="Stimmung auswählen"),
        gr.Slider(minimum=1, maximum=10, step=1, label="Intensität der Stimmung")
    ],
    outputs=[
        gr.Textbox(label="Nachricht"),
        gr.Number(label="Stimmungswert")
    ],
    title="Gradio Komponenten Beispiel",
    description="Geben Sie Ihren Namen, Ihre Stimmung und die Intensität ein."
).launch()