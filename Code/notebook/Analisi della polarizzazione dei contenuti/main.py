import logging
from graph.GraphConstructor import GraphConstructor
from preprocessing.text_preprocessor import TextPreprocessor
from models.sentiment_analysis import SentimentAnalyzer
from models.clustering import Clustering
from models.topic_modeling import TopicModeling
from visualization.sentiment_visualizer import SentimentVisualizer
from visualization.cluster_visualizer import ClusterVisualizer
from visualization.wordcloud_visualizer import WordCloudVisualizer
from visualization.lda_visualizer import LDAViz



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
def main():
    # Costruzione del grafo
    graph_builder = GraphConstructor()
    graph_builder.build_graph()
    graph = graph_builder.graph

    # Estrazione e pre-elaborazione dei testi
    preprocessor = TextPreprocessor()
    user_opinions = preprocessor.extract_user_opinions(graph)

    # Analisi del sentiment
    sentiment_analyzer = SentimentAnalyzer()
    sentiment_scores = sentiment_analyzer.analyze(user_opinions)

    # Clustering
    clustering = Clustering()
    cluster_labels = clustering.cluster(user_opinions, method="dbscan")

    # Visualizzazione dei cluster
    cluster_visualizer = ClusterVisualizer(output_dir="output")
    cluster_visualizer.visualize(user_opinions, cluster_labels)
    
    sentiment_visualizer = SentimentVisualizer()
    
    # Visualizza la distribuzione del sentiment
    analyzer.visualize_sentiment_distribution(sentiment_scores, cluster_labels)
    
    analyzer.visualize_sentiment_vs_themes_heatmap(sentiment_scores, user_opinions, cluster_labels)
    # Identificazione e visualizzazione temi polarizzanti
    polarizing_words = clustering.identify_polarizing_themes(user_opinions, cluster_labels)
    wordcloud_visualizer = WordCloudVisualizer()
    wordcloud_visualizer.visualize(polarizing_words,"output")

    # Topic Modeling
    topic_modeling = TopicModeling()
    lda_model, dictionary, corpus = topic_modeling.perform_topic_modeling(user_opinions,len(set(cluster_labels.values())))

    # Visualizzazione dei temi
    lda_visualizer = LDAViz()
    lda_visualizer.visualize(lda_model, corpus, dictionary,output_dir="output")

if __name__ == "__main__":
    main()
