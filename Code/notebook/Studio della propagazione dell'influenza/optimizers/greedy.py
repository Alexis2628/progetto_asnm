from models.independent_cascade_model import independent_cascade_model


def greedy(graph, k, p=0.1):
    """Algoritmo Greedy per la massimizzazione dell'influenza"""
    current_seeds = set()
    for _ in range(k):
        best_node = None
        best_influence = 0
        for node in graph.nodes():
            if node not in current_seeds:
                temp_seeds = current_seeds | {node}
                influence = len(independent_cascade_model(temp_seeds, p))
                if influence > best_influence:
                    best_influence = influence
                    best_node = node
        current_seeds.add(best_node)
    return current_seeds
