# Client

The browser UI: a Flask app (Jinja templates + static CSS/JS) that renders the pages and talks to `server/` over `API_BASE_URL`. It has no business logic of its own — every action is a fetch call to the gateway.

## Setup

```bash
cd client
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Edit `static/js/config.js` if the gateway isn't at the default address:

```js
const API_BASE_URL = window.API_BASE_URL || "http://localhost:5000";
```

## Run

The server (gateway) must be running first (see `server/README.md`), which in turn needs the agent running (see `agent/README.md`).

```bash
python wsgi.py
```

Open `http://localhost:8000`.

For production, run behind a WSGI server instead:

```bash
gunicorn wsgi:app -b 0.0.0.0:8000
```

## Adding a new page

1. Add a template in `templates/` that extends `base.html` (see `templates/index.html` for an example).
2. Add a route for it in `app/blueprints/pages.py` (or a new blueprint if the page group needs its own URL prefix), returning `render_template("your_page.html")`.
3. Link to it from `templates/base.html`'s navbar if it should be reachable from every page.

## Structure

```
app/
  __init__.py            # create_app() — points Flask at templates/ and static/
  blueprints/pages.py     # page routes
templates/
  base.html               # shared layout (navbar, CSS/JS includes)
  index.html              # Upload / Ask / Generate page
static/
  css/style.css
  js/config.js            # API_BASE_URL
  js/app.js               # fetch calls + DOM wiring for index.html
wsgi.py
requirements.txt
```
