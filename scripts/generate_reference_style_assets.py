#!/usr/bin/env python3
"""Generate the five self-contained profile panels used by README.md."""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY = "#070b16"
SURFACE = "#0b1323"
PANEL = "#0e2244"
BLUE = "#247bff"
ICE = "#f2f5ff"
MUTED = "#99b1db"
LINE = "#26364d"

BASE_CSS = """
 text { font-family: Arial, Helvetica, sans-serif; }
.display { font-family: Impact, 'Arial Black', Arial, sans-serif; font-weight: 900; letter-spacing: -2px; }
.mono { font-family: 'Courier New', monospace; letter-spacing: 1px; }
.kicker { fill: #99b1db; font: 700 13px 'Courier New', monospace; letter-spacing: 1.4px; }
.motion { pointer-events: none; }
@media (prefers-reduced-motion: reduce) { .motion { display: none !important; animation: none !important; } }
"""


def doc(name: str, width: int, height: int, title: str, description: str,
        definitions: str, body: str, css: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="#f2f5ff" role="img" aria-labelledby="{name}-title {name}-desc">
<title id="{name}-title">{escape(title)}</title>
<desc id="{name}-desc">{escape(description)}</desc>
<defs>{definitions}</defs>
<style><![CDATA[{BASE_CSS}{css}]]></style>
{body}
</svg>
'''


def write(name: str, content: str) -> None:
    (ASSETS / name).write_text(content, encoding="utf-8")


def hero() -> None:
    portrait = base64.b64encode((ASSETS / "sameer-portrait.png").read_bytes()).decode("ascii")
    definitions = f'''
<linearGradient id="hero-field" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{NAVY}"/><stop offset="1" stop-color="#10244c"/></linearGradient>
<linearGradient id="hero-sheen" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="#8bc6ff" stop-opacity=".28"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<clipPath id="hero-photo-clip"><rect x="809" y="126" width="316" height="316"/></clipPath>
<filter id="hero-blue-shadow" x="-.25" y="-.25" width="1.5" height="1.5"><feDropShadow dx="12" dy="12" stdDeviation="0" flood-color="#030712" flood-opacity=".85"/></filter>
'''
    css = '''
@keyframes hero-arrive { 0%, 62% { transform: translateX(-480px); opacity: 0; } 70% { opacity: .95; } 100% { transform: translateX(950px); opacity: 0; } }
@keyframes hero-mark { 0%, 15%, 100% { transform: translateY(0); } 45% { transform: translateY(-6px); } 70% { transform: translateY(0); } }
.hero-sheen { animation: hero-arrive 14s cubic-bezier(.2,.7,.2,1) infinite; }
.hero-mark { animation: hero-mark 9s ease-in-out infinite; transform-origin: center; }
'''
    body = f'''
<rect width="1200" height="640" fill="url(#hero-field)"/>
<path d="M0 0H1200V10H0Z" fill="{BLUE}"/>
<path d="M55 94H1145" stroke="{LINE}" stroke-width="1"/>
<text x="58" y="71" class="kicker">SAMEER8549  /  DEVELOPER PROFILE</text>
<text x="1142" y="71" text-anchor="end" class="kicker">BENGALURU  /  INDIA</text>
<rect x="58" y="139" width="680" height="369" fill="#102756" stroke="{BLUE}" stroke-width="2"/>
<text x="88" y="254" class="display" font-size="100" fill="{ICE}">ABDUL</text>
<text x="88" y="357" class="display" font-size="100" fill="{BLUE}">SAMEER</text>
<text x="92" y="416" class="mono" font-size="22" font-weight="700">AI / ML ENGINEER</text>
<text x="92" y="451" class="mono" font-size="22" font-weight="700" fill="{MUTED}">FULL-STACK DEVELOPER</text>
<text x="92" y="480" class="mono" font-size="14" fill="{MUTED}">IDEAS INTO SYSTEMS.</text>
<rect x="790" y="108" width="354" height="354" fill="#02040b" stroke="{BLUE}" stroke-width="2" filter="url(#hero-blue-shadow)"/>
<rect x="802" y="120" width="328" height="328" fill="#0e2244" stroke="{ICE}" stroke-opacity=".75"/>
<image x="809" y="126" width="316" height="316" href="data:image/png;base64,{portrait}" preserveAspectRatio="xMidYMid slice" clip-path="url(#hero-photo-clip)"/>
<rect x="809" y="474" width="316" height="38" fill="{ICE}"/>
<text x="827" y="498" class="mono" font-size="12" font-weight="700" fill="{NAVY}">AI / PRODUCT / APPLIED SYSTEMS</text>
<path d="M58 550H1142" stroke="{LINE}" stroke-width="2"/>
<path d="M58 550H1142" stroke="{BLUE}" stroke-width="3" stroke-dasharray="70 1030" class="motion hero-sheen"/>
<g class="motion hero-mark"><path d="M1137 538l10 12-10 12" fill="none" stroke="{ICE}" stroke-width="2"/></g>
<text x="58" y="592" class="kicker">AI / ML  ·  PRODUCT ENGINEERING  ·  CREATIVE TECHNOLOGY</text>
<text x="1142" y="592" text-anchor="end" class="kicker">HKBK  /  GOOGLE STUDENT AMBASSADOR</text>
'''
    write("hero.svg", doc("hero", 1200, 640, "Abdul Sameer — profile", "AI/ML Engineer and Full-Stack Developer in Bengaluru. Royal-blue profile card with portrait and a slow moving light across the lower rule.", definitions, body, css))


def about() -> None:
    definitions = f'''
<linearGradient id="about-field" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{SURFACE}"/><stop offset="1" stop-color="#101f3b"/></linearGradient>
<linearGradient id="about-route" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{BLUE}" stop-opacity="0"/><stop offset=".52" stop-color="#8bc6ff"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
'''
    css = '''
@keyframes about-route { 0%, 16% { transform: translateX(-380px); opacity: 0; } 30% { opacity: .9; } 78% { opacity: .9; } 100% { transform: translateX(820px); opacity: 0; } }
.about-route { animation: about-route 16s ease-in-out infinite; }
'''
    body = f'''
<rect width="1200" height="620" fill="url(#about-field)"/>
<path d="M0 0H1200V8H0Z" fill="{BLUE}"/>
<text x="55" y="62" class="kicker">01  /  THE WORK</text><text x="1145" y="62" text-anchor="end" class="kicker">AI  ·  SYSTEMS  ·  PEOPLE</text>
<text x="58" y="211" class="display" font-size="89" fill="{ICE}">IDEAS</text>
<text x="58" y="300" class="display" font-size="89" fill="{BLUE}">INTO</text>
<text x="58" y="389" class="display" font-size="89" fill="{ICE}">SYSTEMS.</text>
<text x="62" y="447" class="mono" font-size="15" fill="{MUTED}">HEALTH / AGRICULTURE / RAIL / CIVIC</text>
<path d="M464 105V467" stroke="{LINE}" stroke-width="2"/>
<text x="516" y="113" class="kicker">HOW I BUILD</text>
<g>
  <rect x="516" y="150" width="628" height="62" fill="#101f3b" stroke="{LINE}"/>
  <text x="540" y="176" class="kicker">01</text><text x="594" y="190" class="display" font-size="26">SEE</text><text x="790" y="187" class="mono" font-size="15" fill="{MUTED}">VISION  /  SIGNAL</text>
  <rect x="516" y="229" width="628" height="62" fill="#101f3b" stroke="{LINE}"/>
  <text x="540" y="255" class="kicker">02</text><text x="594" y="269" class="display" font-size="26">REASON</text><text x="790" y="266" class="mono" font-size="15" fill="{MUTED}">MODELS  /  CONTEXT</text>
  <rect x="516" y="308" width="628" height="62" fill="#101f3b" stroke="{LINE}"/>
  <text x="540" y="334" class="kicker">03</text><text x="594" y="348" class="display" font-size="26">CONNECT</text><text x="790" y="345" class="mono" font-size="15" fill="{MUTED}">API  /  DATA</text>
  <rect x="516" y="387" width="628" height="62" fill="#101f3b" stroke="{LINE}"/>
  <text x="540" y="413" class="kicker">04</text><text x="594" y="427" class="display" font-size="26">SHIP</text><text x="790" y="424" class="mono" font-size="15" fill="{MUTED}">PRODUCT  /  PEOPLE</text>
</g>
<path d="M523 181H1138" stroke="{BLUE}" stroke-width="2" stroke-dasharray="92 950" class="motion about-route"/>
<text x="516" y="510" class="mono" font-size="13" fill="{MUTED}">HKBK  ·  INFORMATION SCIENCE ENGINEERING</text>
<text x="1144" y="510" text-anchor="end" class="mono" font-size="12" fill="{ICE}">GOOGLE STUDENT AMBASSADOR</text>
<path d="M58 550H1144" stroke="{LINE}"/>
<text x="58" y="583" class="kicker">AI / ML ENGINEERING  —  FULL-STACK PRODUCT DEVELOPMENT</text>
'''
    write("about-life.svg", doc("about", 1200, 620, "Ideas into systems", "Abdul Sameer builds across AI/ML, full-stack product engineering, and real-world systems in health, agriculture, rail, and civic technology.", definitions, body, css))


def stack() -> None:
    definitions = f'''
<linearGradient id="stack-field" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{NAVY}"/><stop offset="1" stop-color="#0d1b36"/></linearGradient>
<linearGradient id="stack-light" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="#8bc6ff" stop-opacity=".24"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
'''
    css = '''
@keyframes stack-light { 0%, 20% { transform: translateX(-360px); opacity: 0; } 35% { opacity: 1; } 75% { opacity: .8; } 100% { transform: translateX(1080px); opacity: 0; } }
.stack-light { animation: stack-light 15s cubic-bezier(.2,.7,.2,1) infinite; }
'''
    rows = [
        ("LANGUAGES", "PYTHON   /   JAVASCRIPT   /   TYPESCRIPT   /   C++"),
        ("APPLICATIONS", "REACT   /   NEXT.JS   /   FASTAPI   /   NODE.JS"),
        ("AI / VISION", "YOLOv8   /   OPENCV   /   GEMINI   /   LSTM   /   RAG"),
        ("DATA", "POSTGRESQL   /   MONGODB   /   REDIS   /   FIREBASE"),
        ("DELIVERY", "DOCKER   /   KUBERNETES   /   VERCEL   /   GOOGLE CLOUD   /   LINUX   /   GIT"),
    ]
    parts = [f'''<rect width="1200" height="600" fill="url(#stack-field)"/>
<path d="M0 0H1200V8H0Z" fill="{BLUE}"/>
<text x="55" y="62" class="kicker">02  /  SELECTED TOOLKIT</text><text x="1145" y="62" text-anchor="end" class="kicker">VERIFIED IN PROJECTS</text>
<text x="58" y="150" class="display" font-size="54">TOOLS THAT MOVE WORK.</text>
<text x="62" y="187" class="mono" font-size="15" fill="{MUTED}">LANGUAGES  /  PRODUCT  /  APPLIED AI  /  DELIVERY</text>''']
    for idx, (label, technologies) in enumerate(rows):
        y = 218 + idx * 56
        parts.append(f'''<rect x="58" y="{y}" width="1084" height="48" fill="#0b1730" stroke="{LINE}"/>
<rect x="58" y="{y}" width="238" height="48" fill="#102756"/>
<text x="78" y="{y + 30}" class="mono" font-size="14" font-weight="700">{label}</text>
<text x="322" y="{y + 30}" class="mono" font-size="17" font-weight="700">{technologies}</text>''')
    parts.append(f'''<rect x="58" y="218" width="1084" height="272" fill="url(#stack-light)" class="motion stack-light"/>
<text x="58" y="570" class="kicker">CLICKABLE BRAND ICONS FOLLOW BELOW</text><text x="1142" y="570" text-anchor="end" class="kicker">ROYAL BLUE  /  BUILDER STACK</text>''')
    write("stack.svg", doc("stack", 1200, 600, "Selected technology stack", "Grouped programming languages, application frameworks, AI and vision tools, data stores, and delivery platforms used across Abdul Sameer's projects.", definitions, "\n".join(parts), css))


ROWS = [
    "00000000000000000000000000000001000000200000000000200",
    "00200000000000000020000000000000001000000010000200000",
    "00000000000000000000000000000000000010200010000400000",
    "00000000000000000000000100000000400000200000004000121",
    "00000000010000000000000200000000101000000000000000000",
    "00000000000000000000100000000000011000000110000000400",
    "00000000000000000000000000000000000002100102000000100",
]


def dashboard() -> None:
    colors = ["#111827", "#123a9c", "#1d56d8", "#3b82f6", "#93c5fd"]
    cell, gap, stride = 13, 4, 17
    grid_width = 53 * cell + 52 * gap
    grid_x = (1200 - grid_width) // 2
    grid_y = 364
    cells = []
    pulses = []
    for col in range(53):
        for row in range(7):
            level = int(ROWS[row][col])
            x, y = grid_x + col * stride, grid_y + row * stride
            cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{colors[level]}"/>')
            if level >= 3 and (col + row) % 3 == 0:
                phase = "abcd"[(col + row) % 4]
                pulses.append(f'<rect x="{x - 1}" y="{y - 1}" width="{cell + 2}" height="{cell + 2}" rx="3" fill="none" stroke="#8bc6ff" stroke-width="1.5" class="motion dashboard-pulse pulse-{phase}"/>')
    month_labels = []
    # Approximate the visible Oct-to-Oct month starts used by the supplied profile snapshot.
    for label, col in [("OCT", 0), ("NOV", 4), ("DEC", 8), ("JAN", 13), ("FEB", 17), ("MAR", 21), ("APR", 26), ("MAY", 30), ("JUN", 34), ("JUL", 39), ("AUG", 43), ("SEP", 47), ("OCT", 51)]:
        month_labels.append(f'<text x="{grid_x + col * stride}" y="337" class="mono" font-size="11" fill="{MUTED}">{label}</text>')
    definitions = f'''
<linearGradient id="dashboard-field" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{SURFACE}"/><stop offset="1" stop-color="{NAVY}"/></linearGradient>
<linearGradient id="dashboard-edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="#8bc6ff"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
'''
    css = '''
@keyframes dashboard-edge { 0%, 20% { transform: translateX(-680px); opacity: 0; } 35% { opacity: .9; } 72% { opacity: .9; } 100% { transform: translateX(1200px); opacity: 0; } }
.dashboard-edge { animation: dashboard-edge 18s ease-in-out infinite; }
@keyframes dashboard-pulse { 0%, 100% { opacity: .08; } 50% { opacity: .9; } }
.dashboard-pulse { animation: dashboard-pulse 5.4s ease-in-out infinite; }
.pulse-a { animation-delay: -1.2s; }
.pulse-b { animation-delay: -2.4s; }
.pulse-c { animation-delay: -3.6s; }
.pulse-d { animation-delay: -4.8s; }
'''
    body = f'''
<rect width="1200" height="640" fill="url(#dashboard-field)"/>
<path d="M0 0H1200V8H0Z" fill="{BLUE}"/>
<text x="55" y="62" class="kicker">03  /  PROFILE SNAPSHOT</text><text x="1145" y="62" text-anchor="end" class="kicker">SOURCE  /  GITHUB PROFILE</text>
<text x="58" y="203" class="display" font-size="142" fill="{BLUE}">90</text>
<text x="66" y="244" class="mono" font-size="17" font-weight="700">CONTRIBUTIONS</text>
<text x="66" y="274" class="mono" font-size="13" fill="{MUTED}">LAST 12 MONTHS  /  21 OCT 2026</text>
<path d="M66 298H1134" stroke="{LINE}"/>
<text x="66" y="326" class="kicker">PROFILE CONTRIBUTION RECORD  ·  DATED SNAPSHOT</text>
{''.join(month_labels)}
<text x="68" y="{grid_y + stride * 1}" class="mono" font-size="9" fill="{MUTED}">M</text>
<text x="68" y="{grid_y + stride * 3}" class="mono" font-size="9" fill="{MUTED}">W</text>
<text x="68" y="{grid_y + stride * 5}" class="mono" font-size="9" fill="{MUTED}">F</text>
{''.join(cells)}
{''.join(pulses)}
<text x="{grid_x + 820}" y="{grid_y + 143}" class="mono" font-size="10" fill="{MUTED}">LESS</text>
{''.join(f'<rect x="{grid_x + 862 + i * 22}" y="{grid_y + 132}" width="14" height="14" rx="2" fill="{color}"/>' for i, color in enumerate(colors))}
<text x="{grid_x + 986}" y="{grid_y + 143}" class="mono" font-size="10" fill="{MUTED}">MORE</text>
<rect x="58" y="545" width="1084" height="1" fill="{LINE}"/>
<text x="58" y="580" class="mono" font-size="14" font-weight="700">10 SELECTED BUILDS</text>
<text x="428" y="580" class="mono" font-size="14" font-weight="700">2 RESEARCH PAPERS</text>
<text x="805" y="580" class="mono" font-size="14" font-weight="700">HKBK  /  GOOGLE STUDENT AMBASSADOR</text>
<path d="M58 610H1142" stroke="{BLUE}" stroke-width="2" stroke-dasharray="90 1000" class="motion dashboard-edge"/>
'''
    write("id-dashboard.svg", doc("dashboard", 1200, 640, "GitHub contribution and work snapshot", "A dated snapshot of 90 contributions in the last 12 months as shown on 21 October 2026, with ten selected builds and two linked research papers.", definitions, body, css))


def connect() -> None:
    definitions = f'''
<linearGradient id="connect-field" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0b1323"/><stop offset="1" stop-color="#10244c"/></linearGradient>
<linearGradient id="connect-signal" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="#8bc6ff"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
'''
    css = '''
@keyframes connect-signal { 0%, 25% { transform: translateX(-420px); opacity: 0; } 38% { opacity: 1; } 82% { opacity: 1; } 100% { transform: translateX(860px); opacity: 0; } }
.connect-signal { animation: connect-signal 14s ease-in-out infinite; }
'''
    body = f'''
<rect width="1200" height="500" fill="url(#connect-field)"/>
<path d="M0 0H1200V8H0Z" fill="{BLUE}"/>
<text x="55" y="62" class="kicker">04  /  OPEN CHANNEL</text><text x="1145" y="62" text-anchor="end" class="kicker">CONNECT  ·  COLLABORATE  ·  BUILD</text>
<text x="58" y="213" class="display" font-size="81" fill="{ICE}">LET'S BUILD</text>
<text x="58" y="302" class="display" font-size="81" fill="{BLUE}">WHAT'S NEXT.</text>
<text x="64" y="360" class="mono" font-size="16" fill="{MUTED}">AI / ML  ·  FULL-STACK  ·  PRODUCT SYSTEMS</text>
<path d="M58 402H1142" stroke="{LINE}" stroke-width="2"/>
<path d="M58 402H1142" stroke="{BLUE}" stroke-width="3" stroke-dasharray="110 950" class="motion connect-signal"/>
<text x="58" y="449" class="kicker">LINKEDIN</text><text x="330" y="449" class="kicker">PORTFOLIO</text><text x="635" y="449" class="kicker">GITHUB</text><text x="905" y="449" class="kicker">EMAIL</text>
<path d="M58 470H1142" stroke="{LINE}"/>
<text x="58" y="488" class="mono" font-size="11" fill="{MUTED}">BENGALURU, INDIA</text><text x="1142" y="488" text-anchor="end" class="mono" font-size="11" fill="{MUTED}">ABDUL SAMEER  /  SAMEER8549</text>
'''
    write("connect.svg", doc("connect", 1200, 500, "Connect with Abdul Sameer", "Contact panel for LinkedIn, portfolio, GitHub, and email, with a slow moving signal line and a static reduced-motion fallback.", definitions, body, css))


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    hero()
    about()
    stack()
    dashboard()
    connect()
    print("Generated five self-contained profile SVG panels.")


if __name__ == "__main__":
    main()
