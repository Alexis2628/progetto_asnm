# """
# Simulazione con Threshold - Greater-Than Model)
# Teoria: Il Greater-Than (GT) Model è un tipo di modello di diffusione basato su soglie in cui un nodo diventa attivo o infetto se la somma delle influenze che riceve dai suoi vicini supera una certa soglia predefinita. La "Greater-Than" fa riferimento alla condizione in cui un nodo diventa attivo solo quando l'influenza combinata dei suoi vicini supera un valore specificato.
# 1.	Dinamica: Ogni nodo ha una soglia e una probabilità associata. Se la somma delle probabilità di attivazione dei suoi vicini supera la soglia, il nodo si attiva.
# 2.	Condizione: Un nodo ii diventa attivo se: ∑j∈N(i)pij>θi\sum_{j \in N(i)} p_{ij} > \theta_i Dove pijp_{ij} è la probabilità che il nodo jj attivi il nodo ii, e θi\theta_i è la soglia di attivazione di ii.
# Applicazioni:
# •	Comportamenti collettivi: Come l'adozione di una nuova tecnologia o comportamento.
# •	Infezioni virali: Il contagio si verifica solo quando un nodo supera una certa "soglia" di esposizione.
# Implementazione: Nel codice, la funzione simulate_gt simula la diffusione in una rete, dove ogni nodo ha una soglia e si attiva quando la somma delle probabilità degli archi che lo connettono supera questa soglia.
# """
import random


def simulate_gt(graph, thresholds, steps):
    activated = set()
    seed = random.choice(list(graph.nodes))
    activated.add(seed)

    results = []
    for _ in range(steps):
        new_activated = activated.copy()
        for node in graph.nodes:
            if node not in activated:
                active_neighbors = sum(
                    1 for neighbor in graph.neighbors(node) if neighbor in activated
                )
                if (
                    graph.degree[node] > 0
                    and active_neighbors / graph.degree[node] >= thresholds[node]
                ):
                    new_activated.add(node)
        activated = new_activated
        results.append(activated.copy())
    return results
