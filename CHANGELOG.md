# Changelog

All notable changes to Kometa Helper will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2025-XX-XX

### Added
- **Install page** — auto-detect Python/Git, one-click Kometa clone + venv setup, one-click update
- **Connections page** — configure and live-test Plex, TMDb, Trakt, MDBList, Radarr, Sonarr; auto-discover Plex libraries; generate config.yml
- **YAML Editor** — split form/raw editor with live validation, plain-English error messages, templates, and auto-backup
- **Collections page** — browse collection/overlay files, see item counts, Kometa Defaults picker (28 collections, 24 overlays), one-click apply to library
- **Runner page** — flag selector with live command preview, real-time log streaming, start/stop controls
- **Scheduler page** — Windows Task Scheduler integration with visual day/time/type builder
- **Logs page** — log file browser, errors-only filter, full text search
- **Backups page** — auto-versioned YAML backups, preview + one-click restore
- **Settings page** — path configuration, notification toggles, theme switcher, about info
- **Dashboard** — status overview with quick-action buttons
- **Sidebar navigation** with live Kometa status indicator
- **GitHub Actions** CI/CD workflow: auto-build `.exe` on version tags
- **PyInstaller spec** for single-file Windows executable
- **Inno Setup** script for polished Windows installer
- **MIT License**

---

## Roadmap

### v1.1.0 (Planned)
- [ ] Windows system tray icon (minimize to tray, status in tray)
- [ ] Toast notifications on run complete / error (via plyer)
- [ ] Community Configs browser — search and import from the Kometa Community Configs repo
- [ ] Overlay preview — render a sample poster with selected overlays applied
- [ ] YAML diff viewer — compare two versions of a config file

### v1.2.0 (Planned)
- [ ] Dead link checker for collection file URLs
- [ ] Multi-library bulk operations
- [ ] Dark/light theme toggle in-app
- [ ] Run history chart (runs over time, success/fail ratio)

### Future Ideas
- [ ] Collection dry-run preview (show what would be added without writing)
- [ ] Import from Kometa Quickstart configs
- [ ] Integrated Kometa wiki search
