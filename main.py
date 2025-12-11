"""
Haupteinstiegspunkt für das Gradio-Beispiel Projekt.

Diese Datei dient als Standard-Einstiegspunkt für das Projekt.
Sie kann verwendet werden, um:
- Alle Beispiele der Reihe nach zu demonstrieren
- Ein bestimmtes Beispiel zu starten
- Das Projekt als Modul zu initialisieren

=== Projektstruktur ===
Das Projekt enthält verschiedene Beispiele mit steigender Komplexität:

1. hello_gradio.py
   → Einfachstes Beispiel mit gr.Interface()
   → Zeigt: Grundprinzip Input → Funktion → Output

2. hello_gradio_blocks.py
   → Gleiche Funktionalität mit gr.Blocks()
   → Zeigt: Manuelle Event-Verknüpfung, mehr Kontrolle

3. gradio_components.py
   → Mehrere Komponenten (Textbox, Dropdown, Slider)
   → Zeigt: Verschiedene Eingabetypen, mehrere Outputs

4. gradio_components_blocks.py
   → Gleiche Komponenten mit Blocks und Layout
   → Zeigt: gr.Row() für horizontales Layout

5. gradio_gemini.py
   → Integration mit Google Gemini API
   → Zeigt: Externe API-Anbindung, Markdown-Ausgabe

6. gradio_adk.py
   → Agent mit Google ADK und Werkzeugen
   → Zeigt: KI-Agenten, Tool-Nutzung, Chatbot-UI

=== Ausführung ===
Einzelne Beispiele starten:
    uv run python hello_gradio.py
    uv run python gradio_gemini.py
    etc.

Diese Datei starten:
    uv run python main.py
"""


def main():
    """
    Hauptfunktion des Projekts.
    
    Aktuell nur eine einfache Begrüßung.
    Kann erweitert werden, um z.B.:
    - Ein Menü zur Beispielauswahl anzuzeigen
    - Alle Beispiele nacheinander zu starten
    - Projektinformationen auszugeben
    """
    print("Hello from gradio-beispiel!")
    print("\nVerfügbare Beispiele:")
    print("  • hello_gradio.py          - Einfachstes Gradio-Beispiel")
    print("  • hello_gradio_blocks.py   - Blocks API Grundlagen")
    print("  • gradio_components.py     - Verschiedene Komponenten")
    print("  • gradio_components_blocks.py - Komponenten mit Layout")
    print("  • gradio_gemini.py         - Gemini Integration")
    print("  • gradio_adk.py            - Agent Development Kit")
    print("\nStarte ein Beispiel mit: uv run python <dateiname>")


# ============================================================================
# Skript-Ausführung
# ============================================================================
# Der folgende Block wird nur ausgeführt, wenn die Datei direkt gestartet wird
# (nicht wenn sie als Modul importiert wird).
#
# Das ist ein Python-Standard-Pattern:
# - __name__ ist der Name des aktuellen Moduls
# - Wenn die Datei direkt ausgeführt wird, ist __name__ == "__main__"
# - Wenn die Datei importiert wird, ist __name__ der Modulname
# ============================================================================

if __name__ == "__main__":
    main()
