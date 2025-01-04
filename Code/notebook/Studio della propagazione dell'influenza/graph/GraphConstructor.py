import networkx as nx
import random
import json 
import logging

class GraphConstructor:
    def __init__(self, followers_path="../../../dataset/dataset_cleaned.json"):
        with open(followers_path, "rb") as f:
            self.user_data = json.load(f)
        self.graph = nx.DiGraph()

    def build_graph(self):
        for user_id, user_info in self.user_data.items():
            user_id = int(user_id)

            # Aggiungi il nodo per l'utente principale
           
            self.graph.add_node(user_id, username=user_info.get("username", ""), user_data=user_info.get("user_data_translated", []))

            # Aggiungi i follower diretti
            for follower in user_info.get("followers", []):
                follower_id = int(follower["user_id"])

                
                self.graph.add_node(follower_id, username=follower.get("username", ""), user_data=follower.get("user_data_translated", []))

                # Aggiungi l'arco tra il follower e il nodo principale
                self.graph.add_edge(follower_id, user_id)

                # Aggiungi i follower del follower (al livello successivo, cioè fino ai follower dei follower)
                for follower_of_follower in follower.get("followers", []):
                    follower_of_follower_id = int(follower_of_follower["user_id"])
                    
                    # Aggiungi l'arco dal follower del follower al follower
                    self.graph.add_edge(follower_of_follower_id, follower_id)

        # Aggiungi soglie casuali per ogni nodo
        for node in self.graph.nodes():
            self.graph.nodes[node]["threshold"] = random.uniform(0, 1)

    def log_graph_info(self):
        logging.info(f"Numero di nodi del grafo: {len(self.graph.nodes)}")
        logging.info(f"Numero di archi del grafo: {len(self.graph.edges)}")

    def trust_function(self,neighbor, node):
        """
        Funzione di fiducia che determina il livello di fiducia tra un nodo e il suo vicino.
        :param neighbor: Il vicino del nodo corrente.
        :param node: Il nodo corrente.
        :return: Valore di fiducia tra 0 e 1.
        """
        weight = self.graph[node][neighbor].get("weight", 1)
        neighbor_threshold = self.graph.nodes[neighbor].get("threshold", 0.5)
        trust = weight * (1 - neighbor_threshold)
        return max(0, min(trust, 1))

    def calculate_centralities(self):
        centralities = {
            'Degree Centrality': nx.degree_centrality(self.graph),
            'Closeness Centrality': nx.closeness_centrality(self.graph),
            'Betweenness Centrality': nx.betweenness_centrality(self.graph, normalized=True, weight='weight'),
            'PageRank': nx.pagerank(self.graph, alpha=0.85),
            'Katz Centrality': nx.katz_centrality(self.graph, alpha=0.1, beta=1.0, max_iter=1000, tol=1e-06),
            'Eigenvector Centrality': nx.eigenvector_centrality(self.graph, max_iter=1000),
            'HITS Hub Scores': nx.hits(self.graph, max_iter=1000, tol=1e-08)[0],
            'HITS Authority Scores': nx.hits(self.graph, max_iter=1000, tol=1e-08)[1]
        }
        return centralities
    
    def print_top_centralities(self, top_k=5):
        from operator import itemgetter

        centralities = self.calculate_centralities()

        for centrality_name, values in centralities.items():
            print(f"\n{centrality_name} (Top {top_k}):")
            print("-" * (len(centrality_name) + 10))
            # Ordina i nodi per valore decrescente e seleziona i primi `top_k`
            sorted_values = sorted(values.items(), key=itemgetter(1), reverse=True)[:top_k]
            for node, value in sorted_values:
                print(f"Node {node}: {value:.4f}")

