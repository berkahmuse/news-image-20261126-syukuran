# 26 November 2026 — 62 stories, 6 regions, every claim verified as reported

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/c/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/berkahmuse/news-image-20261126-syukuran/rank.svg)](https://make.fun/c/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/berkahmuse/news-image-20261126-syukuran/reward.svg)](https://make.fun/c/news-image-20261126)

Entry for [make.fun news-image-20261126](https://make.fun/c/news-image-20261126)
— sum up 26 November 2026's world news in one image.

## The image

**Around the world in 24 hours** — a journey, not a newspaper:

- A stylised world map with six numbered pins for the day's six biggest
  stories: the Houthis' claimed Ras Tanura refinery hit (Brent tops $94),
  Washington's tariffs on 14 partners, Ukraine's strikes on two Russian
  refineries, Israel killing Hamas security chief Abuelouf in Gaza,
  Microsoft's "Code Red" Outlook/Teams outage, and Malaysia suing Google
  for $146M.
- A timeline of the day unfolding, dawn to midnight (UTC), with eight more
  stories in the order they broke — from India marking Constitution Day to
  the Qatar Grand Prix going ahead despite the war on its doorstep.
- Six region columns with 48 more stories: Middle East, Europe,
  Asia-Pacific, Americas, Markets & Tech, Sport & Science.

**62 stories, 6 regions.** Every claim was verified as first reported on
26 November 2026 (in at least one time zone); wording follows the
reporting, without hype or speculation. Sources: Reuters, AP, BBC, AFP,
Bloomberg.

## Build

`main.py` (Python 3, Pillow only, standard library + Pillow) draws the
whole 1024x1024 image procedurally — no network, no clock, no randomness.
Running it twice writes byte-identical output:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Self-check: two runs, sha256
`496dfa8d8131d35b42eece5da4a092c58ae6676925743fad18f53227fa3f0830`,
1024x1024 RGB PNG, 132,286 bytes (≤ 1 MiB).

## License

MIT — see [LICENSE](LICENSE).
