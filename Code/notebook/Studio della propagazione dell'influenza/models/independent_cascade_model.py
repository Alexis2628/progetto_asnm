# """
# Modello a Cascata Indipendente (Independent Cascade Model)
# Teoria: Nel modello a cascata indipendente, ogni nodo ha una probabilità fissa pp di attivare un vicino non attivo durante ogni passo temporale. Questo modello è basato sull'idea che, una volta che un nodo diventa attivo, può influenzare i suoi vicini in modo indipendente, cioè ogni vicino ha una probabilità pp di essere influenzato, ma l'influenza di un nodo su un altro è stocastica e avviene solo una volta.
# 1.	Attivazione iniziale: Un nodo (seed) inizia come attivo.
# 2.	Cascata: Quando un nodo ii diventa attivo, ha una probabilità pp di attivare ciascun vicino non attivo.
# 3.	Indipendenza: Ogni arco di attivazione tra due nodi è indipendente dagli altri.
# Formula: La probabilità di attivare un vicino jj da un nodo ii durante il passo tt è data da P(attivazione di j da i)=pP(\text{attivazione di } j \text{ da } i) = p. Se ii è attivo, si prova a attivare jj con probabilità pp.
# Applicazioni:
# •	Marketing virale: Un'informazione che si diffonde attraverso una rete di utenti con probabilità stocastica.
# •	Epidemie: La diffusione di una malattia che può colpire i vicini in modo stocastico.
# •	Comportamenti sociali: La diffusione di opinioni o comportamenti in una rete sociale.
# Implementazione: Nel codice, ogni nodo ha una probabilità pp di attivare i suoi vicini non attivi. La diffusione continua fino a quando non ci sono più nodi che possono essere attivati.
# """


import numpy as np


def independent_cascade_model(graph, seed_nodes, p=0.1):
    graph = graph.to_undirected()
    activated = set(seed_nodes)
    newly_activated = set(seed_nodes)

    while newly_activated:
        next_activated = set()
        for node in newly_activated:
            neighbors = set(graph.neighbors(node)) - activated
            for neighbor in neighbors:
                if np.random.rand() < p:
                    next_activated.add(neighbor)
        newly_activated = next_activated
        activated.update(newly_activated)
    return activated
