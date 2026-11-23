# News-image 22 Nov 2026 — the world in one page

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Sasikianlarasati/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Sasikianlarasati/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for make.fun's **"Sum up 22 November's world news in one image"**
bounty ($100 in USDC, 50 places paid): a program that writes one image of
the day's news to `/output/entry.png`.

## The image

`entry.png` (1024×1024) sums up Sunday 22 November 2026 — nine real stories
reported that day, verified against live news sources (Reuters, AP, AFP,
Al Jazeera) on the evening of 23 November 2026:

- **Lead — Climate:** COP31 talks in Antalya collapse with no deal; the final
  draft does not even mention "fossil fuels".
- **Conflict — Strait of Hormuz:** Iran says two supertankers struck naval
  mines east of Hormuz and caught fire; a strike hits a civilian site in
  Bahrain.
- **Politics — United States:** Democrats win their largest House majority
  since 1992 — at least 258 seats after a North Carolina recount.
- **Economy — Markets:** stocks slide as the AI sell-off spreads — S&P 500
  down 3.7%, Nasdaq 5.3%, Nikkei 5.06%.
- **War — Ukraine:** 14 missing after a Russian drone hits a block in Dymer,
  near Kyiv; a Russian warship is hit at Benghazi, Libya.
- **Also today:** cartel boss El Chapo Isidro captured in Sinaloa (11 killed
  in the raid); three dead and 36 missing after a candy factory fire in
  Cikande, Indonesia; BepiColombo enters orbit around Mercury; James Harden
  scores 51 and passes Kobe Bryant.

## Run

```sh
python3 main.py
```

Writes `entry.png` to `/output/entry.png`. Python 3.13 and its standard
library alone — deterministic (byte-identical on every run), no network.
