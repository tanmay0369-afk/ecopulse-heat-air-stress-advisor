"""Heat-Air Stress scoring engine (rule-based). Milestone 2 prototype.

Levels: 0 Low, 1 Moderate, 2 High, 3 Severe.
Thresholds are a starting design and must be reviewed against IMD/NCDC guidance.
"""
from math import sqrt

LEVEL_NAMES = ["Low", "Moderate", "High", "Severe"]
LEVEL_COLOURS = ["green", "yellow", "orange", "red"]
HIGH_EXERTION_JOBS = {"delivery_rider", "construction", "sanitation"}
JOBS = ["delivery_rider", "construction", "street_vendor", "driver", "security_guard", "sanitation"]


def heat_index_c(temp_c: float, rh: float) -> float:
    """Heat index (Rothfusz regression, NWS) in deg C from air temp (deg C) and relative humidity (%)."""
    t = temp_c * 9 / 5 + 32
    simple = 0.5 * (t + 61.0 + (t - 68.0) * 1.2 + rh * 0.094)
    if (simple + t) / 2 < 80:
        hi = simple
    else:
        hi = (-42.379 + 2.04901523 * t + 10.14333127 * rh - 0.22475541 * t * rh
              - 0.00683783 * t * t - 0.05481717 * rh * rh + 0.00122874 * t * t * rh
              + 0.00085282 * t * rh * rh - 0.00000199 * t * t * rh * rh)
        if rh < 13 and 80 <= t <= 112:
            hi -= ((13 - rh) / 4) * sqrt((17 - abs(t - 95)) / 17)
        elif rh > 85 and 80 <= t <= 87:
            hi += ((rh - 85) / 10) * ((87 - t) / 5)
    return (hi - 32) * 5 / 9


def heat_level(hi_c: float, imd_alert: str = "none") -> int:
    lvl = 0 if hi_c < 32 else 1 if hi_c < 39 else 2 if hi_c < 51 else 3
    if imd_alert == "orange":
        lvl = max(lvl, 2)
    elif imd_alert == "red":
        lvl = max(lvl, 3)
    return lvl


def air_level_from_pm25(pm25: float) -> int:
    """CPCB PM2.5 bands: <=60 Good/Satisfactory, 61-90 Moderate, 91-120 Poor, >120 Very Poor/Severe."""
    return 0 if pm25 <= 60 else 1 if pm25 <= 90 else 2 if pm25 <= 120 else 3


def air_level_from_aqi(aqi: float) -> int:
    """Indian AQI bands: 0-100, 101-200, 201-300, 301+."""
    return 0 if aqi <= 100 else 1 if aqi <= 200 else 2 if aqi <= 300 else 3


def combine(h: int, a: int, job: str = "street_vendor") -> int:
    base = max(h, a)
    if h >= 2 and a >= 2:          # interaction rule
        base = min(3, base + 1)
    if job in HIGH_EXERTION_JOBS and base >= 1:   # exertion factor
        base = min(3, base + 1)
    return base


def stress(temp_c, rh, pm25, job="street_vendor", imd_alert="none"):
    hi = heat_index_c(temp_c, rh)
    h, a = heat_level(hi, imd_alert), air_level_from_pm25(pm25)
    return {"heat_index_c": round(hi, 1), "heat_level": h, "air_level": a,
            "score": combine(h, a, job), "job": job}


def safer_hours(hourly, job="street_vendor", imd_alert="none", start=6, end=22):
    """hourly: list of dicts {hour,temp_c,rh,pm25}. Returns scores plus best-work and rest hour lists."""
    rows = []
    for r in hourly:
        if start <= r["hour"] < end:
            s = stress(r["temp_c"], r["rh"], r["pm25"], job, imd_alert)
            rows.append({"hour": r["hour"], "temp_c": r["temp_c"], "rh": r["rh"], "pm25": r["pm25"], **s})
    lo = min(r["score"] for r in rows)
    hi = max(r["score"] for r in rows)
    # if every hour has the same score there is no genuinely safer window
    best = [] if lo == hi else [r["hour"] for r in rows if r["score"] == lo]
    rest = [r["hour"] for r in rows if r["score"] == hi and hi >= 2]
    return {"rows": rows, "best_work_hours": best, "rest_hours": rest}


def runs(hours):
    """Group sorted hours into contiguous (start, end_exclusive) windows."""
    out, hours = [], sorted(hours)
    for h in hours:
        if out and h == out[-1][1]:
            out[-1][1] = h + 1
        else:
            out.append([h, h + 1])
    return [tuple(x) for x in out]
