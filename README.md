# Gradio-Beispiel

Dieses Repository enthält mehrere kleine Gradio-Apps, die unterschiedliche Wege zeigen, wie man Python-Funktionen als Weboberfläche bereitstellt – von der einfachen `gr.Interface`-Variante bis zum frei gestaltbaren `gr.Blocks`-Layout und einer Anbindung an Googles Gemini-API.

## Voraussetzungen

- [uv](https://github.com/astral-sh/uv) ist installiert (verwaltet Abhängigkeiten und virtuelle Umgebung).
- Python 3.11 (wird von uv automatisch bereitgestellt).
- Für `gradio_gemini.py`: Ein Gemini-API-Schlüssel aus [Google AI Studio](https://aistudio.google.com/api-keys).

## Setup

1. Repository klonen oder herunterladen.
2. Ins Projekt wechseln:
   ```bash
   cd gradio-beispiel
   ```
3. Abhängigkeiten installieren (legt auch die virtuelle Umgebung an):
   ```bash
   uv sync
   ```
4. Optional Editor öffnen, z. B. mit VS Code:
   ```bash
   code .
   ```

## Überblick über die Beispiele

- `hello_gradio.py` – minimaler Einstieg mit `gr.Interface`.
- `hello_gradio_blocks.py` – gleiche Logik, aber mit manuell aufgebautem Blocks-Layout.
- `gradio_components.py` – zeigt mehrere Eingabe- und Ausgabekomponenten in einem Interface.
- `gradio_components_blocks.py` – dasselbe Szenario, frei arrangiert mit Rows und Buttons.
- `gradio_gemini.py` – verbindet eine Textbox mit Googles Gemini-Modell und nutzt `gr.Blocks`.

## Gemini konfigurieren

Für `gradio_gemini.py` wird eine `.env`-Datei mit folgendem Inhalt benötigt:

```
GEMINI_API_KEY=api_schluessel
```

Die Datei darf **nicht** eingecheckt werden, damit der Schlüssel privat bleibt.

## Anwendungen starten

Alle Beispiele lassen sich direkt über uv starten. Die folgenden Befehle immer aus dem Projektordner heraus ausführen; uv sorgt automatisch für die richtige Umgebung.

Hello World mit Interface

```bash
uv run python hello_gradio.py
```

Hello World mit Blocks

```bash
uv run python hello_gradio_blocks.py
```

Komponenten-Demo mit Interface

```bash
uv run python gradio_components.py
```

Komponenten-Demo mit Blocks

```bash
uv run python gradio_components_blocks.py
```

Gemini Text Generator (benötigt gültigen GEMINI_API_KEY)

```bash
uv run python gradio_gemini.py
```

> **Wichtig:** Immer nur eine Gradio-App gleichzeitig laufen lassen. Um eine laufende App zu beenden, ins Terminal wechseln und `Strg + C` (macOS/Linux) bzw. `Ctrl + C` (Windows) drücken. Erst danach den nächsten `uv run`-Befehl ausführen.
