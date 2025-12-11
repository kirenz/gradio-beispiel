"""
Gradio mit Google Gemini - KI-Textgenerierung im Browser.

Dieses Skript zeigt, wie man Google's Gemini-Modell in eine
Gradio-Anwendung integriert für interaktive KI-Textgenerierung.

=== Was ist Google Gemini? ===
Gemini ist Googles multimodales KI-Modell (früher "Bard").
Es kann:
- Text verstehen und generieren
- Bilder analysieren (multimodal)
- Code schreiben und erklären
- Fragen beantworten
- Kreative Texte erstellen

=== Das google-genai Paket ===
Das `google-genai` Paket ist die offizielle Python-Bibliothek
für Google's generative AI-Modelle. Es ersetzt das ältere
`google-generativeai` Paket und bietet:
- Einfache Client-Erstellung mit API-Key
- Synchrone und asynchrone Aufrufe
- Konfigurierbare Generierungsparameter
- Streaming-Unterstützung für lange Antworten

=== API-Key erhalten ===
1. Besuche https://aistudio.google.com/
2. Melde dich mit einem Google-Konto an
3. Erstelle einen API-Key unter "Get API key"
4. Speichere den Key in einer .env-Datei als GEMINI_API_KEY=...

=== Wichtige Parameter ===
- temperature: Kreativität (0.0 = deterministisch, 1.0 = kreativ)
- max_output_tokens: Maximale Länge der Antwort
- top_p, top_k: Sampling-Parameter für Texterzeugung
"""

import os  # Für Umgebungsvariablen
import gradio as gr  # Gradio-Framework für die Web-Oberfläche
from dotenv import load_dotenv  # Lädt Variablen aus .env-Datei
from google import genai  # Google GenAI Client
from google.genai import types  # Datentypen für Konfiguration


# ============================================================================
# Konfiguration und Initialisierung
# ============================================================================
# Die Initialisierung sollte EINMAL beim Start erfolgen, nicht bei jedem
# Funktionsaufruf. Das spart Ressourcen und beschleunigt die Antworten.
# ============================================================================

# --- Umgebungsvariablen laden ---
# load_dotenv() sucht nach einer .env-Datei im aktuellen Verzeichnis
# und lädt alle Variablen als Umgebungsvariablen.
# Das ist sicherer als API-Keys direkt im Code zu haben.
load_dotenv()

# --- API-Key aus Umgebungsvariable holen ---
# os.getenv() gibt None zurück, wenn die Variable nicht existiert.
# In Produktionsumgebungen sollte man hier einen Fehler werfen,
# wenn der Key fehlt.
API_KEY = os.getenv("GEMINI_API_KEY")

# --- Client erstellen ---
# Der Client ist das Hauptobjekt für die API-Kommunikation.
# Er wird EINMAL erstellt und dann für alle Anfragen wiederverwendet.
# Der Client verwaltet:
# - Authentifizierung mit dem API-Key
# - HTTP-Verbindungen zur API
# - Retry-Logik bei Fehlern
client = genai.Client(api_key=API_KEY)

# --- Modell als Konstante ---
# Das Modell als Konstante zu definieren macht es einfach,
# zwischen verschiedenen Modellen zu wechseln:
# - gemini-2.0-flash: Schnell und günstig, gut für die meisten Aufgaben
# - gemini-1.5-pro: Leistungsstärker, längerer Kontext
# - gemini-1.5-flash: Schnelle Alternative zu Pro
MODEL_NAME = "gemini-2.0-flash"


# ============================================================================
# Textgenerierungsfunktion
# ============================================================================
# Diese Funktion ist der "Kern" der Anwendung - sie sendet Prompts
# an Gemini und gibt die generierten Antworten zurück.
# ============================================================================

def generate_text(prompt):
    """
    Sendet einen Prompt an Gemini und gibt die generierte Antwort zurück.
    
    Ablauf:
    1. Prompt wird an die Gemini-API gesendet
    2. Das Modell generiert eine Antwort basierend auf dem Prompt
    3. Die Antwort wird als Text zurückgegeben
    
    Der Parameter 'temperature' steuert die "Kreativität":
    - 0.0: Sehr deterministisch, immer ähnliche Antworten
    - 0.5: Ausgewogen (Standard in diesem Beispiel)
    - 1.0: Sehr kreativ, aber manchmal unvorhersehbar
    
    Für Faktenfragen niedrige temperature, für kreative Aufgaben höhere.
    
    Args:
        prompt: Die Frage oder Anweisung des Benutzers
        
    Returns:
        Der generierte Text von Gemini
    """
    # generate_content() ist der Hauptaufruf für Textgenerierung
    # Parameter:
    # - model: Welches Modell verwendet werden soll
    # - contents: Der Eingabetext (kann auch Liste von Messages sein)
    # - config: Optionale Konfiguration für die Generierung
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        # GenerateContentConfig enthält alle Generierungsparameter
        # Weitere Optionen:
        # - max_output_tokens: Maximale Antwortlänge
        # - top_p: Nucleus Sampling Parameter
        # - top_k: Top-K Sampling Parameter
        # - stop_sequences: Strings, bei denen die Generierung stoppt
        config=types.GenerateContentConfig(temperature=0.5)
    )
    # response.text extrahiert den generierten Text aus der Antwort
    # Die vollständige Response enthält auch Metadaten wie Token-Counts
    return response.text


# ============================================================================
# Gradio-Benutzeroberfläche
# ============================================================================
# Wir verwenden gr.Blocks() für mehr Flexibilität.
# Die UI ist einfach gehalten: Eingabefeld, Button, Ausgabe.
# ============================================================================

with gr.Blocks(title="Gemini Text Generator") as demo:

    # --- Anleitung für Benutzer ---
    # Kurze Erklärung, was die App macht
    gr.Markdown('Stelle Gemini eine Frage:')

    # --- Prompt-Eingabefeld ---
    # Mehrzeilige Textbox für längere Prompts.
    # 'lines=3' macht das Feld standardmäßig 3 Zeilen hoch.
    # 'placeholder' zeigt Hinweistext im leeren Feld.
    #
    # HINWEIS: Das Komma am Ende erzeugt ein Tuple - dies ist
    # in diesem Fall gewollt für Gradio's internes Handling.
    prompt_box = gr.Textbox(
        label="Deine Frage",
        lines=3,
        placeholder="Hier Frage eingeben ..."
        ),

    # --- Generierungs-Button ---
    # Löst die Textgenerierung aus
    run_button = gr.Button("Generiere Antwort")
    
    # --- Ausgabefeld ---
    # gr.Markdown() statt gr.Textbox() für formatierte Ausgabe.
    # Gemini gibt oft Markdown-formatierten Text zurück
    # (z.B. mit Überschriften, Listen, Code-Blöcken).
    # gr.Markdown() rendert diesen korrekt.
    output_box = gr.Markdown(label="Gemini Antwort")
    
    # --- Event-Handler ---
    # Button-Klick verbindet Eingabe mit Generierungsfunktion
    # und zeigt das Ergebnis im Ausgabefeld an.
    run_button.click(generate_text, inputs=prompt_box, outputs=output_box)

    # --- Webserver starten ---
    # launch() macht die App unter http://127.0.0.1:7860 erreichbar
    demo.launch()
