import os
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.0-flash"

def generate_text(prompt):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.5)
    )
    return response.text

with gr.Blocks(title="Gemini Text Generator") as demo:

    gr.Markdown('Stelle Gemini eine Frage:')

    prompt_box = gr.Textbox(
        label="Deine Frage",
        lines=3,
        placeholder="Hier Frage eingeben ..."
        ),

    run_button = gr.Button("Generiere Antwort")
    output_box = gr.Markdown(label="Gemini Antwort")
    
    run_button.click(generate_text, inputs=prompt_box, outputs=output_box)

    demo.launch()
