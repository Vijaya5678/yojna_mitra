# yojna_mitra

Simple demo web app to collect personal details and show Indian government schemes a person may be eligible for. This version is a minimal Python + Flask app (no FastAPI).

Run locally

1. Create a virtual environment (recommended) and activate it.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies and start the app

```bash
pip install -r requirements.txt
python app.py
```

3. Open http://localhost:3000 in your browser and use the form.

Notes

- Eligibility logic is a small set of demo heuristics in `app.py` for hackathon/demo use.
- If you'd like a Gemini integration or more advanced rules, I can add that next.
# yojna_mitra