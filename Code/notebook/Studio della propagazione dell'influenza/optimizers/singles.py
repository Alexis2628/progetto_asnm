from models.independent_cascade_model import independent_cascade_model


def singles(graph, k, p=0.1):
    """Singles: Valutazione dei singoli nodi"""
    return set(
        sorted(
            graph.nodes(),
            key=lambda n: len(independent_cascade_model({n}, p)),
            reverse=True,
        )[:k]
    )
