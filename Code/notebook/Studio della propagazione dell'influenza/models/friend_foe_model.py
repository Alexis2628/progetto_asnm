# """
# Dinamicità amico-nemico con soglia lineare)
# Teoria: Nel modello Friend-Foe Dynamic Linear Threshold, la rete viene suddivisa in due categorie principali: amici e nemici. Ogni nodo ha una soglia e viene influenzato dai suoi vicini, che possono essere amici (che rinforzano il comportamento) o nemici (che contrastano l'influenza).
# 1.	Amici: I vicini amici aumentano la probabilità che un nodo si attivi o adotti un comportamento.
# 2.	Nemici: I vicini nemici riducono la probabilità di attivazione.
# Dinamica: Ogni nodo ha una soglia e viene influenzato in modo diverso da amici e nemici. Un nodo si attiva solo se l'influenza netta (amici - nemici) supera una soglia prestabilita.
# Equazione:
# •	La somma delle influenze dei vicini amichevoli e nemici deve superare la soglia per l'attivazione: ∑j∈amiciwij−∑k∈nemiciwik>θi\sum_{j \in \text{amici}} w_{ij} - \sum_{k \in \text{nemici}} w_{ik} > \theta_i
# Applicazioni:
# •	Dinamiche sociali: Influenze positive (amici) e negative (nemici) che determinano se un comportamento o una tendenza si diffonde.
# •	Politiche: Come le opinioni politiche o ideologiche si diffondono tra alleati e oppositori.
# Implementazione: La funzione friend_foe_dynamic_linear_threshold implementa una rete di influenze in cui gli amici rinforzano l'influenza e i nemici la indeboliscono, determinando l'attivazione in base alla soglia lineare.
# """


import random


def friend_foe_dynamic_linear_threshold(graph, seed_nodes, trust_function):
    activated = set(seed_nodes)
    quiescent = {}

    for node in graph.nodes():
        graph.nodes[node]["threshold"] = random.uniform(0, 1)

    while True:
        new_activations = set()
        for node in graph.nodes():
            if node not in activated:
                trusted_influence = sum(
                    trust_function(neighbor, node)
                    for neighbor in graph.predecessors(node)
                    if neighbor in activated
                )
                if trusted_influence >= graph.nodes[node]["threshold"]:
                    quiescence_time = random.uniform(0, 1)
                    quiescent[node] = quiescence_time
                    new_activations.add(node)

        if not new_activations:
            break

        for node in new_activations:
            if quiescent.get(node, 0) <= 0:
                activated.add(node)
            else:
                quiescent[node] -= 0.1

    return activated
