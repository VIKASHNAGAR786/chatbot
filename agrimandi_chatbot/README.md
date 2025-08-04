AgriMandi Chatbot - README
===========================

Project Overview:
-----------------
This is an intelligent chatbot designed for the AgriMandi platform. It assists users (farmers and buyers) with common queries related to farming, crop selling, mandi rates, and more using:

- Predefined FAQs with fuzzy matching
- LLM (Hugging Face Transformers) based fallback
- Intent classification and dynamic response generation

Features:
---------
✔ FAQ-based response matching using FuzzyWuzzy  
✔ LLM-powered answer generation as fallback  
✔ Intent-based response handling  
✔ Scalable and modular architecture  
✔ Logging support for debugging  
✔ Easy to extend with new intents and questions

File Structure:
---------------
- `main.py`                : Entry point of the chatbot
- `faq_handler.py`         : Handles FAQs using fuzzy matching
- `llm_fallback.py`        : Uses Transformers for fallback responses
- `intent_handler.py`      : Maps detected intents to responses
- `train_classifier.py`    : Trains a machine learning model on intent data
- `data/faq_data.json`     : Dictionary of questions and answers
- `data/intents.json`      : Sample dataset for training intent model

Requirements:
-------------
Python 3.8+  
Install required packages using:
