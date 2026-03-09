# Song Translator

Song Translator is a browser tool for musicians, translators, and language learners. Load any YouTube video, paste the lyrics, and sync each line to the exact moment it plays. Add translation columns in any language — powered by Gemini AI or manually — and export everything as text. No installation, no account, no server. Just open and start working.

**[▶ Open Online](https://shulenok.github.io/song-translator/)**

---

## Features

- 🎬 **YouTube sync** — load any video and timestamp each lyric line to the exact second
- 📝 **Side-by-side columns** — original + multiple translations visible at once
- ✦ **Gemini AI translation** — generate 10 rhythm-matched variants per line
- 📋 **Import & clean** — paste raw lyrics, auto-removes chords, section labels, URLs
- 🏷️ **Auto section detection** — Verse, Chorus, Bridge labels detected automatically
- 💾 **Save / Open projects** — `.json` format preserves everything including timestamps
- 📤 **Export** — save any column or all columns as `.txt`
- ⌨️ **Keyboard shortcuts** — Space to play/pause, arrows to seek and navigate lines

## Online Version

Open directly in your browser — no installation needed:

**https://shulenok.github.io/song-translator/**

> **Note:** The online version works fully except for the **Get Subtitles** button, which requires the local server (see below).

---

## Local Version (with Subtitles)

The local server enables auto-loading of YouTube subtitles.

### Requirements
- Python 3.8+

### Setup

1. Download or clone this repository
2. Double-click **`start-server.bat`** (Windows)  
   — or run manually: `python server.py`
3. Browser opens at `http://localhost:8080`

The server auto-installs `youtube-transcript-api` on first run.

### Optional: Fix YouTube blocking

If subtitles fail to load, export cookies from your browser using the **"Get cookies.txt LOCALLY"** extension and save the file as `cookies.txt` in the same folder as `server.py`.

---

## Gemini AI Setup

1. Get a free API key at [aistudio.google.com](https://aistudio.google.com)
2. Open **Settings** in the app and paste the key
3. Click ✦ on any row → AI Translate

---

## License

MIT
