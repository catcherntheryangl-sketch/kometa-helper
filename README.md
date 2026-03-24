# ⚡ Kometa Helper

<div align="center">

![Kometa Helper](https://img.shields.io/badge/Kometa-Helper-0bc8e0?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A Windows GUI wrapper that makes installing, configuring, and running [Kometa](https://github.com/Kometa-Team/Kometa) easy for everyone.**

[Download](#download) · [Features](#features) · [Screenshots](#screenshots) · [Getting Started](#getting-started) · [Build from Source](#build-from-source)

</div>

---

## What is Kometa Helper?

[Kometa](https://kometa.wiki) is a powerful Python tool that manages Plex metadata, builds collections, and applies overlays — but getting it installed and configured on Windows requires navigating Python environments, editing raw YAML files, and manually setting up scheduled tasks.

**Kometa Helper** wraps all of that in a clean Windows GUI so you can:

- ✅ Install Kometa in a few clicks (Python, Git, venv handled for you)
- ✅ Connect to Plex, TMDb, Trakt, MDBList, Radarr, and Sonarr with guided setup and live connection tests
- ✅ Edit YAML config files visually — form editor on the left, live YAML on the right
- ✅ Browse and enable Kometa's built-in default collections and overlays
- ✅ Run Kometa with a GUI flag selector and live log streaming
- ✅ Schedule automated runs via Windows Task Scheduler
- ✅ Browse and filter run logs (errors-only view, search)
- ✅ Auto-backup configs and restore previous versions

> **Note:** Kometa Helper complements the official [Kometa Quickstart](https://github.com/Kometa-Team/Quickstart) tool. Quickstart is great for initial config generation; Kometa Helper focuses on ongoing management, YAML editing, scheduling, and log monitoring.

---

## Features

### 🏠 Dashboard
Status overview showing Kometa install status, last run time, config status, and library count. Quick-action buttons to the most-used pages.

### ⚙️ Install & Update
- Detects Python 3.10+ and Git automatically
- Clones Kometa from GitHub with one click
- Creates a Python virtual environment and installs all dependencies
- One-click update (git pull)
- Shows installed vs. latest version

### 🔌 Connections
- Configure Plex, TMDb, Trakt, MDBList, Radarr, and Sonarr
- **Live connection test** for each service with instant feedback
- Plex library discovery — see all your libraries after connecting
- Links directly to each service's API key page
- "Generate config.yml" button creates your initial config from entered credentials

### 📋 YAML Editor
- Split view: form quick-editor on the left, raw YAML on the right
- YAML validation on every keystroke with plain-English error messages (not raw YAML exceptions)
- Templates: blank config.yml, collection file, overlay file
- Auto-saves backups before every write
- Quick-edit panel pre-fills from your existing config

### 🗂️ Collections & Overlays
- Browse all your collection and overlay YAML files
- See collection count per file at a glance
- Edit any file directly in the YAML editor
- **Kometa Defaults picker** — checkbox-select from all 28 default collections and 24 default overlays, then apply to any library with one click

### ▶️ Run Kometa
- Checkbox flag selector (--run, --collections-only, --overlays-only, --operations-only, --debug, etc.)
- Live command preview updates as you select flags
- **Live log streaming** — see output in real time as Kometa runs
- Error/warning/success color coding in the log output
- Stop running process at any time

### 📅 Scheduler
- Visual Windows Task Scheduler builder
- Select run type, time, and days of the week
- Creates actual Windows scheduled tasks via `schtasks`
- Lists and manages all Kometa Helper-created tasks

### 📜 Logs
- Browse all Kometa log files
- **Errors-only filter** — one click to see just what went wrong
- Full text search across the current log
- Split view: file list + log content

### 💾 Backups
- All YAML saves are automatically versioned (up to 20 per file)
- Browse backup history with timestamps
- Preview any backup before restoring
- One-click restore (backs up current config first)

---

## Download

### Option 1 — Standalone `.exe` (Recommended)
No Python required. Download the latest release from the [Releases page](../../releases).

```
KometaHelper-v1.0.0-Windows.exe
```

Double-click to run. No installation needed.

### Option 2 — Run from Source
Requires Python 3.10+ and Git.

```bash
git clone https://github.com/catcherntheryangl-sketch/kometa-helper
cd kometa-helper
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## Getting Started

1. **Launch Kometa Helper**
2. Go to **Install** → click "Check Python" and "Check Git"
3. Enter your desired install directory and click **Install Kometa**
4. Go to **Connections** → enter your Plex URL and token, TMDb API key
5. Click **Test Connection** for each service, then **Generate config.yml**
6. Go to **Collections** → Kometa Defaults tab → pick your collections → Apply to a library
7. Go to **Run Kometa** → click **▶ Run Kometa** and watch the live output
8. (Optional) Go to **Scheduler** → create a daily scheduled task

### Getting Your Plex Token
In Plex Web: open any movie → click `···` → `Get Info` → `View XML`. Look for `X-Plex-Token=` in the URL.

### Getting a TMDb API Key
Visit [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api) — free account required.

---

## Build from Source

### Requirements
- Python 3.10+
- Git

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run directly
```bash
python main.py
```

### Build a standalone `.exe`
```bash
pip install pyinstaller
pyinstaller kometa-helper.spec
```

The output will be in `dist/KometaHelper.exe`.

---

## Project Structure

```
kometa-helper/
├── main.py                        # Entry point
├── requirements.txt
├── kometa-helper.spec             # PyInstaller spec
├── installer/
│   └── setup.iss                  # Inno Setup installer script
├── src/
│   ├── app.py                     # App orchestrator
│   ├── core/
│   │   ├── config_manager.py      # Settings + YAML persistence
│   │   └── kometa_manager.py      # Install/run/update/test connections
│   ├── ui/
│   │   ├── theme.py               # Color palette, fonts, constants
│   │   ├── main_window.py         # Sidebar nav + page routing
│   │   └── pages/
│   │       ├── base_page.py
│   │       ├── dashboard.py
│   │       ├── install.py
│   │       ├── connections.py
│   │       ├── yaml_editor.py
│   │       ├── collections.py
│   │       ├── runner.py
│   │       ├── scheduler.py
│   │       ├── logs.py
│   │       ├── backups.py
│   │       └── settings.py
│   └── utils/
│       └── yaml_utils.py
└── .github/
    └── workflows/
        └── build.yml              # GitHub Actions: build + release .exe
```

---

## Relationship to Kometa & Quickstart

| Tool | Purpose |
|------|---------|
| [Kometa](https://github.com/Kometa-Team/Kometa) | The core metadata manager — Kometa Helper runs this |
| [Kometa Quickstart](https://github.com/Kometa-Team/Quickstart) | Official web UI for generating your initial config.yml |
| **Kometa Helper** | Windows GUI for install, ongoing YAML management, scheduling, and log monitoring |

Kometa Helper is not affiliated with or endorsed by the Kometa team.

---

## Contributing

Pull requests welcome! Please open an issue first for major changes.

```bash
git checkout -b feature/my-feature
# make your changes
git commit -m "Add: my feature"
git push origin feature/my-feature
# open a PR
```

---

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">
Made with ❤️ for the Plex & Kometa community
</div>
