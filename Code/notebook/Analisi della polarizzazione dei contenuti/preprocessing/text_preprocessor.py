import re
import unicodedata
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from config.settings import SUPPORTED_LANGUAGES

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
        words = [self.stemmer.stem(word) for word in words if word not in self.stop_words]
        return " ".join(words)

    def extract_user_opinions(self,graph): 
        """ Estrae le opinioni (contenuto testuale) degli utenti dal grafo e applica pre-elaborazione del testo. 
            :return: Dizionario {user_id: testo_completo} """ 
        logging.info("Estrazione e pre-elaborazione delle opinioni degli utenti dal grafo.")
        user_opinions = {} 
        for node, data in graph.nodes(data=True): 
            threads = data.get("user_data", []) 
            if threads is None: 
                threads = [] 
            raw_text = " ".join(thread.get("Caption Text", "") for thread in threads) 
            preprocessed_text = self.preprocess_text(raw_text) 
            user_opinions[node] = preprocessed_text 
            logging.info(f"Opinioni estratte e pre-elaborate per {len(user_opinions)} utenti.") 
        return user_opinions
