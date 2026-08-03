# Google Analytics 4

The site has GA4 tracking built in. The snippet loads only on production builds — it is silently skipped during local development.

## How to enable

### 1. Create a GA4 property

1. Go to [analytics.google.com](https://analytics.google.com) and sign in
2. Click **Admin** (bottom-left gear icon) → **Create** → **Property**
3. Enter a name, select your timezone and currency, click **Next**
4. Fill in business details, click **Create**
5. Choose **Web** as the platform
6. Enter your site URL and stream name, click **Create stream**
7. Copy the **Measurement ID** — it looks like `G-XXXXXXXXXX`

### 2. Add the ID to `_config.yml`

Open `_config.yml` and replace the placeholder:

```yaml
google_analytics: G-XXXXXXXXXX  # ← replace this
```

with your real Measurement ID:

```yaml
google_analytics: G-A1B2C3D4E5
```

That's it. Commit and push — GitHub Pages builds with `JEKYLL_ENV=production` automatically, so the snippet will be injected into every page on the live site.

## How it works

The gtag snippet is included at the bottom of `_includes/head.html` behind two conditions:

```liquid
{% if site.google_analytics and jekyll.environment == "production" %}
```

- **`site.google_analytics`** — must be set in `_config.yml` (non-empty)
- **`jekyll.environment == "production"`** — GitHub Pages sets this automatically; your local `bundle exec jekyll serve` leaves it as `"development"`, so the script never loads locally

## Testing locally

If you need to verify the snippet appears in the HTML output:

```bash
JEKYLL_ENV=production bundle exec jekyll serve
```

Then open any page and search the source for `googletagmanager` — you should see the gtag script tags.

## What you can track in GA4

Once live, open [analytics.google.com](https://analytics.google.com) and go to your property:

- **Realtime** — visitors on the site right now
- **Reports → Acquisition** — where traffic comes from (search, direct, social)
- **Reports → Engagement → Pages and screens** — which pages/stories get the most views
- **Reports → Demographics** — countries, languages
- **Explore** — custom reports, funnels, path analysis

GA4 tracks page views, scrolls, outbound clicks, and session duration out of the box with no extra configuration.
