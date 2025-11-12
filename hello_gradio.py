# Gradio stellt UI-Bausteine bereit, mit denen wir ohne Frontend-Wissen kleine Apps bauen können.
import gradio as gr


# Diese Funktion bildet das komplette Verhalten der App: Sie nimmt den eingegebenen Namen
# entgegen und liefert eine personalisierte Begrüßung zurück.
def greet(name):
    """Function to greet the user by name."""
    return f"Hallo, {name}!! 🙂"

# `gr.Interface` ist der einfachste Start mit Gradio:
#   * fn: welche Python-Funktion ausgeführt werden soll
#   * inputs / outputs: welche Komponenten auf der Oberfläche erscheinen
#   * title / description: Kopfbereich im Browser
# Das `.launch()` am Ende startet den lokalen Webserver.
gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="Name eingeben"),
    outputs=gr.Textbox(label="Begrüßung"),
    title="Hello World mit Gradio",
    description="Geben Sie Ihren Namen ein, um eine Begrüßung zu erhalten."
).launch()
