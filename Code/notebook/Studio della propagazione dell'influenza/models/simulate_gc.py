# """
# Simulazione con Cascata Stocastica - General Cascade Model)
# Teoria: Il modello General Cascade è un'estensione dei modelli di cascata, come il modello di soglia o il modello a cascata indipendente. In questo caso, l'attivazione di un nodo dipende da una probabilità di attivazione stocastica, che può essere influenzata da diversi fattori.
# 1.	Cascata: I nodi si attivano in base a probabilità calcolate stocasticamente, che sono influenzate sia dalle caratteristiche del nodo stesso che dai suoi vicini.
# 2.	Cascata Multipla: A differenza di un modello di cascata semplice, in un modello generale, più di un nodo può attivare un altro nodo simultaneamente.
# Dinamica:
# •	Ogni nodo ii ha una probabilità di attivarsi basata sull'influenza ricevuta dai suoi vicini, ma l'attivazione di ii è stocastica.
# •	A ogni passo, ogni nodo ha una probabilità di attivare i suoi vicini, creando una cascata di attivazioni.
# Applicazioni:
# •	Diffusione di innovazioni: L'adozione di nuovi prodotti o comportamenti che avviene in modo stocastico.
# •	Epidemie: La diffusione di malattie che può variare in base a variabili ambientali o comportamentali.
# Implementazione: Nel codice, la funzione simulate_gc tiene conto delle probabilità stocastiche, permettendo a un nodo di attivare i suoi vicini con probabilità variabili, innescando una cascata.
# """

import random


def simulate_gc(graph, prob, steps):
    activated = set()
    seed = random.choice(list(graph.nodes))
    activated.add(seed)

    results = []
    for _ in range(steps):
        new_activated = activated.copy()
        for node in graph.nodes:
            if node not in activated:
                for neighbor in graph.neighbors(node):
                    if neighbor in activated and random.random() < prob:
                        new_activated.add(node)
                        break
        activated = new_activated
        results.append(activated.copy())
    return results
