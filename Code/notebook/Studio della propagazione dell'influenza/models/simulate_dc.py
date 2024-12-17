# """
# Simulazione con Diffusione Deterministica e Caotica)
# Teoria: Il modello Deterministic and Chaotic Diffusion (DC) unisce aspetti della diffusione deterministica e caotica, dove la diffusione segue leggi deterministiche in alcuni periodi, ma può diventare caotica in altre fasi. La transizione tra questi due stati dipende da vari fattori esterni e dalle interazioni tra i nodi.
# 1.	Determinismo: La diffusione segue regole precise basate sulla rete e le caratteristiche dei nodi.
# 2.	Caos: In altri momenti, la diffusione diventa imprevedibile e sensibile alle condizioni iniziali, producendo risultati caotici.
# Dinamica:
# •	In una fase, la diffusione può seguire un modello di cascata o soglia deterministico, ma successivamente può entrare in una fase caotica, dove l'attivazione di un nodo dipende in modo non lineare da vari fattori.
# Applicazioni:
# •	Comportamenti complessi: Quando il comportamento di una popolazione o sistema sociale diventa imprevedibile a causa di influenze non lineari.
# •	Sistema economici: Mercati o sistemi economici che alternano fasi stabili e caotiche.
# Implementazione: Nel codice, simulate_dc modella la transizione tra una diffusione deterministica (basata su probabilità e soglie) e una caotica (dove le dinamiche diventano imprevedibili).
# """


import random


def simulate_dc(graph, initial_prob, decay_factor, steps):
    activated = set()
    seed = random.choice(list(graph.nodes))
    activated.add(seed)

    prob = initial_prob
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
        prob *= decay_factor
        results.append(activated.copy())
    return results
