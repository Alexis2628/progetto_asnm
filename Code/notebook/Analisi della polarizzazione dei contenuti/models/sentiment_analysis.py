from textblob import TextBlob
from transformers import pipeline
import torch

class SentimentAnalyzer:
    def __init__(self, method="textblob"):
        self.method = method
        if self.method == "huggingface":
            self.device = 0 if torch.cuda.is_available() else -1
            self.pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=self.device)

    def analyze(self, user_opinions):
        if self.method == "textblob":
            return {user_id: TextBlob(text).sentiment.polarity for user_id, text in user_opinions.items()}
        elif self.method == "huggingface":
            return self._analyze_huggingface(user_opinions)

    def _analyze_huggingface(self, user_opinions):
        results = {}
        for user_id, text in user_opinions.items():
            result = self.pipeline(text[:512])[0]
            results[user_id] = result['label']
        return results
    

    def extract_sentiments_from_graph(self,graph):
        """
        Estrai i dati di sentiment dai nodi del grafo.
        :param graph: Il grafo costruito con i dati degli utenti.
        :return: Un dizionario con il sentiment score per ogni utente.
        """
        sentiment_scores = {}
        for node, data in graph.nodes(data=True):
            user_data = data.get("user_data", [])
            if user_data:
                # Calcola il sentiment medio per ogni utente in base ai loro post
                average_sentiment = sum(
                post["Sentiment"]["score"] if post["Sentiment"]["sentiment"] == "positive" 
                else (1 - post["Sentiment"]["score"] if post["Sentiment"]["sentiment"] == "negative" else 0.5) 
                for post in user_data) / len(user_data)

                sentiment_scores[node] = average_sentiment
            # else:
            #     sentiment_scores[node] = 0  # Nessun dato, valore di default
        return sentiment_scores
