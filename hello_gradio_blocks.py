"""
Hello World mit Gradio Blocks - Mehr Kontrolle über die UI.

Dieses Skript zeigt dieselbe Funktionalität wie hello_gradio.py,
aber verwendet die flexiblere `gr.Blocks`-API anstelle von `gr.Interface`.

=== Wann gr.Blocks statt gr.Interface? ===

gr.Interface() ist einfacher, aber eingeschränkt:
- Feste Layout-Struktur (Eingaben links, Ausgaben rechts)
- Automatische Submit-Buttons
- Ein Event pro Funktion

gr.Blocks() bietet volle Kontrolle:
- Eigenes Layout (Rows, Columns, Tabs, etc.)
- Eigene Buttons und Event-Trigger
- Mehrere Events für verschiedene Interaktionen
- Komponenten können aktualisiert werden ohne Neuladen
- State-Management zwischen Komponenten möglich

=== Grundprinzip von gr.Blocks() ===
1. Blocks-Kontext erstellen: `with gr.Blocks() as demo:`
2. Komponenten als Variablen definieren (nicht als Parameter)
3. Events manuell verbinden: `button.click(fn, inputs, outputs)`
4. Am Ende `demo.launch()` aufrufen

Dieses Beispiel zeigt die Grundstruktur - spätere Beispiele
zeigen komplexere Layouts und Interaktionen.
"""

import gradio as gr  # Das Gradio-Framework importieren


# ============================================================================
# Die Verarbeitungsfunktion
# ============================================================================
# Die Funktion bleibt identisch zu hello_gradio.py.
# Bei gr.Blocks() ändert sich nur die UI-Definition, nicht die Logik.
# Das ermöglicht eine saubere Trennung von Backend (Logik) und Frontend (UI).
# ============================================================================

def greet(name):
    """
    Begrüßt den Benutzer mit seinem Namen.
    
    Identisch zur Funktion im Interface-Beispiel.
    Die Trennung von Funktion und UI ist ein Kernprinzip von Gradio:
    - Die Funktion kann unabhängig getestet werden
    - Die UI kann geändert werden, ohne die Logik anzupassen
    
    Args:
        name: Der eingegebene Name des Benutzers
        
    Returns:
        Eine personalisierte Begrüßungsnachricht
    """
    return f"Hallo, {name}!! 🙂"


# ============================================================================
# Gradio Blocks UI erstellen
# ============================================================================
# gr.Blocks() verwendet einen Context-Manager ("with"-Statement).
# Alles innerhalb des "with"-Blocks gehört zu dieser UI.
#
# Das `as demo` speichert das Blocks-Objekt in einer Variable,
# damit wir später `demo.launch()` aufrufen können.
#
# Der `title`-Parameter setzt den Browser-Tab-Titel.
# ============================================================================

with gr.Blocks(title="Hello World mit Gradio") as demo:
    
    # --- Markdown für Überschriften und Erklärungen ---
    # gr.Markdown() rendert Markdown-Text als HTML
    # Perfekt für: Titel, Anleitungen, Erklärungen, formatierte Texte
    # Unterstützt: Überschriften (#), fett (**), kursiv (*), Listen, Links, etc.
    gr.Markdown("Geben Sie Ihren Namen ein, um eine Begrüßung zu erhalten.")

    # --- Eingabekomponente definieren ---
    # Bei Blocks speichern wir jede Komponente als Variable.
    # Das ist nötig, um sie später bei Events zu referenzieren.
    # Anders als bei Interface werden Komponenten nicht automatisch verbunden.
    name_input = gr.Textbox(label="Name eingeben")
    
    # --- Button erstellen ---
    # gr.Button() erstellt einen klickbaren Button.
    # Bei Interface gibt es automatisch einen "Submit"-Button.
    # Bei Blocks müssen wir Buttons explizit erstellen.
    greet_button = gr.Button("Begrüßen")
    
    # --- Ausgabekomponente definieren ---
    # interactive=False verhindert, dass der Benutzer das Feld bearbeiten kann.
    # Das ist sinnvoll für Ausgabefelder, die nur Ergebnisse anzeigen sollen.
    # Bei Interface sind Ausgabefelder automatisch nicht-interaktiv.
    output_box = gr.Textbox(label="Begrüßung", interactive=False)

    # --- Event-Handler verbinden ---
    # Bei Blocks müssen Events manuell verknüpft werden.
    # Die Syntax ist: komponente.event(funktion, inputs, outputs)
    #
    # .click() wird ausgelöst, wenn der Button geklickt wird.
    # Alternative Events:
    # - .change(): Wenn sich der Wert einer Komponente ändert
    # - .submit(): Wenn Enter in einem Textfeld gedrückt wird
    # - .select(): Wenn ein Element ausgewählt wird (z.B. in Dropdown)
    #
    # Parameter:
    # - fn: Die aufzurufende Funktion (greet)
    # - inputs: Komponente(n), deren Werte an die Funktion übergeben werden
    # - outputs: Komponente(n), die mit dem Rückgabewert aktualisiert werden
    greet_button.click(greet, inputs=name_input, outputs=output_box)

# ============================================================================
# Anwendung starten
# ============================================================================
# demo.launch() startet den Webserver.
# Das muss AUSSERHALB des "with"-Blocks geschehen, damit alle
# Komponenten und Events bereits definiert sind.
#
# Hinweis: Das launch() kann auch innerhalb des with-Blocks stehen
# (wie in den anderen Beispielen), aber die Trennung ist übersichtlicher.
# ============================================================================

demo.launch()
