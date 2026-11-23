#!/usr/bin/env python3
"""Front page for 22 November 2026: the world in one page.

Draws a 1024x1024 PNG with Pillow only. The layout is built from
measured text: every block measures its wrapped lines first, reports
how tall it is, and the next block starts below it, so text can never
overlap. Nothing here is random and nothing depends on the clock, so
running it twice gives the same bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
SIDE = 38                      # outer margin, left and right
GUTTER = 18                    # gap between the two columns

# --- palette ------------------------------------------------------------
PAPER = (247, 242, 231)        # warm cream page
NAVY = (16, 28, 51)            # masthead band
GOLD = (201, 162, 75)          # masthead rule + masthead accents
INK = (24, 24, 24)             # headlines and body text
RED = (164, 18, 32)            # kickers
SLATE = (84, 84, 84)           # secondary text
CARD = (255, 255, 255)         # story card fill
CARD_EDGE = (205, 198, 184)    # card outline
HAIRLINE = (178, 170, 156)     # thin rules
DIVIDER = (216, 208, 192)      # vertical dividers in the bottom strip

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    """Load a DejaVu face; fall back to Pillow's built-in bitmap font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


# --- type scale ---------------------------------------------------------
F_DATE = load("DejaVuSerif-Bold.ttf", 72)
F_MAST_SUB = load("DejaVuSans-Bold.ttf", 23)
F_KICKER = load("DejaVuSans-Bold.ttf", 21)
F_KICKER_SM = load("DejaVuSans-Bold.ttf", 17)
F_LEAD_HEAD = load("DejaVuSerif-Bold.ttf", 44)
F_LEAD_DECK = load("DejaVuSans.ttf", 25)
F_HEAD = load("DejaVuSerif-Bold.ttf", 31)
F_BODY = load("DejaVuSans.ttf", 21)
F_STRIP_HEAD = load("DejaVuSans-Bold.ttf", 22)
F_STRIP_BODY = load("DejaVuSans.ttf", 18)
F_STRIP_TAG = load("DejaVuSans-Bold.ttf", 22)
F_FOOT = load("DejaVuSans.ttf", 17)


def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    """Draw stacked lines; return the y just below the last one."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# --- story copy (my own concise wording) -------------------------------
LEAD = {
    "kicker": "CLIMATE  •  COP31 IN ANTALYA, TÜRKIYE",
    "head": "Climate talks collapse without a deal",
    "deck": "The UN summit ends with no agreement after the EU and others "
            "reject a final text that does not even mention \u201cfossil fuels\u201d.",
}

GRID = [
    {
        "kicker": "CONFLICT  •  STRAIT OF HORMUZ",
        "colour": RED,
        "head": "Two tankers hit mines",
        "body": "Iran says two supertankers struck naval mines east of "
                "Hormuz and caught fire; a strike hits a civilian site "
                "in Bahrain.",
    },
    {
        "kicker": "POLITICS  •  UNITED STATES",
        "colour": RED,
        "head": "Democrats\u2019 biggest win since 1992",
        "body": "A North Carolina recount gives Democrats at least 258 "
                "House seats, their largest majority in 34 years.",
    },
    {
        "kicker": "ECONOMY  •  MARKETS",
        "colour": NAVY,
        "head": "Stocks slide as AI sell-off spreads",
        "body": "The S&P 500 falls 3.7% and the Nasdaq 5.3%; Japan\u2019s "
                "Nikkei drops 5.06% as the rout reaches Asia.",
    },
    {
        "kicker": "WAR  •  UKRAINE",
        "colour": NAVY,
        "head": "Drone hits flats near Kyiv",
        "body": "Fourteen missing after a Russian drone strikes a block "
                "in Dymer; a Russian warship is hit at Benghazi, Libya.",
    },
]

STRIP = [
    {
        "tag": "MEXICO",
        "head": "Cartel boss captured",
        "body": "El Chapo Isidro seized in Sinaloa; 11 killed.",
    },
    {
        "tag": "INDONESIA",
        "head": "Factory fire in Cikande",
        "body": "Three dead, 36 missing in a candy factory fire.",
    },
    {
        "tag": "SPACE",
        "head": "BepiColombo reaches Mercury",
        "body": "European-Japanese probe enters Mercury orbit.",
    },
    {
        "tag": "SPORT  •  NBA",
        "head": "Harden passes Kobe",
        "body": "James Harden scores 51 in the Cavaliers\u2019 win.",
    },
]


# --- builders -----------------------------------------------------------
def build_masthead(draw):
    """Navy band: big date, strapline, gold rule underneath."""
    draw.rectangle([0, 0, PAGE_W, 122], fill=NAVY)
    draw.text((SIDE, 10), "22 NOVEMBER 2026", font=F_DATE, fill=(255, 255, 255))
    draw.text((SIDE, 88), "SUNDAY  •  THE WORLD IN ONE PAGE",
              font=F_MAST_SUB, fill=GOLD)
    right = "WORLD NEWS"
    rw = draw.textlength(right, font=F_MAST_SUB)
    draw.text((PAGE_W - SIDE - rw, 88), right, font=F_MAST_SUB, fill=GOLD)
    draw.rectangle([0, 122, PAGE_W, 128], fill=GOLD)
    return 128


def build_lead(draw, top):
    """Lead story: red kicker, two-line serif headline, deck, rule."""
    y = top + 12
    y = draw_lines(draw, SIDE, y, [LEAD["kicker"]], F_KICKER, RED, 26)
    y += 4
    head_lines = wrap(draw, LEAD["head"], F_LEAD_HEAD, PAGE_W - 2 * SIDE)
    y = draw_lines(draw, SIDE, y, head_lines, F_LEAD_HEAD, INK, 52)
    y += 6
    deck_lines = wrap(draw, LEAD["deck"], F_LEAD_DECK, PAGE_W - 2 * SIDE)
    y = draw_lines(draw, SIDE, y, deck_lines, F_LEAD_DECK, INK, 29)
    y += 12
    draw.line([SIDE, y, PAGE_W - SIDE, y], fill=HAIRLINE, width=2)
    return y + 2


def card_lines(draw, story, inner_w):
    """Wrapped lines for one grid card, plus the height they need."""
    kicker = wrap(draw, story["kicker"], F_KICKER_SM, inner_w)
    head = wrap(draw, story["head"], F_HEAD, inner_w)
    body = wrap(draw, story["body"], F_BODY, inner_w)
    height = 14 + len(kicker) * 23 + 6 + len(head) * 36 + 8 + len(body) * 25 + 14
    return kicker, head, body, height


def draw_card(draw, story, x, y, w, h):
    """One white story card with kicker, headline and body."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12,
                           fill=CARD, outline=CARD_EDGE, width=2)
    inner = w - 40
    kicker, head, body, _ = card_lines(draw, story, inner)
    cy = y + 14
    cy = draw_lines(draw, x + 20, cy, kicker, F_KICKER_SM, story["colour"], 23)
    cy += 6
    cy = draw_lines(draw, x + 20, cy, head, F_HEAD, INK, 36)
    cy += 8
    draw_lines(draw, x + 20, cy, body, F_BODY, INK, 25)


def build_grid(draw, top):
    """Two rows of two cards; each row is as tall as its taller card."""
    col_w = (PAGE_W - 2 * SIDE - GUTTER) // 2
    y = top + 14
    for row in range(2):
        pair = GRID[row * 2: row * 2 + 2]
        heights = [card_lines(draw, s, col_w - 40)[3] for s in pair]
        row_h = max(heights)
        for i, story in enumerate(pair):
            x = SIDE + i * (col_w + GUTTER)
            draw_card(draw, story, x, y, col_w, row_h)
        y += row_h + 16
    draw.line([SIDE, y - 2, PAGE_W - SIDE, y - 2], fill=HAIRLINE, width=2)
    return y


def build_strip(draw, top):
    """'Also today': four short columns separated by thin rules."""
    y = top + 12
    y = draw_lines(draw, SIDE, y, ["ALSO TODAY"], F_STRIP_TAG, SLATE, 26)
    y += 8
    col_w = (PAGE_W - 2 * SIDE) // 4
    start_y = y
    bottom = start_y
    for i, item in enumerate(STRIP):
        x = SIDE + i * col_w
        inner = col_w - 22
        cy = start_y
        cy = draw_lines(draw, x, cy, [item["tag"]], F_KICKER_SM, RED, 22)
        cy += 5
        head = wrap(draw, item["head"], F_STRIP_HEAD, inner)
        cy = draw_lines(draw, x, cy, head, F_STRIP_HEAD, INK, 27)
        cy += 6
        body = wrap(draw, item["body"], F_STRIP_BODY, inner)
        cy = draw_lines(draw, x, cy, body, F_STRIP_BODY, SLATE, 22)
        bottom = max(bottom, cy)
    for i in range(1, 4):
        x = SIDE + i * col_w
        draw.line([x - 9, start_y + 2, x - 9, bottom - 2],
                  fill=DIVIDER, width=2)
    draw.line([SIDE, bottom + 12, PAGE_W - SIDE, bottom + 12],
              fill=HAIRLINE, width=2)
    return bottom + 14


def build_footer(draw, top):
    draw.text((SIDE, top), "Sources: Reuters, AP, AFP, Al Jazeera  •  22 November 2026",
              font=F_FOOT, fill=SLATE)


def render():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    y = build_masthead(draw)
    y = build_lead(draw, y)
    y = build_grid(draw, y)
    y = build_strip(draw, y)
    build_footer(draw, y + 6)
    img.save(OUT_PATH, "PNG", optimize=True)
    return OUT_PATH


if __name__ == "__main__":
    path = render()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")
