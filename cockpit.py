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

def print_delta_surface(schema):
    print("\nDELTA SURFACE")
    print("-----------------------------------------")
    print("| Expiry → | Deep ITM |  ATM  |  OTM  |")
    print("-----------------------------------------")

    for row in schema["delta_surface_data"]:
        print(f"| {row['expiry']:>6} yrs |   {row['deep_itm']:.2f}    | {row['atm']:.2f} | {row['otm']:.2f} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Deep ITM delta rises as expiry shortens (gamma blowout zone)")
    print("- ATM delta becomes unstable as expiry shortens")
    print("- OTM delta collapses as expiry shortens")

def print_iv_crush_panel(schema):
    print("\nIV CRUSH PANEL")
    print("-----------------------------------------")
    print("| Regime Transition   | IV Move   | Price Move |")
    print("-----------------------------------------")

    for row in schema["iv_crush_transitions"]:
        label = f"{row['from']} → {row['to']}"
        print(f"| {label:<18} | {row['iv_move']:<9} | {row['price_move']:<11} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Rallies reduce uncertainty → IV falls.")
    print("- IV falls → extrinsic value collapses.")
    print("- Short-dated options suffer the worst crush.")
    print("- LEAPS dampen crush but do not eliminate it.")

def print_iv_spike_panel(schema):
    print("\nIV SPIKE PANEL")
    print("-----------------------------------------")
    print("| Regime Transition   | IV Move   | Price Move |")
    print("-----------------------------------------")

    for row in schema["iv_spike_transitions"]:
        label = f"{row['from']} → {row['to']}"
        print(f"| {label:<18} | {row['iv_move']:<9} | {row['price_move']:<11} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Dips increase uncertainty → IV rises.")
    print("- IV rises → extrinsic expands.")
    print("- Short-dated options inflate fastest.")
    print("- LEAPS benefit from IV spikes during dips.")

def main():
    schema = load_schema()
    print("LEAP RISK COCKPIT —", schema["underlying"])
    print("Regimes:", ", ".join(schema["regimes"].keys()))
    print_delta_surface(schema)
    print_iv_crush_panel(schema)
    print_iv_spike_panel(schema)

if __name__ == "__main__":
    main()
