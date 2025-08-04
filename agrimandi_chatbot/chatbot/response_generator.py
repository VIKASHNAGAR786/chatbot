import logging

def generate_response(intent: str, user_input: str = None, score: float = None) -> str:
    """
    Generate a chatbot response based on intent and optional user input/context.

    Args:
        intent (str): The predicted intent key.
        user_input (str, optional): The original user query (for future use).
        score (float, optional): Confidence score for debugging/logging.

    Returns:
        str: Bot response or fallback message.
    """

    response_templates = {
        "register": "To register, visit the AgriMandi website and click on 'Register as a Farmer'.",
        "sell_crop": "You can list your crops in the 'Sell Crops' section after logging in.",
        "buy_crop": "To purchase crops, browse the 'Marketplace' section and choose your items.",
        "mandi_rate": "Today's mandi rate for wheat is ₹2100 per quintal.",
        "seasonal_crops": "Currently, wheat, rice, and mustard are in season.",
        # Add more intent-response pairs here as needed
    }

    response = response_templates.get(intent)

    if response:
        if score is not None:
            logging.info(f"Intent: {intent} | Confidence: {score:.2f} | Response: {response}")
        return response

    logging.warning(f"Unknown intent received: '{intent}' | Score: {score} | Input: {user_input}")
    return "I'm sorry, I couldn't understand your request. Can you rephrase it?"
