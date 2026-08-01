import json

def load_schema(path="cockpit_schema.json"):
    with open(path, "r") as f:
        return json.load(f)

def classify_regime(iv, rate_trend, time):
    if time > 1.0 and iv < 0.20 and rate_trend == "stable":
        return "calm"
    if time > 1.0 and iv > 0.30 and rate_trend == "stable":
        return "volatile"
    if time > 1.0 and iv < 0.25 and rate_trend == "rising":
        return "rate"
    if time > 1.0 and iv > 0.30 and rate_trend == "falling":
        return "compress"
    if time <= 0.5:
        return "late"
    return "unknown"

def main():
    schema = load_schema()
    print("LEAP RISK COCKPIT —", schema["underlying"])
    print("Regimes:", ", ".join(schema["regimes"].keys()))

if __name__ == "__main__":
    main()
