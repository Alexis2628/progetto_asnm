import logging
from graph.GraphConstructor import GraphConstructor
from preprocessing.text_preprocessor import TextPreprocessor
from models.clustering import Clustering
from visualization.cluster_visualizer import ClusterVisualizer
from visualization.sentiment_visualizer import SentimentVisualizer
from visualization.wordcloud_visualizer import WordCloudVisualizer
from visualization.lda_visualizer import LDAViz

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

def main():
    # Costruzione del grafo
    graph_builder = GraphConstructor(followers_path="dataset/dataset_cleaned.json")
    graph_builder.build_graph()
    graph = graph_builder.graph

    # Estrazione e pre-elaborazione dei testi
    preprocessor = TextPreprocessor()
    user_opinions = preprocessor.extract_user_opinions(graph)

    # Estrazione dei sentiment dal grafo
    sentiment_scores = extract_sentiments_from_graph(graph)

    import json
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(user_opinions, json_file, ensure_ascii=False, indent=4)

    # Clustering
    clustering = Clustering()
    cluster_labels = clustering.cluster(user_opinions, method="dbscan")

    # Visualizzazione dei cluster
    cluster_visualizer = ClusterVisualizer(output_dir="Code\notebook\Analisi della polarizzazione dei contenuti\output")
    cluster_visualizer.visualize(user_opinions, cluster_labels)

    # Visualizzazione del sentiment
    sentiment_visualizer = SentimentVisualizer(output_dir="Code\notebook\Analisi della polarizzazione dei contenuti\output")

    # Visualizza la distribuzione del sentiment
    sentiment_visualizer.visualize_sentiment_distribution(sentiment_scores, cluster_labels)

    # Visualizza la mappa di calore sentiment vs temi
    sentiment_visualizer.visualize_sentiment_vs_themes_heatmap(sentiment_scores, user_opinions, cluster_labels)

    # Identificazione e visualizzazione temi polarizzanti
    polarizing_words = clustering.identify_polarizing_themes(user_opinions, cluster_labels)
    wordcloud_visualizer = WordCloudVisualizer()
    wordcloud_visualizer.visualize(polarizing_words, "output")

    # Topic Modeling
    from models.topic_modeling import TopicModeling
    topic_modeling = TopicModeling()
    lda_model, dictionary, corpus = topic_modeling.perform_topic_modeling(user_opinions, len(set(cluster_labels.values())))

    # Visualizzazione dei temi
    lda_visualizer = LDAViz()
    lda_visualizer.visualize(lda_model, corpus, dictionary, output_dir="output")

def extract_sentiments_from_graph(graph):
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
            average_sentiment = sum(post["Sentiment"]["score"] for post in user_data) / len(user_data)
            sentiment_scores[node] = average_sentiment
        else:
            sentiment_scores[node] = 0  # Nessun dato, valore di default
    return sentiment_scores

if __name__ == "__main__":
    main()
