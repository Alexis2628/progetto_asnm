from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from transformers import BertTokenizer, BertModel
import torch

class Clustering:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')

    def embed_texts(self, texts):
        inputs = self.tokenizer(texts, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings

    def cluster(self, user_opinions, method="kmeans", n_clusters=5):
        texts = list(user_opinions.values())
        embeddings = self.embed_texts(texts)
        if method == "kmeans":
            model = KMeans(n_clusters=n_clusters)
        elif method == "dbscan":
            model = DBSCAN(metric="cosine")
        labels = model.fit_predict(embeddings)
        return dict(zip(user_opinions.keys(), labels))

    def identify_polarizing_themes(self, user_opinions, cluster_labels):
        texts = list(user_opinions.values())
        embeddings = self.embed_texts(texts)
        polarizing_words = []
        for cluster in set(cluster_labels.values()):
            cluster_indices = [i for i, label in enumerate(cluster_labels.values()) if label == cluster]
            cluster_mean = embeddings[cluster_indices].mean(axis=0)
            polarizing_words.extend([self.tokenizer.decode([i]) for i in torch.argsort(-cluster_mean)[:10]])
        return polarizing_words