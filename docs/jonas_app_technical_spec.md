# JONAS PRODUCTIONS SITE MANAGER
# Complete technical spec — CLI app + Electron desktop app
# Built by Rudi Willock. To be sold to Tom Jonas.
# Start a new Claude session with this document + the project setup doc.

---

## WHAT THIS DOCUMENT IS

The full technical spec and build plan for converting manage.py into:

1. A polished CLI management tool (enhanced terminal version)
2. A packaged Electron desktop app (double-click, no Terminal, sellable)

Both ship from the same codebase. The Electron app wraps the existing
manage.py web UI inside a native Mac/Windows window. The CLI is an
enhanced version of what already exists.

---

## CURRENT STATE — WHAT EXISTS

manage.py is a working Python CMS with two modes:

```
python manage.py          → interactive CLI menu
python manage.py web-ui   → browser admin at http://127.0.0.1:8082
```

**What it does today:**
- Edit contact info (address, phone, fax, email)
- Add/edit/delete touring artists (name + since year)
- Add/edit/delete backline equipment categories + brand lists
- Add/edit/delete audio equipment categories + brand lists
- Add/edit/delete client categories + name lists
- Rebuild all 6 HTML pages from JSON data (inject between HTML markers)
- Publish to GitHub Pages (git add -A → commit → push)
- Auto-backup before every change (timestamped snapshots in .backups/)
- Restore from any backup
- Seed data files from defaults on first run

**What it does NOT do yet (gaps to fill):**
- No image/photo management
- No photo upload to the site
- No custom domain setup helper
- No update checker
- No installer — requires Python installed manually
- No native app packaging

**The HTML injection markers in the site files:**
```
<!-- BACKLINE_CATEGORIES_START --> ... <!-- BACKLINE_CATEGORIES_END -->
<!-- AUDIO_CATEGORIES_START -->   ... <!-- AUDIO_CATEGORIES_END -->
<!-- CLIENTS_START -->            ... <!-- CLIENTS_END -->
<!-- TOURS_START -->              ... <!-- TOURS_END -->
<!-- CONTACT_INFO_START -->       ... <!-- CONTACT_INFO_END -->
```

---

## REPO + FILE STRUCTURE

```
jonas-productions/
├── index.html
├── backline.html
├── audio.html
├── clients.html
├── about.html
├── contact.html
├── style.css
├── nav.js
├── manage.py              ← CMS (existing, working)
├── data/
│   ├── backline.json
│   ├── audio.json
│   ├── clients.json
│   ├── tours.json
│   └── contact.json
└── .backups/              ← auto-created, git-ignored

GitHub repo: github.com/willockrudi/jonas-productions
Live site:   willockrudi.github.io/jonas-productions
```

---

## PART 1 — ENHANCED CLI APP

The CLI is for Rudi — for quick terminal edits without opening a browser.
Keep everything that exists. Add these improvements:

### New CLI commands to add

```
manage.py status          → print site status: last publish time,
                            uncommitted changes, JSON data summary
manage.py publish "msg"   → publish with commit message, no prompts
manage.py rebuild         → rebuild all pages, no prompts
manage.py backup          → create a named backup right now
manage.py restore         → interactive: list + restore from backup
manage.py open            → open the site in the default browser
manage.py add-artist      → prompt for artist + year, save, rebuild
manage.py add-brand       → prompt for section + brand, save, rebuild
manage.py add-client      → prompt for category + name, save, rebuild
manage.py contact         → interactive contact info editor
manage.py check           → validate all JSON files + HTML markers
manage.py version         → print current version string
```

### CLI improvements to existing behavior

```
- Color output: green for success, yellow for warnings, red for errors
  Use colorama (pip install colorama) — cross-platform terminal colors
- Progress indicators: show "Rebuilding..." then "✓ Done" not just silence
- git status check before publish: warn if working tree is clean
  (nothing to commit)
- --dry-run flag: show what would change without writing anything
- Confirm prompts on destructive actions (delete, restore)
- Better error messages: "Marker not found in about.html" not a traceback
```

### CLI quick reference card (print this, keep it handy)

```
python manage.py                   Interactive menu
python manage.py web-ui            Open admin at localhost:8082
python manage.py status            Print current site state
python manage.py rebuild           Rebuild all pages now
python manage.py publish           Publish to GitHub (prompts for message)
python manage.py publish "msg"     Publish with commit message inline
python manage.py backup            Create backup snapshot now
python manage.py restore           List + restore a backup
python manage.py open              Open index.html in browser
python manage.py check             Validate JSON + HTML markers
python manage.py add-artist        Add a touring artist
python manage.py add-brand         Add a brand to a category
python manage.py add-client        Add a client name
```

---

## PART 2 — ELECTRON DESKTOP APP

The Electron app wraps the existing manage.py web UI into a native
Mac/Windows window. Tom Jonas double-clicks it and sees the admin panel —
no browser, no Terminal, no Python visible.

### Why Electron is the right choice

- The manage.py web UI (HTML/CSS/JS at localhost:8082) already exists
  and looks professional. No need to rebuild the UI.
- Electron wraps any web content in a native window. Perfect fit.
- electron-builder packages it as a .dmg (Mac) or .exe installer (Windows)
- No Python installation required on Tom's machine — Python is bundled
- Real dock icon, real app menu, real native Mac/Windows behavior
- This is what VS Code, Slack, Discord, and Figma are built on

### Architecture

```
jonas-site-manager/              ← separate repo from the website
├── main.js                      Electron main process
│                                starts Python manage.py web-ui as a child
│                                process, opens a BrowserWindow
├── preload.js                   IPC bridge (security boundary)
├── renderer/
│   └── loading.html             Splash screen shown while Python starts
├── backend/
│   └── manage.py                Copy of Jonas site manage.py
├── assets/
│   └── icon.icns                App icon (Mac) — get from icons8.com
│   └── icon.ico                 App icon (Windows)
├── package.json                 Electron config + electron-builder config
└── requirements.txt             Python deps for the bundled backend
```

### main.js — what it needs to do

```javascript
// 1. On app ready, show loading window
// 2. Spawn Python process:
//    python manage.py web-ui --port 8082
//    capture stdout to know when server is ready
//    ("✅ Jonas Admin UI →" in stdout = ready signal)
// 3. When ready signal received, close loading window
//    open BrowserWindow pointing to http://127.0.0.1:8082
// 4. On window close, kill the Python process cleanly
// 5. App menu: File → Quit, Help → About, Edit → standard cut/copy/paste
// 6. Handle port conflict: if 8082 busy, try 8083, 8084...
```

### package.json (key sections)

```json
{
  "name": "jonas-site-manager",
  "version": "1.0.0",
  "description": "Jonas Productions website manager",
  "main": "main.js",
  "scripts": {
    "start":   "electron .",
    "pack":    "electron-builder --dir",
    "dist":    "electron-builder",
    "dist-mac": "electron-builder --mac",
    "dist-win": "electron-builder --win"
  },
  "devDependencies": {
    "electron": "^28.0.0",
    "electron-builder": "^24.0.0"
  },
  "build": {
    "appId": "com.rudiwillock.jonassitemanager",
    "productName": "Jonas Site Manager",
    "directories": { "output": "dist" },
    "extraResources": [
      { "from": "backend/", "to": "backend" }
    ],
    "mac": {
      "category": "public.app-category.business",
      "icon": "assets/icon.icns",
      "target": [{ "target": "dmg", "arch": ["x64", "arm64"] }]
    },
    "win": {
      "icon": "assets/icon.ico",
      "target": [{ "target": "nsis", "arch": ["x64"] }]
    }
  }
}
```

### Bundling Python with the app

This is the critical piece. Tom's Mac doesn't have Python.
Use **pyinstaller** to bundle manage.py + Python into a standalone binary:

```bash
# On your Mac — do this ONCE to create the bundled binary
cd jonas-site-manager/backend
pip install pyinstaller colorama
pyinstaller --onefile manage.py --name manage_server

# This creates: backend/dist/manage_server
# That binary contains Python + all dependencies
# Electron's main.js spawns backend/dist/manage_server instead of
# calling python manage.py
```

In main.js, detect whether you're in dev or prod:
```javascript
const isDev = !app.isPackaged;
const backendBin = isDev
  ? 'python'
  : path.join(process.resourcesPath, 'backend', 'manage_server');
const backendArgs = isDev ? ['backend/manage.py', 'web-ui'] : ['web-ui'];
```

### Build and package commands

```bash
# Install Electron and builder
npm install

# Run in dev (Python must be installed on your machine)
npm start

# Package as .app for Mac (run this on your Mac)
npm run dist-mac
# Output: dist/Jonas Site Manager-1.0.0.dmg
# Give this DMG to Tom — drag app to Applications, done

# Package as .exe installer for Windows
npm run dist-win
# Output: dist/Jonas Site Manager Setup 1.0.0.exe
```

### What Tom sees

```
1. Double-click "Jonas Site Manager" in Applications
2. Small loading screen: "Jonas Site Manager — starting..."
   (Python server takes 2-3 seconds to start)
3. Admin panel opens in native window — no browser, no Terminal
4. Uses it: edits content, clicks "Rebuild", clicks "Publish to GitHub"
5. Closes the window — Python process exits cleanly
```

---

## PART 3 — FEATURES TO ADD BEFORE SELLING

These are the gaps between "works for Rudi" and "polished enough to sell":

### Must-have before demo

```
[ ] Status bar in web UI showing last published time
    (read from git log --oneline -1 -- format it nicely)
[ ] "You have unpublished changes" warning badge
    (compare data/ JSON mtime to last git commit time)
[ ] Confirmation dialog before deleting anything
    Currently: click delete → gone. No confirm.
[ ] Success/error toasts that auto-dismiss
    Currently: flash a green msg param in URL, easy to miss
[ ] Loading spinner on "Publish to GitHub" button
    Currently: button does nothing visible for 3-5 seconds during push
[ ] "Open site in browser" button in the web UI header
    One click to preview the live site
```

### Nice-to-have for v1.0

```
[ ] Photo upload to a gallery section
    Add <!-- GALLERY_START/END --> markers to index.html
    Web UI: drag-drop image → resize to web → save to images/ folder
    manage.py injects <img> tags between markers
[ ] Formspree integration for contact form
    Replace mailto: with Formspree endpoint
    Add a field in web UI: "Contact form ID"
    manage.py injects the form action URL
[ ] Custom domain helper
    "Connect your domain" guide built into the app
    Walks through GitHub Pages CNAME setup step by step
[ ] Auto-update checker
    On launch: compare version string to GitHub releases API
    Show "Update available" if newer version exists
[ ] Settings screen
    Git remote URL (default: origin)
    Site folder path (currently: same folder as manage.py)
    Backup retention count
    Port number
```

---

## PART 4 — PROJECT PHASES

```
Phase 1 — Polish existing (1-2 sessions)
  Enhance CLI with color output and new commands
  Add confirmation dialogs, status bar, loading spinner to web UI
  Fix contact form (mailto → Formspree)
  Test everything end-to-end

Phase 2 — Electron wrapper (1-2 sessions)
  Set up Electron project structure
  Write main.js: spawn Python, open window, handle shutdown
  Write loading.html splash screen
  Test locally: npm start

Phase 3 — Bundle Python + package (1 session)
  PyInstaller: bundle manage.py → standalone binary
  Wire binary into Electron build
  npm run dist-mac → .dmg
  Test: install on clean Mac, open, use, publish

Phase 4 — Demo and pitch
  Install on your demo laptop
  Walk through demo script (see pitch doc)
  Present to Tom
```

---

## PART 5 — DEV ENVIRONMENT SETUP

### On your Mac

```bash
# Python side
pip3 install colorama pyinstaller

# Node/Electron side
brew install node          # if not installed
npm install -g electron    # optional global install for testing

# Clone or create the Electron project
mkdir jonas-site-manager
cd jonas-site-manager
npm init -y
npm install --save-dev electron electron-builder
```

### Project boot sequence in dev

```bash
# Terminal 1: start Python backend
cd jonas-site-manager/backend
python manage.py web-ui

# Terminal 2: start Electron (points to localhost:8082)
cd jonas-site-manager
npm start
```

Or with npm scripts configured in package.json, just:
```bash
npm start   # launches both Python and Electron
```

### Folder where Jonas website lives

The Electron app and the website repo are **two separate things**:
```
~/dev/jonas-productions/         ← the website (GitHub repo, live site)
~/dev/jonas-site-manager/        ← the Electron app (separate repo)
```

The Electron app bundles a copy of manage.py that knows the path
to the Jonas website folder. On Tom's machine, this path is configured
in the app's Settings screen (or defaults to ~/Documents/jonas-website/).

---

## PART 6 — KNOWN ISSUES TO FIX

```
Issue: manage.py won't run from a flash drive on a machine without Python
Fix: Electron app bundles Python via PyInstaller — no install needed

Issue: Contact form uses mailto: — unreliable, doesn't work on mobile
Fix: Formspree (free tier: 50 submissions/month)
     Sign up at formspree.io → create form → get URL
     Add URL field to manage.py → inject into contact.html

Issue: No confirmation before deleting a touring artist/category/client
Fix: Add <dialog> confirm in web UI or confirm() in JS before form submit

Issue: "Publish to GitHub" button hangs silently for 3-5 seconds
Fix: Add spinner + disable button during submit
     Show progress in status bar: "Pushing to GitHub..."

Issue: Loading the web UI for the first time shows no data if JSON
       files don't exist yet (first run on a new machine)
Fix: Already handled by init_data() in manage.py — just verify it runs

Issue: App needs to be rebuilt on Mac to get .dmg, on Windows to get .exe
       Cannot cross-compile
Fix: Build both on your Mac and a Windows machine, or use GitHub Actions
     (free CI/CD) to build for both platforms automatically
```

---

## PROMPTS FOR CLAUDE SESSIONS

**To build the Electron wrapper:**
```
I have a Python web app (manage.py) that serves a local web UI at
localhost:8082 for managing a static website. I want to wrap it in
an Electron app so it opens as a native window without needing a
browser or Terminal.

Project context: [paste project setup doc]
Current manage.py: [paste manage.py]

Build me:
1. main.js — spawns manage.py web-ui as a child process, waits for
   the "✅ Jonas Admin UI" ready signal in stdout, then opens a
   BrowserWindow at http://127.0.0.1:8082
2. package.json — with electron-builder config for Mac .dmg and
   Windows .exe packaging
3. renderer/loading.html — simple "Starting Jonas Site Manager..."
   splash screen shown while Python starts up
4. preload.js — basic IPC bridge (security standard)

The Python binary will be bundled via PyInstaller as 'manage_server'.
In production (app.isPackaged), spawn from process.resourcesPath/backend/manage_server.
In dev, spawn python manage.py web-ui.
```

**To enhance the CLI:**
```
I have a Python CLI management tool for a static website.
Current manage.py: [paste manage.py]
Project context: [paste project setup doc]

Enhance manage.py with:
1. Colorama color output (green success, yellow warning, red error)
2. New subcommands: status, rebuild, publish "msg", backup, restore,
   open, add-artist, add-brand, add-client, contact, check, version
3. --dry-run flag on destructive operations
4. Confirm prompts before delete/restore
5. Progress output during rebuild and publish
6. Better error messages (no raw tracebacks)
Keep all existing functionality. Backwards compatible.
```

**To add the status bar + confirmation to web UI:**
```
I have a Python web UI (serve from manage.py, HTML embedded in Python).
Current manage.py: [paste manage.py]

Add to the web UI:
1. Status bar at bottom of every page: last git commit time,
   "unpublished changes" warning if data/ JSON is newer than last commit
2. Confirmation dialog before any delete action
3. Loading spinner on the "Publish to GitHub" button
4. "Open site in browser" button in header
5. Auto-dismissing toast notifications (replace the ?msg= URL flash)
Keep it as embedded HTML in Python — single file, no external dependencies.
```
