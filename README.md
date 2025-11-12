# Gradio-Beispiel für Einsteiger

Dieses Repository enthält ein minimales Gradio-Projekt (`hello_gradio.py`), das Schritt für Schritt zeigt, wie Sie eine kleine Weboberfläche für Python-Funktionen erstellen. 

## Voraussetzungen

- **uv**: Moderner Paket- und Projektmanager (https://github.com/astral-sh/uv). Installieren Sie ihn einmalig laut Projektseite.

## Schritt-für-Schritt Setup

1. **Projekt anlegen im Terminal (macOS) oder Git Bash (Windows)**
   ```bash
   uv init gradio-beispiel --python 3.11
   ```
   Dadurch legt uv ein neues Projektverzeichnis inklusive virtueller Umgebung an.

2. **Ins Projekt wechseln**
   ```bash
   cd gradio-beispiel
   ```

3. **Abhängigkeiten hinzufügen**
   ```bash
   uv add gradio google-genai python-dotenv
   ```
   - `gradio`: stellt die Weboberfläche bereit.
   - `google-genai`: Beispiel-Client für Google Generative AI 
   - `python-dotenv`: lädt API-Schlüssel oder andere Variablen aus einer `.env`-Datei.

4. **Editor öffnen**
   Starten Sie z. B. VS Code im aktuellen Ordner, um den Code zu bearbeiten:
   ```bash
   code .
   ```

## Beispieldatei ausführen

Integriertes Temrinal in VS Code öffnen oder externes Terminal nutzen:

1. Stellen Sie sicher, dass Sie sich im Projektordner befinden.
2. Führen Sie das Beispiel aus:
   ```bash
   uv run python main.py
   ```
