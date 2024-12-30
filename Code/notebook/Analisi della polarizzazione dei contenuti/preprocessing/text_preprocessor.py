import re
import unicodedata
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from config.settings import SUPPORTED_LANGUAGES
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')


class TextPreprocessor:
    def __init__(self):
        self.stop_words = [
            word for lang in SUPPORTED_LANGUAGES 
            for word in stopwords.words(lang)
        ]
        self.stemmer = PorterStemmer()

    def preprocess_text(self, text):
        text = unicodedata.normalize('NFKD', text).lower()
        text = re.sub(r'[^\w\s]', '', text)
        words = word_tokenize(text)
        words = [word for word in words if word not in self.stop_words]
        words = [self.stemmer.stem(word) for word in words]
        return " ".join(words)

    def extract_user_opinions(self, graph): 
        user_opinions = {} 
        for node, data in graph.nodes(data=True): 
            threads = data.get("user_data", []) 
            if not threads:  # Handle missing threads
                continue
            raw_text = " ".join(thread.get("Caption Text", "") for thread in threads if thread.get("Caption Text"))
            preprocessed_text = self.preprocess_text(raw_text)
            if not preprocessed_text.strip():  # Handle empty processed text
                preprocessed_text = "empty_content"
            user_opinions[node] = preprocessed_text
        return user_opinions
