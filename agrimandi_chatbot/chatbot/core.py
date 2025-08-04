import re
import time
from fuzzywuzzy import process
from transformers import pipeline
from termcolor import colored
import logging
from .data_loader import load_faq_data
from .intent_classifier import classify_intent
from .response_generator import generate_response
from utils.text_cleaner import clean_text

# Load FAQ
faq_data = load_faq_data()
faq_questions = list(faq_data.keys())

# Load QA model (DistilBERT is fast and lightweight)
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Define fallback context (can be expanded or replaced by a real document)
fallback_context = """
The AgriMandi system helps farmers get fair prices by providing up-to-date mandi rates, crop recommendations, and weather forecasts.
Common crops in India include wheat, rice, mustard, cotton, and sugarcane. Farmers can sell their produce through local mandis or digital platforms.
"""

# Greeting and exit setup
greetings = ['hello', 'hi', 'hey', 'namaste']
greeting_response = "Hello! How can I assist you in your farming journey today?"
exit_commands = ['exit', 'quit', 'bye', 'goodbye']

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def preprocess(text):
    """Clean and normalize the text."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_faq_response(user_input, threshold=70, suggest_alternatives=True):
    try:
        cleaned_input = preprocess(user_input)
        cleaned_questions = {q: preprocess(q) for q in faq_questions}

        best_match, score = process.extractOne(
            cleaned_input, cleaned_questions.values()
        )

        # Reverse lookup to get original question
        original_question = next(
            k for k, v in cleaned_questions.items() if v == best_match
        )

        logging.info(f"User Input: '{user_input}' | Matched: '{original_question}' | Score: {score}")

        if score >= threshold:
            return faq_data[original_question]

        # Optional fallback: suggest close matches
        if suggest_alternatives:
            close_matches = process.extract(cleaned_input, cleaned_questions.values(), limit=3)
            suggestions = [
                k for (match, sc) in close_matches if sc >= threshold - 10
                for k, v in cleaned_questions.items() if v == match
            ]
            if suggestions:
                return f"Sorry, I couldn’t find an exact answer. Did you mean:\n- " + "\n- ".join(suggestions)

        return "Sorry, I couldn’t understand that. Please try again."
    
    except Exception as e:
        logging.error(f"FAQ processing error: {e}")
        return "Oops! Something went wrong. Please try again later."

def get_llm_response(user_input: str, confidence_threshold: float = 0.3, max_response_length: int = 300) -> str:
    """
    Generate a response from the LLM pipeline given a user input.

    Args:
        user_input (str): The user's query.
        confidence_threshold (float): Minimum confidence score to consider response valid.
        max_response_length (int): Maximum allowed length for the model's response.

    Returns:
        str: The LLM's answer or a fallback message.
    """

    user_input = user_input.strip()
    if not user_input:
        return "Please enter a valid question."

    # Optional: basic input normalization
    user_input = re.sub(r'\s+', ' ', user_input)

    start_time = time.time()
    try:
        result = qa_pipeline(question=user_input, context=fallback_context)

        score = result.get("score", 0)
        answer = result.get("answer", "").strip()

        logging.info(f"LLM → User: '{user_input}' | Score: {score:.3f} | Answer: '{answer[:80]}...'")

        if score >= confidence_threshold and answer:
            # Truncate or clean long answers
            if len(answer) > max_response_length:
                answer = answer[:max_response_length].rsplit(' ', 1)[0] + "..."

            # Optional: strip non-informative phrases
            if answer.lower().startswith("i'm sorry") or "i don't know" in answer.lower():
                return "The system couldn't find a reliable answer right now."

            return answer

    except Exception as e:
        logging.exception("LLM Exception while processing input: %s", user_input)

    finally:
        elapsed = time.time() - start_time
        logging.debug(f"LLM response time: {elapsed:.2f}s")

    return "Sorry, I couldn't find a suitable answer at the moment."

def get_response(user_input):
    cleaned_input = clean_text(user_input)

    if any(greet in cleaned_input for greet in greetings):
        return greeting_response

    # Step 1: Try intent-based response
    intent = classify_intent(cleaned_input)
    if intent and intent != "unknown":
        intent_response = generate_response(intent, cleaned_input)
        if intent_response:
            return intent_response

    # Step 2: Try FAQ
    faq_response = get_faq_response(cleaned_input)
    if faq_response:
        return faq_response

    # Step 3: Fallback to LLM
    return get_llm_response(user_input)


def start_chat():
    print(colored("👨‍🌾 Welcome to AgriMandi Chatbot with AI Support!", 'green'))
    print(colored("Type 'exit' to quit.\n", 'yellow'))

    while True:
        try:
            user_input = input(colored("🧑 You: ", 'cyan')).strip()
            if user_input.lower() in exit_commands:
                print(colored("🤖 Chatbot: Thank you! Stay safe and keep farming 🌾", 'magenta'))
                break

            response = get_response(user_input)
            print(colored(f"🤖 Chatbot: {response}", 'blue'))

        except KeyboardInterrupt:
            print(colored("\n🤖 Chatbot: Session ended. Goodbye!", 'red'))
            break
