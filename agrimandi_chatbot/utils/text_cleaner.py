import re
import string
import unicodedata
import nltk

# Optional: use NLTK or SpaCy stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def clean_text(text, remove_numbers=True, remove_stopwords=True, remove_html=True, normalize_unicode=True):
    # Lowercase
    text = text.lower()

    # Unicode normalization
    if normalize_unicode:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # Remove HTML tags
    if remove_html:
        text = re.sub(r'<[^>]+>', '', text)

    # Remove punctuation
    text = re.sub(rf"[{re.escape(string.punctuation)}]", "", text)

    # Remove numbers
    if remove_numbers:
        text = re.sub(r'\d+', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove stopwords
    if remove_stopwords:
        text = ' '.join([word for word in text.split() if word not in stop_words])

    return text
