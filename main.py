#!/usr/bin/env python3
"""news-image-20261126 — entry for @syukuran.

"Around the world in 24 hours": one 1024x1024 image that sums up the world
news of Thursday 26 November 2026 as a journey, not a newspaper.

  * a stylised equirectangular world map with six numbered pins for the
    day's six biggest stories (legend underneath the map);
  * a timeline of the day unfolding, dawn to midnight (UTC), with eight
    more stories in the order they broke;
  * six region columns with 48 more stories.

62 stories in total, 6 regions, every claim verified as reported on
26 November 2026 (in at least one time zone); wording follows the
reporting, without hype or speculation.

Deterministic: pure Pillow drawing, no network, no clock, no randomness.
Running it twice writes byte-identical output.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Anchor (quoted before the first write): drand quicknet round 34283533,
fetched 2026-11-26T00:45:55Z, signature
a2b8fc8208185f70734bdc2096a95ed613d07fdd272ac078af643730fa753515af6e596a6ac3504049d3c5620b98efe8.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

NAVY = (16, 35, 58)
OCEAN = (213, 231, 241)
LAND = (176, 196, 143)
LAND_EDGE = (118, 143, 92)
GRID_LINE = (190, 208, 220)
PAPER = (250, 248, 243)
INK = (20, 24, 30)
GREY = (92, 96, 101)
RED = (176, 32, 32)
BLUE = (31, 78, 156)
GREEN = (30, 122, 70)
ORANGE = (194, 94, 0)
PURPLE = (106, 63, 160)
TEAL = (14, 124, 123)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap text, cap at max_lines, ellipsis on the last line if cut."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    out = lines[:max_lines]
    last = out[-1]
    while last and draw.textlength(last + "\u2026", font=fnt) > width:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    out[-1] = last + "\u2026"
    return out


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# --- the day's six biggest stories, pinned on the map ---
# (number, place, lon, lat, headline)
PINS = [
    (1, "RAS TANURA", 50.0, 26.6,
     "Houthis claim refinery hit; Brent tops $94 (claim unconfirmed)"),
    (2, "WASHINGTON", -77.0, 38.9,
     "US unveils tariffs up to 15% on 14 partners"),
    (3, "SAMARA", 50.0, 53.2,
     "Ukraine hits two Russian refineries; Putin vows revenge"),
    (4, "GAZA", 34.5, 31.5,
     "Israel kills Hamas security chief Abuelouf"),
    (5, "REDMOND", -122.1, 47.7,
     "Microsoft 'Code Red' after Outlook/Teams outage"),
    (6, "KUALA LUMPUR", 101.7, 3.1,
     "Malaysia sues Google for $146M over YouTube"),
]

# --- the day unfolds: (daypart, story) ---
TIMELINE = [
    ("OVERNIGHT", "India marks Constitution Day; 18 years since 26/11"),
    ("OVERNIGHT", "First Thanksgiving Eve NFL game: Packers-Rams"),
    ("MORNING", "Coalition jets strike Hodeidah port"),
    ("MORNING", "Vietnam races US to finish trade deal"),
    ("MIDDAY", "Thanksgiving storm lashes East Coast; parade goes on"),
    ("AFTERNOON", "Judge bars FCC from threatening ABC licence"),
    ("EVENING", "Thanksgiving NFL triple-header kicks off in Detroit"),
    ("NIGHT", "Qatar Grand Prix goes ahead despite war on its doorstep"),
]

# --- 48 more stories, by region: (region, colour, [stories]) ---
REGIONS = [
    ("MIDDLE EAST", RED, [
        "Saudi coalition: four drones downed over Ras Tanura",
        "Houthi projectile hits Jazan port; minor damage",
        "US tells citizens to leave Iran after Riyadh tower attack",
        "Iran says it shot down two US drones near Hormuz",
        "Two oil tankers hit naval mines in Strait of Hormuz",
        "Two Libyan officers die in drone strike on Russian warship",
        "Libya vows retaliation after Benghazi strike",
        "Sudan drone strikes kill 19 civilians",
    ]),
    ("EUROPE", BLUE, [
        "Leaked data: 490,334 Russian soldiers dead in Ukraine",
        "Russia hits Odesa: two killed, child hurt; Kyiv flat ablaze",
        "UK warns firms of Russian sabotage threat",
        "Zelenskyy: Ukraine needs EUR 115bn for 2027",
        "EU proposes EUR 45bn Ukraine loan",
        "Lille stun Bayern in Champions League",
        "Sporting 2-2 Man Utd: Fernandes double, VAR drama",
        "Hungary approves wealth tax on millionaires",
    ]),
    ("ASIA-PACIFIC", ORANGE, [
        "Pakistan's first astronaut to fly Shenzhou-24 to Tiangong",
        "Taiwan shares plunge 1,927 pts; dollar past 33",
        "India unveils Rs 15,000-crore package for Nepal",
        "Hasina seeks return to Bangladesh on Dec 16",
        "Bangladesh raises garment wage 36%",
        "Indonesia gold-mine flood kills nine miners",
        "Lebanon plans second airport at Kleiat",
        "North Korea closes Swiss office in Pyongyang",
    ]),
    ("AMERICAS", TEAL, [
        "Trump: Nvidia CEO pardon is 'always an option'",
        "US Army destroys entire lead-azide stockpile in Iowa",
        "Abrego Garcia leaves US for Spain",
        "Colombia police free 20 hostages after 17 hours",
        "US pauses joint ops with Ecuador over Sept raid probe",
        "Fed Beige Book: modest growth, sticky prices",
        "US attorney general dodges Nvidia probe questions",
        "US FinCEN systems offline after suspected cyberattack",
    ]),
    ("MARKETS & TECH", PURPLE, [
        "Huawei guilty on 10 of 12 counts in Brooklyn trial",
        "AI-bubble fears hit tech stocks; Nvidia down 8%",
        "US tightens remote AI-chip access rules",
        "Dow holds 50,000; worst Nov since 2008 looms",
        "PCE inflation 3.8%; Q3 GDP revised up to 4.3%",
        "Bitcoin near $59,000 as gold and silver slip",
        "EU to impose visa bans and quotas on Chinese cars",
        "France's Senate rejects crypto declaration",
    ]),
    ("SPORT & SCIENCE", GREEN, [
        "Gukesh faces Sindarov at World Chess Championship",
        "Sooryavanshi, 15, hits fastest List A double ton",
        "IPL 2027 auction draws 1,220 players",
        "Sterling spared jail over dangerous driving",
        "Wolbachia mosquitoes cut Brazil infections 68%",
        "Cairo tanker fire kills at least 31",
        "BepiColombo reaches Mercury orbit after 8 years",
        "DART asteroid close-ups to be revealed",
    ]),
]

TOTAL_STORIES = len(PINS) + len(TIMELINE) + sum(len(s) for _, _, s in REGIONS)
assert TOTAL_STORIES == 62, f"story count {TOTAL_STORIES} != 62"

# --- simplified continents, as (lon, lat) polygons (equirectangular) ---
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    # Greenland
    [(-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-58, 64)],
    # South America
    [(-80, 9), (-72, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -54), (-73, -40),
     (-72, -20), (-80, -5)],
    # Africa
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (32, 31), (43, 12),
     (51, 11), (48, 0), (40, -10), (35, -20), (32, -29), (20, -35),
     (12, -18), (9, -1), (-8, 4)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (3, 51), (8, 57), (12, 60), (18, 56),
     (23, 59), (30, 60), (28, 66), (32, 70), (45, 68), (60, 69), (70, 72),
     (90, 75), (110, 76), (130, 72), (150, 70), (170, 66), (178, 65),
     (170, 60), (162, 56), (158, 52), (142, 50), (140, 40), (130, 35),
     (122, 30), (120, 22), (110, 20), (105, 10), (100, 8), (97, 16),
     (92, 21), (88, 22), (80, 13), (77, 8), (73, 20), (66, 25), (60, 25),
     (57, 27), (52, 28), (50, 30), (48, 30), (44, 39), (40, 36), (36, 36),
     (30, 36), (26, 38), (23, 36), (19, 40), (12, 44), (8, 44), (3, 43),
     (0, 40), (-2, 37), (-9, 37)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (142, -38), (147, -39), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 39),
     (142, 42), (144, 44), (140, 42), (139, 38), (137, 36), (133, 34)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25),
     (43, -21)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (147, -9),
     (142, -8), (136, -7), (132, -4)],
    # Borneo
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -3), (110, -1)],
    # Sumatra
    [(95, 5), (100, 0), (104, -3), (106, -6), (103, -5), (99, -1), (96, 3)],
]

MAP_X0, MAP_X1, MAP_Y0, MAP_Y1 = 16, 1008, 100, 292


def project(lon, lat):
    x = MAP_X0 + (lon + 180.0) / 360.0 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (75.0 - lat) / 130.0 * (MAP_Y1 - MAP_Y0)
    return (x, y)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 92], fill=NAVY)
    title = "AROUND THE WORLD IN 24 HOURS"
    tf = font(SERIF_B, 40)
    d.text(((W - d.textlength(title, font=tf)) / 2, 12), title, font=tf,
           fill=(255, 255, 255))
    sub = ("THURSDAY 26 NOVEMBER 2026   \u2022   62 STORIES   \u2022   6 REGIONS   "
           "\u2022   EVERY CLAIM VERIFIED AS REPORTED")
    sf = font(SANS_B, 15)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 62), sub, font=sf,
           fill=(255, 200, 90))
    d.rectangle([0, 92, W, 94], fill=RED)

    # ---- world map ----
    d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=OCEAN,
                outline=(150, 170, 185), width=1)
    # graticule every 30 degrees
    for lon in range(-150, 181, 30):
        x = MAP_X0 + (lon + 180.0) / 360.0 * (MAP_X1 - MAP_X0)
        d.line([x, MAP_Y0, x, MAP_Y1], fill=GRID_LINE, width=1)
    for lat in (60, 30, 0, -30):
        _, y = project(0, lat)
        d.line([MAP_X0, y, MAP_X1, y], fill=GRID_LINE, width=1)
    d.text((MAP_X0 + 8, MAP_Y1 - 16), "THE WORLD, 26 NOVEMBER 2026",
           font=font(SANS_B, 11), fill=(70, 90, 105))
    d.text((MAP_X1 - 8, MAP_Y1 - 16), "1\u20136 = THE DAY'S BIGGEST STORIES",
           font=font(SANS_B, 11), fill=(70, 90, 105), anchor="ra")
    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_EDGE)
    for num, _place, lon, lat, _head in PINS:
        x, y = project(lon, lat)
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=RED,
                  outline=(255, 255, 255), width=2)
        nf = font(SANS_B, 13)
        tw = d.textlength(str(num), font=nf)
        d.text((x - tw / 2, y - 8), str(num), font=nf, fill=(255, 255, 255))

    # ---- pin legend: 2 rows x 3 columns ----
    lx, ly = 16, 300
    cw, ch = 322, 40
    for i, (num, place, _lon, _lat, head) in enumerate(PINS):
        x = lx + (i % 3) * (cw + 5)
        y = ly + (i // 3) * ch
        d.ellipse([x, y + 1, x + 18, y + 19], fill=RED)
        nf = font(SANS_B, 11)
        tw = d.textlength(str(num), font=nf)
        d.text((x + 9 - tw / 2, y + 3), str(num), font=nf,
               fill=(255, 255, 255))
        d.text((x + 24, y + 1), place, font=font(SANS_B, 11), fill=RED)
        text_block(d, x + 24, y + 15,
                   fit_lines(d, head, font(SANS, 10), cw - 24, 2),
                   font(SANS, 10), INK, 12)

    # ---- timeline: the day unfolds ----
    ty = 382
    d.text((16, ty), "THE DAY UNFOLDS \u2014 FROM DAWN TO MIDNIGHT (UTC)",
           font=font(SANS_B, 14), fill=INK)
    d.rectangle([16, ty + 22, W - 17, ty + 24], fill=NAVY)
    line_y = ty + 44
    d.line([40, line_y, W - 40, line_y], fill=NAVY, width=2)
    slot_w = (W - 80) / len(TIMELINE)
    for i, (part, story) in enumerate(TIMELINE):
        cx = 40 + slot_w * i + slot_w / 2
        d.ellipse([cx - 6, line_y - 6, cx + 6, line_y + 6], fill=RED,
                  outline=(255, 255, 255), width=2)
        pf = font(SANS_B, 9)
        pw = d.textlength(part, font=pf)
        d.text((cx - pw / 2, line_y - 20), part, font=pf, fill=RED)
        text_block(d, cx - slot_w / 2 + 4, line_y + 12,
                   fit_lines(d, story, font(SANS, 10), slot_w - 8, 3),
                   font(SANS, 10), INK, 12)
    d.rectangle([16, ty + 102, W - 17, ty + 104], fill=NAVY)

    # ---- 48 more stories, by region ----
    gy = 496
    d.text((16, gy), "48 MORE STORIES \u2014 BY REGION",
           font=font(SANS_B, 14), fill=INK)
    d.rectangle([16, gy + 22, W - 17, gy + 24], fill=NAVY)
    col_w, col_gap = 158, 8
    y0 = gy + 32
    for ci, (region, colour, stories) in enumerate(REGIONS):
        x = 16 + ci * (col_w + col_gap)
        d.rectangle([x, y0, x + col_w, y0 + 3], fill=colour)
        d.text((x, y0 + 7), region, font=font(SANS_B, 10), fill=colour)
        y = y0 + 22
        for story in stories:
            lines = fit_lines(d, story, font(SANS_B, 10), col_w, 3)
            assert len(lines) <= 3, f"story too long: {story}"
            y = text_block(d, x, y, lines, font(SANS_B, 10), INK, 12)
            y += 5
        assert y <= 972, f"column {region} overflows: {y}"

    # ---- footer ----
    foot = ("Drawn entirely by code \u2014 no photographs. Every story above was "
            "first reported on 26 November 2026 in at least one time zone; "
            "wording follows the reporting, without hype or speculation. "
            "Sources: Reuters, AP, BBC, AFP, Bloomberg.")
    text_block(d, 22, 984, fit_lines(d, foot, font(SANS, 10), W - 44, 2),
               font(SANS, 10), GREY, 13)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes, {TOTAL_STORIES} stories)")


if __name__ == "__main__":
    main()
