"""
Hello World mit Gradio - Einfachstes Beispiel.

Dieses Skript zeigt die einfachste Art, eine Gradio-App zu erstellen.
Es verwendet die `gr.Interface`-Klasse, die perfekt für schnelle Prototypen ist.

=== Was ist Gradio? ===
Gradio ist ein Python-Framework, das Python-Funktionen in interaktive
Web-Anwendungen verwandelt. Es wurde speziell für Machine Learning und
KI-Demos entwickelt, eignet sich aber für jede Art von Funktion.

Vorteile von Gradio:
- Keine HTML/CSS/JavaScript-Kenntnisse nötig
- Automatische UI-Generierung basierend auf Funktionssignaturen
- Einfaches Teilen von Demos (lokaler Server oder öffentlicher Link)
- Integration mit Hugging Face Spaces für kostenloses Hosting

=== gr.Interface vs. gr.Blocks ===
Gradio bietet zwei Hauptansätze:
1. gr.Interface() - Einfach und schnell, aber weniger flexibel
   → Perfekt für: Einzelne Funktionen, schnelle Demos, Prototypen
   
2. gr.Blocks() - Flexibel und mächtig, mehr Code
   → Perfekt für: Komplexe Layouts, mehrere Interaktionen, Custom-Apps
   
Dieses Beispiel verwendet gr.Interface() - die einfachste Variante.
"""

import gradio as gr  # Das Gradio-Framework importieren


# ============================================================================
# Die Verarbeitungsfunktion
# ============================================================================
# In Gradio definiert man zuerst die "Backend-Logik" als Python-Funktion.
# Diese Funktion:
# - Erhält die Benutzereingaben als Parameter
# - Verarbeitet die Daten
# - Gibt die Ergebnisse zurück
#
# Gradio erstellt automatisch die passende UI basierend auf:
# - Den Parametern (werden zu Eingabefeldern)
# - Den Rückgabewerten (werden zu Ausgabefeldern)
# ============================================================================

def greet(name):
    """
    Begrüßt den Benutzer mit seinem Namen.
    
    Diese einfache Funktion demonstriert das Grundprinzip:
    - Input: Ein String (Name des Benutzers)
    - Output: Ein String (personalisierte Begrüßung)
    
    Gradio ruft diese Funktion automatisch auf, wenn:
    - Der Benutzer auf "Submit" klickt
    - Der Benutzer Enter drückt (bei entsprechender Konfiguration)
    
    Args:
        name: Der eingegebene Name des Benutzers
        
    Returns:
        Eine personalisierte Begrüßungsnachricht
    """
    return f"Hallo, {name}!! 🙂"


# ============================================================================
# Die Gradio-Oberfläche erstellen und starten
# ============================================================================
# gr.Interface() ist ein "High-Level"-Wrapper, der alles in einem Aufruf macht:
# 1. UI-Komponenten basierend auf fn, inputs, outputs erstellen
# 2. Event-Handler automatisch verbinden
# 3. Layout automatisch generieren
#
# Die wichtigsten Parameter:
# - fn: Die Python-Funktion, die aufgerufen werden soll
# - inputs: Welche Komponenten für Eingaben verwendet werden
# - outputs: Welche Komponenten für Ausgaben verwendet werden
# - title: Überschrift der App (erscheint im Browser-Tab und auf der Seite)
# - description: Beschreibungstext unter dem Titel
# ============================================================================

gr.Interface(
    # Die Funktion, die bei Benutzerinteraktion aufgerufen wird
    fn=greet,
    
    # Eingabekomponente: Textbox für den Namen
    # gr.Textbox() ist ein einzeiliges Texteingabefeld
    # Das label erscheint als Beschriftung über dem Feld
    inputs=gr.Textbox(label="Name eingeben"),
    
    # Ausgabekomponente: Textbox für die Begrüßung
    # Bei Ausgabe-Textboxen kann der Benutzer den Text nicht ändern
    outputs=gr.Textbox(label="Begrüßung"),
    
    # Titel der Anwendung (erscheint groß oben)
    title="Hello World mit Gradio",
    
    # Beschreibung unter dem Titel (erklärt die App)
    description="Geben Sie Ihren Namen ein, um eine Begrüßung zu erhalten."

# launch() startet den lokalen Webserver
# Standardmäßig auf http://127.0.0.1:7860 erreichbar
# Optionale Parameter:
# - share=True: Erstellt einen öffentlichen temporären Link
# - server_port=8080: Verwendet einen anderen Port
# - inbrowser=True: Öffnet automatisch den Browser
).launch()
