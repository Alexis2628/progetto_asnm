from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from transformers import BertTokenizer, BertModel
import torch

class Clustering:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')

    def embed_texts(self, texts, batch_size=8):
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            inputs = self.tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            batch_embeddings = outputs.last_hidden_state.mean(dim=1)
            embeddings.append(batch_embeddings)
        return torch.cat(embeddings, dim=0)


    def cluster(self, user_opinions, method="kmeans", n_clusters=20):
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