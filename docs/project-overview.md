# Project Overview

A Jekyll 4.4 static site for Ukrainian prose — stories, media collections, and personal pages. Hosted on GitHub Pages, no backend, no build pipeline beyond Jekyll.

---

## Stack

- **Jekyll 4.4** — static site generator
- **IBM Plex Mono** — single font throughout, loaded from Google Fonts
- **No JS build step** — all CSS in one file, all JS inlined in includes
- **Plugins:** `jekyll-feed` (RSS), `jekyll-seo-tag` (meta tags)

---

## Structure

```
_layouts/       — page shells (default, story)
_includes/      — reusable partials (header, footer, head, media-cards, effects)
_stories/       — story Markdown files
_data/          — YAML data for media pages
pages/          — static pages (about, contact, explanations, media pages)
assets/
  css/          — style.css (single file, no preprocessor)
  images/       — organized into about/, site/, stories/
scripts/        — dev tooling (add-media.py)
docs/           — project documentation
```

---

## Pages

| URL | File | Description |
|-----|------|-------------|
| `/` | `index.html` | Homepage — story card grid |
| `/about/` | `pages/about.md` | Author bio + media collections |
| `/explanations/` | `pages/explanations.md` | FAQ-style toggle sections |
| `/contact/` | `pages/contact.md` | Email contact |
| `/movies/` | `pages/movies.md` | Film cards |
| `/series/` | `pages/series.md` | Series cards |
| `/music/` | `pages/music.md` | Music cards |
| `/books/` | `pages/books.md` | Book cards |
| `/podcasts/` | `pages/podcasts.md` | Podcast cards |
| `/youtube/` | `pages/youtube.md` | YouTube channel cards |
| `/stories/:name/` | `_stories/*.md` | Individual story pages |

---

## Adding a story

Create `_stories/my-story.md`:

```markdown
---
title: Назва оповідання
date: 2026-06-30
cover_image: /assets/images/stories/my-story/cover.png
cover_color: "linear-gradient(135deg, #f8a84b, #c94070)"
rain: true   # optional visual effect
fog: true    # optional visual effect
---

Текст оповідання тут...
```

Place the cover image at `assets/images/stories/my-story/cover.png`. Stories are sorted by `date` descending on the homepage.

---

## Adding media entries

Use the script from the project root:

```bash
python3 scripts/add-media.py "<url>" <page>
```

Supported pages: `movies`, `series`, `music`, `books`, `podcasts`, `youtube`

```bash
python3 scripts/add-media.py "https://www.imdb.com/title/tt1375666/" movies
python3 scripts/add-media.py "https://www.goodreads.com/book/show/..." books "Читаю"
python3 scripts/add-media.py "https://open.spotify.com/album/..." music "Альбоми"
```

IMDB requires `OMDB_KEY` — see [google-analytics.md](google-analytics.md) for the GA4 setup pattern; same idea: add to `~/.zshrc`:

```bash
echo 'export OMDB_KEY=your_key_here' >> ~/.zshrc && source ~/.zshrc
```

---

## Theming

Light/dark mode via CSS custom properties. OS preference is followed automatically; user can override with the toggle (saved to `localStorage`).

Key variables:
- `--yellow: #FFCE00` — primary accent
- `--bg`, `--text`, `--border` — change under `[data-theme="dark"]`
- Dark palette: `--bg: #0D0D0D`, `--text: #E8E4DC`, `--border: #242424`

---

## Visual effects

Pages opt in via front matter:

- `rain: true` — animated canvas rain
- `fog: true` — animated fog blobs

Both automatically show a floating toggle button (bottom-right) that lets the user pause/resume. Respects `prefers-reduced-motion`.

---

## Editable content

Page text lives in separate files — edit them like stories:

| File | Page |
|------|------|
| `_includes/content/home-intro.md` | Homepage intro |
| `_includes/content/about-text.md` | About page bio |
| `_includes/content/contact-text.md` | Contact page intro |
| `_data/explanations.yml` | Explanations page sections |

Full formatting reference: [docs/content-guide.md](content-guide.md)

---

## Analytics

Google Analytics 4 — configured in `_config.yml`:

```yaml
google_analytics: G-XXXXXXXXXX
```

Loads only on production builds (GitHub Pages sets `JEKYLL_ENV=production` automatically). See [docs/google-analytics.md](google-analytics.md) for setup instructions.

---

## Local development

```bash
bundle install
bundle exec jekyll serve --livereload
```

Build for production:

```bash
bundle exec jekyll build
```
