def generate_response(intent, user_input=None):
    responses = {
        "register": "To register, visit the AgriMandi website and click on 'Register as a Farmer'.",
        "sell_crop": "To sell your crops, go to the 'Sell Crops' section and list your items.",
        "buy_crop": "Visit the 'Marketplace' section to explore and buy available crops.",
        "mandi_rate": "Today's mandi rate for wheat is ₹2100 per quintal.",
        "seasonal_crops": "Currently, wheat, rice, and mustard are in season."
    }
    return responses.get(intent, None)
