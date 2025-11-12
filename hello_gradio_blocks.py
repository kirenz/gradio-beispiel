# In dieser Variante nutzen wir `gr.Blocks`, um Layout und Event-Logik selbst zu steuern.
import gradio as gr


# Gleiche Logik wie im Interface-Beispiel: Eine einfache Begrüßung abhängig vom Namen.
def greet(name):
    """Function to greet the user by name."""
    return f"Hallo, {name}!! 🙂"


with gr.Blocks(title="Hello World mit Gradio") as demo:
    # Markdown eignet sich für Einleitungen oder kurze Erklärtexte.
    gr.Markdown("Geben Sie Ihren Namen ein, um eine Begrüßung zu erhalten.")

    # Jede Komponente wird als Variable gespeichert, damit wir sie später verbinden können.
    name_input = gr.Textbox(label="Name eingeben")
    greet_button = gr.Button("Begrüßen")
    output_box = gr.Textbox(label="Begrüßung", interactive=False)  # Nutzer kann das Feld nicht ändern.

    # Events müssen in Blocks manuell verknüpft werden:
    # Beim Klick auf den Button wird `greet` mit dem Textbox-Wert aufgerufen
    # und das Ergebnis landet im Ausgabefeld.
    greet_button.click(greet, inputs=name_input, outputs=output_box)

    # `demo` ist das Blocks-Objekt; Launch startet die App, sobald der Kontext endet.
    demo.launch()
