# Broken image/link paths on GitHub Pages (404s under `/assets/...`)

**Symptom:** images and internal links 404 in production (e.g. `https://nazariihaidych.github.io/assets/images/about/photo.png`).

**Root cause:** `_config.yml` sets:

```yaml
baseurl: "/online-writing-page"
url: "https://nazariihaidych.github.io"
```

This is a GitHub Pages *project* site, so it's served under a `/online-writing-page/` path prefix rather than at the domain root. Jekyll does not automatically prepend `baseurl` to hardcoded absolute paths — any link written as `/assets/...` or `/music` resolves to the domain root, missing the prefix entirely.

**Fix — pages, includes, layouts:** wrap the path in the `relative_url` filter, which prepends `site.baseurl` at build time:

```liquid
<img src="{{ '/assets/images/about/photo.png' | relative_url }}" alt="...">
<a href="{{ '/music' | relative_url }}">Музика</a>
```

`relative_url` is safe to apply even when the value might already be an absolute URL (`https://...` or `//...`) — it leaves those untouched and only rewrites paths starting with `/`. This matters for the fix below.

## The "fix every data file" trap — and the better pattern

Liquid tags (`{{ }}`, `{% %}`) only get parsed in files Jekyll runs through its templating engine (pages, layouts, includes, collection docs with front matter). Files under `_data/` are plain YAML — their string values are injected verbatim wherever `site.data.xxx` is referenced, so a `{{ '...' | relative_url }}` typed *inside* a data file prints out literally instead of being evaluated.

The first pass at this fix hardcoded the baseurl directly into each affected data file (`_data/explanations.yml`, `_data/music.yml`, `_data/books.yml` thumbnails, `assets/css/style.css`). That works but doesn't scale — every new local asset path added to any data file in the future needs the same manual prefix, and it silently breaks if `baseurl` ever changes.

**Better: apply `relative_url` once, in the template that consumes the data**, not in the data itself. The filter runs at render time regardless of where the string came from — data file, hardcoded literal, doesn't matter.

- `_includes/media-cards.html` renders `item.url` and `item.thumbnail` from `site.data.<music|books|movies|...>`. Fixed once, at the point of use:
  ```liquid
  <a href="{{ item.url | relative_url }}" ...>
    <img src="{{ item.thumbnail | relative_url }}" ...>
  ```
  Now *every* media entry across all 6 pages — present and future — is covered automatically. Local thumbnails (e.g. `/assets/images/about/music/ukr-rok.webp`) get prefixed; external ones (Spotify/YouTube/IMDb links, external cover art URLs) pass through unchanged. No data file needed editing.

- `pages/explanations.md` renders `section.content` as a raw HTML blob from `_data/explanations.yml` (arbitrary Markdown/HTML, not a single URL field), so `relative_url` can't be applied to the whole string directly. Used `replace` instead, to rewrite just the `/assets/` references before markdownifying:
  ```liquid
  {% capture assets_prefix %}"{{ site.baseurl }}/assets/{% endcapture %}
  {{ section.content | replace: '"/assets/', assets_prefix | markdownify }}
  ```
  Any future section added to `explanations.yml` with an embedded `<img src="/assets/...">` is covered automatically, no per-entry fix needed.

**Remaining exception — `assets/css/style.css`:** static assets under `assets/` have no front matter, so Jekyll copies them byte-for-byte and never runs Liquid over them at all — not even at the "apply the filter at the point of use" level, since there's no template rendering step for this file. Two options, neither applied automatically:
  1. Add empty front matter (`---\n---`) to the top of the file to opt it into Liquid processing, then use `{{ "..." | relative_url }}` inside `url(...)`. Untried here — means Jekyll re-parses the whole stylesheet as a template on every build.
  2. Hardcode the prefix, e.g. `url('/online-writing-page/assets/images/site/home-banner.png')` — what's currently in place. Only breaks if `baseurl` changes, and it's a single line.

**Files touched:** `pages/about.md`, `pages/contact.md`, `pages/explanations.md`, `_includes/media-cards.html`, `assets/css/style.css`. (`_data/explanations.yml`, `_data/music.yml`, `_data/books.yml` were reverted back to plain `/assets/...` paths once the template-level fix made the hardcoding unnecessary.)

**Prevention:** grep for hardcoded absolute paths before shipping new content:

```bash
grep -rn 'src="/\|href="/\|](/assets' --include="*.md" --include="*.html" .
```

Any match not already wrapped in `relative_url` (directly, or via the include/template that renders it) is a future 404. When adding a new template that renders a URL/path sourced from `_data/`, front matter, or anywhere else — wrap it in `relative_url` at that render point rather than normalizing the source data.
