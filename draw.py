#!/usr/bin/env python3
"""news-22 b13 regions-seven: draw entry.png (1024x1024) with PIL.
Layout (top-20 pattern): masthead -> kicker -> number strip -> region bar
-> UTC strip -> 3 hero scenes -> 10 small cards -> map + ALSO list
-> DATE CHECK -> footer. All facts from BEDAH-TOP20 / NEWS-20261122.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (26, 26, 26)
NAVY = (20, 38, 77)
RED = (166, 25, 46)
GOLD = (212, 160, 40)
CREAM2 = (238, 230, 211)
OCEAN = (207, 224, 234)
LAND = (232, 220, 192)
LANDLINE = (20, 38, 77)

REGION_COLORS = {
    "EUROPE": (31, 78, 121),
    "MIDDLE EAST": (166, 25, 46),
    "ASIA-PACIFIC": (46, 107, 52),
    "AMERICAS": (91, 45, 142),
    "AFRICA": (194, 94, 0),
    "OCEANIA": (14, 124, 123),
    "WORLD": (85, 85, 85),
}
REGION_SHORT = {
    "EUROPE": "EUROPE",
    "MIDDLE EAST": "M. EAST",
    "ASIA-PACIFIC": "ASIA-PAC.",
    "AMERICAS": "AMERICAS",
    "AFRICA": "AFRICA",
    "OCEANIA": "OCEANIA",
    "WORLD": "WORLD",
}

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


f_mast = F("DejaVuSerif-Bold.ttf", 44)
f_kick = F("DejaVuSans-Bold.ttf", 12)
f_kick_it = F("DejaVuSans-Bold.ttf", 12)
f_strip_n = F("DejaVuSans-Bold.ttf", 15)
f_strip_l = F("DejaVuSans.ttf", 10)
f_bar = F("DejaVuSans-Bold.ttf", 12)
f_utc_h = F("DejaVuSans-Bold.ttf", 11)
f_utc = F("DejaVuSans.ttf", 10)
f_hero_k = F("DejaVuSans-Bold.ttf", 11)
f_hero_h = F("DejaVuSerif-Bold.ttf", 23)
f_hero_b = F("DejaVuSans.ttf", 12)
f_card_k = F("DejaVuSans-Bold.ttf", 9)
f_card_t = F("DejaVuSans-Bold.ttf", 13)
f_card_b = F("DejaVuSans.ttf", 10)
f_src = F("DejaVuSans.ttf", 9)
f_chip = F("DejaVuSans-Bold.ttf", 8)
f_also = F("DejaVuSans-Bold.ttf", 9)
f_also_s = F("DejaVuSans.ttf", 9)
f_dc_h = F("DejaVuSans-Bold.ttf", 13)
f_dc = F("DejaVuSans.ttf", 11)
f_dc_b = F("DejaVuSans-Bold.ttf", 11)
f_foot = F("DejaVuSans.ttf", 10)
f_pin = F("DejaVuSans-Bold.ttf", 8)
f_map_h = F("DejaVuSans-Bold.ttf", 11)

CHIP_COLORS = {
    "CONFIRMED": (30, 110, 45),
    "REPORTED": (31, 78, 121),
    "CLAIM": (166, 25, 46),
    "ONGOING": (120, 70, 0),
    "PENDING": (90, 90, 90),
    "OFFICIAL": (20, 38, 77),
    "FORECAST": (110, 60, 140),
}


def wrap(d, text, font, maxw):
    """Greedy wrap by words using textlength."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(d, x, y, label):
    col = CHIP_COLORS[label]
    w = int(d.textlength(label, font=f_chip)) + 10
    h = 13
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=col)
    d.text((x + 5, y + 1), label, font=f_chip, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- scenes
def scene_cop31(d, x0, y0, w, h):
    # dusk sky: orange horizon -> purple top, conference hall silhouette
    for i in range(h):
        t = i / max(1, h - 1)
        r = int(70 + (230 - 70) * t)
        g = int(40 + (140 - 40) * t)
        b = int(90 + (60 - 90) * t)
        d.line([(x0, y0 + i), (x0 + w, y0 + i)], fill=(r, g, b))
    d.ellipse([x0 + w - 52, y0 + h - 46, x0 + w - 16, y0 + h - 10], fill=(255, 190, 80))
    # hall
    d.rectangle([x0 + 14, y0 + h - 34, x0 + w - 14, y0 + h], fill=(30, 22, 48))
    for cx in range(x0 + 24, x0 + w - 20, 26):
        d.rectangle([cx, y0 + h - 30, cx + 8, y0 + h - 8], fill=(255, 205, 110))
    d.rectangle([x0 + 14, y0 + h - 38, x0 + w - 14, y0 + h - 32], fill=(30, 22, 48))
    # flags
    for fx in (x0 + 30, x0 + w // 2, x0 + w - 34):
        d.line([(fx, y0 + h - 52), (fx, y0 + h - 38)], fill=(240, 240, 240), width=2)
        d.polygon([(fx, y0 + h - 52), (fx + 12, y0 + h - 49), (fx, y0 + h - 46)],
                  fill=(166, 25, 46))
    # delegates walking out (tiny silhouettes)
    for sx in (x0 + w - 90, x0 + w - 74, x0 + w - 58):
        d.ellipse([sx, y0 + h - 14, sx + 6, y0 + h - 8], fill=(15, 10, 25))
        d.rectangle([sx + 1, y0 + h - 8, sx + 5, y0 + h], fill=(15, 10, 25))


def scene_drones(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(12, 20, 48))
    for sx, sy in [(x0 + 20, y0 + 12), (x0 + 70, y0 + 22), (x0 + 130, y0 + 8),
                   (x0 + 200, y0 + 18), (x0 + 260, y0 + 10), (x0 + 300, y0 + 26)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # tracer arcs (kept inside the scene box)
    d.arc([x0 + 40, y0, x0 + 220, y0 + 70], 20, 160, fill=(255, 170, 60), width=2)
    d.arc([x0 + 120, y0 + 10, x0 + 300, y0 + 80], 20, 160, fill=(255, 200, 100), width=2)
    # drones: small dark crosses with lights
    for dx, dy in [(x0 + 90, y0 + 30), (x0 + 180, y0 + 44), (x0 + 250, y0 + 26)]:
        d.line([(dx - 7, dy), (dx + 7, dy)], fill=(10, 10, 10), width=2)
        d.line([(dx, dy - 4), (dx, dy + 4)], fill=(10, 10, 10), width=2)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 60, 60))
    # burning block bottom
    d.rectangle([x0 + 24, y0 + h - 34, x0 + 120, y0 + h], fill=(40, 32, 40))
    for fx in range(x0 + 30, x0 + 116, 14):
        d.polygon([(fx, y0 + h - 34), (fx + 6, y0 + h - 52), (fx + 12, y0 + h - 34)],
                  fill=(255, 140, 20))
        d.polygon([(fx + 3, y0 + h - 34), (fx + 6, y0 + h - 44), (fx + 9, y0 + h - 34)],
                  fill=(255, 210, 60))
    # smoke (kept inside the scene box)
    for sx, sy, r in [(x0 + 60, y0 + h - 40, 8), (x0 + 84, y0 + h - 48, 10),
                      (x0 + 108, y0 + h - 42, 7)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(90, 85, 95))


def scene_patriot(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 24, 52))
    for sx, sy in [(x0 + 30, y0 + 10), (x0 + 90, y0 + 20), (x0 + 160, y0 + 8),
                   (x0 + 230, y0 + 16), (x0 + 290, y0 + 12)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # explosion glow (kept inside the scene box)
    cx, cy = x0 + w - 70, y0 + 30
    for r, col in [(26, (255, 120, 30)), (18, (255, 170, 60)), (10, (255, 220, 120))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for ang in (0, 45, 90, 135, 180, 225, 270, 315):
        import math
        a = math.radians(ang)
        d.line([(cx + 28 * math.cos(a), cy + 28 * math.sin(a)),
                (cx + 36 * math.cos(a), cy + 36 * math.sin(a))],
               fill=(255, 170, 60), width=2)
    # radar dish (arc box kept inside the scene box)
    d.line([(x0 + 60, y0 + h - 6), (x0 + 60, y0 + h - 46)], fill=(200, 200, 200), width=3)
    d.arc([x0 + 34, y0 + h - 56, x0 + 86, y0 + h - 16], 200, 340, fill=(220, 220, 220), width=3)
    d.line([(x0 + 60, y0 + h - 46), (x0 + 86, y0 + h - 48)], fill=(220, 220, 220), width=2)
    # second dish smaller
    d.line([(x0 + 130, y0 + h - 6), (x0 + 130, y0 + h - 34)], fill=(180, 180, 180), width=3)
    d.arc([x0 + 112, y0 + h - 48, x0 + 148, y0 + h - 20], 200, 340, fill=(200, 200, 200), width=3)
    # ground + fence
    d.rectangle([x0, y0 + h - 6, x0 + w, y0 + h], fill=(40, 36, 44))
    for fx in range(x0 + 8, x0 + w - 8, 18):
        d.line([(fx, y0 + h - 20), (fx, y0 + h - 6)], fill=(150, 150, 150), width=1)


def strip_scene(d, x0, y0, w, h, kind):
    """Small 200x40 illustration strip for a small card."""
    if kind == "hk":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(70, 90, 130))
        d.ellipse([x0 + w - 34, y0 + 5, x0 + w - 12, y0 + 27], fill=(255, 200, 90))
        for bx, bh in [(6, 22), (26, 30), (48, 18), (66, 26), (86, 14), (104, 24)]:
            d.rectangle([x0 + bx, y0 + h - bh, x0 + bx + 16, y0 + h], fill=(25, 35, 60))
        d.rectangle([x0, y0 + h - 4, x0 + w, y0 + h], fill=(40, 60, 90))
    elif kind == "india":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(46, 120, 60))
        d.rectangle([x0, y0 + h - 10, x0 + w, y0 + h], fill=(210, 190, 140))
        d.line([(x0 + 20, y0 + 8), (x0 + 20, y0 + h - 10)], fill=(255, 255, 255), width=2)
        d.line([(x0 + 150, y0 + 8), (x0 + 150, y0 + h - 10)], fill=(255, 255, 255), width=2)
        d.ellipse([x0 + 96, y0 + 12, x0 + 108, y0 + 24], fill=(200, 30, 30))
        d.rectangle([x0 + 60, y0 + 22, x0 + 88, y0 + 27], fill=(180, 140, 90))
    elif kind == "dems":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(20, 38, 77))
        d.ellipse([x0 + 84, y0 + 4, x0 + 116, y0 + 22], fill=(240, 240, 240))
        d.rectangle([x0 + 78, y0 + 20, x0 + 122, y0 + 26], fill=(240, 240, 240))
        for i in range(12):
            col = (60, 110, 220) if i < 8 else (200, 60, 60)
            d.ellipse([x0 + 8 + i * 15, y0 + h - 12, x0 + 16 + i * 15, y0 + h - 4], fill=col)
    elif kind == "cikande":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(60, 55, 60))
        d.rectangle([x0 + 10, y0 + 14, x0 + 70, y0 + h], fill=(35, 32, 38))
        d.rectangle([x0 + 76, y0 + 22, x0 + 110, y0 + h], fill=(35, 32, 38))
        d.polygon([(x0 + 112, y0 + h - 4), (x0 + 112, y0 + 4), (x0 + 116, y0 + 4),
                   (x0 + 116, y0 + h - 4)], fill=(35, 32, 38))
        for fx in range(x0 + 14, x0 + 106, 16):
            d.polygon([(fx, y0 + h), (fx + 6, y0 + h - 20), (fx + 12, y0 + h)],
                      fill=(255, 140, 20))
        d.ellipse([x0 + 140, y0 + 4, x0 + 160, y0 + 20], fill=(120, 115, 125))
        d.ellipse([x0 + 158, y0 + 10, x0 + 174, y0 + 24], fill=(100, 95, 105))
    elif kind == "wemby":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 142, 90))
        d.ellipse([x0 + w - 30, y0 + 6, x0 + w - 6, y0 + 30], fill=(230, 110, 30))
        d.arc([x0 + w - 34, y0 + 2, x0 + w - 2, y0 + 34], 0, 360, fill=(90, 40, 10), width=1)
        d.line([(x0 + 10, y0 + h - 12), (x0 + w - 10, y0 + h - 12)], fill=(255, 255, 255), width=2)
        d.ellipse([x0 + 20, y0 + h - 22, x0 + 34, y0 + h - 8], fill=(240, 120, 40))
    elif kind == "merkury":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(40, 90, 130))
        d.rectangle([x0, y0 + h - 10, x0 + w, y0 + h], fill=(25, 60, 95))
        d.polygon([(x0 + 60, y0 + 22), (x0 + 140, y0 + 22), (x0 + 132, y0 + h - 10),
                   (x0 + 68, y0 + h - 10)], fill=(30, 30, 35))
        d.line([(x0 + 96, y0 + 6), (x0 + 96, y0 + 22)], fill=(30, 30, 35), width=3)
        for sx, sy in [(x0 + 150, y0 + 12), (x0 + 160, y0 + 20)]:
            d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 170, 40))
        d.ellipse([x0 + 40, y0 + 10, x0 + 48, y0 + 18], fill=(20, 20, 20))
    elif kind == "gaza":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(120, 110, 95))
        d.rectangle([x0, y0 + h - 8, x0 + w, y0 + h], fill=(70, 65, 60))
        d.rectangle([x0 + 70, y0 + 18, x0 + 130, y0 + h - 8], fill=(240, 240, 240))
        d.rectangle([x0 + 70, y0 + 18, x0 + 96, y0 + h - 8], fill=(200, 30, 30))
        d.ellipse([x0 + 80, y0 + h - 12, x0 + 90, y0 + h - 2], fill=(20, 20, 20))
        d.ellipse([x0 + 112, y0 + h - 12, x0 + 122, y0 + h - 2], fill=(20, 20, 20))
        d.ellipse([x0 + 150, y0 + 4, x0 + 166, y0 + 18], fill=(90, 85, 80))
        d.ellipse([x0 + 162, y0 + 10, x0 + 176, y0 + 22], fill=(105, 100, 95))
    elif kind == "korea":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(150, 150, 145))
        d.rectangle([x0 + 60, y0 + 10, x0 + 140, y0 + h], fill=(90, 90, 100))
        d.rectangle([x0 + 66, y0 + 26, x0 + 134, y0 + h], fill=(40, 40, 55))
        for dx in range(x0 + 72, x0 + 132, 16):
            d.rectangle([dx, y0 + 30, dx + 8, y0 + h - 4], fill=(255, 210, 90))
        d.line([(x0 + 150, y0 + 4), (x0 + 150, y0 + h)], fill=(220, 220, 220), width=2)
        d.polygon([(x0 + 150, y0 + 4), (x0 + 166, y0 + 8), (x0 + 150, y0 + 12)],
                  fill=(30, 90, 180))
    elif kind == "verstappen":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(25, 25, 35))
        for i in range(8):
            for j in range(2):
                if (i + j) % 2 == 0:
                    d.rectangle([x0 + 8 + i * 12, y0 + 6 + j * 12,
                                 x0 + 20 + i * 12, y0 + 18 + j * 12], fill=(255, 255, 255))
        d.rectangle([x0 + 110, y0 + 24, x0 + 180, y0 + 32], fill=(200, 30, 30))
        d.ellipse([x0 + 118, y0 + 30, x0 + 128, y0 + h - 4], fill=(15, 15, 15))
        d.ellipse([x0 + 164, y0 + 30, x0 + 174, y0 + h - 4], fill=(15, 15, 15))
        d.line([(x0 + 10, y0 + h - 4), (x0 + w - 10, y0 + h - 4)], fill=(255, 200, 60), width=2)
    elif kind == "alcaraz":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(40, 110, 70))
        d.line([(x0, y0 + h // 2), (x0 + w, y0 + h // 2)], fill=(255, 255, 255), width=2)
        d.ellipse([x0 + 30, y0 + 8, x0 + 44, y0 + 22], fill=(220, 230, 60))
        d.ellipse([x0 + 150, y0 + 18, x0 + 164, y0 + 32], fill=(220, 230, 60))
        d.line([(x0 + 90, y0 + 6), (x0 + 110, y0 + h - 6)], fill=(255, 255, 255), width=2)


# ---------------------------------------------------------------- map
def project(lon, lat, mx0, my0, mw, mh):
    x = mx0 + (lon + 170) / 360.0 * mw
    y = my0 + (75 - lat) / 135.0 * mh
    return x, y


CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
           (-55, 47), (-70, 42), (-80, 32), (-90, 21), (-97, 16), (-105, 20),
           (-117, 33), (-125, 40), (-140, 60), (-168, 66)],
    "SA": [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-50, -30),
           (-60, -38), (-70, -50), (-73, -40), (-75, -20), (-80, -5), (-80, 10)],
    "EU": [(-10, 36), (-10, 44), (0, 48), (5, 58), (10, 58), (18, 56), (23, 60),
           (30, 60), (30, 55), (40, 50), (30, 45), (23, 40), (18, 40), (12, 44),
           (3, 43), (-2, 37), (-10, 36)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
           (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -29), (20, -35),
           (15, -30), (12, -18), (9, -1), (9, 4), (-8, 5), (-17, 15)],
    "AS": [(30, 60), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
           (160, 70), (178, 65), (170, 60), (162, 55), (158, 50), (142, 45),
           (140, 38), (130, 35), (127, 40), (122, 32), (120, 25), (110, 20),
           (105, 10), (100, 8), (95, 15), (90, 22), (80, 15), (75, 10), (70, 20),
           (60, 25), (55, 27), (50, 30), (48, 30), (42, 35), (38, 40), (30, 42),
           (30, 55), (30, 60)],
    "OC": [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
           (140, -38), (146, -39), (150, -37), (153, -27), (146, -19), (142, -11),
           (136, -12), (132, -12), (126, -14), (122, -17), (118, -20), (113, -22)],
    "JP": [(130, 31), (132, 33), (135, 35), (138, 38), (140, 40), (142, 43),
           (144, 44), (141, 42), (138, 36), (134, 34), (130, 31)],
    "ID": [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
           (125, -9), (130, -4), (135, -3), (140, -8), (138, -5), (130, -2),
           (120, -2), (110, 0), (100, 5), (95, 5)],
    "UK": [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 53), (1, 51), (-5, 50)],
}

# story num -> (lon, lat, dx, dy) pin offsets in px
PINS = {
    1: (30.7, 36.9, -14, -4),    # Antalya
    2: (30.5, 50.5, 0, -8),      # Kyiv/Dymer
    3: (50.6, 26.2, 12, -10),    # Bahrain
    4: (114.2, 22.3, 0, 0),      # Hong Kong
    5: (174.8, -41.3, 0, 0),     # Wellington (India Test in NZ)
    6: (-77.0, 38.9, 0, 0),      # Washington
    7: (106.2, -6.3, 0, 0),      # Cikande, Java
    8: (-98.5, 29.4, 0, 0),      # San Antonio
    9: (20.1, 32.1, -14, 2),     # Benghazi
    10: (34.5, 31.5, 2, 8),      # Gaza
    11: (127.0, 37.6, 0, 0),     # Seoul
    12: (-115.1, 36.2, 0, 0),    # Las Vegas
    13: (7.7, 45.1, 0, 0),       # Turin
    14: (24.7, 59.4, 0, 0),      # Tallinn
    18: (51.4, 35.7, 14, -2),    # Tehran
    21: (77.2, 28.6, 0, 0),      # Delhi
    28: (32.5, 15.5, 0, 0),      # Khartoum
    33: (151.2, -33.9, 0, 0),    # Sydney
}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle([0, 0, W - 1, H - 1], outline=RED, width=3)

    # ---- masthead
    d.text((16, 6), "THE WORLD IN ONE DAY", font=f_kick, fill=RED)
    d.text((W - 16 - d.textlength("36 STORIES · 7 REGIONS", font=f_kick), 6),
           "36 STORIES · 7 REGIONS", font=f_kick, fill=NAVY)
    d.text((16, 14), "SUNDAY 22 NOVEMBER 2026", font=f_mast, fill=INK)
    d.line([(16, 60), (W - 16, 60)], fill=RED, width=2)
    d.text((16, 64), "COP31 collapses  ·  186 drones over Ukraine  ·  Bahrain radar claim — the day the world said no",
           font=F("DejaVuSans.ttf", 11), fill=(120, 30, 40))

    # ---- number strip
    y = 82
    d.rectangle([0, y, W, y + 26], fill=NAVY)
    strip = [("186", "drones"), ("161", "down"), ("720/9", "India"),
             ("98.79%", "HK vote"), ("$120bn", "dropped"),
             ("35%", "power 2035"), ("44h", "OT"),
             ("50", "Wemby"), ("24", "Nigeria"),
             ("2", "radars"), ("16", "crew safe"), ("258", "Dems")]
    x = 10
    for num, lab in strip:
        nw = d.textlength(num, font=f_strip_n)
        d.text((x, y + 2), num, font=f_strip_n, fill=GOLD)
        x += nw + 4
        lw = d.textlength(lab, font=f_strip_l)
        d.text((x, y + 7), lab, font=f_strip_l, fill=(255, 255, 255))
        x += lw + 12
    # ---- region bar
    y = 110
    counts = [("EUROPE", 8), ("MIDDLE EAST", 7), ("ASIA-PACIFIC", 7), ("AMERICAS", 5),
              ("AFRICA", 3), ("OCEANIA", 3), ("WORLD", 3)]
    total = 36
    x = 0
    for name, n in counts:
        wseg = int((n / total) * W)
        d.rectangle([x, y, x + wseg, y + 20], fill=REGION_COLORS[name])
        label = f"{REGION_SHORT[name]} {n}"
        tw = d.textlength(label, font=f_bar)
        d.text((x + (wseg - tw) / 2, y + 3), label, font=f_bar, fill=(255, 255, 255))
        x += wseg

    # ---- UTC strip
    y = 132
    d.text((16, y + 3), "THE DAY IN UTC", font=f_utc_h, fill=RED)
    utc = [("01:00", "HK polls"), ("03:00", "objections close"),
           ("06:00", "approval session"), ("16:00", "COP31 ends, no deal"),
           ("17:00", "ATP final"), ("18:13", "Dems 258"),
           ("23:00", "wires close")]
    x = 126
    for t, lab in utc:
        d.text((x, y + 3), t, font=f_utc_h, fill=NAVY)
        x += d.textlength(t, font=f_utc_h) + 4
        d.text((x, y + 4), lab, font=f_utc, fill=INK)
        x += d.textlength(lab, font=f_utc) + 10
        d.text((x, y + 3), "·", font=f_utc_h, fill=RED)
        x += 10

    # ---- heroes
    hy, hh = 156, 168
    heroes = [
        dict(num=1, region="MIDDLE EAST", kick="CLIMATE · ANTALYA",
             title="NO DEAL", scene=scene_cop31,
             body="Final text drops fossil fuels; EU + ~130 parties refuse it. Talks end after 44 hours overtime — first collapse since 2009.",
             src="Reuters · AP", chip="CONFIRMED"),
        dict(num=2, region="EUROPE", kick="WAR · UKRAINE",
             title="186 DRONES, 161 DOWN", scene=scene_drones,
             body="Russia fires 186 drones at Ukraine overnight; 161 shot down or jammed. A block in Dymer collapses — 1 killed, 14 unaccounted. Strikes in 18 places.",
             src="Ukrainian Air Force", chip="REPORTED"),
        dict(num=3, region="MIDDLE EAST", kick="GULF · BAHRAIN",
             title="2 RADARS “HIT”", scene=scene_patriot,
             body="Iran claims 2 US Patriot radars hit in Bahrain, al-Riffa and Awali. Bahrain denies a military strike — a civilian site in Sitra burns, 2 hurt, no deaths.",
             src="IRGC · Bahrain MoI", chip="CLAIM"),
    ]
    hx = 10
    hw = 330
    for hro in heroes:
        d.rectangle([hx, hy, hx + hw, hy + hh], outline=NAVY, width=1, fill=(255, 255, 255))
        col = REGION_COLORS[hro["region"]]
        d.rectangle([hx, hy, hx + hw, hy + 16], fill=col)
        d.text((hx + 6, hy + 2), hro["kick"], font=f_hero_k, fill=(255, 255, 255))
        d.text((hx + hw - 34, hy + 2), "HERO", font=f_chip, fill=(255, 220, 100))
        hro["scene"](d, hx + 1, hy + 17, hw - 2, 60)
        ty = hy + 17 + 60 + 4
        d.text((hx + 8, ty), hro["title"], font=f_hero_h, fill=INK)
        ty += 28
        lines = wrap(d, hro["body"], f_hero_b, hw - 16)
        ty = text_block(d, hx + 8, ty, lines[:3], f_hero_b, INK, 13)
        d.text((hx + 8, hy + hh - 16), hro["src"], font=f_src, fill=(90, 90, 90))
        cw = chip(d, hx + hw - 78, hy + hh - 17, hro["chip"])
        hx += hw + 7

    # ---- small cards (2 rows x 5)
    cards = [
        dict(num=4, region="EUROPE", kick="EUROPE · HONG KONG", title="98.79% TURNOUT",
             scene="hk", body="Election Committee vote: 856 candidates, 723 seats. 5,640 of 5,709 voters cast ballots.",
             src="Reuters", chip="CONFIRMED"),
        dict(num=5, region="ASIA-PACIFIC", kick="ASIA-PACIFIC · CRICKET", title="INDIA DECLARE 720/9",
             scene="india", body="Highest Test total in New Zealand. Rahul 136, Pant 128 as India pile on the runs.",
             src="Reuters", chip="CONFIRMED"),
        dict(num=6, region="AMERICAS", kick="AMERICAS · WASHINGTON", title="DEMS TAKE HOUSE, 258",
             scene="dems", body="Hubbard beats Foxx by 330 in NC recount. Largest majority since 1992; 4 races uncalled.",
             src="AP · Reuters", chip="CONFIRMED"),
        dict(num=7, region="ASIA-PACIFIC", kick="ASIA-PACIFIC · INDONESIA", title="FACTORY FIRE: 3 DEAD",
             scene="cikande", body="Candy-plant blaze in Cikande: 3 killed, 36 missing, 15 survived. Fire began Saturday night.",
             src="Detiknews · Basarnas", chip="REPORTED"),
        dict(num=8, region="AMERICAS", kick="AMERICAS · NBA", title="WEMBY SCORES 50",
             scene="wemby", body="50 points, 19 rebounds, 5 blocks as Spurs beat Pelicans 114–91.",
             src="AP", chip="CONFIRMED"),
        dict(num=9, region="MIDDLE EAST", kick="MIDDLE EAST · BENGHAZI", title="CORVETTE HIT AT SEA",
             scene="merkury", body="Russian corvette Merkury hit by sea drones in Benghazi; ship lists, several killed. Blame disputed.",
             src="AP · Reuters", chip="CLAIM"),
        dict(num=10, region="MIDDLE EAST", kick="MIDDLE EAST · GAZA", title="AID VAN STRUCK, 3 DEAD",
             scene="gaza", body="Drone strike hits food-aid van in Tel al-Hawa; Israeli fire kills 4. Hamas seeks mediator talks. WCK: van was not ours.",
             src="Reuters", chip="REPORTED"),
        dict(num=11, region="ASIA-PACIFIC", kick="ASIA-PACIFIC · SEOUL", title="MINISTER QUITS OVER AI CHEAT",
             scene="korea", body="Education minister Choi Kyo-jin resigns after CSAT chaos; 111 device-cheating cases found.",
             src="Yonhap · Reuters", chip="CONFIRMED"),
        dict(num=12, region="EUROPE", kick="EUROPE · LAS VEGAS GP", title="VERSTAPPEN WINS BY 0.639s",
             scene="verstappen", body="Beats Norris in Las Vegas; Piastri third. His 75th Grand Prix win.",
             src="Reuters", chip="CONFIRMED"),
        dict(num=13, region="EUROPE", kick="EUROPE · ATP FINALS", title="ALCARAZ TAKES FIRST TITLE",
             scene="alcaraz", body="Beats Zverev 6–2, 7–6(7) to win his first ATP Finals crown.",
             src="AP", chip="CONFIRMED"),
    ]
    cy, chh = 330, 148
    cw_ = 200
    for i, c in enumerate(cards):
        row, col_i = divmod(i, 5)
        cx = 10 + col_i * (cw_ + 3)
        cy0 = cy + row * (chh + 4)
        d.rectangle([cx, cy0, cx + cw_, cy0 + chh], outline=(150, 140, 120), width=1,
                    fill=(255, 255, 255))
        strip_scene(d, cx + 1, cy0 + 1, cw_ - 2, 38, c["scene"])
        d.rectangle([cx, cy0 + 39, cx + cw_, cy0 + 52], fill=REGION_COLORS[c["region"]])
        d.text((cx + 5, cy0 + 41), f"{c['num']:02d}  {c['kick']}", font=f_card_k,
               fill=(255, 255, 255))
        ty = cy0 + 56
        tlines = wrap(d, c["title"], f_card_t, cw_ - 10)
        ty = text_block(d, cx + 5, ty, tlines[:2], f_card_t, INK, 15)
        blines = wrap(d, c["body"], f_card_b, cw_ - 10)
        ty = text_block(d, cx + 5, ty + 2, blines[:3], f_card_b, INK, 12)
        d.text((cx + 5, cy0 + chh - 14), c["src"], font=f_src, fill=(90, 90, 90))
        chip(d, cx + cw_ - 76, cy0 + chh - 15, c["chip"])

    # ---- map + ALSO list
    my, mh = 634, 152
    d.text((16, my), "WHERE IT HAPPENED — EVERY HERO PINNED", font=f_map_h, fill=NAVY)
    mx0, my0, mw = 10, my + 16, 500
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh - 16], fill=OCEAN, outline=NAVY, width=1)
    for poly in CONTINENTS.values():
        pts = [project(lon, lat, mx0, my0, mw, mh - 16) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LANDLINE)
    for num, (lon, lat, dx, dy) in PINS.items():
        px, py = project(lon, lat, mx0, my0, mw, mh - 16)
        px, py = px + dx, py + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((px - d.textlength(t, font=f_pin) / 2, py - 5), t, font=f_pin,
               fill=(255, 255, 255))
    d.text((mx0, my0 + mh - 14), "PIN KEY: numbers match the stories. Red pins = heroes 1–3.",
           font=f_src, fill=(90, 90, 90))

    also = [
        (14, "EUROPE", "Estonia shuts 5 Russia crossings", "Reuters"),
        (15, "EUROPE", "Denmark expels Russian attaché", "Reuters"),
        (16, "EUROPE", "Belgian controllers join Mon strike", "Reuters"),
        (17, "EUROPE", "Sparta II still burning, towed home", "Reuters"),
        (18, "MIDDLE EAST", "Iran starts power rationing, ~2h cuts", "Reuters"),
        (19, "MIDDLE EAST", "Eisenkot invites Likud to talks", "Israeli media"),
        (20, "MIDDLE EAST", "Settlers burn 12 cars in West Bank", "Guardian"),
        (21, "ASIA-PACIFIC", "Nepal PM Balen Shah lands in Delhi", "Reuters"),
        (22, "ASIA-PACIFIC", "Manipur liquor toll rises", "Reuters"),
        (23, "ASIA-PACIFIC", "EU–Indonesia trade deal signed", "Reuters"),
        (24, "ASIA-PACIFIC", "Marles rejects US AUKUS subs report", "Reuters"),
        (25, "AMERICAS", "Bolsonaro in intensive care, stable", "Reuters"),
        (26, "AMERICAS", "Falcon 9 launches NROL-136", "SpaceX"),
        (27, "AMERICAS", "FBI probes NCIC database hack", "Reuters"),
        (28, "AFRICA", "Drones kill 4 near Khartoum", "AP"),
        (29, "AFRICA", "Mourners' boat capsizes; 24 dead", "Reuters"),
        (30, "AFRICA", "Ebola in DR Congo: 11,613 cases", "WHO"),
        (31, "OCEANIA", "Melbourne marks 70 yrs since 1956", "AAP"),
        (32, "OCEANIA", "Fred Nile dies at 92 (died 21 Nov)", "Guardian"),
        (33, "OCEANIA", "Cummins stays Australia Test captain", "Cricket Australia"),
        (34, "WORLD", "Bitcoin back above $60,000", "Reuters"),
        (35, "WORLD", "Nvidia faces SEC probe; shares -14%", "Reuters"),
        (36, "WORLD", "Liverpool thrash Man Utd 4–0", "Reuters"),
    ]
    ax = 526
    d.text((ax, my), "ALSO ON SUNDAY — 23 MORE STORIES", font=f_map_h, fill=NAVY)
    d.line([(ax, my + 14), (W - 10, my + 14)], fill=NAVY, width=1)
    colw = 238
    for i, (num, region, title, src) in enumerate(also):
        col_i, row_i = divmod(i, 12)
        rx = ax + col_i * (colw + 6)
        ry = my + 20 + row_i * 13
        d.rectangle([rx, ry, rx + 16, ry + 11], fill=REGION_COLORS[region])
        t = f"{num:02d}"
        d.text((rx + (16 - d.textlength(t, font=f_pin)) / 2, ry + 1), t, font=f_pin,
               fill=(255, 255, 255))
        tt = title
        while d.textlength(tt, font=f_also) > colw - 20 and len(tt) > 10:
            tt = tt[:-1]
        if tt != title:
            tt = tt.rstrip() + "…"
        d.text((rx + 19, ry), tt, font=f_also, fill=INK)

    # ---- DATE CHECK
    dy = 794
    d.rectangle([10, dy, W - 10, dy + 150], outline=RED, width=3, fill=(253, 240, 240))
    d.rectangle([10, dy, W - 10, dy + 22], fill=RED)
    d.text((16, dy + 4), "DATE CHECK — EVERY STORY HAPPENED OR WAS FIRST REPORTED SUNDAY 22 NOVEMBER 2026",
           font=f_dc_h, fill=(255, 255, 255))
    y = dy + 28
    y = text_block(d, 16, y, wrap(d, "Wires read to 23:00 UTC. Every story on this page happened or was first "
           "reported on 22 Nov 2026, unless its kicker says otherwise. Numbers in the strip match the "
           "stories: 186 / 161 / 720/9 / 98.79% / $120bn / 35% / 44h / 50 / 24 / 2 / 16 / 258.",
           f_dc, W - 32), f_dc, INK, 13)
    y += 4
    y = text_block(d, 16, y, wrap(d, "LEFT OUT — not Sunday stories: 400-drone / 110-missile barrage (19–20 Nov) · "
           "El Chapo Isidro captured (20 Nov) · BepiColombo Mercury orbit (21 Nov, burn 18:24 GMT) · "
           "Kryvyi Rih (20 Nov night) · Peru quake (20 Nov) · Hormuz tankers Torkel + Arina (hit Sat 21 Nov "
           "05:00 GMT, reported Sun 17:13 UTC) · Mongolia snap vote (resignation 19 Nov).",
           f_dc, W - 32), f_dc, INK, 13)
    y += 4
    y = text_block(d, 16, y, wrap(d, "DATE SPLIT — reported both days, carried as REPORTED: EU–Indonesia deal "
           "(21 vs 22 Nov) · Nigeria boat (20 vs 22 Nov) · FBI NCIC hack (20/21 Nov) · Sparta II hit Sat 21, "
           "still burning Sun.",
           f_dc, W - 32), f_dc, INK, 13)
    y += 4
    text_block(d, 16, y, wrap(d, "NOT YET — undecided when drawn: 4 House races uncalled · COP32 venue not set · "
           "Gaza ceasefire talks: no deal announced.", f_dc, W - 32), f_dc, INK, 13)

    # ---- footer
    fy = 950
    d.text((16, fy), "SOURCES: AP · Reuters · BBC · CNN · Al Jazeera · The Guardian · Yonhap · Detiknews · "
           "Basarnas · MONTSAME · WHO · ICC · ATP · FIA · SpaceX", font=f_foot, fill=(70, 70, 70))
    d.text((16, fy + 13), "LEGEND: CONFIRMED = 2+ outlets · REPORTED = wires that day · CLAIM = one side, "
           "unverified · ONGOING = still developing", font=f_foot, fill=(70, 70, 70))
    d.text((16, fy + 26), "PENDING = undecided · OFFICIAL = recorded result · FORECAST = not yet happened",
           font=f_foot, fill=(70, 70, 70))
    d.text((16, fy + 39), "Scenes are drawn illustrations, not photographs. 36 stories · 7 regions · "
           "Wires read to 23:00 UTC. — THE WORLD IN ONE DAY", font=f_foot, fill=(70, 70, 70))

    img.save("entry.png", optimize=True)
    img.resize((300, 300)).save("preview300.png")
    # crops for zoom verification
    img.crop((0, 150, 1024, 330)).save("crop-heroes.png")
    img.crop((0, 330, 1024, 630)).save("crop-cards.png")
    img.crop((0, 630, 1024, 800)).save("crop-map.png")
    img.crop((0, 790, 1024, 950)).save("crop-datecheck.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
