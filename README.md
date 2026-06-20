# Desvio Astral

Desvio Astral is a 2D avoidance/survival game. The main implementation uses Python and Pygame, and the repository also includes a browser-playable version for quick online testing.

## Run locally with Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Test online in the browser

Open `web/index.html` directly in a browser, or serve it locally:

```bash
python -m http.server 8000 -d web
```

Then open:

```text
http://localhost:8000
```

## GitHub Pages deployment

This repository includes a GitHub Actions workflow that publishes the `web/` folder to GitHub Pages.

1. Push the branch to GitHub.
2. In the repository settings, enable **Pages** with **GitHub Actions** as the source.
3. Open the URL shown by GitHub Pages after the workflow finishes.

## Controls

- Left / Right arrow keys: move the spaceship.
- Enter: start or restart.
