# Heat-Air Stress Advisor — Team EcoPulse (2026CSAE102)

Rule-based advisor that combines Heat Index (NWS Rothfusz regression) and PM2.5 (CPCB bands) into a single **0–3 Stress Score** (0 Low, 1 Moderate, 2 High, 3 Severe) for outdoor workers in Delhi-NCR, adjusts for occupational exertion, identifies safer working hours and rest periods, and delivers short plain-language advice in **English and Hindi**.

> **Disclaimer:** General safety advisory only, not medical advice. Sample scenarios in `data/sample_days.json` and `index.html` are clearly labelled as **SIMULATED**; live forecasts are fetched via Open-Meteo (CC-BY 4.0).

## Team EcoPulse (Bennett University — 2026CSAE102)
- **Tanmay Dhummy** (`S26CSEU3103`) — Team Leader, Core Scoring Engine & Documentation
- **Adarsh Gupta** (`S26CSEU3132`) — Live Data Fetching, Validation & App Audit
- **Aditya Singh** (`S26CSEU3113`) — Mobile Web UI, Bilingual Advice & SDG/BMC Mapping
- **Anshuman Singh** (`S26CSEU3092`) — Testing, Primary Survey Analysis & Secondary Research
- **Faculty Coordinator:** Dr. Saurabh Mittal

## Repository Structure
- `index.html` — Mobile-first bilingual (English/Hindi) web prototype (deploy directly via GitHub Pages)
- `heat_air_stress/scoring.py` — Heat index, CPCB PM2.5 & AQI levels, interaction + exertion rules, safer-hours search
- `heat_air_stress/advice.py` — Bilingual (English/Hindi) plain-language advice templates
- `heat_air_stress/data_fetch.py` — Live hourly weather & PM2.5 fetcher from Open-Meteo (no API key required; attribute Open-Meteo)
- `heat_air_stress/cli.py` — Command-line demo runner (supports `--sample` and `--live LAT LON`)
- `data/sample_days.json` — 4 simulated 24-hour Delhi-NCR reference scenarios (Summer Heatwave, Winter Smog, Humid Pre-Monsoon, Mild Day)
- `tests/test_scoring.py` — 18 unit tests covering heat index, boundaries, IMD overrides, interaction/exertion rules, safer-hours, and bilingual advice

## Quick Start
```bash
pip install -r requirements.txt          # Required only for --live mode
python -m unittest discover -v           # Run all 18 unit tests
python -m heat_air_stress.cli --sample summer_heatwave --job delivery_rider --lang hi
python -m heat_air_stress.cli --live 28.45 77.50 --job construction
```

## Verification Summary
- **Unit Tests:** 18 / 18 passing (`python -m unittest discover -v`)
- **Python vs. Web JS Parity:** 2,304 / 2,304 combinations matched (4 scenarios × 24 hours × 6 jobs × 4 IMD alert levels; 0 mismatches)

## Live Web Deployment (GitHub Pages — 30 Seconds)
1. Push this repository to GitHub (public repo).
2. Go to **Settings → Pages → Deploy from a branch → `main` / `/ (root)` → Save**.
3. Your live mobile prototype URL (`https://<username>.github.io/<repo-name>/`) will go live automatically from `index.html`.

## Scoring Rules (0–3 Scale)
1. **Heat level (HI °C):** `< 32` = 0, `32–<39` = 1, `39–<51` = 2, `≥ 51` = 3 (IMD Orange alert raises heat level to `≥ 2`; Red alert sets it to `3`).
2. **Air level (CPCB PM2.5 µg/m³):** `≤ 60` = 0, `61–90` = 1, `91–120` = 2, `> 120` = 3.
3. **Base & Interaction:** `base = max(heat_level, air_level)`; if both `≥ 2`, add `+1` (capped at `3`).
4. **Job-Exertion Uplift:** For high-exertion jobs (`delivery_rider`, `construction`, `sanitation`), add `+1` when `base ≥ 1` (capped at `3`).

## Known Limitations
- Open-Meteo provides gridded model data rather than street-level sensor readings.
- Comparing hourly PM2.5 values against 24-hour CPCB breakpoints is an approximation documented for transparency.
- Thresholds are a transparent starting design pending clinical/NCDC review. No personal user data is stored.
