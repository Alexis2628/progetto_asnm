import numpy as np
import pandas as pd
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import TruncatedSVD
import seaborn as sns
import matplotlib.pyplot as plt

class SentimentVisualizer:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def visualize_sentiment_distribution(self, sentiment_scores, cluster_labels):
        logging.info("Visualizzazione della distribuzione del sentiment tra i cluster.")
        data = pd.DataFrame({
            "User": list(sentiment_scores.keys()),
            "Sentiment": list(sentiment_scores.values()),
            "Cluster": [cluster_labels[user] for user in sentiment_scores.keys()]
        })

        # Grafico a violino
        plt.figure(figsize=(12, 6))
        sns.violinplot(x="Cluster", y="Sentiment", data=data, palette="coolwarm")
        plt.title("Distribuzione del sentiment nei cluster (Violino)")
        plt.xlabel("Cluster")
        plt.ylabel("Sentiment")
        plt.savefig(f"{self.output_dir}/sentiment_violin_plot.png")
        plt.close()

        # Grafico a barre
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x="Cluster",
            y="Sentiment",
            data=data,
            ci=None,
            estimator=np.mean,
            palette="viridis"
        )
        plt.title("Sentiment medio per cluster (Barre)")
        plt.xlabel("Cluster")
        plt.ylabel("Sentiment medio")
        plt.savefig(f"{self.output_dir}/sentiment_bar_plot.png")
        plt.close()

    def visualize_sentiment_vs_themes_heatmap(self, sentiment_scores, user_opinions, cluster_labels):
        logging.info("Creazione della heatmap tra sentiment e temi polarizzanti.")
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(user_opinions.values())
        feature_names = vectorizer.get_feature_names_out()

        sentiment_array = np.array([sentiment_scores[user] for user in user_opinions.keys()])
        tfidf_array = tfidf_matrix.toarray()

        # Calcolo della correlazione
        sentiment_to_terms_corr = np.corrcoef(sentiment_array, tfidf_array.T)[0, 1:]

        # Preparazione della heatmap
        top_indices = np.argsort(np.abs(sentiment_to_terms_corr))[-20:]  # Top 20 parole più correlate
        top_words = [feature_names[i] for i in top_indices]
        correlations = sentiment_to_terms_corr[top_indices]

        heatmap_data = pd.DataFrame({
            "Terms": top_words,
            "Correlation": correlations
        }).pivot_table(index="Terms", values="Correlation")

        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title("Relazione tra Sentiment e Temi Polarizzanti")
        plt.savefig(f"{self.output_dir}/sentiment_themes_heatmap.png")
        plt.close()