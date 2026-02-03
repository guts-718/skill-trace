def explain(signals: dict):
    reasons = []

    if signals["is_cold"]:
        reasons.append("You have never practiced this topic")

    if signals["days_since_last"] > 30:
        reasons.append(
            f"Not practiced in {signals['days_since_last']} days"
        )

    if signals["total_solved"] < 30:
        reasons.append(
            f"Only {signals['total_solved']} problems solved so far"
        )

    if signals["recent_7d"] == 0:
        reasons.append(
            "No problems solved from this topic in the last week"
        )

    if not reasons:
        reasons.append("Good topic for balanced practice")

    return reasons
