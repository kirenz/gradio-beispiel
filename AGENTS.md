# AGENTS.md

## Projektübersicht

Dies ist ein Lernprojekt für **Gradio-Basics** in Kombination mit **Google Gemini** und dem **Agent Development Kit (ADK)**. Das Projekt dient als praktische Einführung in die Erstellung von KI-gestützten Web-Interfaces.

## Technologie-Stack

- **Gradio** - Python-Framework für schnelle UI-Entwicklung von ML/KI-Anwendungen
- **Google Gemini** - Multimodales KI-Modell von Google (`google-genai`)
- **ADK** - Agent Development Kit für die Entwicklung von KI-Agenten
- **Python 3.11+** - Programmiersprache

## Paketverwaltung

Dieses Projekt verwendet **uv** als Paketmanager.

### Pakete installieren

```bash
uv add <paketname>
```

### Projekt einrichten

```bash
uv sync
```

### Projekt ausführen

```bash
uv run python <dateiname>.py
```

## Projektstruktur

| Datei | Beschreibung |
|-------|-------------|
| `hello_gradio.py` | Einfaches Gradio-Beispiel für den Einstieg |
| `hello_gradio_blocks.py` | Gradio Blocks API Beispiel |
| `gradio_components.py` | Übersicht verschiedener Gradio-Komponenten |
| `gradio_components_blocks.py` | Komponenten mit Blocks API |
| `gradio_gemini.py` | Integration von Gradio mit Google Gemini |
| `gradio_adk.py` | Verwendung des Agent Development Kit |
| `main.py` | Haupteinstiegspunkt |

## Umgebungsvariablen

Erstelle eine `.env`-Datei im Projektverzeichnis mit:

```
GOOGLE_API_KEY=dein_api_key
```

## Code-Stil

- Verwende deutsche Kommentare für Lernzwecke
- Halte den Code einfach und gut dokumentiert
- Jede Datei sollte als eigenständiges Beispiel funktionieren

## Lernziele

1. Grundlagen von Gradio verstehen (Interface, Blocks, Components)
2. Integration von LLMs (Gemini) in Gradio-Anwendungen
3. Entwicklung von KI-Agenten mit ADK
4. Best Practices für interaktive KI-Demos
