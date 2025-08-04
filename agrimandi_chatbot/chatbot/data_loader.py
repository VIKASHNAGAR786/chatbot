import json
import os



def load_faq_data():
    path = os.path.join(os.path.dirname(__file__), 'faq_data.json')
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
