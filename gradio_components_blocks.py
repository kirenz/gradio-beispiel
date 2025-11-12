# Gleiche Funktionalität wie im Interface-Beispiel, aber komplett mit Blocks aufgebaut.
import gradio as gr


def compute(name: str, stimmung: str, intensitaet: int):
    """Funktion erzeugt eine kurze Nachricht basierend auf Name, Stimmung und Intensität."""
    message = f"{name} fühlt sich {stimmung}"
    score = intensitaet * 10
    return message, score


with gr.Blocks(title="Gradio Komponenten Beispiel") as demo:
    # Intro-Text über der App für Kontext.
    gr.Markdown("Geben Sie Ihren Namen, Ihre Stimmung und die Intensität ein.")

    # `gr.Row` ordnet die enthaltenen Komponenten nebeneinander an.
    with gr.Row():
        name_input = gr.Textbox(label="Name eingeben")
        mood_input = gr.Dropdown(
            choices=["glücklich", "traurig", "aufgeregt"],
            label="Stimmung auswählen",
        )
        intensity_input = gr.Slider(
            minimum=1, maximum=10, value=5, step=1, label="Intensität der Stimmung"
        )

    compute_button = gr.Button("Berechnen")  # Button löst die Berechnung aus.

    # Ergebnisse in einer separaten Zeile, damit Inputs und Outputs klar getrennt sind.
    with gr.Row():
        message_output = gr.Textbox(label="Nachricht", interactive=False)
        score_output = gr.Number(label="Stimmungswert", interactive=False)

    # Event-Verkettung: Button-Klick -> compute() -> beide Ausgabefelder auffüllen.
    compute_button.click(
        compute,
        inputs=[name_input, mood_input, intensity_input],
        outputs=[message_output, score_output],
    )

    demo.launch()
