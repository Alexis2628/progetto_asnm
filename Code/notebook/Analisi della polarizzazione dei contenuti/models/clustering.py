from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
from sklearn.cluster import KMeans, DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import logging

class Clustering:
    def __init__(self):
        # Inizializza il vettorizzatore TF-IDF
        self.vectorizer = TfidfVectorizer()

    def embed_texts(self, texts):
        # Genera la rappresentazione TF-IDF per i testi
        return self.vectorizer.fit_transform(texts)

    def cluster(self, user_opinions, method="kmeans", n_clusters=20):
        logging.info(f"Clustering degli utenti utilizzando il metodo {method}.")
        texts = list(user_opinions.values())
        embeddings = self.embed_texts(texts)  # Usa TF-IDF invece di BERT
        if method == "kmeans":
            model = KMeans(n_clusters=n_clusters)
        elif method == "dbscan":
            model = DBSCAN(metric="cosine")
        labels = model.fit_predict(embeddings)
        logging.info("Clustering completato.")
        return dict(zip(user_opinions.keys(), labels))

    def identify_polarizing_themes(self, user_opinions, cluster_labels):
        logging.info("Identificazione dei temi polarizzanti.")
        texts = list(user_opinions.values())
        embeddings = self.embed_texts(texts).toarray()  # TF-IDF in formato array
        polarizing_words = []
        for cluster in set(cluster_labels.values()):
            cluster_indices = [i for i, label in enumerate(cluster_labels.values()) if label == cluster]
            cluster_mean = embeddings[cluster_indices].mean(axis=0)
            top_features_indices = np.argsort(-cluster_mean)[:10]
            polarizing_words.extend([self.vectorizer.get_feature_names_out()[i] for i in top_features_indices])
        logging.info("Identificazione dei temi polarizzanti completata.")
        return polarizing_words


class ClusteringEmdedding:
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
        logging.info(f"Clustering degli utenti utilizzando il metodo {method}.")
        texts = list(user_opinions.values())
        embeddings = self.embed_texts(texts)
        if method == "kmeans":
            model = KMeans(n_clusters=n_clusters)
        elif method == "dbscan":
            model = DBSCAN(metric="cosine")
        labels = model.fit_predict(embeddings)
        logging.info("Clustering completato.")
        return dict(zip(user_opinions.keys(), labels))

    def identify_polarizing_themes(self, user_opinions, cluster_labels):
        logging.info("Identificazione dei temi polarizzanti.")
        texts = list(user_opinions.values())
        embeddings = self.embed_texts(texts)
        polarizing_words = []
        for cluster in set(cluster_labels.values()):
            cluster_indices = [i for i, label in enumerate(cluster_labels.values()) if label == cluster]
            cluster_mean = embeddings[cluster_indices].mean(axis=0)
            polarizing_words.extend([self.tokenizer.decode([i]) for i in torch.argsort(-cluster_mean)[:10]])
        logging.info("Identificazione dei temi polarizzanti completata.")
        return polarizing_words