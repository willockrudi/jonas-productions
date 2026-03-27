# JONAS PRODUCTIONS — MASTER PROJECT DOCUMENT
# Paste this at the top of any new Claude session to restore full context.
# Covers: website, manage.py CMS, CLI app, Electron app, pitch strategy.

---

## TLDR — WHAT THIS PROJECT IS

Rudi Willock (you) works at Jonas Productions as a bench tech / tech lead.
On your own time you built:
1. A new professional website for Jonas Productions (6 pages, static HTML)
2. A Python CMS tool (manage.py) to update the site without touching code
3. Plan to convert manage.py into a sellable Electron desktop app

Goal: sell the website + app to Tom Jonas (the owner), establish
yourself as the go-to developer for Jonas Productions, and use that
trust to pitch Backline OS (the bigger production management platform)
in 3-6 months.

---

## PEOPLE

```
Rudi Willock      You. Lead bench tech at Jonas. Built everything.
Tom Jonas         Owner. Not technical. Needs to double-click to use anything.
Karen             Logistics / office. Likely the day-to-day site editor.
```

---

## JONAS PRODUCTIONS — COMPANY FACTS

```
Full name:    Jonas Productions, Inc.
What:         Full-service audio and backline rental, turn-key event production
              Staffed by degreed professionals, techs travel with every rental
Founded:      1987, Indianapolis IN
Address:      8606 N 700 West, Fountaintown IN 46130
Phone:        317-835-7826
Fax:          317-835-2207
Email:        info@jonasproductions.com
Domain:       jonasproductions.com
Revenue:      $1M–$10M estimated (ZoomInfo)
Employees:    ~30
```

**Long-term touring partnerships:**
The Four Tops (since 1988), The Temptations (1989), The O'Jays (1994),
Harry Connick Jr. (1995), Brian McKnight (1998)

**Notable past clients:**
Aerosmith, Tony Bennett, Boyz II Men, Jimmy Buffett, Julio Iglesias,
Julie Andrews, Barbara Eden, Mandy Patinkin, American Express, Ford,
Procter & Gamble, Daimler-Chrysler, NHRA, President Bush Inauguration,
President Clinton Inauguration, President Nixon Library, President Reagan,
Indianapolis/London/Paris/New York Symphony, Cincinnati/Indianapolis/
New Orleans Jazz Festivals, ABC/Disney, NBC Today Show, Motown Live,
Tonight Show Jay Leno, David Letterman, Assemblies of God, Promise Keepers,
Pope John Paul II

**Backline inventory includes:**
Keyboards: Ensoniq, Korg, Kurzweil, Roland, Yamaha
Organs/Electric Pianos: Fender Rhodes, Hammond, Leslie, Wurlitzer
Samplers: Akai, Alesis, Roland
Drums: Drum Workshop, Ludwig, Yamaha, Gretch, Pearl
Guitar Amps: Ampeg, Fender, Line 6, Mesa Boogie, Peavey, Roland,
             Matchless, Trace Elliot, Vox
Bass Amps: Ampeg, David Eden, Gallien-Krueger, Hartke, Hughes & Kettner, SWR
Percussion: Latin Percussion, Sabian, Paiste, Zildjian
Symphonic: Gongs, Vibes, Tympani, Xylophone, Wenger Chairs, Music Stands

**Audio inventory includes:**
PA: EAW, JBL, Meyer
Electronics: Brooke Siren, Klark-Teknik, Lexicon, Midas, TC Electronics, Yamaha
Mics: AKG, Audio-Technica, Barcus-Berry, Beyer-Dynamic, C-Ducer,
      EV, Neuman, Sennheiser, Shure
Wireless/IEM: Audio-Technica, Sennheiser, Samson, Shure

---

## THE WEBSITE

**Live URL:** willockrudi.github.io/jonas-productions
**GitHub repo:** github.com/willockrudi/jonas-productions
**Stack:** Pure static HTML/CSS/JS. No framework. No build step.
**Hosting:** GitHub Pages (free)

**6 pages:**
```
index.html     Home — hero, intro stats, services, touring artists, CTA
backline.html  Backline rentals — equipment categories + brand lists
audio.html     Audio equipment — PA, electronics, mics, wireless
clients.html   Client roster — all categories
about.html     Company history, touring contracts
contact.html   Contact info + contact form
```

**Design tokens:**
```css
--black:      #0a0a0a    /* page background */
--amber:      #f5a623    /* primary accent, buttons */
--white:      #f0ede8    /* warm white body text */
--muted:      #888       /* secondary text */
--font-display: 'Bebas Neue', sans-serif
--font-body:    'Barlow', sans-serif
```

**HTML injection markers** (manage.py writes between these):
```
<!-- BACKLINE_CATEGORIES_START/END -->
<!-- AUDIO_CATEGORIES_START/END -->
<!-- CLIENTS_START/END -->
<!-- TOURS_START/END -->
<!-- CONTACT_INFO_START/END -->
```

---

## MANAGE.PY — CURRENT CMS TOOL

**Two modes:**
```bash
python manage.py          # CLI interactive menu
python manage.py web-ui   # Admin panel at http://127.0.0.1:8082
```

**Data files it manages:**
```
data/backline.json    backline equipment categories + brand lists
data/audio.json       audio equipment categories + brand lists
data/clients.json     client categories + name lists
data/tours.json       touring artist partnerships
data/contact.json     contact info (address, phone, fax, email)
```

**What it does:**
- Edit all content sections via web forms or CLI prompts
- Rebuild all 6 HTML pages from JSON (inject between markers)
- Publish to GitHub Pages (git add -A → commit with message → push)
- Auto-backup before every change (.backups/ folder, timestamped)
- Restore from any previous backup
- First run seeds default data if JSON files don't exist

**Current web UI routes:**
```
GET  /              Dashboard — contact, tours, quick links
GET  /backline       Backline categories list + add form
GET  /audio          Audio categories list + add form
GET  /clients        Client categories list + add form
GET  /backline/edit  Edit one backline category
GET  /audio/edit     Edit one audio category
GET  /clients/edit   Edit one client category
GET  /tours/edit     Edit one touring artist
POST /rebuild        Rebuild all HTML pages
POST /publish        Git commit + push to GitHub
POST /contact/save   Save contact info + rebuild
POST /tours/add      Add touring artist + rebuild
POST /tours/save     Update touring artist + rebuild
POST /tours/delete   Delete touring artist + rebuild
POST /backline/add   Add backline category + rebuild
POST /backline/save  Update backline category + rebuild
POST /backline/delete Delete backline category + rebuild
POST /audio/*        Same CRUD for audio
POST /clients/*      Same CRUD for clients
```

---

## THE ELECTRON APP — WHAT WE'RE BUILDING

**The goal:** Take the manage.py web UI and package it as a native
macOS/Windows desktop app that Tom Jonas can double-click without
needing Python, Terminal, or a browser.

**Architecture:**
```
Electron main process (main.js)
  ↓ spawns
Python backend (manage.py → bundled via PyInstaller as manage_server)
  ↓ serves
Web UI at http://127.0.0.1:8082
  ↓ shown in
BrowserWindow (native app window)
```

**Repo structure:**
```
jonas-site-manager/      ← separate from the website repo
├── main.js
├── preload.js
├── renderer/loading.html
├── backend/manage.py    ← copy of the CMS
├── assets/icon.icns     ← Mac icon
├── package.json
└── requirements.txt
```

**Key package.json config:**
```json
{
  "name": "jonas-site-manager",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
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
    "mac": { "category": "public.app-category.business",
             "target": [{"target": "dmg", "arch": ["x64","arm64"]}] },
    "win": { "target": [{"target": "nsis", "arch": ["x64"]}] },
    "extraResources": [{"from": "backend/", "to": "backend"}]
  }
}
```

**main.js logic:**
1. Show loading.html splash screen
2. Spawn `backend/dist/manage_server web-ui` (production) or
   `python backend/manage.py web-ui` (dev)
3. Watch stdout for `"✅ Jonas Admin UI"` — server ready signal
4. Close splash, open BrowserWindow at http://127.0.0.1:8082
5. On window close: kill Python process, quit app

**Python bundling:**
```bash
cd backend
pip install pyinstaller colorama
pyinstaller --onefile manage.py --name manage_server
# Produces: backend/dist/manage_server (no Python install needed)
```

**Build output:**
```bash
npm run dist-mac   → dist/Jonas Site Manager-1.0.0.dmg
npm run dist-win   → dist/Jonas Site Manager Setup 1.0.0.exe
```

---

## WHAT NEEDS TO BE BUILT (in priority order)

```
1. Enhanced CLI (manage.py improvements)
   - colorama color output
   - New subcommands: status, rebuild, publish "msg", backup,
     restore, open, add-artist, add-brand, add-client, check
   - Confirmation prompts before delete
   - --dry-run flag
   - Progress output during publish

2. Web UI polish (manage.py web UI improvements)
   - Status bar: last published time + "unpublished changes" warning
   - Confirmation dialog before delete
   - Loading spinner on Publish button
   - Success/error toasts (replace ?msg= URL flash)
   - "Open site" button in header

3. Electron app
   - Set up project structure
   - Write main.js (spawn Python, open window, handle shutdown)
   - Write loading.html splash
   - Bundle Python with PyInstaller
   - Wire into electron-builder
   - npm run dist-mac → .dmg

4. Optional v1.1 features
   - Photo upload/gallery management
   - Formspree contact form integration
   - Custom domain setup wizard
   - Auto-update checker
```

---

## KNOWN ISSUES

```
1. Contact form uses mailto: — opens email client, doesn't work on mobile
   Fix: Formspree (free, sign up at formspree.io)

2. manage.py requires Python — won't run on Tom's Mac without install
   Fix: PyInstaller bundle inside Electron app

3. No confirmation before deleting items in web UI
   Fix: JavaScript confirm() or <dialog> modal

4. Publish button has no loading state (hangs silently 3-5 seconds)
   Fix: Disable button + show spinner + status bar message

5. First-run on new machine requires running manage.py once to seed data
   Fix: Already handled by init_data() — just verify it works cleanly
```

---

## PITCH SUMMARY (for new session context)

You're planning to demo this to Tom Jonas and propose:

**Option A:** One-time fee — hand over website + app, brief training
**Option B:** Monthly retainer — you maintain and update everything ongoing
**Option C:** Gift it free — use the goodwill to pitch Backline OS later

The demo order:
1. Show old jonasproductions.com side by side with new site
2. Click through all 6 pages of new site
3. Open admin panel — make live edit → show change on site
4. Click Publish → show it go live on the internet
5. Present the proposal PDF with your pricing

The website is not the endgame. It's the trust-builder for Backline OS.

---

## STARTING PROMPT FOR A NEW CLAUDE SESSION

Paste this document, then add one of these:

**For Electron app build:**
"I want to build the Electron wrapper for manage.py.
Here is the full project context above. Start with main.js."

**For CLI enhancements:**
"I want to enhance the manage.py CLI with color output and new subcommands.
Here is the full project context above.
Here is the current manage.py: [paste it]"

**For web UI polish:**
"I want to add a status bar, loading spinner, and confirmation dialogs
to the manage.py web UI (the HTML is embedded in the Python file).
Here is the full project context above.
Here is the current manage.py: [paste it]"

**For website changes:**
"I want to change [describe] on the Jonas Productions website.
Here is the full project context above.
Here is the current [page].html: [paste it]"
