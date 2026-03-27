# Jonas Productions — Complete Claude Instruction Set
### Every prompt, every phase, A to Z
*For Rudi Willock — private document*

---

## HOW TO USE THIS DOCUMENT

Every section below is a self-contained Claude session prompt. Start a new Claude session, paste the MASTER CONTEXT block first, then paste the phase prompt for whatever you are working on. Claude will have everything it needs to complete that phase without re-explanation.

Do the phases in order. Do not skip phases. Each phase builds on the last.

When a prompt says [paste X here], you paste that file's full contents inline before sending.

---

---

# MASTER CONTEXT BLOCK
### Paste this at the top of EVERY new Claude session before anything else.

---

You are helping Rudi Willock complete and sell a website and desktop CMS app to Ted Jonas, owner of Jonas Productions, Inc. Read this entire context before doing anything.

## The project

Rudi built a complete new website for Jonas Productions on his own time and a Python CMS tool called manage.py that manages the site content and publishes to GitHub Pages. He is presenting both to Ted Jonas this week as a package deal. The goal is to get paid, lock in a retainer, and eventually pitch Backline OS.

## The people

- Rudi Willock: bench tech and lead tech at Jonas Productions. Built everything. Presenting this week.
- Ted Jonas: the owner. Moderate tech. Mac only. Old school production specialist, been in the industry since 1987. Will not respond to developer talk. Will respond to things that work and look professional.
- Karen: office and logistics. Will be the day-to-day site editor once Ted buys in.

## The website

Live URL: willockrudi.github.io/jonas-productions
GitHub repo: github.com/willockrudi/jonas-productions
Stack: pure static HTML, CSS, JavaScript. No framework. No build step. No dependencies.
Hosting: GitHub Pages, free.

Six pages: index.html, backline.html, audio.html, clients.html, about.html, contact.html.
Shared files: style.css, nav.js.
CMS data files: data/backline.json, data/audio.json, data/clients.json, data/tours.json, data/contact.json.
CMS tool: manage.py — runs as python manage.py (CLI) or python manage.py web-ui (browser admin at localhost:8082).

## The brand rules — NON-NEGOTIABLE

Jonas Productions brand DNA: black backgrounds, red as the primary color, white text, bold italic display type.

The current site uses warm amber/gold tokens. These must be replaced with red. That is the ONLY color change. Do not change anything else about the CSS.

Color token replacements:
- --gold becomes #cc2200
- --gold-lt becomes #e8321a
- --gold-dim becomes #992200
- --amber becomes #cc2200
- --amber-dim becomes #7a1a00

Everything else in style.css stays exactly as-is. Do not change fonts. Do not change layout. Do not change spacing. Do not change any token that is not a gold or amber value. Do not touch JavaScript. Do not touch HTML structure. Color tokens only.

Logo: text only. "Jonas Productions" — same treatment already in the site. No logo mark.

No Las Vegas office. Ted confirmed it no longer exists. Do not add it anywhere.

## The CMS — how it works

manage.py reads JSON data files and injects HTML content between marker comments in the HTML pages.

Markers:
- BACKLINE_CATEGORIES_START and BACKLINE_CATEGORIES_END in backline.html
- AUDIO_CATEGORIES_START and AUDIO_CATEGORIES_END in audio.html
- CLIENTS_START and CLIENTS_END in clients.html
- TOURS_START and TOURS_END in about.html
- CONTACT_INFO_START and CONTACT_INFO_END in contact.html

When content is saved in the admin, manage.py rewrites the HTML between those markers and optionally runs git add -A, git commit, git push to publish to GitHub Pages.

## Critical rules for every session

1. Never change fonts, layout, spacing, or JavaScript.
2. Never change HTML structure — only content inside marker blocks or adding new marker blocks.
3. Never add a Las Vegas office.
4. Never change the CSS cascade or architecture — only token values.
5. When editing manage.py, do not break existing functionality. Add to it, do not replace it.
6. All new manage.py web UI HTML must use the Jonas brand: red/black/white, same font stack as the public site (Playfair Display, Crimson Pro, Barlow Condensed from Google Fonts).
7. Output complete files when asked. Do not abbreviate with comments like "rest of file unchanged."

---

---

# PHASE 00 — Color Rebrand
### Goal: Swap amber/gold tokens to red in style.css. One file. Nothing else.
### Estimated time: 1 hour

---

## Phase 00-A — Do the color swap

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need you to do the Jonas Productions color token swap on style.css. This is the only thing we are doing in this session.

Rules:
- Replace every instance of the gold and amber CSS variable values with the red equivalents listed below
- Do not change variable names
- Do not change any other values in the file
- Do not change anything else — not fonts, not spacing, not layout, not any other colors
- Output the complete updated style.css with no abbreviations

Token replacements to make:
- Wherever you see the current gold value replace it with #cc2200
- Wherever you see the current gold-lt value replace it with #e8321a
- Wherever you see the current gold-dim value replace it with #992200
- Wherever you see the current amber value replace it with #cc2200
- Wherever you see the current amber-dim value replace it with #7a1a00
- Any other warm orange or amber hex values in the root token block get replaced with the nearest red equivalent

After the swap, verify: every mention of gold or amber in the :root block should now be a red value. No warm yellows or oranges should remain in the token definitions.

Current style.css:
[paste style.css here]

---

## Phase 00-B — Verify the swap

After applying the new style.css, open each of the six pages in a browser and check that all of these are now red and not amber or gold:

Nav link hover color. Active nav link. CTA button background. Hero rule line. Section eyebrow lines and their decorative bars. Card top border accents. Footer gradient lines. Form input focus border. Touring act "Since" year labels. All btn-primary buttons.

If anything is still amber or gold, paste that specific CSS rule back to Claude and say: "This element is still showing amber/gold. Fix it using the Jonas red token."

## Phase 00-C — Commit

```
cd /path/to/jonas-productions
git add style.css
git commit -m "rebrand: swap amber/gold tokens to Jonas red"
git push origin main
```

Open willockrudi.github.io/jonas-productions and confirm the live site is now red.

---

---

# PHASE 01 — Website Content Fixes
### Goal: Fix every content gap, add SEO, fix the contact form, update copy.
### Estimated time: 2-3 hours

---

## Phase 01-A — SEO meta tags on all six pages

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add SEO meta tags to all six pages of the Jonas Productions website. Add to the head section of each page, after the viewport meta tag and before the font link. Do not change anything else on any page. Output each complete updated file with no abbreviations.

Add these exact meta tags to index.html:

```html
<meta name="description" content="Jonas Productions — full-service audio and backline rental company. Turn-key event production staffed by degreed professionals. Serving artists and corporations since 1987. Indianapolis, Indiana.">
<meta property="og:title" content="Jonas Productions — Audio and Backline Rentals Since 1987">
<meta property="og:description" content="Full-service audio and backline rental. Professionally trained technicians accompany every rental. Indianapolis, Indiana.">
<meta property="og:url" content="https://jonasproductions.com/">
<meta property="og:type" content="website">
```

Add these to backline.html:

```html
<meta name="description" content="Jonas Productions backline rental inventory — keyboards, drum kits, guitar and bass amplifiers, organs, percussion, symphonic instruments. Top brands, maintained to spec.">
<meta property="og:title" content="Backline Rentals — Jonas Productions">
<meta property="og:description" content="Full backline rental inventory including Yamaha, Roland, Ampeg, Fender, Ludwig, DW, Hammond, and more. Professionally staffed.">
<meta property="og:url" content="https://jonasproductions.com/backline.html">
<meta property="og:type" content="website">
```

Add these to audio.html:

```html
<meta name="description" content="Jonas Productions professional audio equipment rental — PA systems, microphones, wireless in-ear monitors, electronics. EAW, JBL, Meyer, Shure, Sennheiser, Midas, and more.">
<meta property="og:title" content="Audio Equipment — Jonas Productions">
<meta property="og:description" content="Professional audio rental including PA cabinets, microphones, wireless systems, and professional electronics from the world's leading manufacturers.">
<meta property="og:url" content="https://jonasproductions.com/audio.html">
<meta property="og:type" content="website">
```

Add these to clients.html:

```html
<meta name="description" content="Jonas Productions client roster — Presidential inaugurations, Aerosmith, Tony Bennett, London Philharmonic, ABC/Disney, NBC Today Show, and hundreds more.">
<meta property="og:title" content="Clients — Jonas Productions">
<meta property="og:description" content="From Presidential inaugurations to Broadway stages, Fortune 500 corporations to world symphony orchestras — Jonas Productions has served them all.">
<meta property="og:url" content="https://jonasproductions.com/clients.html">
<meta property="og:type" content="website">
```

Add these to about.html:

```html
<meta name="description" content="About Jonas Productions — full-service audio and backline rental since 1987. Long-term touring partnerships with The Four Tops, The Temptations, Harry Connick Jr., The O'Jays, and Brian McKnight.">
<meta property="og:title" content="About Us — Jonas Productions">
<meta property="og:description" content="A rapidly growing corporate and concert service company providing the highest quality audio and backline equipment since 1987. Indianapolis headquartered, nationwide reach.">
<meta property="og:url" content="https://jonasproductions.com/about.html">
<meta property="og:type" content="website">
```

Add these to contact.html:

```html
<meta name="description" content="Contact Jonas Productions — 317-835-7826 — 8606 N 700 West, Fountaintown IN 46130. Call anytime for audio and backline rental inquiries.">
<meta property="og:title" content="Contact — Jonas Productions">
<meta property="og:description" content="Call our Indianapolis office anytime — 317-835-7826. Our friendly, knowledgeable team is ready to help with your event production needs.">
<meta property="og:url" content="https://jonasproductions.com/contact.html">
<meta property="og:type" content="website">
```

Current files:
[paste all six HTML files here, one after another]

---

## Phase 01-B — Fix the contact form

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to replace the mailto: contact form action in contact.html with Formspree.

Change only the form action and method. Do not change form fields, labels, layout, or styling. Do not change anything else on the page. Output the complete updated contact.html.

Change this line:
```html
<form class="contact-form" action="mailto:info@jonasproductions.com" method="post" enctype="text/plain">
```

To this:
```html
<form class="contact-form" action="https://formspree.io/f/FORM_ID_HERE" method="POST">
```

Also add this as the first element inside the form, right after the opening form tag:
```html
<input type="hidden" name="_subject" value="New inquiry from jonasproductions.com">
```

Flag clearly in your response where I need to insert the actual Formspree form ID. I will sign up at formspree.io and replace FORM_ID_HERE with my real endpoint.

Current contact.html:
[paste contact.html here]

---

## Phase 01-C — Update about page for international reach

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to update one paragraph in the about-text section of about.html.

Do not change layout, structure, fonts, or styling. Do not change the touring artists list. Only update the paragraph described below. Output the complete updated about.html.

Find this paragraph: "With Indianapolis as our corporate headquarters, we ensure cost effective coverage anywhere in North America."

Replace it with: "With Indianapolis as our corporate headquarters, we ensure cost-effective coverage anywhere in North America — and beyond. Our technicians have traveled with productions to Canada, Australia, Europe, and Asia, delivering the same standard of excellence regardless of location."

Current about.html:
[paste about.html here]

---

## Phase 01-D — Update copyright and footer tagline on all six pages

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to make two small changes to the footer of all six HTML pages. Only change the footer-bottom section. Do not change anything else on any page. Output all six complete updated files.

Change 1: In every page's footer-bottom div, change "2024 Jonas Productions" to "2025 Jonas Productions."

Change 2: In every page's footer-bottom div, the existing footer text currently ends with a period or with the rights reserved line. After that text, add this on a new line inside the same paragraph or as a second paragraph within footer-bottom: "For all your production needs, contact us anytime — 317-835-7826"

Current files:
[paste all six HTML files here]

---

## Phase 01-E — Add manufacturer brand strip to backline and audio pages

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add a manufacturer credibility strip to backline.html and audio.html. This is a section showing "Brands We Carry" as a flex row of styled brand name badges.

Rules:
- Use only existing CSS variables from style.css — do not add a new stylesheet
- Match the dark card aesthetic of the rest of the site exactly
- Insert the new section between the page-hero closing tag and the equip-page opening tag
- Do not change the existing equip-grid or any existing content
- Brand names should appear as small uppercase pill badges with a subtle border, using the muted color palette — not loud or colorful
- The section heading "Brands We Carry" should use the section-eyebrow style
- Output complete updated files for both pages

Brands for backline.html: Yamaha, Roland, Korg, Hammond, Fender, Ampeg, Mesa Boogie, Ludwig, Drum Workshop, Pearl, Zildjian, Paiste, Kurzweil, Ensoniq, Wurlitzer, Vox, Matchless, Fender Rhodes, Akai, Alesis, Gretch, Hartke, SWR, David Eden, Gallien-Krueger, Latin Percussion, Sabian, Hughes and Kettner

Brands for audio.html: EAW, JBL, Meyer, Shure, Sennheiser, AKG, Midas, Yamaha, Lexicon, Klark-Teknik, TC Electronics, Audio-Technica, Neumann, Brooke Siren, EV, Barcus-Berry, Beyer-Dynamic, C-Ducer, Samson

Current files:
[paste backline.html and audio.html here]

---

## Phase 01-F — Commit all Phase 01 changes

```
cd /path/to/jonas-productions
git add -A
git commit -m "phase 01: SEO tags, Formspree form, copy updates, brand strips, footer tagline, copyright 2025"
git push origin main
```

Verify on the live site: page titles in the browser tab should now be descriptive, the contact form should submit without opening an email client, the brand strips should appear on backline and audio pages, and the footer should show the Jonas tagline.

---

---

# PHASE 02 — Admin UI Polish
### Goal: The manage.py admin panel looks and feels like Jonas Productions.
### Estimated time: 2-3 hours

---

## Phase 02-A — Rebrand the admin UI

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to rebrand the embedded web UI inside manage.py. The admin panel at localhost:8082 currently uses a generic dark gray theme with a maroon topbar. It needs to look like Jonas Productions — red, black, white — matching the public site's brand exactly.

Rules:
- Do not break any existing functionality
- Do not change any route logic, data handling, form processing, or Python business logic
- Only change the _layout() function's embedded CSS and the topbar HTML within it
- Output the complete updated manage.py with no abbreviations

Make these specific changes inside the _layout() function:

Add a Google Fonts link in the head for: Playfair Display (weights 700 and 900, including italic), Crimson Pro (weights 300 and 400), Barlow Condensed (weights 600 and 700).

Replace the entire embedded style block with a new one using these values:
- Page background: #0a0a0a
- Card background: #111111
- Card border: 1px solid #1e1e1e
- Topbar background: #0d0000
- Topbar border-bottom: 2px solid #cc2200
- Primary accent (buttons, links, card headings): #cc2200
- Primary accent hover: #e8321a
- Muted accent: #992200
- Body text: #f0e8d8
- Muted text: #888888
- Input background: #0d0d0d
- Input border: 1px solid #2a2a2a
- Input focus border: #cc2200
- Display font: Playfair Display, serif
- Body font: Crimson Pro, serif
- Label and button font: Barlow Condensed, sans-serif
- Button text: uppercase, letter-spacing 0.12em
- Success message background: #0d1a0d, border: 1px solid #1a3a1a, text: #88cc88
- Delete button: background #3a0000, text #ffaaaa, hover background #550000

Update the topbar HTML to:
- Show the title as "Jonas Productions — Site Manager" in Playfair Display italic
- Include a "View Live Site" link that opens willockrudi.github.io/jonas-productions in a new tab, styled in the muted red color
- Include the existing "Dashboard" back link

Current manage.py:
[paste manage.py here]

---

## Phase 02-B — Add status bar

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add a status bar to the manage.py admin UI. It appears at the bottom of every admin page and shows when the site was last published and whether there are unpublished changes.

Rules:
- Do not break any existing functionality
- Add a helper function called get_site_status() that returns last published time and whether changes are pending
- Add the status bar HTML to the _layout() function so it appears on every page automatically
- Output the complete updated manage.py with no abbreviations

The get_site_status() function should:
- Run git log -1 --format="%ci" in the ROOT directory to get the last commit timestamp
- Compare the modification time of each file in data/ against that timestamp
- Return a dict with: last_published as a human-readable string like "Tuesday March 25, 2025 at 2:47 pm", and has_changes as a boolean

Handle edge cases: if git is not available return "Never published" and has_changes as True. If there are no commits yet return "Never published."

The status bar HTML should:
- Appear at the bottom of the page inside the wrap div, always
- Show "Last published: [datetime]" in muted text using Barlow Condensed
- Show a yellow warning badge "Unpublished changes" if has_changes is True
- Show a small green "Up to date" badge if has_changes is False
- Use the Jonas brand colors — dark background, subtle top border in the muted red

Current manage.py (already updated with Phase 02-A changes):
[paste updated manage.py here]

---

## Phase 02-C — Add confirmation dialogs before all deletes

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add JavaScript confirmation dialogs to every delete button in the manage.py admin UI. Currently clicking delete removes items immediately with no warning.

Rules:
- Do not change any server-side logic at all
- Add onclick handlers to delete buttons that call confirm() and return false if the user cancels
- Include the item name in the confirmation message
- Do not change anything else
- Output the complete updated manage.py with no abbreviations

For touring artist deletes the message should be: "Delete [artist name] from touring contracts? This cannot be undone."
For backline category deletes: "Delete [category name] from backline equipment? This cannot be undone."
For audio category deletes: "Delete [category name] from audio equipment? This cannot be undone."
For client category deletes: "Delete [category name] from client roster? This cannot be undone."

The item name is rendered server-side into the list HTML. Pass it as a properly escaped JavaScript string in the onclick attribute of the delete button.

Current manage.py (already updated with Phase 02-A and 02-B changes):
[paste updated manage.py here]

---

## Phase 02-D — Add publish spinner and toast notifications

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add two UI improvements to the manage.py admin:

First, a loading spinner on the Publish button. When any form that posts to /publish is submitted, the button should immediately show "Publishing..." and be disabled to prevent double-submits. Add a simple CSS animation — either animated dots or a rotating character.

Second, toast notifications. The current system reloads the page with a ?msg= URL parameter that flashes briefly. Keep the server-side ?msg= system intact but intercept it client-side: on page load, read the msg parameter from the URL, display it as a toast notification in the bottom-right corner, remove the parameter from the URL without reloading, and auto-dismiss the toast after 4 seconds with a fade-out animation.

Toast styling must match the Jonas brand:
- Position fixed, bottom-right, 20px from each edge
- Background #1a1a1a
- Border 1px solid #cc2200
- Text #f0ede8 in Barlow Condensed
- Border-radius 4px
- Padding 12px 20px
- Fade in on appear, fade out over 0.5 seconds before removal
- Z-index 9999

Add all JavaScript to the _layout() function's embedded script block. Do not change any server-side logic. Output the complete updated manage.py with no abbreviations.

Current manage.py (already updated with Phase 02-A, 02-B, and 02-C changes):
[paste updated manage.py here]

---

## Phase 02-E — Test checklist

Run: python manage.py web-ui

Open http://localhost:8082 and confirm all of the following:

The header background is very dark red-black with a bright red bottom border. The title reads "Jonas Productions — Site Manager" in italic serif font. The "View Live Site" link is visible in the header. All buttons use Barlow Condensed font and are uppercase. All inputs have dark backgrounds and turn red on focus. The status bar appears at the bottom of every page. The status bar correctly shows published or unpublished state. Delete buttons trigger a confirmation dialog showing the item name. The Publish button shows a spinner and disables when clicked. Success and error messages appear as toasts in the bottom-right corner and fade away after 4 seconds.

If anything looks wrong, paste the broken element's HTML and a description of the problem to Claude. Do not attempt to fix CSS issues by guessing.

---

---

# PHASE 03 — Desktop App Packaging
### Goal: A double-click Mac app. No terminal, no browser, no Python visible.
### Estimated time: 2 hours

---

## Phase 03-A — Build the PyWebView launcher

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to create app.py — a PyWebView launcher that wraps the manage.py web UI in a native Mac window. This file lives in the same directory as manage.py.

Rules:
- Do not modify manage.py at all
- app.py starts the manage.py web server in a background thread, waits until it is ready, then opens a pywebview window
- Window title: "Jonas Site Manager"
- Window loads http://localhost:8082
- If port 8082 is busy, try 8083 then 8084 automatically
- When the window closes, the server shuts down cleanly — no orphan processes
- Show a simple loading page in the window while the server is starting: dark background matching the Jonas brand, text "Starting Jonas Site Manager..." in red and white, no external dependencies
- Must work when run as: python app.py
- Must also work when bundled by PyInstaller — detect sys.frozen and adjust resource paths accordingly

Write the complete app.py.

Also write a requirements.txt file listing all Python dependencies: pywebview and any other packages manage.py depends on.

---

## Phase 03-B — Build script and instructions

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need two files to package the Jonas Site Manager as a Mac app using PyInstaller.

File 1: build_mac.sh

This shell script should:
1. Check that pip, pyinstaller, and pywebview are installed — install them if not
2. Remove previous dist/ and build/ directories to start clean
3. Run PyInstaller with: --windowed flag so no terminal appears, --onedir for reliability with pywebview, --name "Jonas Site Manager", --add-data flags to include all HTML files, CSS files, JS files, and the entire data directory, --icon assets/icon.icns only if that file exists (skip silently if it does not)
4. Copy the resulting .app from dist/ to the user's Desktop
5. Print a clear success message showing the path to the .app

File 2: BUILD_INSTRUCTIONS.md

Plain English instructions covering:
- Prerequisites: what needs to be installed first and the exact commands
- How to run the build: exact command
- How to test the .app before giving it to Ted
- How Ted installs it: drag to Applications folder
- Common Mac issues and how to fix them: Gatekeeper blocking unknown developers, pywebview blank window on first launch, port already in use errors

Write both files completely.

---

## Phase 03-C — Demo decision

For the in-person demo this week, you do not need the packaged .app to be ready. You can show the admin panel running at localhost:8082 in a browser window and say: "This ships as a double-click Mac app that Ted installs like any other application. I will hand that over when we finalize the agreement."

The .app is what you deliver after Ted says yes. Build and test it on your machine before handoff, not before the demo.

---

---

# PHASE 04 — The Demo
### Goal: Walk in, show it, let the contrast do the selling.

---

## Phase 04-A — Pre-demo checklist

Do all of these the morning of the meeting:

```
[ ] git pull on your demo machine — confirm live site is current
[ ] python manage.py web-ui — confirm admin opens at localhost:8082
[ ] Make one test edit, rebuild, confirm the change appears in the browser tab
[ ] Open willockrudi.github.io/jonas-productions — confirm it is live and red
[ ] Have jonasproductions.com open in a separate browser tab
[ ] Have localhost:8082 already open and logged in as a third tab
[ ] Confirm the Formspree form ID is inserted in contact.html
[ ] Laptop charged, power cable in bag as backup
[ ] Know the two pricing options you are going to propose — have numbers decided
```

---

## Phase 04-B — The demo script

Keep it under 20 minutes.

Opening — 2 minutes. Do not start with technology. Start with the problem.

"Ted, I have been looking at the Jonas website. It is not broken, but it does not show what this company actually is. Presidential inaugurations. Four Tops since 1988. London Philharmonic. That company does not have a website that matches it. I rebuilt it from scratch on my own time. Here is what I've got."

The reveal — 5 minutes. Pull up jonasproductions.com first. Let it sit. Do not say anything negative. Let him see it. Then switch to your site.

"Same company. Same content. Same history. Just built for 2025."

Click through slowly. Talk about what people see, not how it was built.

Home — "Touring partnerships right there on the front page. Four Tops, Temptations, Connick, O'Jays, McKnight."
Backline — "Every category, every brand, readable on any phone."
Clients — "Presidential inaugurations, London Philharmonic, Letterman, Today Show. This is the roster laid out like it deserves to be."
About — "1987. Indianapolis. The whole story."
Contact — "One tap to call from a phone."

The admin demo — 5 minutes. Open localhost:8082.

"Here is the other thing I built. Because I did not want Jonas to have to call a developer every time the touring roster changes."

Do these steps live in this exact order:
1. Show the dashboard. Point to the status bar.
2. Find Harry Connick Jr. in touring contracts. Click Edit.
3. Change something small — add or remove a period. Click Save and Rebuild.
4. Switch to the browser tab with the public site. Refresh.
5. Point to the change. "It updated."
6. Click Publish to GitHub.
7. Open the live URL. "And now it is live on the internet."
8. Point to the status bar showing the new publish time.

The ask — 3 minutes.

"I want to make this official. Two options.

Option A: one-time fee. You own the site, I set everything up, one session with you or Karen showing how to use it, and you are good.

Option B: monthly retainer. You get my number. Any time you want something changed or added, I handle it. The site stays current and grows with the business."

Stop talking. Let him respond first. Do not fill the silence.

---

## Phase 04-C — Objection responses

"We already have a website."
"You do. This is just a better one. Same address, same content, loads on phones, looks like what Jonas Productions actually is today. I handle the switchover."

"What does hosting cost?"
"Nothing. GitHub Pages is free. That is where it is running right now. Your domain needs one DNS change — I do that."

"What if something breaks?"
"That is what the retainer is for. But this is static HTML — there is genuinely nothing to break. It is as reliable as the web gets."

"Do I have to learn anything technical?"
"No. There is one button that says Publish. You make a change, you click it, it is live. That is the whole thing."

"Why did you build this?"
"Because I work here and I want Jonas to look like what it is. And I want to do more of this work. Jonas is a good place to start."

---

---

# PHASE 05 — Post-Sale: Domain and Google
### Do this once Ted says yes. One afternoon.

---

## Phase 05-A — Connect jonasproductions.com to GitHub Pages

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

Write step-by-step plain English instructions for connecting the jonasproductions.com domain to the Jonas Productions GitHub Pages site at willockrudi.github.io/jonas-productions.

Write it as if explaining to someone who has never touched DNS settings before. No jargon. Number every step. Cover:

1. How to find out who holds the domain registration using a WhoIs lookup tool
2. Exactly what DNS records to create at the registrar — the specific GitHub Pages IP addresses for A records or the CNAME approach
3. How to create the CNAME file in the GitHub repo with the exact content it needs
4. How to set the custom domain in GitHub Pages repository settings
5. What the 24 to 48 hour propagation period means and how to check progress
6. How to confirm it is working once propagation completes
7. How GitHub Pages handles HTTPS automatically and what to click to enable it

---

## Phase 05-B — Claim and update the Google Business listing

Once jonasproductions.com is live:

Go to business.google.com. Search for Jonas Productions. The listing already exists — claim it using the phone verification or postcard option. Once claimed, update these fields:

Website URL: jonasproductions.com
Business description: "Full-service audio and backline rental company. Turn-key entertainment and event production. Professionally trained technicians accompany every rental. Serving artists, corporations, and events since 1987. Indianapolis, Indiana."
Phone: 317-835-7826
Address: 8606 N 700 West, Fountaintown IN 46130

Add photos once Ted provides real event photography. A claimed and complete Google Business listing is the single highest-return free SEO action available for a local business.

---

---

# PHASE 06 — Post-Sale Month One: Feature Expansion
### Everything you promised. Now you build it.

---

## Phase 06-A — Add photo gallery to the site and CMS

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add a managed photo gallery to the Jonas Productions website. This is a two-part build.

Part 1 — HTML and CSS:
- Add a new section to clients.html between the equip-page section and the cta-banner section
- Add injection markers: GALLERY_START and GALLERY_END
- The gallery section uses the existing dark card style and CSS variables — do not add a new stylesheet
- Gallery items are images with optional captions displayed in a responsive grid
- Images fill their grid cells using object-fit cover
- Match the visual style of the existing equip-grid sections exactly
- Output complete updated clients.html and any additions to style.css

Part 2 — CMS management in manage.py:
- Add data/gallery.json structure: array of objects, each with url, caption, and alt fields
- Add a default_gallery() function returning an empty array
- Add a GET /gallery route showing the gallery list and an upload form
- Add a POST /gallery/add route that accepts an image file upload, saves it to an images/ folder, creates a web-optimized copy using Pillow (max 1200px wide, 85% JPEG quality), and adds the entry to gallery.json
- Add a POST /gallery/delete route
- Add a gallery_html() function that generates the injected HTML
- Integrate gallery into rebuild_all() so it rebuilds with everything else
- Output complete updated manage.py with no abbreviations

Current files:
[paste clients.html, style.css, manage.py]

---

## Phase 06-B — Add staff bios section

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add a staff bios section to about.html managed through manage.py.

Rules:
- Add a new section to about.html below the about-grid section and above the cta-banner
- Add injection markers: STAFF_START and STAFF_END
- If no staff entries exist in the data, the section renders nothing — it is invisible until populated
- Staff cards show: name, title, optional short bio of two to three sentences, optional headshot photo
- Style matches the existing about page — dark cards, red accents, Playfair Display for names
- Add staff management to manage.py: data/staff.json, GET /staff route, POST /staff/add, POST /staff/save, POST /staff/delete, photo upload using Pillow same as gallery
- Output complete updated about.html, any style.css additions, and full manage.py

Current files:
[paste about.html, style.css, manage.py]

---

## Phase 06-C — Add SEO field management to admin

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add SEO field management to the manage.py admin panel so Ted or Karen can edit page titles and meta descriptions without touching HTML.

Rules:
- Add data/seo.json with entries for each of the six pages — each entry has a title and description field
- Seed seo.json with the values added in Phase 01-A as the defaults
- Add SEO injection markers to every HTML page: SEO_TITLE_START and SEO_TITLE_END around the title tag content, SEO_DESCRIPTION_START and SEO_DESCRIPTION_END around the meta description content tag
- Add a GET /seo admin route showing all six pages with editable title and description fields
- Add a POST /seo/save route that saves to seo.json and rebuilds all pages
- Add a link to the SEO section from the admin dashboard
- The rebuild injects the correct values into every page's markers
- Output complete updated manage.py and all six HTML files with the new markers added

Current files:
[paste manage.py and all six HTML files]

---

## Phase 06-D — Add activity log

New Claude session. Paste MASTER CONTEXT. Then paste this:

---

I need to add an activity log to the manage.py admin panel. Every save, delete, rebuild, and publish action gets logged with a timestamp and a human-readable description.

Rules:
- Log to data/activity.json as an array of entries, each with a timestamp and an action string
- Cap at 100 entries — trim the oldest when over the limit
- Add a GET /activity route that displays the log as a full-page card in the admin
- Add a link from the dashboard to the activity log
- Log every POST action server-side after it succeeds: describe what changed, when, and whether it succeeded or failed
- Format entries in plain English: "Touring artist updated: Harry Connick Jr. — Tuesday March 25, 2025 at 2:47 pm"
- Output complete updated manage.py with no abbreviations

Current manage.py:
[paste manage.py]

---

---

# PHASE 07 — The Backline OS Conversation
### Three to six months after Ted buys in. Do not rush this.

---

## When to bring it up

Wait until Ted has had the site running on his domain for at least a month. Wait until Karen or Ted has used the admin panel without issues multiple times. Wait until Ted says something that signals he sees you as someone who builds things that work — not just a tech fixing gear.

The moment is usually when he mentions a pain point. Scheduling. Rider matching. Tracking what gear is out and when it comes back. Quote generation. Anything where he describes a problem that sounds like a software problem.

That is when you say: "Ted, I have been working on something bigger. Can I show you something next week?"

## The framing

Do not open with the product. Open with the problem he just described.

"Right now when a promoter calls and wants to know if you have a specific console available for their dates, what does that look like? Someone checks a spreadsheet? Calls the shop?"

Let him answer.

"What I have been building is a system that handles that. Availability tracking, rider matching, quote generation, client history — all in one place. The same way the site manager handles the website. I want Jonas to be the first company running it."

## What this moment means

The website and the site manager were never the product. They were the proof. By the time you have the Backline OS conversation, Ted has watched you build something real, deliver it on time, and keep it running without drama. That is worth more than any demo.

The website pitch opens the door. Backline OS is what you walk through it to get to.

---

---

# QUICK REFERENCE — Fix-It Prompts

Use these in a new session when something specific needs fixing.

---

## Fix a broken page element

MASTER CONTEXT: [paste context]

The [element name] on [page].html is displaying incorrectly. [Describe the problem]. Here is the relevant HTML section: [paste it]. Fix only this element. Do not change anything else. Output the complete updated file.

## Fix a manage.py error

MASTER CONTEXT: [paste context]

manage.py is throwing this error when I [describe what triggered it]: [paste full error traceback]. Here is the current manage.py: [paste file]. Fix only this bug. Do not change any other functionality. Output the complete updated manage.py.

## Add a touring artist manually

MASTER CONTEXT: [paste context]

Add [artist name], touring since [year], to data/tours.json. Then show me the updated JSON and the rebuilt HTML that would be injected between the TOURS_START and TOURS_END markers in about.html.

## Update contact information

MASTER CONTEXT: [paste context]

Update data/contact.json with these new values: [list each field and new value]. Show me the updated JSON and the resulting HTML that would be injected between the CONTACT_INFO markers in contact.html.

## Debug a CSS issue

MASTER CONTEXT: [paste context]

The [element description] is showing the wrong [color / size / layout] on [page name or admin]. It should look like [describe correct appearance]. Here is the relevant CSS: [paste]. Here is the HTML: [paste]. Fix only this specific issue. Output only the changed CSS rules, not the whole file.

## Add a brand to an equipment category

MASTER CONTEXT: [paste context]

Add [brand name] to the [category name] category in data/[backline or audio].json. Show me the updated JSON entry and confirm it will render correctly in the rebuilt HTML.

---

---

# APPENDIX — Project Reference

## File structure

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
├── manage.py
├── app.py                  created in Phase 03
├── build_mac.sh            created in Phase 03
├── requirements.txt        created in Phase 03
├── data/
│   ├── backline.json
│   ├── audio.json
│   ├── clients.json
│   ├── tours.json
│   ├── contact.json
│   ├── gallery.json        created in Phase 06-A
│   ├── staff.json          created in Phase 06-B
│   ├── seo.json            created in Phase 06-C
│   └── activity.json       created in Phase 06-D
├── images/                 created in Phase 06-A
└── .backups/
```

## All HTML injection markers

```
backline.html     BACKLINE_CATEGORIES_START / BACKLINE_CATEGORIES_END
audio.html        AUDIO_CATEGORIES_START / AUDIO_CATEGORIES_END
clients.html      CLIENTS_START / CLIENTS_END
clients.html      GALLERY_START / GALLERY_END           Phase 06-A
about.html        TOURS_START / TOURS_END
about.html        STAFF_START / STAFF_END               Phase 06-B
contact.html      CONTACT_INFO_START / CONTACT_INFO_END
all six pages     SEO_TITLE_START / SEO_TITLE_END       Phase 06-C
all six pages     SEO_DESCRIPTION_START / SEO_DESCRIPTION_END
```

## Final CSS color tokens after Phase 00

```
--ink:        #0a0a0a     page background, unchanged
--deep:       #221a12     alternate background, unchanged
--warm:       #2e2318     section backgrounds, unchanged
--panel:      #352a1c     card backgrounds, unchanged
--border:     #4a3a26     borders, unchanged
--border-lt:  #6b5438     light borders, unchanged
--gold:       #cc2200     PRIMARY RED, was amber
--gold-lt:    #e8321a     BRIGHT RED, was amber light
--gold-dim:   #992200     DEEP RED, was amber dim
--cream:      #f0e8d8     body text, unchanged
--cream-dim:  #c8b99a     secondary text, unchanged
--muted:      #8a7560     muted text, unchanged
```

## Key URLs and accounts

```
GitHub repo:        github.com/willockrudi/jonas-productions
Live demo URL:      willockrudi.github.io/jonas-productions
Target domain:      jonasproductions.com
Admin panel URL:    http://localhost:8082
Run admin:          python manage.py web-ui
Formspree:          formspree.io — sign up, create form, copy the endpoint ID
Google Business:    business.google.com — claim Jonas Productions listing
Jonas phone:        317-835-7826
Jonas email:        info@jonasproductions.com
Jonas address:      8606 N 700 West, Fountaintown IN 46130
```

---

*End of document.*
*Phase 00 through Phase 07. Every prompt. A to Z.*
*Rudi Willock — Jonas Productions — private.*
