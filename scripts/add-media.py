#!/usr/bin/env python3
"""
Add a media entry to _data/<page>.yml.

Usage:
  python3 scripts/add-media.py "<url>" <page> ["section"]

────────────────────────────────────────────────────────────
PAGES & SECTIONS
────────────────────────────────────────────────────────────

  music      — Spotify track/album/playlist, YouTube playlist or channel
               Sections: "З нового" | "Плейлисти" | "Окремі композиції" | "Альбоми"
               Default section: "Плейлисти"
               Example:
                 python3 scripts/add-media.py "https://open.spotify.com/album/..." music "Альбоми"
                 python3 scripts/add-media.py "https://open.spotify.com/track/..." music "З нового"

  movies     — IMDB film URL (requires OMDb API key)
               Section: "Фільми" (single section, no need to specify)
               Example:
                 python3 scripts/add-media.py "https://www.imdb.com/title/tt0468569/" movies

  series     — IMDB series URL (requires OMDb API key)
               Sections: "Дивлюсь" | "З недавніх | Рекомендую"
               Default section: "Серіали" — ALWAYS specify the section explicitly
               Example:
                 python3 scripts/add-media.py "https://www.imdb.com/title/tt4574334/" series "З недавніх | Рекомендую"

  podcasts   — Spotify show, YouTube playlist or YouTube channel
               Section: "Подкасти" (single section, no need to specify)
               Example:
                 python3 scripts/add-media.py "https://open.spotify.com/show/..." podcasts
                 python3 scripts/add-media.py "https://youtube.com/playlist?list=..." podcasts

  books      — Goodreads book URL or any generic web URL
               Sections: "Читаю" | "Сподобалось | Рекомендую"
               Default section: "Книги" — ALWAYS specify the section explicitly
               Example:
                 python3 scripts/add-media.py "https://www.goodreads.com/book/show/..." books "Читаю"

  youtube    — YouTube channel URL
               Section: "Канали" (single section, no need to specify)
               Example:
                 python3 scripts/add-media.py "https://youtube.com/@channel" youtube

────────────────────────────────────────────────────────────
NOTES
────────────────────────────────────────────────────────────

  • IMDB (movies/series): requires OMDB_KEY env var.
    Get a free key at omdbapi.com/apikey.aspx, then run once:
      echo 'export OMDB_KEY=your_key_here' >> ~/.zshrc && source ~/.zshrc
    Or inline:
      OMDB_KEY=your_key_here python3 scripts/add-media.py "https://www.imdb.com/title/tt..." movies

  • Spotify: no key needed — uses oEmbed + embed page metadata

  • YouTube: no key needed — uses oEmbed for playlists/videos,
    og tags for channels

  • Goodreads: no key needed — scrapes og tags + JSON-LD author
"""
import sys, json, re, os
import urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent

PAGE_DEFAULTS = {
    "music":    "Плейлисти",
    "movies":   "Фільми",
    "series":   "Серіали",
    "podcasts": "Подкасти",
    "books":    "Книги",
    "youtube":  "Канали",
}

def ua():
    return {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

def clean_url(url):
    url = url.replace("\\", "")
    parsed = urllib.parse.urlparse(url)
    drop = {"si", "feature", "from_search", "from_srp", "qid", "rank", "ac"}
    qs = {k: v for k, v in urllib.parse.parse_qsl(parsed.query) if k not in drop}
    return parsed._replace(query=urllib.parse.urlencode(qs)).geturl()

def fetch(url, timeout=12):
    req = urllib.request.Request(url, headers=ua())
    try:
        return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", errors="ignore")
    except Exception as e:
        raise SystemExit(f"Fetch failed ({e})\nURL: {url}") from None

def fetch_json(url, timeout=12):
    return json.loads(fetch(url, timeout))

def og_tags(html):
    tags = {}
    for m in re.finditer(r'<meta[^>]+property=["\']og:([^"\']+)["\'][^>]+content=["\']([^"\']*)["\']', html, re.I):
        tags[m.group(1)] = m.group(2)
    for m in re.finditer(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']og:([^"\']+)["\']', html, re.I):
        tags[m.group(2)] = m.group(1)
    return tags

def _pisni(n):
    n = abs(n) % 100
    if 11 <= n <= 19:
        return "пісень"
    m = n % 10
    if m == 1:
        return "пісня"
    if 2 <= m <= 4:
        return "пісні"
    return "пісень"

def _sezony(n):
    try:
        n = int(n)
    except (ValueError, TypeError):
        return ""
    if n % 10 == 1 and n % 100 != 11:
        return f"{n} сезон"
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return f"{n} сезони"
    return f"{n} сезонів"

def spotify_entity(url):
    path = urllib.parse.urlparse(url).path
    html = fetch(f"https://open.spotify.com/embed{path}")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.+?)</script>', html, re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))["props"]["pageProps"]["state"]["data"]["entity"]
    except Exception:
        return {}

def handle_spotify(url):
    kind = urllib.parse.urlparse(url).path.strip("/").split("/")[0]
    oe = fetch_json(f"https://open.spotify.com/oembed?url={urllib.parse.quote(url)}")
    e = spotify_entity(url)

    if kind == "show":
        title = oe.get("title", "") or e.get("name", "")
        # og:description = "Podcast · {publisher} · {actual description}"
        html = fetch(url)
        og = og_tags(html)
        desc = og.get("description", "")
        parts = desc.split(" · ", 2)
        subtitle = parts[2][:120] if len(parts) >= 3 else desc[:120]
    else:
        title = oe.get("title", "")
        subtitle = ""
        if e.get("artists"):
            subtitle = e["artists"][0]["name"]
        elif e.get("subtitle"):
            subtitle = e["subtitle"]

    year = ""
    rd = e.get("releaseDate") or {}
    if isinstance(rd, dict) and rd.get("isoString"):
        year = rd["isoString"][:4]

    tracks = len(e.get("trackList", []))
    extra = f"{tracks} {_pisni(tracks)}" if tracks else ""

    return dict(title=title, subtitle=subtitle, year=year, extra=extra,
                thumbnail=oe.get("thumbnail_url", ""), aspect="square", platform="spotify")

def handle_youtube(url):
    is_channel = "/@" in url or "/channel/" in url or "/c/" in url or "/user/" in url

    if is_channel:
        html = fetch(url)
        og = og_tags(html)
        thumb = re.sub(r'=s\d+', '=s200', og.get("image", ""))
        if "yt3.googleusercontent.com" in thumb and "=s200" not in thumb:
            thumb += "=s200-c-k-c0x00ffffff-no-rj"
        return dict(title=og.get("title", ""), subtitle=og.get("description", "")[:100],
                    thumbnail=thumb, aspect="square", platform="youtube")

    oe = fetch_json(f"https://www.youtube.com/oembed?url={urllib.parse.quote(url)}&format=json")
    return dict(title=oe.get("title", ""), subtitle=oe.get("author_name", ""),
                thumbnail=oe.get("thumbnail_url", ""), aspect="square", platform="youtube")

def handle_imdb(url):
    tt = re.search(r"tt\d+", url)
    if not tt:
        raise SystemExit(f"No IMDB ID found in: {url}")
    key = os.environ.get("OMDB_KEY")
    if not key:
        raise SystemExit("OMDB_KEY env var is not set. Get a free key at omdbapi.com/apikey.aspx")
    d = fetch_json(f"http://www.omdbapi.com/?i={tt.group()}&apikey={key}")
    if d.get("Response") != "True":
        raise SystemExit(f"OMDb error: {d.get('Error')}")

    is_series = d.get("Type") == "series"
    extra = _sezony(d.get("totalSeasons", "")) if is_series else d.get("Genre", "")
    subtitle = d.get("Director", "")
    if not subtitle or subtitle == "N/A":
        subtitle = d.get("Genre", "")
    thumb = d.get("Poster", "").replace("_V1_SX300.jpg", "_V1_SX600.jpg")
    if thumb == "N/A":
        thumb = ""

    return dict(title=d.get("Title", ""), subtitle=subtitle,
                year=d.get("Year", ""), extra=extra,
                thumbnail=thumb, aspect="poster", platform="imdb")

def handle_goodreads(url):
    html = fetch(url)
    og = og_tags(html)
    title = og.get("title", "").replace(" | Goodreads", "").strip()
    author = ""
    m = re.search(r'"author"\s*:\s*\{[^}]+"name"\s*:\s*"([^"]+)"', html)
    if m:
        author = m.group(1)
    if not author:
        for m2 in re.finditer(r'application/ld\+json["\']>(.+?)</script>', html, re.DOTALL):
            try:
                data = json.loads(m2.group(1))
                a = data.get("author")
                if isinstance(a, list) and a:
                    author = a[0].get("name", "")
                elif isinstance(a, dict):
                    author = a.get("name", "")
                if author:
                    break
            except Exception:
                pass
    return dict(title=title, subtitle=author,
                thumbnail=og.get("image", ""), aspect="poster", platform="goodreads")

def handle_generic(url):
    html = fetch(url)
    og = og_tags(html)
    return dict(title=og.get("title", url), subtitle="",
                thumbnail=og.get("image", ""), aspect="square", platform="web")

def detect(url):
    if "spotify" in url:
        return handle_spotify(url)
    if "youtube" in url or "youtu.be" in url:
        return handle_youtube(url)
    if "imdb.com" in url:
        return handle_imdb(url)
    if "goodreads.com" in url:
        return handle_goodreads(url)
    return handle_generic(url)

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    url = clean_url(sys.argv[1])
    page = sys.argv[2].lower()
    if page not in PAGE_DEFAULTS:
        raise SystemExit(f"Unknown page '{page}'. Options: {', '.join(PAGE_DEFAULTS)}")

    section = sys.argv[3] if len(sys.argv) > 3 else PAGE_DEFAULTS[page]
    meta = detect(url)

    block_lines = [f"- section: {section}", f"  url: {url}", f'  title: "{meta["title"]}"']
    if meta.get("subtitle"):
        block_lines.append(f'  subtitle: "{meta["subtitle"]}"')
    if meta.get("year"):
        block_lines.append(f'  year: "{meta["year"]}"')
    if meta.get("extra"):
        block_lines.append(f'  extra: "{meta["extra"]}"')
    block_lines += [f'  thumbnail: {meta.get("thumbnail", "")}',
                    f'  aspect: {meta.get("aspect", "square")}',
                    f'  platform: {meta["platform"]}']
    new_block = "\n".join(block_lines) + "\n"

    data_file = ROOT / "_data" / f"{page}.yml"
    file_lines = data_file.read_text(encoding="utf-8").splitlines(keepends=True)

    insert_at = None
    for i, line in enumerate(file_lines):
        if line.rstrip() == f"- section: {section}":
            insert_at = i
            break

    if insert_at is not None:
        file_lines[insert_at:insert_at] = (new_block + "\n").splitlines(keepends=True)
    else:
        if file_lines and file_lines[-1] != "\n":
            file_lines.append("\n")
        file_lines += ("\n" + new_block).splitlines(keepends=True)

    data_file.write_text("".join(file_lines), encoding="utf-8")

    print(f"Added to {page}.yml: {meta['title']}  [{meta['platform']}] → {section}")

if __name__ == "__main__":
    main()
