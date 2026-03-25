"""
Jonas Productions — Site Manager
=================================
Manages content for the Jonas Productions website via a local web UI.
Run:  python manage.py          (interactive CLI)
      python manage.py web-ui   (browser admin panel at localhost:8082)
"""

import json
import os
import re
import shutil
import html
import subprocess
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))

# HTML page paths
INDEX_PATH        = os.path.join(ROOT, "index.html")
BACKLINE_PATH     = os.path.join(ROOT, "backline.html")
AUDIO_PATH        = os.path.join(ROOT, "audio.html")
CLIENTS_PATH      = os.path.join(ROOT, "clients.html")
ABOUT_PATH        = os.path.join(ROOT, "about.html")
CONTACT_PATH      = os.path.join(ROOT, "contact.html")

# Templates (copies of originals with markers, never overwritten)
BACKLINE_TPL  = os.path.join(ROOT, "templates", "backline_template.html")
AUDIO_TPL     = os.path.join(ROOT, "templates", "audio_template.html")
CLIENTS_TPL   = os.path.join(ROOT, "templates", "clients_template.html")
ABOUT_TPL     = os.path.join(ROOT, "templates", "about_template.html")
CONTACT_TPL   = os.path.join(ROOT, "templates", "contact_template.html")

# Data files
DATA_PATH     = os.path.join(ROOT, "data", "backline.json")
AUDIO_DATA    = os.path.join(ROOT, "data", "audio.json")
CLIENTS_DATA  = os.path.join(ROOT, "data", "clients.json")
TOURS_DATA    = os.path.join(ROOT, "data", "tours.json")
CONTACT_DATA  = os.path.join(ROOT, "data", "contact.json")

BACKUPS_DIR   = os.path.join(ROOT, ".backups")

# Injection markers — these exist in the template HTML files
MARKERS = {
    "backline":  ("<!-- BACKLINE_CATEGORIES_START -->",  "<!-- BACKLINE_CATEGORIES_END -->"),
    "audio":     ("<!-- AUDIO_CATEGORIES_START -->",      "<!-- AUDIO_CATEGORIES_END -->"),
    "clients":   ("<!-- CLIENTS_START -->",               "<!-- CLIENTS_END -->"),
    "tours":     ("<!-- TOURS_START -->",                 "<!-- TOURS_END -->"),
    "contact":   ("<!-- CONTACT_INFO_START -->",          "<!-- CONTACT_INFO_END -->"),
}


# ── Data IO ──────────────────────────────────────────────────────────────────

def _load_json(path: str, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠  JSON error in {os.path.basename(path)}")
        return default

def _save_json(path: str, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def load_backline():
    return _load_json(DATA_PATH, _default_backline())

def load_audio():
    return _load_json(AUDIO_DATA, _default_audio())

def load_clients():
    return _load_json(CLIENTS_DATA, _default_clients())

def load_tours():
    return _load_json(TOURS_DATA, _default_tours())

def load_contact():
    return _load_json(CONTACT_DATA, _default_contact())

def save_backline(data):  _save_json(DATA_PATH,    data)
def save_audio(data):     _save_json(AUDIO_DATA,   data)
def save_clients(data):   _save_json(CLIENTS_DATA, data)
def save_tours(data):     _save_json(TOURS_DATA,   data)
def save_contact(data):   _save_json(CONTACT_DATA, data)


# ── Defaults (seed from current site content) ────────────────────────────────

def _default_backline():
    return [
        {"category": "Keyboards & Synthesizers",  "brands": ["Ensoniq","Korg","Kurzweil","Roland","Yamaha"]},
        {"category": "Organs & Electric Pianos",  "brands": ["Fender Rhodes","Hammond","Leslie","Wurlitzer"]},
        {"category": "Samplers & Sequencers",     "brands": ["Akai","Alesis","Roland"]},
        {"category": "Drum Kits",                 "brands": ["Drum Workshop","Ludwig","Yamaha","Gretch","Pearl"]},
        {"category": "Guitar Amplifiers",         "brands": ["Ampeg","Fender","Line 6","Mesa Boogie","Peavey","Roland","Matchless","Trace Elliot","Vox"]},
        {"category": "Bass Amplifiers",           "brands": ["Ampeg","David Eden","Gallien-Krueger","Hartke","Hughes & Kettner","SWR"]},
        {"category": "Percussion & Cymbals",      "brands": ["Latin Percussion","Sabian","Paiste","Zildjian"]},
        {"category": "Symphonic & Orchestra",     "brands": ["Gongs","Vibes","Tympani","Xylophone","Wenger Orchestra Chairs","Music Stands & Lights"]},
    ]

def _default_audio():
    return [
        {"category": "P.A. Cabinets",                  "brands": ["EAW","JBL","Meyer"]},
        {"category": "Electronics",                     "brands": ["Brooke Siren","Klark-Teknik","Lexicon","Midas","TC Electronics","Yamaha"]},
        {"category": "Microphones",                     "brands": ["AKG","Audio-Technica","Barcus-Berry","Beyer-Dynamic","C-Ducer","EV","Neuman","Sennheiser","Shure"]},
        {"category": "Wireless Mics & In-Ear Monitors", "brands": ["Audio-Technica","Sennheiser","Samson","Shure"]},
    ]

def _default_clients():
    return [
        {"category": "Concert Artists",    "names": ["Aerosmith","Tony Bennett","Boyz II Men","Jimmy Buffett","Julio Iglesias","Gerald Levert"]},
        {"category": "Broadway Artists",   "names": ["Julie Andrews","Barbara Eden","Don Knotts","Mandy Patinkin"]},
        {"category": "Corporations",       "names": ["American Express","Ford","Paine Webber","Proctor & Gamble","Daimler-Chrysler","Philip Morris","Izusu","NHRA"]},
        {"category": "Political Events",   "names": ["President Bush Inauguration","President Clinton Inauguration","President Nixon Library Opening","President Reagan Speech"]},
        {"category": "Symphony Orchestras","names": ["Indianapolis Symphony Orch.","London Philharmonic","Paris Symphony","New York Philharmonic"]},
        {"category": "Festivals",          "names": ["Cincinnati Jazz Festival","Indianapolis Jazz Festival","New Orleans Jazz Festival"]},
        {"category": "TV & Film",          "names": ["ABC / Disney","NBC Today Show","Motown Live","Rosie O'Donnell","Tonight w/ Jay Leno","David Letterman"]},
        {"category": "Religious Events",   "names": ["Assemblies of God","Azusa Fellowship","Nazarene Quadrenium Conf.","Promise Keepers","Pope John Paul II"]},
    ]

def _default_tours():
    return [
        {"artist": "The Four Tops",    "since": "1988"},
        {"artist": "The Temptations",  "since": "1989"},
        {"artist": "Harry Connick, Jr.","since": "1995"},
        {"artist": "The O'Jays",       "since": "1994"},
        {"artist": "Brian McKnight",   "since": "1998"},
    ]

def _default_contact():
    return {
        "address": "8606 N 700 West\nFountaintown, IN 46130",
        "phone":   "317-835-7826",
        "fax":     "317-835-2207",
        "email":   "info@jonasproductions.com",
    }


# ── HTML generators ──────────────────────────────────────────────────────────

def _e(s):
    return html.escape(str(s), quote=True)

def backline_html(categories: list) -> str:
    blocks = []
    for cat in categories:
        items = "\n".join(f"          <li>{_e(b)}</li>" for b in cat.get("brands", []))
        blocks.append(f"""
      <div class="equip-category">
        <h3>{_e(cat['category'])}</h3>
        <ul>
{items}
        </ul>
      </div>""")
    return '\n    <div class="equip-grid">' + "".join(blocks) + '\n    </div>\n    '

def audio_html(categories: list) -> str:
    return backline_html(categories)  # same structure

def clients_html(categories: list) -> str:
    blocks = []
    for cat in categories:
        key = "names" if "names" in cat else "brands"
        items = "\n".join(f"          <li>{_e(n)}</li>" for n in cat.get(key, []))
        blocks.append(f"""
      <div class="client-category">
        <h3>{_e(cat['category'])}</h3>
        <ul>
{items}
        </ul>
      </div>""")
    return '\n    <div class="clients-grid">' + "".join(blocks) + '\n    </div>\n    '

def tours_html(tours: list) -> str:
    lines = []
    for t in tours:
        lines.append(f"""      <div class="tour-item">
        <span>{_e(t['artist'])}</span>
        <em>Since {_e(t['since'])}</em>
      </div>""")
    return "\n" + "\n".join(lines) + "\n      "

def contact_html(info: dict) -> str:
    addr = _e(info.get("address", "")).replace("\n", "<br>")
    phone = _e(info.get("phone", ""))
    phone_raw = info.get("phone", "").replace("-", "")
    fax   = _e(info.get("fax", ""))
    email = _e(info.get("email", ""))
    return f"""
      <div class="contact-card">
        <h4>Indianapolis Office</h4>
        <p>{addr}</p>
        <a href="tel:{phone_raw}" class="big-phone">{phone}</a>
        <p style="margin-top:0.5rem;">Fax: {fax}</p>
      </div>

      <div class="contact-card">
        <h4>Email</h4>
        <p><a href="mailto:{email}">{email}</a></p>
      </div>
      """


# ── Rebuild engine ────────────────────────────────────────────────────────────

def _inject(html_path: str, marker_key: str, new_content: str):
    start_marker, end_marker = MARKERS[marker_key]
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    if start_marker not in content or end_marker not in content:
        print(f"⚠  Markers for '{marker_key}' not found in {os.path.basename(html_path)}")
        return
    s = content.index(start_marker) + len(start_marker)
    e = content.index(end_marker)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content[:s] + "\n" + new_content + content[e:])

def rebuild_all():
    _inject(BACKLINE_PATH, "backline", backline_html(load_backline()))
    _inject(AUDIO_PATH,    "audio",    audio_html(load_audio()))
    _inject(CLIENTS_PATH,  "clients",  clients_html(load_clients()))
    _inject(ABOUT_PATH,    "tours",    tours_html(load_tours()))
    _inject(CONTACT_PATH,  "contact",  contact_html(load_contact()))
    print("✅ Site rebuilt.")


# ── Backup ────────────────────────────────────────────────────────────────────

def create_backup(label: str) -> str:
    os.makedirs(BACKUPS_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d-%H%M%S")
    name = f"{ts}-{label[:30].replace(' ','-')}"
    path = os.path.join(BACKUPS_DIR, name)
    os.makedirs(path, exist_ok=True)
    for src in [DATA_PATH, AUDIO_DATA, CLIENTS_DATA, TOURS_DATA, CONTACT_DATA]:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(path, os.path.basename(src)))
    _save_json(os.path.join(path, "meta.json"), {"label": label, "created": datetime.now().isoformat()})
    return name

def list_backups():
    if not os.path.isdir(BACKUPS_DIR): return []
    names = sorted([n for n in os.listdir(BACKUPS_DIR) if os.path.isdir(os.path.join(BACKUPS_DIR, n))], reverse=True)
    return names

def restore_backup(name: str) -> bool:
    path = os.path.join(BACKUPS_DIR, name)
    if not os.path.isdir(path): return False
    for dst in [DATA_PATH, AUDIO_DATA, CLIENTS_DATA, TOURS_DATA, CONTACT_DATA]:
        src = os.path.join(path, os.path.basename(dst))
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    return True


# ── Git publish ───────────────────────────────────────────────────────────────

def run_git(args):
    try:
        p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except FileNotFoundError:
        return 127, "", "git not found"

def publish_github(msg=None):
    rc, remote, _ = run_git(["remote","get-url","origin"])
    if rc != 0: return False, "No git remote 'origin' configured."
    rc, branch, _ = run_git(["rev-parse","--abbrev-ref","HEAD"])
    if rc != 0: return False, "Could not detect git branch."
    message = msg or f"site update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    run_git(["add","-A"])
    run_git(["commit","-m", message])
    rc, out, err = run_git(["push","origin", branch])
    if rc != 0: return False, f"Push failed: {err or out}"
    return True, f"Published to GitHub ({branch})."


# ── Web UI ────────────────────────────────────────────────────────────────────

def _layout(title: str, body: str, msg: str = "") -> str:
    msg_html = f'<p class="msg">{html.escape(msg)}</p>' if msg else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)} — Jonas Admin</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:system-ui,sans-serif;background:#111;color:#eee;min-height:100vh}}
    .topbar{{background:#1c0000;border-bottom:2px solid #c8181c;padding:12px 24px;display:flex;align-items:center;gap:16px}}
    .topbar h1{{font-size:1.1rem;color:#fff;letter-spacing:.05em}}
    .topbar a{{font-size:.8rem;color:#f0a500;text-decoration:none}}
    .topbar a:hover{{color:#fff}}
    .wrap{{max-width:1100px;margin:0 auto;padding:24px}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px}}
    .card{{background:#1c1c1c;border:1px solid #2e2e2e;border-radius:6px;padding:20px}}
    .card h2{{font-size:1rem;margin-bottom:14px;color:#f0a500;letter-spacing:.05em;text-transform:uppercase}}
    .card h3{{font-size:.85rem;margin:12px 0 8px;color:#ccc}}
    label{{display:block;font-size:.75rem;color:#888;margin:10px 0 4px;text-transform:uppercase;letter-spacing:.08em}}
    input,textarea,select{{width:100%;padding:8px 10px;background:#111;border:1px solid #333;border-radius:4px;color:#eee;font-size:.9rem}}
    textarea{{min-height:80px;resize:vertical}}
    button{{margin-top:10px;padding:9px 14px;border:none;border-radius:4px;cursor:pointer;font-size:.85rem;font-weight:600}}
    .btn-red{{background:#c8181c;color:#fff}}
    .btn-red:hover{{background:#e8272b}}
    .btn-grey{{background:#333;color:#eee}}
    .btn-grey:hover{{background:#444}}
    .btn-del{{background:#5c0000;color:#faa}}
    .btn-del:hover{{background:#800}}
    .msg{{background:#1a3a1a;border:1px solid #2a5a2a;padding:10px 14px;border-radius:4px;margin-bottom:16px;font-size:.9rem;color:#8f8}}
    .row{{display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start}}
    .row form{{margin:0}}
    ul.item-list{{list-style:none;margin:8px 0}}
    ul.item-list li{{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #252525;font-size:.88rem}}
    ul.item-list li:last-child{{border:none}}
    .muted{{color:#666;font-size:.8rem}}
    a.back{{color:#f0a500;font-size:.85rem;display:inline-block;margin-bottom:16px}}
  </style>
</head>
<body>
  <div class="topbar">
    <h1>Jonas Productions — Admin</h1>
    <a href="/">← Dashboard</a>
  </div>
  <div class="wrap">
    {msg_html}
    {body}
  </div>
</body>
</html>"""


def start_web_ui(host="127.0.0.1", port=8082):

    def parse_form(handler):
        length = int(handler.headers.get("Content-Length", "0") or "0")
        raw = handler.rfile.read(length).decode("utf-8") if length > 0 else ""
        parsed = parse_qs(raw, keep_blank_values=True)
        return {k: (v[0] if v else "") for k, v in parsed.items()}

    class Handler(BaseHTTPRequestHandler):
        def _html(self, content, status=200):
            data = content.encode()
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _redir(self, path, msg=""):
            target = f"{path}{'&' if '?' in path else '?'}msg={msg}" if msg else path
            self.send_response(303)
            self.send_header("Location", target)
            self.end_headers()

        # ── Dashboard ──
        def _home(self, msg=""):
            tours   = load_tours()
            contact = load_contact()
            bl      = load_backline()
            au      = load_audio()
            cl      = load_clients()

            bl_summary  = ", ".join(c["category"] for c in bl[:4]) + "..."
            au_summary  = ", ".join(c["category"] for c in au[:3]) + "..."
            cl_summary  = ", ".join(c["category"] for c in cl[:4]) + "..."
            tour_items  = "".join(f"<li><strong>{_e(t['artist'])}</strong> <span class='muted'>since {_e(t['since'])}</span> "
                                  f"<a href='/tours/edit?idx={i}' style='color:#f0a500;margin-left:8px;font-size:.8rem;'>Edit</a>"
                                  f"<form method='post' action='/tours/delete' style='display:inline'>"
                                  f"<input type='hidden' name='idx' value='{i}'>"
                                  f"<button class='btn-del' style='margin:0 0 0 6px;padding:2px 8px;font-size:.75rem'>✕</button></form></li>"
                                  for i, t in enumerate(tours))

            body = f"""
<div class="grid">
  <div class="card">
    <h2>Site Actions</h2>
    <div class="row">
      <form method="post" action="/rebuild"><button class="btn-red">Rebuild All Pages</button></form>
      <form method="post" action="/publish">
        <input name="msg" placeholder="Commit message (optional)" style="width:220px">
        <button class="btn-grey">Publish to GitHub</button>
      </form>
    </div>
  </div>

  <div class="card">
    <h2>Contact Info</h2>
    <form method="post" action="/contact/save">
      <label>Address</label>
      <textarea name="address" rows="2">{_e(contact.get('address',''))}</textarea>
      <label>Phone</label>
      <input name="phone" value="{_e(contact.get('phone',''))}">
      <label>Fax</label>
      <input name="fax" value="{_e(contact.get('fax',''))}">
      <label>Email</label>
      <input name="email" value="{_e(contact.get('email',''))}">
      <button class="btn-red">Save &amp; Rebuild</button>
    </form>
  </div>

  <div class="card">
    <h2>Touring Contracts</h2>
    <ul class="item-list">{tour_items or '<li class="muted">No entries.</li>'}</ul>
    <form method="post" action="/tours/add" style="margin-top:12px">
      <label>Artist Name</label>
      <input name="artist" required placeholder="e.g. Diana Ross">
      <label>Since Year</label>
      <input name="since" required placeholder="e.g. 2001">
      <button class="btn-red">Add Artist</button>
    </form>
  </div>

  <div class="card">
    <h2>Backline Categories</h2>
    <p class="muted" style="margin-bottom:8px">{_e(bl_summary)}</p>
    <a href="/backline" style="color:#f0a500;font-size:.85rem">Manage Backline Equipment →</a>
  </div>

  <div class="card">
    <h2>Audio Categories</h2>
    <p class="muted" style="margin-bottom:8px">{_e(au_summary)}</p>
    <a href="/audio" style="color:#f0a500;font-size:.85rem">Manage Audio Equipment →</a>
  </div>

  <div class="card">
    <h2>Client Roster</h2>
    <p class="muted" style="margin-bottom:8px">{_e(cl_summary)}</p>
    <a href="/clients" style="color:#f0a500;font-size:.85rem">Manage Clients →</a>
  </div>
</div>"""
            self._html(_layout("Dashboard", body, msg))

        # ── Equipment list page ──
        def _equip_page(self, kind, msg=""):
            data   = load_backline() if kind == "backline" else load_audio()
            title  = "Backline" if kind == "backline" else "Audio"
            cats   = "".join(
                f"<li><strong>{_e(c['category'])}</strong> "
                f"<span class='muted'>({len(c.get('brands',[]))} brands)</span> "
                f"<a href='/{kind}/edit?idx={i}' style='color:#f0a500;margin-left:8px;font-size:.8rem'>Edit</a>"
                f"<form method='post' action='/{kind}/delete' style='display:inline'>"
                f"<input type='hidden' name='idx' value='{i}'>"
                f"<button class='btn-del' style='margin:0 0 0 6px;padding:2px 8px;font-size:.75rem'>✕</button></form></li>"
                for i, c in enumerate(data))
            body = f"""
<a class="back" href="/">← Dashboard</a>
<div class="card">
  <h2>{title} Categories</h2>
  <ul class="item-list">{cats or '<li class="muted">None.</li>'}</ul>
  <form method="post" action="/{kind}/add" style="margin-top:16px">
    <label>New Category Name</label>
    <input name="category" required>
    <label>Brands (one per line)</label>
    <textarea name="brands"></textarea>
    <button class="btn-red">Add Category</button>
  </form>
</div>"""
            self._html(_layout(title, body, msg))

        def _equip_edit(self, kind, idx, msg=""):
            data = load_backline() if kind == "backline" else load_audio()
            if idx < 0 or idx >= len(data): self._redir(f"/{kind}", "Invalid."); return
            c = data[idx]
            body = f"""
<a class="back" href="/{kind}">← Back</a>
<div class="card">
  <h2>Edit Category</h2>
  <form method="post" action="/{kind}/save">
    <input type="hidden" name="idx" value="{idx}">
    <label>Category Name</label>
    <input name="category" value="{_e(c['category'])}" required>
    <label>Brands (one per line)</label>
    <textarea name="brands" rows="10">{_e(chr(10).join(c.get('brands',[])))}</textarea>
    <button class="btn-red">Save</button>
  </form>
</div>"""
            self._html(_layout("Edit", body, msg))

        def _clients_page(self, msg=""):
            data = load_clients()
            cats = "".join(
                f"<li><strong>{_e(c['category'])}</strong> "
                f"<span class='muted'>({len(c.get('names', c.get('brands',[])))} entries)</span> "
                f"<a href='/clients/edit?idx={i}' style='color:#f0a500;margin-left:8px;font-size:.8rem'>Edit</a>"
                f"<form method='post' action='/clients/delete' style='display:inline'>"
                f"<input type='hidden' name='idx' value='{i}'>"
                f"<button class='btn-del' style='margin:0 0 0 6px;padding:2px 8px;font-size:.75rem'>✕</button></form></li>"
                for i, c in enumerate(data))
            body = f"""
<a class="back" href="/">← Dashboard</a>
<div class="card">
  <h2>Client Categories</h2>
  <ul class="item-list">{cats or '<li class="muted">None.</li>'}</ul>
  <form method="post" action="/clients/add" style="margin-top:16px">
    <label>New Category Name</label>
    <input name="category" required>
    <label>Names (one per line)</label>
    <textarea name="names"></textarea>
    <button class="btn-red">Add Category</button>
  </form>
</div>"""
            self._html(_layout("Clients", body, msg))

        def _clients_edit(self, idx, msg=""):
            data = load_clients()
            if idx < 0 or idx >= len(data): self._redir("/clients", "Invalid."); return
            c = data[idx]
            key = "names" if "names" in c else "brands"
            body = f"""
<a class="back" href="/clients">← Back</a>
<div class="card">
  <h2>Edit Client Category</h2>
  <form method="post" action="/clients/save">
    <input type="hidden" name="idx" value="{idx}">
    <label>Category Name</label>
    <input name="category" value="{_e(c['category'])}" required>
    <label>Names (one per line)</label>
    <textarea name="names" rows="10">{_e(chr(10).join(c.get(key,[])))}</textarea>
    <button class="btn-red">Save</button>
  </form>
</div>"""
            self._html(_layout("Edit Clients", body, msg))

        # ── Routing ──
        def do_GET(self):
            p = urlparse(self.path)
            q = parse_qs(p.query)
            msg = (q.get("msg") or [""])[0]

            routes = {
                "/":               lambda: self._home(msg),
                "/backline":       lambda: self._equip_page("backline", msg),
                "/audio":          lambda: self._equip_page("audio", msg),
                "/clients":        lambda: self._clients_page(msg),
            }
            if p.path in routes:
                routes[p.path](); return

            def _idx(total):
                raw = (q.get("idx") or ["-1"])[0]
                i = int(raw) if raw.lstrip("-").isdigit() else -1
                return i if 0 <= i < total else -1

            if p.path in ("/backline/edit", "/audio/edit"):
                kind = "backline" if "backline" in p.path else "audio"
                data = load_backline() if kind == "backline" else load_audio()
                self._equip_edit(kind, _idx(len(data)), msg); return

            if p.path == "/clients/edit":
                self._clients_edit(_idx(len(load_clients())), msg); return

            if p.path == "/tours/edit":
                tours = load_tours()
                idx = _idx(len(tours))
                if idx < 0: self._redir("/", "Invalid"); return
                t = tours[idx]
                body = f"""<a class="back" href="/">← Dashboard</a>
<div class="card"><h2>Edit Touring Artist</h2>
<form method="post" action="/tours/save">
  <input type="hidden" name="idx" value="{idx}">
  <label>Artist</label><input name="artist" value="{_e(t['artist'])}" required>
  <label>Since Year</label><input name="since" value="{_e(t['since'])}" required>
  <button class="btn-red">Save</button>
</form></div>"""
                self._html(_layout("Edit Artist", body, msg)); return

            self._html(_layout("404", "<div class='card'><h2>Not Found</h2></div>"), 404)

        def do_POST(self):
            form = parse_form(self)
            path = urlparse(self.path).path

            def _idx(data):
                raw = form.get("idx", "-1")
                i = int(raw) if raw.lstrip("-").isdigit() else -1
                return i if 0 <= i < len(data) else -1

            def _lines(key): return [l.strip() for l in form.get(key,"").splitlines() if l.strip()]

            if path == "/rebuild":
                rebuild_all(); self._redir("/", "Rebuilt site pages."); return

            if path == "/publish":
                ok, msg = publish_github(form.get("msg","").strip() or None)
                self._redir("/", msg); return

            if path == "/contact/save":
                create_backup("contact-save")
                save_contact({
                    "address": form.get("address",""),
                    "phone":   form.get("phone",""),
                    "fax":     form.get("fax",""),
                    "email":   form.get("email",""),
                })
                rebuild_all(); self._redir("/", "Saved contact info."); return

            # ── Tours
            if path == "/tours/add":
                create_backup("tours-add")
                tours = load_tours()
                tours.append({"artist": form.get("artist",""), "since": form.get("since","")})
                save_tours(tours); rebuild_all(); self._redir("/", "Added touring artist."); return

            if path == "/tours/save":
                tours = load_tours(); idx = _idx(tours)
                if idx < 0: self._redir("/", "Invalid."); return
                create_backup("tours-save")
                tours[idx] = {"artist": form.get("artist",""), "since": form.get("since","")}
                save_tours(tours); rebuild_all(); self._redir("/", "Saved."); return

            if path == "/tours/delete":
                tours = load_tours(); idx = _idx(tours)
                if idx < 0: self._redir("/", "Invalid."); return
                create_backup("tours-delete")
                tours.pop(idx); save_tours(tours); rebuild_all()
                self._redir("/", "Deleted."); return

            # ── Backline / Audio (shared logic)
            for kind in ("backline", "audio"):
                loader = load_backline if kind == "backline" else load_audio
                saver  = save_backline if kind == "backline" else save_audio

                if path == f"/{kind}/add":
                    create_backup(f"{kind}-add")
                    data = loader()
                    data.append({"category": form.get("category",""), "brands": _lines("brands")})
                    saver(data); rebuild_all(); self._redir(f"/{kind}", "Added."); return

                if path == f"/{kind}/save":
                    data = loader(); idx = _idx(data)
                    if idx < 0: self._redir(f"/{kind}", "Invalid."); return
                    create_backup(f"{kind}-save")
                    data[idx] = {"category": form.get("category",""), "brands": _lines("brands")}
                    saver(data); rebuild_all(); self._redir(f"/{kind}", "Saved."); return

                if path == f"/{kind}/delete":
                    data = loader(); idx = _idx(data)
                    if idx < 0: self._redir(f"/{kind}", "Invalid."); return
                    create_backup(f"{kind}-delete")
                    data.pop(idx); saver(data); rebuild_all()
                    self._redir(f"/{kind}", "Deleted."); return

            # ── Clients
            if path == "/clients/add":
                create_backup("clients-add")
                data = load_clients()
                data.append({"category": form.get("category",""), "names": _lines("names")})
                save_clients(data); rebuild_all(); self._redir("/clients", "Added."); return

            if path == "/clients/save":
                data = load_clients(); idx = _idx(data)
                if idx < 0: self._redir("/clients", "Invalid."); return
                create_backup("clients-save")
                data[idx] = {"category": form.get("category",""), "names": _lines("names")}
                save_clients(data); rebuild_all(); self._redir("/clients", "Saved."); return

            if path == "/clients/delete":
                data = load_clients(); idx = _idx(data)
                if idx < 0: self._redir("/clients", "Invalid."); return
                create_backup("clients-delete")
                data.pop(idx); save_clients(data); rebuild_all()
                self._redir("/clients", "Deleted."); return

            self._redir("/", "Unknown action.")

        def log_message(self, *a): return

    server = ThreadingHTTPServer((host, port), Handler)
    print(f"\n✅ Jonas Admin UI → http://{host}:{port}")
    print("   Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


# ── CLI ───────────────────────────────────────────────────────────────────────

def _prompt(msg, default=None, optional=False):
    while True:
        suffix = f" [{default}]" if default else ""
        val = input(f"{msg}{suffix}: ").strip()
        if not val and default is not None: return default
        if val or optional: return val
        print("Required.")

def _prompt_list(label, existing=None):
    print(f"{label} (blank line to finish):")
    if existing:
        for x in existing: print(f"  - {x}")
    items = []
    while True:
        v = input("  - ").strip()
        if not v: break
        items.append(v)
    return items if items else (existing or [])

def _yn(msg, default="n"):
    return _prompt(msg, default, optional=True).lower() in ("y","yes")

def init_data():
    """Seed JSON files from built-in defaults if they don't exist."""
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    for path, data in [
        (DATA_PATH,    _default_backline()),
        (AUDIO_DATA,   _default_audio()),
        (CLIENTS_DATA, _default_clients()),
        (TOURS_DATA,   _default_tours()),
        (CONTACT_DATA, _default_contact()),
    ]:
        if not os.path.exists(path):
            _save_json(path, data)
            print(f"  Created {os.path.basename(path)}")

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("web", "web-ui", "ui"):
        port = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 8082
        start_web_ui(port=port)
        return

    # Always ensure data files exist
    init_data()

    while True:
        print("""
Jonas Productions — Site Manager
  1) Open web UI (recommended)
  2) Rebuild site now
  3) Edit contact info
  4) Manage touring artists
  5) Publish to GitHub
  6) List/restore backups
  q) Quit""")
        cmd = _prompt("\nCommand").strip().lower()
        if cmd in ("q","quit","exit"): break

        if cmd in ("1","web","web-ui"):
            start_web_ui(); continue

        if cmd in ("2","rebuild"):
            rebuild_all(); continue

        if cmd in ("3","contact"):
            info = load_contact()
            create_backup("cli-contact")
            info["address"] = _prompt("Address", info.get("address",""))
            info["phone"]   = _prompt("Phone",   info.get("phone",""))
            info["fax"]     = _prompt("Fax",     info.get("fax",""))
            info["email"]   = _prompt("Email",   info.get("email",""))
            save_contact(info); rebuild_all(); continue

        if cmd in ("4","tours"):
            tours = load_tours()
            print("\nCurrent touring artists:")
            for i,t in enumerate(tours,1):
                print(f"  {i}. {t['artist']} (since {t['since']})")
            if _yn("Add new artist?"):
                create_backup("cli-tours-add")
                artist = _prompt("Artist name")
                since  = _prompt("Since year")
                tours.append({"artist":artist,"since":since})
                save_tours(tours); rebuild_all()
            continue

        if cmd in ("5","publish"):
            msg = _prompt("Commit message", optional=True)
            ok, out = publish_github(msg or None)
            print(out); continue

        if cmd in ("6","backups"):
            bs = list_backups()
            if not bs: print("No backups."); continue
            for i,n in enumerate(bs,1): print(f"  {i}. {n}")
            if _yn("Restore a backup? (y/n)", default="n"):
                raw = _prompt("Number")
                if raw.isdigit():
                    idx = int(raw)-1
                    if 0 <= idx < len(bs):
                        restore_backup(bs[idx]); rebuild_all()
                        print(f"Restored {bs[idx]}")
            continue

        print("Unknown command.")


if __name__ == "__main__":
    main()
