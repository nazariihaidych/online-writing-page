# Content Styling Guide

Reference for all styling options available in `.md` content files
(`_includes/content/` and `_data/explanations.yml`).

---

## Text formatting

```md
**жирний текст**
*курсив*
~~закреслений~~
```

---

## Paragraphs

Empty line between paragraphs:

```md
Перший абзац.

Другий абзац.
```

Soft line break (two spaces at end of line):

```md
Перший рядок  
Другий рядок без нового абзацу.
```

---

## Links

```md
[текст посилання](https://example.com)
```

---

## Blockquote

Renders with a yellow left border, muted italic text:

```md
> Це цитата або важлива думка.
```

---

## Yellow highlight

```md
Звичайний текст і <mark>виділений жовтим</mark> текст.
```

---

## Colored text

```md
<span style="color: #E6B800">темно-жовтий текст</span>
<span style="color: var(--yellow)">акцентний жовтий</span>
<span style="color: var(--muted)">приглушений текст</span>
```

---

## Callout box

Standard yellow callout:

```md
<div class="callout">
Текст всередині жовтої підказки.
</div>
```

Border only, no background:

```md
<div class="callout callout--outline">
Текст без жовтого фону, тільки рамка.
</div>
```

---

## Lists

Unordered:

```md
- пункт один
- пункт два
- пункт три
```

Ordered:

```md
1. перший
2. другий
3. третій
```

---

## Horizontal rule

```md
---
```

## Section breaks in stories

Horizontal line:

```md
---
```

Centered asterism (literary section break):

```md
<p class="asterism">* * *</p>
```

---

## Headings

```md
# H1
## H2
### H3
#### H4
```

**Important:** Markdown headings do NOT work inside HTML tags (e.g. inside `<div class="callout">`). Use a real HTML tag instead:

```md
<div class="callout callout--outline">
<h4 style="color: #E6B800; margin: 0 0 0.5rem;">Заголовок</h4>

Текст абзацу тут.
</div>
```

`margin: 0 0 0.5rem` shorthand means: top=0, right=0, bottom=0.5rem, left=0.

---

## Images

Full-width image:

```md
![опис](/assets/images/your-photo.jpg)
```

Full-width with custom style:

```md
<img src="/assets/images/your-photo.jpg" alt="опис" style="width: 100%; border-radius: 4px; margin-bottom: 0.75rem;">
```

Small image floated left (text wraps around it):

```md
<img src="/assets/images/your-photo.jpg" alt="опис" style="width: 200px; float: left; margin: 0 1rem 0.5rem 0;">
```

**Note:** image file must be in `assets/images/`. Inside HTML blocks (e.g. inside `<div class="callout">`), use the `<img>` tag — Markdown `![]()` syntax won't work there.

---

## Inline HTML

Any HTML tag works inline:

```md
Текст з <strong>html тегом</strong> всередині.
```

---

## Story front matter options

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Story title — required |
| `date` | date | Publication date — required |
| `cover_image` | path | e.g. `/assets/images/cover.png` |
| `cover_color` | CSS value | Fallback if no image, e.g. `"linear-gradient(135deg, #f8a84b, #c94070)"` |
| `cover_position` | CSS value | Position of the image on the **story page banner**. Format: `"horizontal vertical"`. Vertical: `0%` = top, `50%` = middle, `100%` = bottom. Example: `"center 82%"` |
| `card_position` | CSS value | Position of the image on the **homepage card**. Same format as `cover_position`. Example: `"center 30%"` |
| `fog` | `true` | Animated purple/gold fog background (Космічний) |
| `rain` | `true` | Animated rain canvas overlay (Силянка) |
| `first_draft` | date | Shown in story metadata |
| `part_of` | string | Collection name shown in metadata |
| `part_of_url` | path | Makes `part_of` a link |

### Adding a new visual effect

1. Add a new flag to the story front matter (e.g. `snow: true`)
2. Create `_includes/<effect>.html` with the effect markup/CSS/JS
3. Include it in `_layouts/default.html`: `{% if page.<effect> %}{% include <effect>.html %}{% endif %}`
4. Add the new element's selector to `getTargets()` in `_includes/effects-toggle.html`:
   ```js
   document.getElementById('<effect>-canvas')
   ```
5. Add the flag to the toggle condition in `_layouts/default.html`:
   ```liquid
   {% if page.fog or page.rain or page.<effect> %}
   ```

---

## Content files location

| File | Page |
|------|------|
| `_includes/content/home-intro.md` | Головна сторінка — вступний текст |
| `_includes/content/about-text.md` | Про мене — біографія |
| `_includes/content/contact-text.md` | Напишіть мені щось — вступний текст |
| `_data/explanations.yml` | Деякі пояснення — callout і всі розділи |
