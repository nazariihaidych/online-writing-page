# Image guidelines

## Naming

- Lowercase ASCII letters, numbers, hyphens only
- No spaces, underscores, or Cyrillic characters
- Descriptive: `irving-shaw-bread.webp`, not `img001.webp`

## Format

- **WebP** — photos and illustrations (best compression, modern support)
- **PNG** — logos, icons, UI elements with transparency

## Folder structure

```
assets/images/
├── about/
│   ├── photo.png          — author photo (About page)
│   ├── books/             — book cover thumbnails
│   └── music/             — music/playlist thumbnails
├── site/
│   ├── home-banner.png    — hero banner (homepage)
│   ├── email-icon.png     — contact page icon
│   ├── owp-icon.png       — site favicon / brand icon
│   └── mock/              — UI mockup screenshots
└── stories/
    └── <story-slug>/
        └── cover.png      — story cover image
```

New story covers go in `stories/<slug>/cover.png`.  
New media thumbnails go in `about/books/` or `about/music/`.  
Site-level assets (banners, icons) go in `site/`.
