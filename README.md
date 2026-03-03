# Synthgubbar.com

Band homepage for **Synthgubbar** — a Swedish synthwave quartet.

## Site Structure

```
index.html          ← Live countdown page (visible at synthgubbar.com)
neon/
  index.html        ← Full site (staging, code-protected)
  img/              ← Album cover images (640x640 JPGs)
CNAME               ← Custom domain config for GitHub Pages
```

## How It Works

- Hosted on **GitHub Pages** from the `master` branch
- Pure HTML/CSS/JS — no build tools, no dependencies
- Push to `master` and the site updates automatically (takes ~1 minute)

## Access Code

The `/neon/` staging site is protected with an access code: **242**

This is a client-side gate (not real security) — just to keep casual visitors out before launch.

## Launch Plan

On **Friday March 6, 2026 at 18:00 CET**:
1. Copy `neon/index.html` → `index.html` (replace the countdown)
2. Push to `master`
3. The full site goes live at synthgubbar.com

## Making Changes

### Quick text edits
1. Edit `neon/index.html` directly on GitHub (pencil icon)
2. Commit — site updates in ~1 minute

### Local editing
```bash
git clone https://github.com/XerxBot/synthgubbar.git
cd synthgubbar
# Edit files, then:
git add .
git commit -m "Description of change"
git push
```

Open `neon/index.html` in a browser to preview locally before pushing.

### Song chapters
Each song is a `<section class="chapter">` block in `neon/index.html`. To edit a chapter's tagline text, search for the song title and edit the `<p class="chapter-tagline">` text.

### Album covers
Located in `neon/img/`. Filenames:
- `cover_you_and_i.jpg`
- `cover_electric_memories.jpg`
- `cover_between_the_silence.jpg`
- `cover_i_lost_you.jpg`
- `cover_tech_noir.jpg`
- `cover_back_to_the_light.jpg`

Replace with same filename to update. Keep images square (640x640 recommended).

## Spotify Links

- **Artist page:** https://open.spotify.com/artist/6JhKsdShjf1GwdUvsnDcPE
- **You and I:** https://open.spotify.com/track/02bLZeqSTshm6ghkTYpCgU
- **Electric Memories:** https://open.spotify.com/track/2thkRY6LnM4XD0YfCVGTln
- **Between the Silence:** https://open.spotify.com/track/7tC5kEe2ooE7TDCuOPjRyW
- **I Lost You:** https://open.spotify.com/track/3x73QZ66DJaRRB1oAhpuKI
- **Tech Noir (Kolingsborg):** https://open.spotify.com/track/1NrsESiYEPdWlcn4dk1Nlj
- **Back to the Light:** https://open.spotify.com/track/522je1XQrGS98h1Stsv0Jc

## Game

The Neon Overdrive game link points to `play.synthgubbar.com` (subdomain setup pending).

## Merch Shop
- **Live shop:** https://shop.synthgubbar.com/
- **On-site promo:** Pixel art character in the merch section runs in and says "Hey! Buy my tee!" — clickable for funny random quotes
- Fulfillment via [Spreadshirt](https://www.spreadshirt.com/) (do NOT expose to customers)

## Fonts

- **Audiowide** — headings, countdown, song titles
- **Rajdhani** — body text, labels

Both loaded from Google Fonts. No local font files needed.
