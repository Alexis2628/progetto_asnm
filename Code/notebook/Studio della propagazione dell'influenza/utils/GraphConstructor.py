import networkx as nx


class GraphConstructor:
    def __init__(self, user_data, df):
        self.user_data = user_data
        self.df = df
        self.graph = nx.DiGraph()

    def build_graph(self):
        for user_id, user_data in self.user_data.items():
            user_info = self.df.loc[self.df['user_id'] == int(user_id)].to_dict(orient='records')
            
            if not self.graph.has_node(int(user_id)):
                self.graph.add_node(int(user_id), info=user_info)

            for follower in user_data.get("followers", []):
                follower_id = int(follower["user_id"])
                follower_info = self.df.loc[self.df['user_id'] == follower_id].to_dict(orient='records')

                if not self.graph.has_node(follower_id):
                    self.graph.add_node(follower_id, info=follower_info)

                self.graph.add_edge(follower_id, int(user_id))

    def calculate_centralities(self):
        centralities = {
            #'Degree Centrality': nx.degree_centrality(self.graph),
            #'Closeness Centrality': nx.closeness_centrality(self.graph),
            #'Betweenness Centrality': nx.betweenness_centrality(self.graph, normalized=True, weight='weight'),
            'PageRank': nx.pagerank(self.graph, alpha=0.85),
            #'Katz Centrality': nx.katz_centrality(self.graph, alpha=0.1, beta=1.0, max_iter=1000, tol=1e-06),
            #'Eigenvector Centrality': nx.eigenvector_centrality(self.graph, max_iter=1000),
            #'HITS Hub Scores': nx.hits(self.graph, max_iter=1000, tol=1e-08)[0],
            #'HITS Authority Scores': nx.hits(self.graph, max_iter=1000, tol=1e-08)[1]
        }
        return centralities
