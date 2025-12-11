"""
Gradio Komponenten mit Blocks API - Flexibles Layout und Kontrolle.

Dieses Skript zeigt dieselbe Funktionalität wie gradio_components.py,
aber mit der flexibleren gr.Blocks()-API für mehr Layout-Kontrolle.

=== Vorteile von gr.Blocks() für komplexe UIs ===

1. Layout-Kontrolle:
   - gr.Row(): Komponenten nebeneinander anordnen
   - gr.Column(): Komponenten untereinander anordnen
   - gr.Tab(): Tabs für verschiedene Ansichten
   - gr.Accordion(): Ein-/ausklappbare Bereiche
   - gr.Group(): Visuelle Gruppierung

2. Feinere Event-Steuerung:
   - Mehrere Buttons mit verschiedenen Aktionen
   - Events bei Wertänderungen (.change())
   - Verkettete Events (eine Aktion löst weitere aus)
   - Bedingte UI-Updates

3. Dynamische UIs:
   - Komponenten können ein-/ausgeblendet werden
   - Werte können programmatisch geändert werden
   - Interaktivität kann dynamisch gesteuert werden

=== Layout-Konzept ===
Ohne Layout-Container werden Komponenten vertikal gestapelt.
Mit gr.Row() werden alle enthaltenen Komponenten nebeneinander angezeigt.
Layout-Container können verschachtelt werden für komplexe Layouts.
"""

import gradio as gr  # Das Gradio-Framework importieren


# ============================================================================
# Verarbeitungsfunktion
# ============================================================================
# Identisch zur Interface-Version - die Funktion bleibt unverändert.
# Bei Blocks ändert sich nur die UI-Definition, nicht die Logik.
# ============================================================================

def compute(name: str, stimmung: str, intensitaet: int):
    """
    Kombiniert Benutzereingaben zu einer Nachricht und berechnet einen Score.
    
    Die gleiche Funktion wie im Interface-Beispiel zeigt,
    dass Backend-Logik und Frontend-Darstellung unabhängig sind.
    
    Args:
        name: Der Name des Benutzers (Freitext)
        stimmung: Die gewählte Stimmung (aus vordefinierten Optionen)
        intensitaet: Wie stark die Stimmung ist (1-10)
        
    Returns:
        Tuple mit:
        - message (str): Beschreibende Nachricht
        - score (int): Berechneter Stimmungswert
    """
    message = f"{name} fühlt sich {stimmung}"
    score = intensitaet * 10
    return message, score


# ============================================================================
# Blocks UI mit Layout-Kontrolle
# ============================================================================
# In diesem Beispiel zeigen wir:
# - gr.Row() für horizontale Anordnung
# - Explizite Button-Definition
# - Trennung von Eingabe- und Ausgabebereich
# - Event-Handling mit .click()
# ============================================================================

with gr.Blocks(title="Gradio Komponenten Beispiel") as demo:
    
    # --- Einleitungstext ---
    # gr.Markdown() für formatierte Beschreibungen
    # Kann auch Überschriften (#), Listen, Links etc. enthalten
    gr.Markdown("Geben Sie Ihren Namen, Ihre Stimmung und die Intensität ein.")

    # --- Eingabebereich mit horizontalem Layout ---
    # gr.Row() ordnet alle enthaltenen Komponenten nebeneinander an.
    # Jede Komponente bekommt gleich viel Platz (kann mit scale= angepasst werden).
    # Ohne gr.Row() wären die Komponenten untereinander.
    with gr.Row():
        # Textbox für den Namen
        name_input = gr.Textbox(label="Name eingeben")
        
        # Dropdown für die Stimmungsauswahl
        # Bei Blocks müssen wir die Komponente als Variable speichern,
        # damit wir sie später im Event-Handler referenzieren können.
        mood_input = gr.Dropdown(
            choices=["glücklich", "traurig", "aufgeregt"],
            label="Stimmung auswählen",
        )
        
        # Slider für die Intensität
        # value=5 setzt einen Standardwert (Mitte des Bereichs)
        # Bei Interface kann das auch, aber bei Blocks ist es übersichtlicher
        intensity_input = gr.Slider(
            minimum=1,
            maximum=10,
            value=5,  # Startwert
            step=1,
            label="Intensität der Stimmung"
        )

    # --- Action-Button ---
    # Bei Blocks müssen wir Buttons explizit erstellen.
    # Der Button löst die Berechnung aus (anders als bei Interface,
    # wo automatisch ein "Submit"-Button erstellt wird).
    compute_button = gr.Button("Berechnen")

    # --- Ausgabebereich ---
    # Wieder gr.Row() für horizontale Anordnung der Ergebnisse.
    # Die Trennung von Eingabe und Ausgabe durch den Button
    # macht die UI übersichtlicher.
    with gr.Row():
        # Textbox für die Nachricht
        # interactive=False verhindert Bearbeitung durch den Benutzer
        message_output = gr.Textbox(label="Nachricht", interactive=False)
        
        # Number für den Score
        # Auch hier interactive=False für reine Anzeige
        score_output = gr.Number(label="Stimmungswert", interactive=False)

    # --- Event-Handler verbinden ---
    # Bei Blocks müssen Events manuell verknüpft werden.
    # 
    # compute_button.click() bedeutet:
    #   "Wenn der Button geklickt wird, führe diese Aktion aus"
    #
    # Parameter:
    # - fn: Die Funktion, die aufgerufen wird (compute)
    # - inputs: Liste der Komponenten, deren Werte übergeben werden
    #           Die Reihenfolge entspricht den Funktionsparametern!
    # - outputs: Liste der Komponenten, die mit Rückgabewerten gefüllt werden
    #            Die Reihenfolge entspricht den Rückgabewerten!
    compute_button.click(
        compute,
        inputs=[name_input, mood_input, intensity_input],
        outputs=[message_output, score_output],
    )

    # --- Webserver starten ---
    # launch() kann innerhalb oder außerhalb des with-Blocks stehen.
    # Hier innerhalb, was bei einfachen Demos übersichtlicher sein kann.
    demo.launch()
