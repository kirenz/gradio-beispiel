"""
Gradio Komponenten - Verschiedene Eingabe- und Ausgabetypen.

Dieses Skript zeigt, wie man mehrere verschiedene Gradio-Komponenten
in einer gr.Interface()-Anwendung kombiniert.

=== Was sind Gradio-Komponenten? ===
Komponenten sind die UI-Bausteine von Gradio. Jede Komponente:
- Stellt einen bestimmten Datentyp dar (Text, Zahl, Bild, Audio, etc.)
- Hat eine visuelle Darstellung (Textfeld, Slider, Dropdown, etc.)
- Kann als Eingabe oder Ausgabe verwendet werden

=== Wichtige Eingabe-Komponenten ===
- gr.Textbox(): Texteingabe (ein- oder mehrzeilig)
- gr.Number(): Zahleneingabe
- gr.Slider(): Schieberegler für Zahlenbereiche
- gr.Dropdown(): Auswahl aus einer Liste von Optionen
- gr.Checkbox(): Ja/Nein-Auswahl
- gr.Radio(): Einfachauswahl aus mehreren Optionen
- gr.Image(): Bildupload
- gr.Audio(): Audioaufnahme oder -upload
- gr.File(): Dateiupload

=== Wichtige Ausgabe-Komponenten ===
- gr.Textbox(): Textausgabe
- gr.Number(): Zahlenausgabe
- gr.Markdown(): Formatierter Text mit Markdown
- gr.Image(): Bildausgabe
- gr.Plot(): Matplotlib/Plotly-Diagramme
- gr.JSON(): Strukturierte Daten als JSON
- gr.Dataframe(): Tabellarische Daten

=== Mehrere Inputs/Outputs ===
Bei gr.Interface() können inputs und outputs Listen sein.
Die Reihenfolge der Parameter/Rückgabewerte muss mit der
Reihenfolge der Komponenten übereinstimmen.
"""

import gradio as gr  # Das Gradio-Framework importieren


# ============================================================================
# Verarbeitungsfunktion mit mehreren Parametern
# ============================================================================
# Diese Funktion demonstriert:
# - Mehrere Eingabeparameter verschiedener Typen
# - Mehrere Rückgabewerte
# - Type Hints für bessere Dokumentation
#
# WICHTIG: Die Reihenfolge der Parameter muss mit der Reihenfolge
# der Komponenten in der inputs-Liste übereinstimmen!
# ============================================================================

def compute(name: str, stimmung: str, intensitaet: int):
    """
    Kombiniert Benutzereingaben zu einer Nachricht und berechnet einen Score.
    
    Diese Funktion zeigt, wie verschiedene Datentypen verarbeitet werden:
    - name (str): Freitext aus einer Textbox
    - stimmung (str): Ausgewählte Option aus einem Dropdown
    - intensitaet (int): Zahlenwert von einem Slider
    
    Die Funktion gibt zwei Werte zurück (Tuple), die dann auf
    zwei Ausgabe-Komponenten verteilt werden.
    
    Args:
        name: Der Name des Benutzers (Freitext)
        stimmung: Die gewählte Stimmung (aus vordefinierten Optionen)
        intensitaet: Wie stark die Stimmung ist (1-10)
        
    Returns:
        Tuple mit:
        - message (str): Beschreibende Nachricht
        - score (int): Berechneter Stimmungswert (intensitaet * 10)
    """
    # Nachricht aus den Eingaben zusammenbauen
    message = f'{name} fühlt sich {stimmung}'
    
    # Einen "Score" berechnen (einfache Beispiellogik)
    # In echten Anwendungen könnte hier komplexere ML-Logik stehen
    score = intensitaet * 10
    
    # Mehrere Werte als Tuple zurückgeben
    # Gradio verteilt diese automatisch auf die Output-Komponenten
    return message, score


# ============================================================================
# Interface mit mehreren Komponenten
# ============================================================================
# Bei mehreren Inputs/Outputs werden Listen verwendet.
# Die Reihenfolge ist entscheidend:
#   inputs[0] -> erster Parameter der Funktion (name)
#   inputs[1] -> zweiter Parameter der Funktion (stimmung)
#   inputs[2] -> dritter Parameter der Funktion (intensitaet)
#
#   Erster Rückgabewert -> outputs[0] (message)
#   Zweiter Rückgabewert -> outputs[1] (score)
# ============================================================================

gr.Interface(
    # Die Verarbeitungsfunktion
    fn=compute,
    
    # Liste der Eingabe-Komponenten (Reihenfolge = Parameter-Reihenfolge)
    inputs=[
        # --- gr.Textbox() ---
        # Für freie Texteingabe (Namen, Beschreibungen, etc.)
        # Parameter:
        # - label: Beschriftung über dem Feld
        # - placeholder: Hinweistext im leeren Feld
        # - lines: Anzahl der Zeilen (1 = einzeilig, >1 = mehrzeilig)
        gr.Textbox(label="Name eingeben"),
        
        # --- gr.Dropdown() ---
        # Für Auswahl aus vordefinierten Optionen
        # Vorteile gegenüber Freitext:
        # - Keine Tippfehler möglich
        # - Validierung automatisch
        # - Einheitliche Werte für Weiterverarbeitung
        # Parameter:
        # - choices: Liste der verfügbaren Optionen
        # - label: Beschriftung
        # - value: Standardwert (optional)
        gr.Dropdown(
            choices=["glücklich", "traurig", "aufgeregt"],
            label="Stimmung auswählen"
        ),
        
        # --- gr.Slider() ---
        # Für Zahlenwerte in einem definierten Bereich
        # Ideal für: Intensitäten, Prozentangaben, Bewertungen
        # Vorteile:
        # - Visuelle Darstellung des Wertebereichs
        # - Keine ungültigen Eingaben möglich
        # - Intuitive Bedienung
        # Parameter:
        # - minimum/maximum: Wertebereich
        # - step: Schrittgröße (1 = nur ganze Zahlen)
        # - value: Startwert (optional)
        # - label: Beschriftung
        gr.Slider(
            minimum=1,
            maximum=10,
            step=1,
            label="Intensität der Stimmung"
        )
    ],
    
    # Liste der Ausgabe-Komponenten (Reihenfolge = Rückgabewert-Reihenfolge)
    outputs=[
        # --- gr.Textbox() als Ausgabe ---
        # Zeigt Text an (bei Ausgabe automatisch nicht-editierbar)
        gr.Textbox(label="Nachricht"),
        
        # --- gr.Number() ---
        # Für numerische Ausgaben
        # Gradio formatiert Zahlen automatisch passend
        # Für komplexere Darstellungen (Währung, Prozent) ggf. Textbox verwenden
        gr.Number(label="Stimmungswert")
    ],
    
    # Titel und Beschreibung für die Benutzeroberfläche
    title="Gradio Komponenten Beispiel",
    description="Geben Sie Ihren Namen, Ihre Stimmung und die Intensität ein."

# launch() startet den Webserver
).launch()
