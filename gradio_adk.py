"""
Einfacher Zeit-Agent mit Google ADK und Gradio.

Ein Einzeldatei-Beispiel, das zeigt, wie man einen Agenten mit Werkzeugen
erstellt, der die aktuelle Uhrzeit in verschiedenen Städten nennen kann.

=== Was ist Google ADK? ===
Das Agent Development Kit (ADK) ist ein Framework von Google zum Erstellen
von KI-Agenten. Ein "Agent" ist ein LLM (Large Language Model), das:
1. Anweisungen befolgen kann (instruction)
2. Werkzeuge (Tools/Funktionen) aufrufen kann, um Aufgaben zu erledigen
3. Konversationen führen und den Kontext behalten kann

=== Was ist Gradio? ===
Gradio ist ein Python-Framework, mit dem man schnell Web-Oberflächen
für KI-Anwendungen erstellen kann. Es wandelt Python-Funktionen in
interaktive Web-Apps um - ohne HTML/CSS/JavaScript-Kenntnisse.
"""

import asyncio  # Für asynchrone Programmierung (async/await)
import datetime  # Für Datum und Uhrzeit
import gradio as gr  # Gradio-Framework für die Web-Oberfläche
from dotenv import load_dotenv  # Lädt Umgebungsvariablen aus .env-Datei
from google.genai import types  # Datentypen für Google GenAI (Content, Part)
from google.adk.agents.llm_agent import Agent  # Die Agent-Klasse von ADK
from google.adk.runners import InMemoryRunner  # Runner zum Ausführen von Agenten

# Umgebungsvariablen laden (z.B. GOOGLE_API_KEY aus der .env-Datei)
# Dies ist notwendig, damit der Agent sich bei Google authentifizieren kann
load_dotenv()


# ============================================================================
# Werkzeug-Funktion (Tool)
# ============================================================================
# Ein "Werkzeug" ist eine Python-Funktion, die der Agent aufrufen kann.
# Der Agent erkennt anhand des Funktionsnamens und der Docstring-Beschreibung,
# WANN er dieses Werkzeug verwenden soll.
#
# WARUM braucht der Agent ein Werkzeug für die Uhrzeit?
# Ein LLM (Large Language Model) hat KEINEN Zugriff auf:
# - Die aktuelle Uhrzeit
# - Das aktuelle Datum
# - Das Internet
# - Dateien auf dem Computer
#
# Das LLM weiß nur, was in seinem Training enthalten war (bis zu einem
# bestimmten Datum). Um aktuelle Informationen zu bekommen, braucht es
# Werkzeuge, die diese Informationen für es abrufen.
#
# Wichtig: Die Funktion muss ein Dictionary zurückgeben, damit der Agent
# das Ergebnis verarbeiten kann.
# ============================================================================

def get_current_time() -> dict:
    """
    Gibt die aktuelle Uhrzeit zurück.
    
    Diese Funktion wird vom Agenten automatisch aufgerufen, wenn der Benutzer
    nach der aktuellen Uhrzeit fragt. Der Agent:
    1. Erkennt die Absicht des Benutzers (Uhrzeit wissen wollen)
    2. Ruft diese Funktion auf
    3. Erhält die aktuelle Systemzeit
    4. Formuliert eine natürliche Antwort basierend auf dem Ergebnis
    
    Returns:
        Dictionary mit Status und aktueller Uhrzeit
    """
    # Aktuelle Systemzeit abrufen und als String formatieren
    # strftime() formatiert die Zeit: %H = Stunde (24h), %M = Minute
    current_time = datetime.datetime.now().strftime("%H:%M")
    
    # Rückgabe als Dictionary - der Agent verwendet diese Daten für seine Antwort
    return {"status": "success", "time": current_time}


# ============================================================================
# Agent und Runner Einrichtung
# ============================================================================
# Der Agent ist das "Gehirn" - er versteht Anfragen und entscheidet, was zu tun ist.
# Der Runner ist der "Manager" - er führt den Agenten aus und verwaltet Sessions.
# ============================================================================

# --- Agent erstellen ---
# Der Agent ist eine Instanz, die das LLM (Gemini) mit Werkzeugen verbindet.
# Er ist wie ein virtueller Assistent mit speziellen Fähigkeiten.
root_agent = Agent(
    # Das verwendete KI-Modell (Gemini 2.0 Flash ist schnell und effizient)
    model='gemini-2.0-flash',
    
    # Interner Name des Agenten (für Logging und Referenzierung)
    name='root_agent',
    
    # Kurze Beschreibung, was der Agent kann (hilft bei Multi-Agent-Systemen)
    description="Ein hilfreicher Assistent, der die aktuelle Uhrzeit nennen kann.",
    
    # Die "Persönlichkeit" und Verhaltensanweisungen für den Agenten.
    # Diese Anweisungen beeinflussen, WIE der Agent antwortet.
    instruction="""
    Du bist ein hilfreicher Assistent.
    Wenn der Benutzer nach der Uhrzeit fragt, verwende das 'get_current_time'-Werkzeug.
    Du selbst weißt NICHT, wie spät es ist - du MUSST das Werkzeug verwenden!
    Antworte in der gleichen Sprache wie die Frage des Benutzers.
    Sei freundlich und präzise in deiner Antwort.
    """,
    
    # Liste der verfügbaren Werkzeuge (Funktionen), die der Agent aufrufen kann.
    # Der Agent analysiert die Funktionssignatur und den Docstring automatisch,
    # um zu verstehen, wann und wie er das Werkzeug verwenden soll.
    tools=[get_current_time],
)

# --- Runner erstellen ---
# Der InMemoryRunner ist der "Ausführungsmanager" für den Agenten.
# Er kümmert sich um:
# 1. Session-Management: Speichert Gesprächsverläufe (im Arbeitsspeicher)
# 2. Nachrichtenverarbeitung: Leitet Nachrichten an den Agenten weiter
# 3. Event-Handling: Gibt Antworten und Zwischenergebnisse zurück
#
# "InMemory" bedeutet, dass alle Daten im RAM gespeichert werden.
# Bei einem Neustart gehen alle Gespräche verloren.
# Für "echte" Anwendungen gibt es auch persistente Runner (z.B. mit Datenbank).
runner = InMemoryRunner(
    agent=root_agent,  # Der Agent, der ausgeführt werden soll
    app_name='root_agent'  # Name der Anwendung (für Session-Gruppierung)
)

# --- Globale Session-ID ---
# Eine Session ist wie ein "Gesprächsfaden". Sie speichert den Verlauf
# aller Nachrichten zwischen Benutzer und Agent.
# Wir speichern die ID global, damit sie über mehrere Funktionsaufrufe
# hinweg erhalten bleibt und das Gespräch fortgesetzt werden kann.
SESSION_ID = None


# ============================================================================
# Chat-Verarbeitungsfunktion (Asynchron)
# ============================================================================
# Diese Funktion ist das Herzstück der Agent-Kommunikation.
# Sie ist "async", weil die Kommunikation mit dem Gemini-API Zeit braucht
# und wir nicht blockieren wollen (andere Anfragen könnten parallel laufen).
# ============================================================================

async def chat_with_agent_async(message: str) -> str:
    """
    Sendet eine Nachricht an den Agenten und gibt die Antwort zurück.
    
    Ablauf:
    1. Session erstellen/wiederverwenden (für Gesprächskontext)
    2. Nachricht in das richtige Format bringen (Content-Objekt)
    3. Nachricht an den Agent senden
    4. Auf Events warten und finale Antwort extrahieren
    
    Args:
        message: Die Textnachricht des Benutzers
        
    Returns:
        Die Textantwort des Agenten
    """
    global SESSION_ID  # Zugriff auf die globale Session-ID

    # --- Session-Management ---
    # Eine Session muss nur EINMAL erstellt werden.
    # Danach verwenden wir dieselbe Session-ID für alle weiteren Nachrichten,
    # damit der Agent sich an vorherige Nachrichten "erinnern" kann.
    if SESSION_ID is None:
        # Neue Session über den Session-Service des Runners erstellen
        session = await runner.session_service.create_session(
            user_id='gradio_user',  # Eindeutige Benutzer-ID
            app_name='root_agent'  # App-Name zur Gruppierung
        )
        SESSION_ID = session.id  # Session-ID für spätere Verwendung speichern

    # --- Nachricht formatieren ---
    # Die ADK erwartet Nachrichten im "Content"-Format von Google GenAI.
    # - role='user': Kennzeichnet die Nachricht als Benutzer-Eingabe
    # - parts: Liste von Nachrichtenteilen (hier nur ein Text-Teil)
    content = types.Content(
        role='user',
        parts=[types.Part(text=message)]
    )

    # --- Agent ausführen ---
    # run_async() startet die Verarbeitung und gibt einen AsyncGenerator zurück.
    # Der Agent kann mehrere "Events" produzieren:
    # - Werkzeug-Aufrufe (z.B. get_current_time wird aufgerufen)
    # - Zwischenantworten
    # - Finale Antwort (is_final_response() == True)
    response_text = ""
    events_async = runner.run_async(
        user_id='gradio_user',  # Muss mit der Session übereinstimmen
        session_id=SESSION_ID,  # Unsere gespeicherte Session-ID
        new_message=content  # Die formatierte Benutzernachricht
    )

    # --- Events durchlaufen ---
    # Wir iterieren über alle Events, bis wir die finale Antwort finden.
    # "async for" ist wie eine for-Schleife, aber für asynchrone Generatoren.
    async for event in events_async:
        # Prüfen, ob dies die finale Antwort ist (nicht nur ein Zwischenschritt)
        if event.is_final_response() and event.content and event.content.parts:
            # Text aus dem ersten Part extrahieren
            response_text = event.content.parts[0].text
            break  # Wir haben die Antwort, Schleife beenden

    return response_text


# ============================================================================
# Synchroner Wrapper für Gradio
# ============================================================================
# Gradio-Komponenten erwarten normalerweise synchrone Funktionen.
# Da unsere Agent-Funktion aber asynchron (async) ist, brauchen wir
# einen "Wrapper", der die asynchrone Funktion in einer synchronen aufruft.
# ============================================================================

def chat_with_agent(message: str, history: list) -> str:
    """
    Synchroner Wrapper für die asynchrone Agent-Kommunikation.
    
    Gradio ruft diese Funktion auf, wenn der Benutzer eine Nachricht sendet.
    Sie verwendet asyncio.run(), um die asynchrone Funktion auszuführen.
    
    Args:
        message: Die Textnachricht des Benutzers
        history: Der bisherige Chatverlauf (von Gradio verwaltet, hier nicht genutzt)
        
    Returns:
        Die Textantwort des Agenten, oder eine Fehlermeldung
    """
    try:
        # asyncio.run() führt eine async-Funktion aus und wartet auf das Ergebnis
        response = asyncio.run(chat_with_agent_async(message))
        return response
    except Exception as e:
        # Bei Fehlern (z.B. API-Fehler) eine lesbare Meldung zurückgeben
        return f"Fehler: {str(e)}"


def reset_session():
    """
    Setzt die Session zurück, um ein neues Gespräch zu starten.
    
    Wird aufgerufen, wenn der Benutzer auf "Chat löschen" klickt.
    Durch das Zurücksetzen der SESSION_ID wird beim nächsten Aufruf
    eine komplett neue Session erstellt - der Agent "vergisst" alles.
    
    Returns:
        Leere Liste, um den Chatverlauf in der UI zu leeren
    """
    global SESSION_ID
    SESSION_ID = None  # Session-ID zurücksetzen
    return []  # Leere Liste = leerer Chat in Gradio


# ============================================================================
# Gradio-Benutzeroberfläche
# ============================================================================
# Gradio bietet zwei Hauptansätze:
# 1. gr.Interface() - Einfach, aber weniger flexibel
# 2. gr.Blocks() - Flexibel, volle Kontrolle über Layout und Interaktionen
#
# Hier verwenden wir gr.Blocks(), weil wir:
# - Einen Chatbot mit mehreren Komponenten haben
# - Eigene Event-Handler definieren wollen
# - Beispiele und einen Reset-Button hinzufügen möchten
# ============================================================================

# gr.Blocks() erstellt einen Kontext für die UI-Definition
# Alles innerhalb des "with"-Blocks gehört zu dieser UI
with gr.Blocks(title="Google ADK Zeit-Agent") as demo:

    # --- Überschriften (Markdown-Komponenten) ---
    # gr.Markdown() rendert Markdown-Text als HTML
    gr.Markdown("# Zeit-Agent mit Google ADK")
    gr.Markdown("Frage den Agenten nach der aktuellen Uhrzeit! Der Agent selbst weiß nicht, wie spät es ist – er muss sein Werkzeug benutzen.")

    # --- Chatbot-Komponente ---
    # gr.Chatbot() zeigt den Gesprächsverlauf an (Benutzer- und Bot-Nachrichten)
    # Das Format ist eine Liste von Dictionaries: {"role": "user/assistant", "content": "..."}
    chatbot = gr.Chatbot(
        label="Chat",  # Beschriftung über der Komponente
        height=400  # Höhe in Pixeln
    )

    # --- Texteingabe ---
    # gr.Textbox() ist ein Eingabefeld für Text
    msg = gr.Textbox(
        label="Deine Nachricht",  # Beschriftung
        placeholder="z.B. 'Wie spät ist es?' oder 'What time is it?'",
        lines=1  # Einzeilige Eingabe
    )

    # --- Button zum Zurücksetzen ---
    # gr.Button() erstellt einen klickbaren Button
    clear = gr.Button("Chat löschen")

    # --- Beispiele ---
    # gr.Examples() zeigt klickbare Beispiel-Eingaben an
    # Wenn der Benutzer darauf klickt, wird der Text ins Eingabefeld eingefügt
    gr.Examples(
        examples=[
            ["Wie spät ist es?"],
            ["What time is it?"],
            ["Kannst du mir die Uhrzeit sagen?"],
            ["Hallo, weißt du wie spät es gerade ist?"],
        ],
        inputs=msg  # Die Komponente, in die das Beispiel eingefügt wird
    )

    # --- Event-Handler-Funktion ---
    # Diese Funktion wird aufgerufen, wenn der Benutzer eine Nachricht absendet
    def respond(message: str, chat_history: list):
        """
        Verarbeitet die Benutzernachricht und aktualisiert den Chat.
        
        Ablauf:
        1. Nachricht an den Agenten senden und Antwort erhalten
        2. Benutzernachricht zum Chatverlauf hinzufügen
        3. Bot-Antwort zum Chatverlauf hinzufügen
        4. Textfeld leeren und aktualisierten Chat zurückgeben
        
        Args:
            message: Die eingegebene Nachricht des Benutzers
            chat_history: Der bisherige Chatverlauf (Liste von Dicts)
            
        Returns:
            Tuple aus:
            - "" (leerer String, um das Textfeld zu leeren)
            - chat_history (aktualisierter Chatverlauf)
        """
        # Antwort vom Agenten holen
        bot_response = chat_with_agent(message, chat_history)
        
        # Nachrichten zum Verlauf hinzufügen (Gradio-Chat-Format)
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_response})
        
        # Rückgabe: Leeres Textfeld + aktualisierter Chat
        return "", chat_history

    # --- Events verbinden ---
    # .submit() wird ausgelöst, wenn Enter gedrückt wird
    # Parameter: (Funktion, [Eingabe-Komponenten], [Ausgabe-Komponenten])
    msg.submit(
        fn=respond,  # Die aufzurufende Funktion
        inputs=[msg, chatbot],  # Werte, die an die Funktion übergeben werden
        outputs=[msg, chatbot]  # Komponenten, die mit den Rückgabewerten aktualisiert werden
    )
    
    # .click() wird ausgelöst, wenn der Button geklickt wird
    clear.click(
        fn=reset_session,  # Funktion zum Zurücksetzen
        inputs=None,  # Keine Eingaben nötig
        outputs=chatbot  # Aktualisiert den Chatbot (mit leerer Liste)
    )


# ============================================================================
# Programmstart
# ============================================================================
# Dieser Block wird nur ausgeführt, wenn das Skript direkt gestartet wird
# (nicht wenn es als Modul importiert wird)
# ============================================================================

if __name__ == "__main__":
    # demo.launch() startet den Gradio-Webserver
    # Standardmäßig auf http://127.0.0.1:7860
    # Optionale Parameter:
    # - share=True: Erstellt einen öffentlichen Link (für Demos)
    # - server_port=8080: Anderer Port
    # - debug=True: Mehr Fehlerausgaben
    demo.launch()
