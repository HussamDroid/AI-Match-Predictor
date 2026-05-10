# AI Match Predictor
A high-impact, real-time football analytics dashboard built with **Streamlit**, powered by **Poisson Distribution** and live data from the **Football-Data.org API**.

## Features
- **Massive Scoreboard UI:** High-visibility display for finished and upcoming matches.
- **AI Predictions:** Win/Loss/Draw probabilities calculated via Poisson Distribution using live team stats.
- **Dynamic Standings:** Real-time league tables with UCL and Relegation zone highlighting.
- **Multi-League Support:** Toggle between La Liga, Premier League, Bundesliga, Serie A, and Ligue 1.

## Tech Stack
- **Frontend:** Streamlit (Python)
- **Data:** Football-Data.org API
- **Logic:** Poisson Distribution Engine (Python/Math)

## How it Works
The app pulls current league standings to determine the "Attack Strength" and "Defense Strength" of each team. It then runs a Poisson simulation across 64 possible scorelines (0-0 through 7-7) to find the most likely outcome.

## Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone [[https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/HussamDroid/AI-Match-Predictor.git)]
   cd AI_Match_Predictor

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Configure Secrets:**
   ```bash
    Create a folder named .streamlit and a file inside it called secrets.toml:
    FOOTBALL_DATA_API_KEY = "your_api_key_here"

4. **Run the App**
   ```bash
    streamlit run app.py
