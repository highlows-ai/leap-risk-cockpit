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

def print_gamma_acceleration_panel(schema):
    print("\nGAMMA ACCELERATION PANEL")
    print("-----------------------------------------")
    print("| Time to Expiry | Gamma Level | Behavior        |")
    print("-----------------------------------------")

    for row in schema["gamma_acceleration"]:
        print(f"| {row['time']:<13} | {row['gamma']:<11} | {row['behavior']:<14} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Gamma accelerates as expiry approaches.")
    print("- Delta becomes unstable in the blowout zone.")
    print("- Short-dated options behave like leveraged spot.")
    print("- LEAPS avoid gamma blowout entirely.")

def print_wing_liquidity_panel(schema):
    print("\nDEEP ITM WING LIQUIDITY PANEL")
    print("-----------------------------------------")
    print("| Moneyness     | Delta       | Liquidity      |")
    print("-----------------------------------------")

    for row in schema["wing_liquidity"]:
        print(f"| {row['moneyness']:<13} | {row['delta']:<11} | {row['liquidity']:<14} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Deep ITM wings behave like synthetic stock.")
    print("- Liquidity is concentrated in deep ITM and near ITM.")
    print("- ATM is active and tight.")
    print("- OTM wings are thin and noisy.")
    print("- LEAPS should live in the deep ITM wing.")

def print_spread_widening_panel(schema):
    print("\nSPREAD WIDENING UNDER STRESS PANEL")
    print("-----------------------------------------")
    print("| Stress Condition     | Spread Behavior |")
    print("-----------------------------------------")

    for row in schema["spread_widening"]:
        print(f"| {row['condition']:<18} | {row['spread']:<15} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Spreads widen when information risk rises.")
    print("- Quote decay is the earliest stress signal.")
    print("- ATM short-dated options widen fastest.")
    print("- Deep ITM LEAPS remain relatively stable.")

def print_market_maker_hedging_panel(schema):
    print("\nMARKET MAKER HEDGING PANEL")
    print("-----------------------------------------")
    print("| Hedge Type     | Behavior Under Stress |")
    print("-----------------------------------------")

    for row in schema["market_maker_hedging"]:
        print(f"| {row['hedge']:<13} | {row['behavior']:<20} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Hedging drives short-term price action.")
    print("- Gamma hedging becomes violent near expiry.")
    print("- Vega hedging widens spreads during stress.")
    print("- LEAPS require smoother, less frequent hedging.")

def print_exit_conditions_panel(schema):
    print("\nEXIT CONDITIONS & SPREAD BEHAVIOR PANEL")
    print("-----------------------------------------")
    print("| Regime            | Spread     | Exit Quality |")
    print("-----------------------------------------")

    for row in schema["exit_conditions"]:
        print(f"| {row['regime']:<16} | {row['spread']:<10} | {row['quality']:<12} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Marks differ from executable prices under stress.")
    print("- Spreads widen when hedging becomes difficult.")
    print("- Deep ITM LEAPS maintain stable exit conditions.")
    print("- Avoid exits during gamma blowout windows.")

def print_calendar_roll_timing_panel(schema):
    print("\nCALENDAR ROLL TIMING PANEL")
    print("-----------------------------------------")
    print("| Window          | Behavior            |")
    print("-----------------------------------------")

    for row in schema["calendar_roll_timing"]:
        print(f"| {row['window']:<15} | {row['behavior']:<18} |")

    print("-----------------------------------------")
    print("Notes:")
    print("- Roll before gamma acceleration.")
    print("- Roll before theta walls.")
    print("- Avoid rolling during stress windows.")
    print("- Deep ITM LEAPS roll cleanly in calm tape.")

def main():
    schema = load_schema()
    print("LEAP RISK COCKPIT —", schema["underlying"])
    print("Regimes:", ", ".join(schema["regimes"].keys()))
    print_delta_surface(schema)
    print_iv_crush_panel(schema)
    print_iv_spike_panel(schema)
    print_gamma_acceleration_panel(schema)
    print_wing_liquidity_panel(schema)
    print_spread_widening_panel(schema)
    print_market_maker_hedging_panel(schema)
    print_exit_conditions_panel(schema)
    print_calendar_roll_timing_panel(schema)

if __name__ == "__main__":
    main()
