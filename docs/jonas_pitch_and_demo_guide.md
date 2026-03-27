# JONAS PRODUCTIONS — PITCH & DEMO GUIDE
# Everything you need to walk into Jonas Productions and sell this.
# Written for Rudi Willock. Keep this private.

---

## THE SITUATION

You built Jonas Productions a new website and a management tool on your
own time. You want to sell it to Tom Jonas (the owner) and ideally get
paid to maintain it going forward.

You have two things to show him:
1. The new website — a massive upgrade over what they have now
2. The Site Manager app — lets anyone on their team update the site
   without touching code or calling you

The website does most of the selling just by existing. The old site
is dated, hard to navigate, and barely works on mobile. Your site is
sharp, professional, and loads instantly. The contrast is the pitch.

The app is the upsell — it means they're not dependent on you for
every single text change, which makes the arrangement sustainable.

---

## BEFORE THE MEETING — CHECKLIST

```
[ ] Run: python3 manage.py  (seed the data files if first run)
[ ] Click through all 6 pages in a browser — nothing broken
[ ] Run: python3 manage.py web-ui  → confirm admin opens at localhost:8082
[ ] Make one test edit in the admin, rebuild, verify change appears
[ ] Git push current state so the live demo URL is up to date
[ ] Have jonasproductions.com open in one tab (old site)
[ ] Have willockrudi.github.io/jonas-productions in another tab (new site)
[ ] Have localhost:8082 running in a third tab (admin panel)
[ ] Print one copy of the proposal PDF with your prices filled in
[ ] Bring your laptop charged — you need the demo to work on YOUR machine
[ ] Flash drive: put the HTML files on it (not manage.py — just site files)
    Tom can open index.html from the drive on ANY computer, no install needed
```

---

## THE DEMO SCRIPT

Keep it under 20 minutes. Tom is a busy guy.

### Opening (2 minutes)

Don't start with tech. Start with the problem.

"Tom, I noticed the Jonas website is still the same one from years ago.
It doesn't work great on phones, it's hard to find the contact info,
and honestly it doesn't look like what the company has become.
I rebuilt it from scratch on my own time — here's what I've got."

### The reveal (5 minutes)

Pull up the old site. Let it speak for itself. Then switch tabs.

"Same company, same content, same pages. Just built to actually work in 2026."

Click through slowly:
- Home: "Full-service audio and backline, all the touring partnerships
  right there on the front page."
- Backline: "Every category, every brand, easy to scan."
- Clients: "Presidential inaugurations, London Philharmonic, Late Night —
  this is the roster, laid out properly."
- About: "Company history, 1987, Indianapolis — all there."
- Contact: "One click to call from a phone."

Don't talk about code. Talk about what it does.

### The management tool (5 minutes)

"Here's the other thing I built. I didn't want Jonas to need a developer
every time the touring roster changes or you add a brand to the backline list."

Pull up localhost:8082.

"This is the management panel. Runs on any computer."

Demo live:
1. Edit a touring artist name — change "Harry Connick, Jr." → "Harry Connick Jr."
2. Click Save & Rebuild
3. Switch to the open browser tab showing the site — show the change appeared
4. Click "Publish to GitHub" — watch it go live
5. Open the live URL — change is there

"That's it. No code. No developer. Anyone on your team can do that."

### The ask (3 minutes)

"I'm looking to make this official. Two things I'd propose:

Option A — I hand it over, you own it. One-time fee, I'll set everything
up, show your team how to use it, and you're on your own.

Option B — I maintain it ongoing. Monthly retainer. You get my number,
I handle updates, fixes, and anything you want changed. You never touch it."

Then stop talking. Let him respond.

---

## PRICING OPTIONS

Fill in your own numbers. These are suggested ranges based on the work
involved and what small businesses typically pay for web services.

**Option A — One-time handover**
```
New website (6 pages, mobile responsive, live on GitHub Pages)   $XXX
Jonas Site Manager app (admin panel + publish tool)             $XXX
Setup + training (1 hour walkthrough at Jonas)                  $XXX
─────────────────────────────────────────────────────────────
Total one-time                                                  $XXX
```
Suggested range: $500–$1,200 total depending on your read of the room.

**Option B — Monthly retainer**
```
Initial setup (site live + app installed)     $XXX  (one-time)
Monthly management                            $XX/mo
  Includes: unlimited content updates, hosting management,
            new page or feature per quarter
```
Suggested range: $75–$200/month. Even $75/month is $900/year.

**Option C — Free gift + Backline OS pitch later**
Give them the website and app for free. No payment.
This is a long play — you gain enormous goodwill, Tom sees what you
can build, and in 3-6 months you pitch Backline OS properly.
The website is your proof of concept. The app is your trust builder.

**Which to choose:**
If you need the money now — Option A or B.
If you're thinking long game (Backline OS is worth tens of thousands
per year in subscription revenue) — Option C.
Don't be greedy on the website. The big money is Backline OS.

---

## OBJECTIONS AND ANSWERS

**"We already have a website."**
"You do, and it works. This is just a better one. Same address,
same content, loads faster on phones, looks more professional.
You don't have to do anything — I'll handle the switchover."

**"What does it cost to host?"**
"Nothing. GitHub Pages is free. That's where it's running right now.
Your domain (jonasproductions.com) just needs a simple DNS change —
I handle that. No hosting bill."

**"What if something breaks?"**
"That's why the retainer exists. But honestly it's static HTML —
there's nothing to break. It's as reliable as it gets on the web."

**"Do I need to learn anything technical?"**
"No. The app I built has one button that says Publish.
You make a change, click Publish, it's live. That's the whole thing."

**"Can we add more stuff later?"**
"Yes. That's what the monthly retainer covers — anything you want
changed or added, I handle it. New artist, new client category,
photos, whatever."

**"Why are you doing this?"**
Be honest: "I built this to learn and to have something real to show.
I want to do more work like this. Jonas is a good place to start —
I know the company, I know what you need, and I care about doing it right."

---

## AFTER THE MEETING

**If they say yes:**
```
[ ] Get payment/agreement in writing — even a simple email counts
[ ] DNS change: add CNAME record pointing jonasproductions.com → willockrudi.github.io
    (GitHub Pages custom domain — takes 24 hours to propagate)
[ ] Add CNAME file to repo: echo "jonasproductions.com" > CNAME && git push
[ ] Install the Site Manager app on Tom's or Karen's computer
    (whoever will manage content day-to-day)
[ ] 1-hour training session: show them the admin panel, make a change together
[ ] Hand over the printed quick-reference card (see tech spec)
[ ] Set up monthly retainer payment method if applicable
```

**If they say not yet:**
That's fine. Leave the proposal PDF.
Follow up in 2 weeks: "Just checking if you had any questions
about the site — happy to answer anything."
Don't push. Let the site speak for itself over time.

---

## THE STRATEGIC PICTURE

```
TODAY          Website + Site Manager app → establishes credibility
               Tom sees: "Rudi builds real things that work"

3-6 MONTHS     Backline OS pitch
               "Tom, I built your website. Now I've built something
               bigger — a production management system that replaces
               FileMaker. Jonas would be the first customer."
               Tom already trusts you. That trust is worth more than
               whatever you make on the website deal.

12 MONTHS      Jonas is on Backline OS
               Monthly subscription, you're managing their tech stack
               Other backline companies hear about it through Jonas
               Word of mouth in the touring industry starts working for you
```

The website deal is not the endgame. It's the opening move.
Do it well, do it right, and use it to get into the room for Backline OS.

---

## DEMO QUICK REFERENCE (keep on your phone)

```
Old site:    jonasproductions.com
New site:    willockrudi.github.io/jonas-productions
Admin panel: localhost:8082  (python3 manage.py web-ui)
GitHub repo: github.com/willockrudi/jonas-productions

Demo order:
1. Show old site → show new site (contrast sells itself)
2. Click through all 6 pages
3. Open admin panel → make a live edit → show it on site
4. Click Publish → show it go live
5. Discuss pricing options
6. Leave proposal PDF
```
