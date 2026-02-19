# 🌟 Life Pattern Analyzer

> A revolutionary daily optimization engine that combines real-time location, weather, moon phase, and circadian rhythm science to predict your optimal daily schedule and energy levels.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-black?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)
![No API Key Required](https://img.shields.io/badge/API%20Key-Not%20Required-brightgreen)

---

## ✨ Features

- 🌍 **Location-aware** — Automatic IP-based geolocation
- 🌤️ **Weather-integrated** — Live data via [Open-Meteo](https://open-meteo.com/) (free, no key needed)
- 🌙 **Moon phase calculations** — Cosmic influence on focus, creativity & social energy
- 🧬 **Circadian rhythm optimization** — Science-backed energy curve modeling
- 📊 **24-hour prediction timeline** — Hourly recommendations for the next day
- 💡 **Personalized insights** — Actionable, confidence-scored tips
- 🎨 **Beautiful UI** — Fully self-contained single-file frontend

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/life-pattern-analyzer.git
cd life-pattern-analyzer
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python life_pattern_analyzer.py
```

Open your browser at **http://localhost:5555**

---

## 🌐 Deployment

### Deploy to Render (recommended — free tier)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New Web Service**.
3. Connect your GitHub repo.
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn life_pattern_analyzer:app`
   - **Environment:** Python 3

### Deploy to Railway

```bash
railway login
railway init
railway up
```

### Deploy to Heroku

```bash
heroku create your-app-name
git push heroku main
```

The included `Procfile` handles the start command automatically for Heroku and Railway.

---

## 📁 Project Structure

```
life-pattern-analyzer/
├── life_pattern_analyzer.py   # Main Flask app (backend + frontend)
├── requirements.txt           # Python dependencies
├── Procfile                   # Process file for Heroku / Railway
├── render.yaml                # Render deployment config
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🔌 APIs Used

| API | Purpose | Key Required? |
|-----|---------|---------------|
| [ip-api.com](http://ip-api.com) | IP geolocation | ❌ No |
| [Open-Meteo](https://open-meteo.com) | Weather data | ❌ No |
| Built-in math | Moon phase & circadian calculations | — |

---

## 🛠️ Configuration

The app runs on port `5555` locally. In production, the port is set automatically via the `PORT` environment variable (handled by `gunicorn`).

---

## 📄 License

[MIT](LICENSE) — free to use, modify, and distribute.
