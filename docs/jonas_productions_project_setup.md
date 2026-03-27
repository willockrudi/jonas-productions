# JONAS PRODUCTIONS — WEBSITE & DESKTOP CMS
# Project setup instructions and full scope document.
# Hand this to a fresh Claude session to pick up exactly where we left off.
# Created by Rudi Willock — Jonas Productions, Fountaintown IN

---

## HOW TO START A NEW CLAUDE SESSION FOR THIS PROJECT

Paste this entire document into a new Claude.ai conversation as your
first message, then describe what you want to do. Claude will have
full context to continue without re-explanation.

Recommended opener after pasting:
> "I want to fine-tune the Jonas Productions website — [describe what
> you want to change]. Here is the current project context."

Or for the desktop app work:
> "I want to convert manage.py from a web UI / CLI tool into a native
> macOS desktop app Tom Jonas can double-click and use. Here is the
> project context."

---

## WHAT THIS PROJECT IS

You (Rudi Willock) built a complete modern website for Jonas Productions
and a content management tool (manage.py) that lets you update the site
and push changes to GitHub Pages without touching code.

The website is live at: **willockrudi.github.io/jonas-productions**
The GitHub repo is: **github.com/willockrudi/jonas-productions**

The goal is to:
1. Fine-tune the website until it is exactly right
2. Convert manage.py into a native macOS desktop app
3. Present the desktop app to Tom Jonas (the owner) as a tool he can
   use to manage his own website — and potentially sell him on it as
   a paid service

This is separate from the Backline OS project. Jonas Productions website
is a standalone deliverable.

---

## ABOUT JONAS PRODUCTIONS

```
Company:      Jonas Productions, Inc.
What they do: Full-service audio and backline rental company
              Specializing in turn-key entertainment and event production
              Professionally trained technicians accompany every rental
Founded:      1987  (Indianapolis, IN)
Location:     8606 N 700 West, Fountaintown, IN 46130
Phone:        317-835-7826
Fax:          317-835-2207
Email:        info@jonasproductions.com
Owner:        Tom Jonas (your boss)
```

**Long-term touring clients (since these years):**
- The Four Tops — 1988
- The Temptations — 1989
- The O'Jays — 1994
- Harry Connick Jr. — 1995
- Brian McKnight — 1998

**Notable past clients:**
Concert: Aerosmith, Tony Bennett, Boyz II Men, Jimmy Buffett,
         Julio Iglesias, Gerald Levert
Broadway: Julie Andrews, Barbara Eden, Don Knotts, Mandy Patinkin
Corps: American Express, Ford, Paine Webber, Procter & Gamble,
       Daimler-Chrysler, Philip Morris, NHRA
Political: President Bush Inauguration, President Clinton Inauguration,
           President Nixon Library Opening, President Reagan Speech
Symphony: Indianapolis Symphony, London Philharmonic, Paris Symphony,
          New York Philharmonic
Festivals: Cincinnati, Indianapolis, and New Orleans Jazz Festivals
TV/Film: ABC/Disney, NBC Today Show, Motown Live, Rosie O'Donnell,
         Tonight with Jay Leno, David Letterman
Religious: Assemblies of God, Promise Keepers, Pope John Paul II

---

## THE WEBSITE — CURRENT STATE

**Design:** Dark theme, amber accents, Bebas Neue display font,
Barlow body font. Feels professional, modern, concert-industry appropriate.

**Tech stack:** Pure static HTML/CSS/JS. No framework, no build step.
Hosted on GitHub Pages (free). Zero dependencies, loads instantly.

**Pages:**
```
index.html     Home — hero, intro stats, services overview, touring clients, CTA
backline.html  Backline rentals — equipment categories and brand lists
audio.html     Audio equipment — PA, electronics, mics, wireless
clients.html   Client roster — all client categories
about.html     Company story, stats, touring contracts
contact.html   Contact info, send message form
```

**Supporting files:**
```
style.css      Complete stylesheet — all 6 pages share this
nav.js         Mobile hamburger menu functionality
manage.py      CMS tool — web UI + CLI (see below)
data/          JSON files driving the CMS
  backline.json    backline equipment categories + brands
  audio.json       audio equipment categories + brands
  clients.json     client categories + names
  tours.json       touring artist partnerships
  contact.json     contact info
.backups/      Auto-created backup snapshots before any change
```

**HTML injection markers** (manage.py writes between these):
```html
<!-- BACKLINE_CATEGORIES_START --> ... <!-- BACKLINE_CATEGORIES_END -->
<!-- AUDIO_CATEGORIES_START -->   ... <!-- AUDIO_CATEGORIES_END -->
<!-- CLIENTS_START -->            ... <!-- CLIENTS_END -->
<!-- TOURS_START -->              ... <!-- TOURS_END -->
<!-- CONTACT_INFO_START -->       ... <!-- CONTACT_INFO_END -->
```

---

## MANAGE.PY — CURRENT STATE

**What it is:** A Python CMS that lets you update site content and
push to GitHub without touching any code. Built around a web UI served
locally at localhost:8082.

**Two modes:**
```bash
python manage.py          # Interactive CLI menu
python manage.py web-ui   # Opens browser admin at http://localhost:8082
```

**What it can do:**
- Edit contact info (address, phone, fax, email) — saves + rebuilds
- Add/edit/delete touring artists — saves + rebuilds
- Add/edit/delete backline equipment categories + brands — saves + rebuilds
- Add/edit/delete audio equipment categories + brands — saves + rebuilds
- Add/edit/delete client categories + names — saves + rebuilds
- Rebuild all pages from JSON data (inject content between HTML markers)
- Publish to GitHub Pages (git add -A → commit → push)
- Create automatic backups before every change
- Restore from any previous backup

**What it does NOT have yet:**
- Native macOS app (double-click to open — no Terminal needed)
- Photo/image upload for equipment or team pages
- Quote request form backend (contact form currently uses mailto:)
- Any server — it is fully local + static

---

## THE DESKTOP APP GOAL

Tom Jonas is not technical. He should be able to:
1. Double-click an icon on his Mac
2. See a window — no Terminal, no browser, no Python knowledge
3. Click buttons to update the website content
4. Click "Publish" and have it go live immediately

**The conversion path: manage.py → native macOS app**

**Option A — Tkinter GUI (simplest, Python built-in)**
- Replace the web UI with a Tkinter window
- Same functionality, native Mac look
- Single file, no extra installs
- Downside: looks dated, basic widgets

**Option B — PyQt6 or PySide6 (modern look, more work)**
- Native-style Mac UI with proper controls
- Tabs, styled buttons, clean layout
- Requires: `pip install PyQt6`
- Distribute with: pyinstaller → .app bundle
- This is the recommended path for selling to Tom

**Option C — PyWebView wrapper**
- Keep the existing manage.py web UI HTML
- Wrap it in a native window using pywebview
- Looks exactly like the current web UI
- No browser needed — opens as a standalone window
- Requires: `pip install pywebview`
- Easiest path — almost no rewrite needed

**Option D — Electron-style (overkill for this)**
- Not worth it for a single-user tool

**Recommended for selling to Tom: Option C (PyWebView)**
- Fastest to implement (manage.py web UI already looks good)
- Distribute as a .app with py2app or PyInstaller
- Tom double-clicks the app, window opens, done
- No browser, no Terminal, no Python installation visible

**How to package for Mac (.app bundle):**
```bash
# Install PyInstaller
pip install pyinstaller

# Create the .app
pyinstaller --windowed --onefile --name "Jonas Site Manager" manage.py

# The .app appears in dist/
# Copy to /Applications or give to Tom as a drag-to-install
```

---

## WHAT STILL NEEDS TO BE DONE

**Website fine-tuning (you drive this):**
```
[ ] Review all 6 pages and make any content/design tweaks
[ ] Add photos — equipment photos, venue photos, event photos
    (currently no images — placeholder sections could use them)
[ ] Update any content Tom wants changed
[ ] Add Google Analytics or simple tracking if desired
[ ] Improve the contact form (mailto: is basic — Formspree is free)
[ ] SEO meta tags — title, description, OG tags per page
[ ] Mobile responsiveness check on real phone
```

**Desktop app conversion:**
```
[ ] Choose approach (recommend PyWebView — see above)
[ ] Wrap manage.py web UI in pywebview window
[ ] Add auto-open browser behavior (currently user goes to localhost:8082)
[ ] Package as .app with PyInstaller
[ ] Test on a Mac without Python installed
[ ] Create simple installer instructions for Tom
[ ] Optional: add app icon (Jonas Productions logo or guitar icon)
```

**Selling it to Tom:**
```
[ ] Book a 20-minute demo at Jonas
[ ] Show the live site on jonasproductions.com side by side
    with willockrudi.github.io/jonas-productions
[ ] Open the .app on your laptop — show him how easy it is
[ ] Demo: update a touring artist name, click Publish, show it live
[ ] Pricing discussion (you built it on your own time)
    Options:
      - One-time setup fee ($300-500) + optional monthly retainer
      - One-time fee ($500-800) all in, no retainer
      - Free gift to build goodwill for Backline OS pitch
```

---

## HOW THE TWO PROJECTS CONNECT

This website project and Backline OS are separate products but connected
strategically:

```
Jonas Productions Website   →  Establishes your credibility as a developer
                               Shows Tom you build real, professional things
                               Opens the door to the Backline OS conversation

Backline OS                →  The bigger pitch — production management system
                               Monthly subscription software
                               Installed at Jonas as a pilot customer
                               Website is the warm-up act
```

The recommended order:
1. Deliver the website — either as a gift or for a small fee
2. Get Tom using the desktop CMS app — makes him feel the value
3. A few months later, pitch Backline OS
4. By then Tom has seen what you can build and trusts you

---

## REPOSITORY INFO

```
GitHub repo:   github.com/willockrudi/jonas-productions
GitHub Pages:  willockrudi.github.io/jonas-productions
Branch:        main (GitHub Pages deploys from main)

Clone command:
  git clone https://github.com/willockrudi/jonas-productions

Local dev:
  cd jonas-productions
  open index.html          # View site in browser
  python manage.py web-ui  # Open CMS at localhost:8082

Publish to live:
  python manage.py web-ui  → click "Publish to GitHub"
  OR: git add -A && git commit -m "update" && git push
```

---

## FILE STRUCTURE

```
jonas-productions/
├── index.html          Home page
├── backline.html       Backline equipment page
├── audio.html          Audio equipment page
├── clients.html        Clients page
├── about.html          About us page
├── contact.html        Contact page
├── style.css           Shared stylesheet
├── nav.js              Mobile nav script
├── manage.py           CMS tool (CLI + web UI)
├── data/
│   ├── backline.json   Backline equipment data
│   ├── audio.json      Audio equipment data
│   ├── clients.json    Client roster data
│   ├── tours.json      Touring partnerships data
│   └── contact.json    Contact info data
└── .backups/           Auto-backups (git-ignored)
    └── TIMESTAMP-label/
        ├── backline.json
        ├── audio.json
        └── meta.json
```

---

## PROMPTS TO USE IN A NEW CLAUDE SESSION

**For website design changes:**
```
I have the Jonas Productions website project. Here is the context:
[paste this document]

I want to [describe change — e.g. "add a photo gallery section to the
home page" or "redesign the services cards with a different layout" or
"improve the mobile view of the navigation"].

The current index.html looks like this: [paste current HTML]
```

**For the desktop app conversion:**
```
I have the Jonas Productions website manage.py CMS tool. Here is the
full project context:
[paste this document]

I want to convert manage.py into a native macOS desktop app using
PyWebView so Tom Jonas can double-click it without needing Terminal
or Python installed. The manage.py already has a web UI at localhost:8082
— I want to wrap that in a native window.

Here is the current manage.py: [paste manage.py]
```

**For adding features to manage.py:**
```
I have the Jonas Productions manage.py CMS. Here is the context:
[paste this document]

I want to add [feature — e.g. "the ability to upload a photo and
display it on the home page" or "a quote request form that sends
to Formspree instead of mailto"].
```

---

## KNOWN ISSUES / THINGS TO WATCH

```
Contact form: Currently uses <form action="mailto:..."> which opens the
  user's email client. This is unreliable on desktop and doesn't work at
  all on mobile. Replace with Formspree (free, easy, no backend needed):
  <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">

Photos: The current site has no images. This is intentional (clean/fast)
  but a real site benefits from at least one hero image or equipment photo.
  If adding images, use WebP format and keep them under 200KB each.

GitHub Pages URL: willockrudi.github.io/jonas-productions
  This is the demo URL. If Jonas wants jonasproductions.com to point here,
  it requires a DNS CNAME change at their domain registrar.
  GitHub Pages supports custom domains natively.

manage.py backup location: .backups/ is not in .gitignore by default.
  Add it to avoid committing backups to GitHub.
  echo ".backups/" >> .gitignore

PyInstaller on Mac: The packaged .app must be built on a Mac to run on a Mac.
  Cannot cross-compile from Windows/Linux.
  You need to run PyInstaller on your Mac to create the .app.
```

---

## MANAGE.PY QUICK REFERENCE

```bash
# Start the web admin UI
python manage.py web-ui
# Opens at http://127.0.0.1:8082

# Start interactive CLI
python manage.py

# CLI menu options:
1  Open web UI
2  Rebuild all HTML pages from JSON
3  Edit contact info
4  Manage touring artists
5  Publish to GitHub Pages
6  List and restore backups
q  Quit

# Manual publish (if manage.py isn't available)
git add -A
git commit -m "site update"
git push origin main
```

---

## DESIGN TOKENS (for consistency in any new Claude session)

```css
--black:      #0a0a0a    /* page background */
--off-black:  #111       /* alternate background */
--panel:      #161616    /* card backgrounds */
--border:     #2a2a2a    /* borders */
--amber:      #f5a623    /* primary accent / CTA buttons */
--amber-dim:  #c4821a    /* hover state on amber */
--white:      #f0ede8    /* body text (warm white, not pure white) */
--muted:      #888       /* secondary text, labels */

--font-display: 'Bebas Neue', sans-serif    /* headings */
--font-body:    'Barlow', sans-serif        /* body text */

/* Standard button */
.btn-primary { background: #f5a623; color: #0a0a0a; font-weight: 600; }
.btn-secondary { border: 1px solid #f5a623; color: #f5a623; }
```
