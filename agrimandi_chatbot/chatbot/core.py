from fuzzywuzzy import process
from transformers import pipeline
from termcolor import colored
import logging
from .data_loader import load_faq_data

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

def get_faq_response(user_input):
    best_match, score = process.extractOne(user_input, faq_questions)
    logging.info(f"User Input: {user_input} | Best Match: {best_match} | Score: {score}")
    if score >= 65:
        return faq_data[best_match]
    return None

def get_llm_response(user_input):
    try:
        result = qa_pipeline(question=user_input, context=fallback_context)
        if result['score'] > 0.3:
            return result['answer']
    except Exception as e:
        logging.error(f"LLM Error: {e}")
    return "Sorry, I couldn't find an answer."

def get_response(user_input):
    user_input = user_input.strip().lower()

    if any(greet in user_input for greet in greetings):
        return greeting_response

    faq_response = get_faq_response(user_input)
    if faq_response:
        return faq_response

    # Fallback to LLM
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
