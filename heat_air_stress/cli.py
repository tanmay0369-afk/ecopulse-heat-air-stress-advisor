"""Command-line demo.
  python -m heat_air_stress.cli --sample summer_heatwave --job delivery_rider --lang hi
  python -m heat_air_stress.cli --live 28.45 77.50 --job construction      (needs internet)
"""
import argparse, json, pathlib
from .scoring import stress, safer_hours, runs, LEVEL_NAMES, JOBS
from .advice import build_advice

SAMPLES = pathlib.Path(__file__).resolve().parent.parent / "data" / "sample_days.json"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sample", default="summer_heatwave")
    p.add_argument("--live", nargs=2, type=float, metavar=("LAT", "LON"))
    p.add_argument("--job", default="street_vendor", choices=JOBS)
    p.add_argument("--alert", default="none", choices=["none", "yellow", "orange", "red"])
    p.add_argument("--lang", default="en", choices=["en", "hi"])
    a = p.parse_args()
    if a.live:
        from .data_fetch import fetch_hourly
        hourly, label = fetch_hourly(*a.live), "LIVE Open-Meteo data"
    else:
        hourly, label = json.loads(SAMPLES.read_text(encoding="utf-8"))[a.sample], f"SIMULATED sample day: {a.sample}"
    res = safer_hours(hourly, a.job, a.alert)
    peak = max(res["rows"], key=lambda r: (r["score"], r["heat_level"] + r["air_level"], r["heat_index_c"]))
    print(label, "| job:", a.job)
    print("Peak stress:", LEVEL_NAMES[peak["score"]], f"at {peak['hour']}:00 (heat index {peak['heat_index_c']} C)")
    print("Best hours to work:", runs(res["best_work_hours"]) or "no clearly safer window today")
    print("Rest hours:", runs(res["rest_hours"]) or "none flagged")
    print("\n".join(build_advice(peak, a.lang)))


if __name__ == "__main__":
    main()
