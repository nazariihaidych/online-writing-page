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

**Fix — `_data/*.yml` content:** Liquid tags (`{{ }}`, `{% %}`) are only parsed in files Jekyll runs through its templating engine (pages, layouts, includes, collection docs with front matter). Files under `_data/` are parsed as plain YAML and their string values are injected verbatim wherever `site.data.xxx` is referenced — Liquid is never re-run over that string. So `{{ '...' | relative_url }}` typed inside a data file prints out literally instead of being evaluated.

Workaround used in `_data/explanations.yml`: hardcode the baseurl prefix directly, e.g. `/online-writing-page/assets/images/site/mock/mock-1.webp`. This is less portable — if `baseurl` ever changes, this line won't update automatically — but it's the only option for content living in a data file.

**Fix — `assets/css/style.css` (`url(...)` references):** static assets under `assets/` have no front matter, so Jekyll copies them byte-for-byte without ever running the Liquid engine over them — `relative_url` simply can't apply here unless front matter is added to the file (untried, since it means Jekyll re-parses the whole stylesheet as a template on every build). Same workaround as the data-file case: hardcode the baseurl prefix, e.g. `url('/online-writing-page/assets/images/site/home-banner.png')`.

**Files touched in this fix:** `pages/about.md`, `pages/contact.md`, `_data/explanations.yml`, `assets/css/style.css`.

**Prevention:** grep for hardcoded absolute paths before shipping new content:

```bash
grep -rn 'src="/\|href="/\|](/assets' --include="*.md" --include="*.html" .
```

Any match not already wrapped in `{{ '...' | relative_url }}` (or, for data files, not already prefixed with the baseurl) is a future 404.
