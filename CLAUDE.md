# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
bundle install

# Serve locally with live reload
bundle exec jekyll serve --livereload

# Build for production (output goes to _site/)
bundle exec jekyll build
```

## Architecture

This is a **Jekyll 4.4** static site in Ukrainian, authored by Назарій Гайдич. There is no JavaScript build step — all CSS is hand-written in `assets/css/style.css` and all JS is inlined in includes.

### Layouts

- `_layouts/default.html` — base shell (head + header + footer wrapping `{{ content }}`); accepts `body_class` front matter to inject a class on `<body>`
- `_layouts/story.html` — extends `default`; renders a single story with cover image or color, back-link, and the article body

### Collections

Stories live in `_stories/` as Markdown files and are output to `/stories/:name/` via the `stories` collection defined in `_config.yml`. Each story's front matter supports:

- `title`, `date` — required
- `cover_image` — path to an image in `assets/images/`
- `cover_color` — CSS color string used as fallback background on the card and story header

The homepage (`index.html`) iterates `site.stories` sorted by `date` descending and renders them as a 3-column card grid (`aspect-ratio: 2/1`).

### Adding a new story

Create a file in `_stories/`:

```markdown
---
title: Назва
date: 2026-06-21
cover_image: /assets/images/stories/my-story/cover.png  # or use cover_color below
cover_color: "linear-gradient(135deg, #f8a84b, #c94070)"
rain: true   # optional: canvas rain animation
fog: true    # optional: animated fog blobs
---

Текст оповідання тут...
```

Stories are sorted by `date` descending on the homepage.

### Theming

The site supports light/dark mode. CSS custom properties are defined in `:root` and overridden under `[data-theme="dark"]`. The OS preference is respected via `@media (prefers-color-scheme: dark)` — the site follows the system setting automatically unless the user clicks the toggle, which saves to `localStorage`. The primary accent colour is `--yellow: #FFCE00`. Font is **IBM Plex Mono** (monospace) throughout, loaded from Google Fonts with weights 400, 500, 700 and italic.

Dark mode palette: `--bg: #0D0D0D`, `--text: #E8E4DC`, `--border: #242424`.

### Per-page container widths

Container width is controlled via `body_class` in front matter, scoped in CSS:

- `page-home` → `max-width: 1300px` (index.html)
- `page-about` → `max-width: 845px` (pages/about.md)
- default → `max-width: 900px` (all other pages)

### Static pages

All pages live in `pages/`:

- `about.md` — Про мене: author photo (float left, 260×260px), bio text, collections grid
- `explanations.md` — Деякі пояснення: yellow callout + `<details>` toggle sections driven by `_data/explanations.yml`
- `contact.md` — Напишіть мені щось: intro text + email link button
- `music.md`, `books.md`, `movies.md`, `series.md`, `podcasts.md`, `youtube.md` — media category pages using `_includes/media-cards.html`

### Editable content files

Page text is extracted into separate files so it can be edited like stories:

| File | Page |
|------|------|
| `_includes/content/home-intro.md` | Main page intro paragraphs |
| `_includes/content/about-text.md` | About page bio text |
| `_includes/content/contact-text.md` | Contact page intro text |
| `_data/explanations.yml` | Explanations callout + all toggle sections |

These files support full Markdown syntax (bold, italic, links, blockquotes, lists, `<mark>`, `<div class="callout">`, inline HTML). See `docs/content-guide.md` for the full reference.

### Media pages

Each media category page uses `{% include media-cards.html data=site.data.<page> %}`. Data lives in `_data/<page>.yml`. Supported fields per entry:

- `section` — section name (groups cards under a heading)
- `url`, `title`, `subtitle`, `year`, `extra` — card content
- `thumbnail` — image URL
- `aspect` — `square` (music, YouTube, podcasts) or `poster` (books, movies, series)
- `platform` — `spotify` | `youtube` | `imdb` | `goodreads` | `web`
- `note` — optional small text shown below the section heading

Use `scripts/add-media.py` to add entries automatically:

```bash
python3 scripts/add-media.py "<url>" <page> ["section"]
```

See the script's docstring for per-page section names and examples.

### Navigation

Header (`_includes/header.html`) shows nav links on desktop. On mobile (≤640px) links are hidden behind a hamburger button that opens an absolute dropdown overlay. Theme toggle is always visible.

### Assets

- `assets/css/style.css` — all styles, single file, no preprocessor
- `assets/images/` — organized into subfolders (see `assets/images/IMAGES.md` for naming rules):
  - `about/photo.png` — author photo (260×260px, float on About page)
  - `about/books/` — book cover thumbnails
  - `about/music/` — music/playlist thumbnails
  - `site/home-banner.png` — hero banner (`background-position: center 10%`)
  - `site/email-icon.png`, `site/owp-icon.png` — contact icon, site favicon/brand icon
  - `site/mock/` — UI mockup screenshots
  - `stories/<story-slug>/cover.png` — one subfolder per story
- `assets/fonts/` — local fonts if added
- `favicon.png` — site favicon (root level)

### Visual effects

Pages and stories can opt into animated visual effects via front matter:

- `rain: true` — renders a canvas rain animation (`_includes/rain.html`); clips itself below the story cover banner on story pages
- `fog: true` — renders animated fog blobs (`.fog__blob` elements, styled in CSS)

Both effects together show a floating `#effects-toggle` button (sticky bottom-right, `_includes/effects-toggle.html`) that lets the user pause/resume. The toggle is wired up in `_layouts/default.html`:

```html
{% if page.rain %}{% include rain.html %}{% endif %}
{% if page.fog %}<div class="fog">…</div>{% endif %}
…
{% if page.fog or page.rain %}<div class="fx-anchor">{% include effects-toggle.html %}</div>{% endif %}
```

The rain effect respects `prefers-reduced-motion` (hidden via CSS + JS early-return). The toggle state is not persisted — it resets on each page load.

### Plugins

- `jekyll-feed` — generates `feed.xml`
- `jekyll-seo-tag` — injected via `{% seo %}` in `_includes/head.html`
