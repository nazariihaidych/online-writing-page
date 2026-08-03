# Local development

## Run the site

```bash
bundle exec jekyll serve --livereload
```

Open `http://localhost:4000` in your browser. The `--livereload` flag automatically refreshes the page on file changes.

## Check if the server is running

```bash
curl -I http://localhost:4000
```

`HTTP/1.1 200 OK` — running. `Connection refused` — not running.

## Reload

Jekyll watches for file changes and rebuilds automatically. If something looks stale, stop the server with `Ctrl+C` and start it again.

## Run on a specific port

Useful when testing multiple sites at the same time:

```bash
bundle exec jekyll serve --port 4001
bundle exec jekyll serve --port 4002
```

Each site is then available at its own port: `http://localhost:4001`, `http://localhost:4002`, etc.

## Run in background

```bash
bundle exec jekyll serve --livereload &
```

The `&` sends the process to the background. Jekyll prints its PID on start — note it if you want to stop it later.

## Stop a background server

Find the process:

```bash
lsof -ti :4000
```

Kill it:

```bash
kill $(lsof -ti :4000)
```

Or if you noted the PID when starting:

```bash
kill <PID>
```
