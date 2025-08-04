import os

# Enhanced project structure (files only, no internal content)
project_structure = {
    "agrimandi_chatbot": {
        "chatbot": {
            "__init__.py": "",
            "core.py": "",
            "nlp_engine.py": "",
            "intent_classifier.py": "",
            "response_generator.py": "",
            "data_loader.py": "",
            "faq_data.json": "",
        },
        "data": {
            "intents.json": "",
            "model.pkl": "",
            "embeddings.pkl": "",
        },
        "utils": {
            "__init__.py": "",
            "text_cleaner.py": "",
            "logger.py": "",
            "config.py": ""
        },
        "tests": {
            "test_core.py": "",
            "test_intent_classifier.py": "",
            "test_response_generator.py": ""
        },
        "main.py": "",
        "requirements.txt": "",
        "README.md": ""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    pass  # create empty file without content

# Create the enhanced project structure
create_structure(".", project_structure)
print("✅ Enhanced AgriMandi Chatbot project structure created successfully (existing files untouched)!")
