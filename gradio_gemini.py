import os
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1) Umgebung laden, damit die Datei `.env` gelesen wird und wir den API-Key nutzen können.
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# 2) Client einmalig erstellen. Das Objekt kapselt die Kommunikation mit der Gemini API.
client = genai.Client(api_key=API_KEY)

# 3) Modell auswählen, damit wir später nur noch die Konstante referenzieren.
MODEL_NAME = "gemini-2.0-flash"


def generate_text(prompt):
    """
    Übergebe den Prompt an Gemini, warte auf die Antwort und liefere sie zurück.
    Die Temperatur steuert, wie kreativ bzw. deterministisch das Modell reagieren soll.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.5)
    )
    return response.text


with gr.Blocks(title="Gemini Text Generator") as demo:

    # Kurze Anleitung für Nutzer:innen.
    gr.Markdown('Stelle Gemini eine Frage:')

    # Mehrzeilige Textbox als Prompt-Eingabe.
    prompt_box = gr.Textbox(
        label="Deine Frage",
        lines=3,
        placeholder="Hier Frage eingeben ..."
        ),

    run_button = gr.Button("Generiere Antwort")
    output_box = gr.Markdown(label="Gemini Antwort")
    
    # Klick-Event: Eingabe -> generate_text -> Markdown-Ausgabe.
    run_button.click(generate_text, inputs=prompt_box, outputs=output_box)

    # Launch startet wie gewohnt den lokalen Server.
    demo.launch()
