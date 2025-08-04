# Later, you can replace this with an ML-based model.


def classify_intent(text):
    if "register" in text:
        return "registration"
    elif "buy" in text:
        return "buy_crop"
    elif "sell" in text:
        return "sell_crop"
    elif "mandi rate" in text or "price" in text:
        return "mandi_rate"
    elif "season" in text:
        return "seasonal_crops"
    else:
        return "unknown"
