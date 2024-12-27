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
