#!/usr/bin/env python3
"""Render the 22 November 2026 world-news infographic, 1024x1024 PNG.

Stories verified from live news sources on the evening of 23 Nov 2026
(One Turn, Daily Summary of World, Reuters/AFP/AP via video roundup,
Candid Dragon evening briefing, Dainik Jagran).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
NAVY2 = (31, 48, 84)
RED = (178, 34, 34)
INK = (24, 24, 24)
GREY = (90, 90, 90)
RULE = (200, 192, 172)
CARD = (255, 255, 255)
ACCENT = (176, 141, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- Masthead ----------
d.rectangle([0, 0, W, 148], fill=NAVY)
d.rectangle([0, 148, W, 154], fill=ACCENT)
f_mast = font(SERIF_B, 66)
f_sub = font(SANS_B, 21)
d.text((36, 26), "22 NOVEMBER 2026", font=f_mast, fill=(255, 255, 255))
d.text((36, 104), "SUNDAY  •  THE WORLD IN ONE PAGE", font=f_sub, fill=(214, 196, 140))
d.text((W - 36, 104), "WORLD NEWS", font=f_sub, fill=(214, 196, 140), anchor="ra")

# ---------- Lead story: COP31 ----------
y = 176
f_kick = font(SANS_B, 20)
f_lead_h = font(SANS_B, 40)
f_lead_b = font(SANS, 22)
d.text((36, y), "CLIMATE  •  COP31 IN ANTALYA, TURKIYE", font=f_kick, fill=RED)
y += 32
d.text((36, y), "Climate talks collapse", font=f_lead_h, fill=INK)
y += 52
d.text((36, y), "without a deal", font=f_lead_h, fill=INK)
y += 56
y = para(d, 36, y, "The UN climate summit ends with no agreement after the EU "
        "and others reject a final text that does not even mention "
        "\u201cfossil fuels\u201d.", f_lead_b, (60, 60, 60), 952, 30)
d.line([36, y + 8, W - 36, y + 8], fill=RULE, width=2)

# ---------- Two-column grid ----------
def card(x, y, w, h, kicker, kcolor, headline, body, hsize=27, bsize=20):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=RULE, width=1)
    d.text((x + 18, y + 14), kicker, font=font(SANS_B, 17), fill=kcolor)
    yy = y + 42
    yy = para(d, x + 18, yy, headline, font(SANS_B, hsize), INK, w - 36, hsize + 6)
    para(d, x + 18, yy + 6, body, font(SANS, bsize), (70, 70, 70), w - 36, bsize + 6)

gy = 396
card(36, gy, 466, 196, "CONFLICT  •  STRAIT OF HORMUZ", RED,
     "Two tankers hit mines",
     "Iran says two supertankers struck naval mines east of Hormuz and "
     "caught fire; a strike hits a civilian site in Bahrain.")
card(522, gy, 466, 196, "POLITICS  •  UNITED STATES", RED,
     "Democrats' biggest win since 1992",
     "A North Carolina recount gives Democrats at least 258 House seats, "
     "their largest majority in 34 years.")
gy = 608
card(36, gy, 466, 196, "ECONOMY  •  MARKETS", NAVY2,
     "Stocks slide as AI sell-off spreads",
     "The S&P 500 falls 3.7% and the Nasdaq 5.3%; Japan's Nikkei drops "
     "5.06% as the rout reaches Asia.")
card(522, gy, 466, 196, "WAR  •  UKRAINE", NAVY2,
     "Drone hits flats near Kyiv",
     "Fourteen missing after a Russian drone strikes a block in Dymer; a "
     "Russian warship is hit at Benghazi, Libya.")

# ---------- Bottom strip: four short items ----------
d.line([36, 828, W - 36, 828], fill=RULE, width=2)
d.text((36, 842), "ALSO TODAY", font=font(SANS_B, 18), fill=GREY)
items = [
    ("MEXICO", "Cartel boss captured",
     "El Chapo Isidro seized in Sinaloa; 11 killed in the raid."),
    ("INDONESIA", "Factory fire in Cikande",
     "Three dead, 36 missing after a candy factory fire."),
    ("SPACE", "BepiColombo reaches Mercury",
     "European-Japanese probe enters Mercury orbit."),
    ("SPORT  •  NBA", "Harden passes Kobe",
     "James Harden scores 51 in the Cavaliers' win over Indiana."),
]
bx, bw, gap = 36, 226, 16
for i, (kick, head, body) in enumerate(items):
    x = bx + i * (bw + gap)
    if i:
        d.line([x - gap // 2, 872, x - gap // 2, 972], fill=RULE, width=1)
    d.text((x, 872), kick, font=font(SANS_B, 14), fill=RED)
    yy = para(d, x, 894, head, font(SANS_B, 18), INK, bw, 22)
    para(d, x, yy + 3, body, font(SANS, 15), (70, 70, 70), bw, 19)

# ---------- Footer ----------
d.line([36, 992, W - 36, 992], fill=RULE, width=1)
d.text((36, 999), "Sources: Reuters, AP, AFP, Al Jazeera  •  22 November 2026",
       font=font(SANS, 14), fill=GREY)

img.save("/home/hatch/workspace/makefun/news-image-20261122/entry.png")
print("saved", img.size)
