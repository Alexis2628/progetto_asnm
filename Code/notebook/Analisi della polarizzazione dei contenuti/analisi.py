import os
import nltk
import torch
# nltk.download('punkt')
# nltk.download('stopwords')
import logging
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
import pyLDAvis
import pyLDAvis.gensim_models
import numpy as np
from transformers import pipeline
from matplotlib import pyplot as plt
from graph.GraphConstructor import GraphConstructor
from textblob import TextBlob
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans, DBSCAN
import seaborn as sns
import re 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


# Configura il logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class ContentPolarizationAnalyzer:
    supported_languages = [ 'english', 'spanish', 'chinese', 'french', 
                           'arabic', 'russian', 'portuguese', 'german', 
                           'italian', 'dutch', 'turkish', 'swedish' ]
    def __init__(self, graph):
        """
        Analizzatore di polarizzazione dei contenuti.
        :param graph: Il grafo orientato (nx.DiGraph).
        """

        self.graph = graph
        self.output_dir = "output"
        self.stop_words = [word for lang in self.supported_languages for word in stopwords.words(lang)]
        os.makedirs(self.output_dir, exist_ok=True)

    def preprocess_text(self, text): 
        """ Pre-elabora il testo. 
        :param text: Testo da pre-elaborare. 
        :return: Testo pre-elaborato. """
        import unicodedata
        text = unicodedata.normalize('NFKD', text)
        # Converti a minuscolo 
        text = text.lower() 
        # # Rimuovi punteggiatura 
        text = re.sub(r'[^\w\s]', '', text) 
        # Tokenizzazione 
        words = word_tokenize(text)
        # Rimuovi stop words 

        words = [word for word in words if word not in self.stop_words]
        # Stemming 
        stemmer = PorterStemmer() 
        words = [stemmer.stem(word) for word in words]
        preprocessed_text = " ".join(words) 
        return preprocessed_text 
    
    def extract_user_opinions(self): 
        """ Estrae le opinioni (contenuto testuale) degli utenti dal grafo e applica pre-elaborazione del testo. 
            :return: Dizionario {user_id: testo_completo} """ 
        logging.info("Estrazione e pre-elaborazione delle opinioni degli utenti dal grafo.")
        user_opinions = {} 
        for node, data in self.graph.nodes(data=True): 
            threads = data.get("user_data", []) 
            if threads is None: 
                threads = [] 
            raw_text = " ".join(thread.get("Caption Text", "") for thread in threads) 
            preprocessed_text = self.preprocess_text(raw_text) 
            user_opinions[node] = preprocessed_text 
            logging.info(f"Opinioni estratte e pre-elaborate per {len(user_opinions)} utenti.") 
        return user_opinions

    def perform_sentiment_analysis(self, user_opinions):
        """
        Analizza il sentiment dei testi degli utenti.
        :param user_opinions: Dizionario {user_id: testo_completo}.
        :return: Dizionario {user_id: sentiment_score}.
        """
        logging.info("Inizio analisi del sentiment.")
        sentiment_scores = {}
        for user_id, text in user_opinions.items():
            sentiment_scores[user_id] = TextBlob(text).sentiment.polarity
        logging.info("Analisi del sentiment completata.")
        return sentiment_scores

    def cluster_users(self, user_opinions, method="kmeans", n_clusters=5):
        """
        Raggruppa gli utenti in base al contenuto pubblicato.
        :param user_opinions: Dizionario {user_id: testo_completo}.
        :param method: Metodo di clustering ("kmeans" o "dbscan").
        :param n_clusters: Numero di cluster (per K-means).
        :return: Dizionario {user_id: cluster_label}.
        """
        logging.info(f"Clustering degli utenti usando il metodo: {method}.")
        vectorizer = TfidfVectorizer(stop_words=self.supported_languages)
        tfidf_matrix = vectorizer.fit_transform(user_opinions.values())

        if method == "kmeans":
            clustering_model = KMeans(n_clusters=n_clusters, random_state=42)
        elif method == "dbscan":
            clustering_model = DBSCAN(metric="cosine", eps=0.5, min_samples=5)
        else:
            raise ValueError("Metodo di clustering non supportato: usa 'kmeans' o 'dbscan'.")

        cluster_labels = clustering_model.fit_predict(tfidf_matrix)
        logging.info(f"Clustering completato. Numero di cluster unici: {len(set(cluster_labels))}.")
        return dict(zip(user_opinions.keys(), cluster_labels))

    def visualize_clusters(self, user_opinions, cluster_labels):
        """
        Visualizza i cluster degli utenti su due dimensioni principali.
        :param user_opinions: Dizionario {user_id: testo_completo}.
        :param cluster_labels: Dizionario {user_id: cluster_label}.
        """
        logging.info("Visualizzazione dei cluster.")
        vectorizer = TfidfVectorizer(stop_words=self.supported_languages)
        tfidf_matrix = vectorizer.fit_transform(user_opinions.values())

        svd = TruncatedSVD(n_components=2)
        reduced_data = svd.fit_transform(tfidf_matrix)

        plt.figure(figsize=(10, 8))
        sns.scatterplot(
            x=reduced_data[:, 0], 
            y=reduced_data[:, 1], 
            hue=list(cluster_labels.values()), 
            palette="viridis"
        )
        plt.title("Cluster di utenti basati sul contenuto")
        plt.xlabel("Dimensione 1")
        plt.ylabel("Dimensione 2")
        plt.legend(title="Cluster")

        output_path = os.path.join(self.output_dir, "user_clusters.png")
        plt.savefig(output_path)
        logging.info(f"Cluster salvati in: {output_path}")
        plt.close()

    def identify_polarizing_themes(self, user_opinions, cluster_labels):
        """
        Identifica i temi più polarizzanti in base ai cluster.
        :param user_opinions: Dizionario {user_id: testo_completo}.
        :param cluster_labels: Dizionario {user_id: cluster_label}.
        :return: Lista di parole chiave polarizzanti.
        """
        logging.info("Identificazione dei temi polarizzanti.")
        vectorizer = TfidfVectorizer(stop_words=self.supported_languages)
        tfidf_matrix = vectorizer.fit_transform(user_opinions.values())
        feature_names = vectorizer.get_feature_names_out()

        polarizing_words = []
        for cluster in set(cluster_labels.values()):
            cluster_indices = [i for i, label in enumerate(cluster_labels.values()) if label == cluster]
            cluster_tfidf = tfidf_matrix[cluster_indices].mean(axis=0)
            top_words = [feature_names[i] for i in np.argsort(-cluster_tfidf.A[0])[:10]]
            polarizing_words.extend(top_words)

        logging.info(f"Temi polarizzanti identificati: {polarizing_words}.")
        return list(set(polarizing_words))
    
    def perform_sentiment_analysis_huggingface(self, user_opinions, threshold_neutral=0.3):
        """
        Analizza il sentiment dei testi degli utenti utilizzando un modello di Hugging Face.
        :param user_opinions: Dizionario {user_id: testo_completo}.
        :param threshold_neutral: Soglia per classificare sentiment neutrale (range 0.0 - 1.0).
        :return: Dizionario {user_id: {"sentiment": sentiment_label, "score": sentiment_score}}.
        """
        logging.info("Inizio analisi del sentiment con Hugging Face.")
        device = 0 if torch.cuda.is_available() else -1
        logging.info(f"Utilizzando dispositivo: {'GPU' if device == 0 else 'CPU'}")
        # Carica il pipeline di sentiment analysis
        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english",device=device)

        sentiment_scores = {}
        for user_id, text in user_opinions.items():
            # Esegui l'analisi del sentiment
            result = sentiment_pipeline(text[:512])  # Limite di 512 token per il modello
            label = result[0]['label']  # "POSITIVE" o "NEGATIVE"
            score = result[0]['score']  # Confidenza del modello

            # Classifica il risultato in base alla soglia neutrale
            if score < threshold_neutral:
                sentiment_label = "NEUTRAL"
            else:
                sentiment_label = label

            sentiment_scores[user_id] = {"sentiment": sentiment_label, "score": score}

        logging.info("Analisi del sentiment con Hugging Face completata.")
        return sentiment_scores

    def visualize_polarizing_themes(self, polarizing_words):
        """
        Crea una word cloud dei temi più polarizzanti.
        :param polarizing_words: Lista di parole polarizzanti.
        """
        logging.info("Creazione della word cloud per i temi polarizzanti.")
        word_cloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(polarizing_words))

        plt.figure(figsize=(10, 6))
        plt.imshow(word_cloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Temi più polarizzanti")

        output_path = os.path.join(self.output_dir, "polarizing_themes.png")
        plt.savefig(output_path)
        logging.info(f"Word cloud salvata in: {output_path}")
        plt.close()
        
    def perform_topic_modeling(self, user_opinions, num_topics=5):
        """
        Identifica i temi principali utilizzando LDA.
        :param user_opinions: Dizionario {user_id: testo_completo}.
        :param num_topics: Numero di temi da identificare.
        :return: Modello LDA e dizionario dei dati.
        """
        logging.info("Esecuzione del topic modeling con LDA.")
        
        # Pre-elabora i testi e prepara i dati per l'LDA
        texts = [self.preprocess_text(opinion).split() for opinion in user_opinions.values()]
        dictionary = Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        
        # Addestra il modello LDA
        lda_model = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, random_state=42)
        
        logging.info(f"Modello LDA addestrato con {num_topics} temi.")
        return lda_model, dictionary, corpus
    
    def visualize_topics(self, lda_model, corpus, dictionary):
        """
        Visualizza i temi principali utilizzando pyLDAvis.
        :param lda_model: Modello LDA.
        :param corpus: Corpus utilizzato per addestrare il modello.
        :param dictionary: Dizionario di termini.
        """
        logging.info("Visualizzazione dei temi con pyLDAvis.")
        vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
        output_path = os.path.join(self.output_dir, "lda_visualization.html")
        pyLDAvis.save_html(vis, output_path)
        logging.info(f"Visualizzazione dei temi salvata in: {output_path}")


if __name__ == "__main__":
    graph_builder = GraphConstructor()
    graph_builder.build_graph()
    graph = graph_builder.graph

    analyzer = ContentPolarizationAnalyzer(graph)
    user_opinions = analyzer.extract_user_opinions()
    # Analisi del sentiment
    # sentiment_scores_hf = analyzer.perform_sentiment_analysis_huggingface(user_opinions, threshold_neutral=0.3)
    # for i ,(user_id, sentiment) in enumerate(sentiment_scores_hf.items()):
    #     if i == 10:
    #         break
    #     logging.info(f"User: {user_id}, Sentiment: {sentiment['sentiment']}, Score: {sentiment['score']}")
    sentiment_scores = analyzer.perform_sentiment_analysis(user_opinions)
    # Clustering degli utenti
    cluster_labels = analyzer.cluster_users(user_opinions, method="dbscan")
    # Visualizza i cluster
    analyzer.visualize_clusters(user_opinions, cluster_labels)
    # Identifica e visualizza i temi polarizzanti
    polarizing_themes = analyzer.identify_polarizing_themes(user_opinions, cluster_labels)
    analyzer.visualize_polarizing_themes(polarizing_themes)
    
     # Identifica i temi principali utilizzando il topic modeling
    lda_model, dictionary, corpus = analyzer.perform_topic_modeling(user_opinions, num_topics=len(set(list(cluster_labels))))
    
    # Visualizza i temi identificati
    analyzer.visualize_topics(lda_model, corpus, dictionary)