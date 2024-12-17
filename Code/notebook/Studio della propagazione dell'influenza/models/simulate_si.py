# """
# Simulazione SI - Susceptible-Infected)
# Teoria: Il modello SI (Susceptible-Infected) è una versione semplificata dei modelli epidemiologici, che si concentra solo sulla diffusione di una malattia o comportamento da "suscettibili" a "infetti", senza considerare la fase di recupero. È utile per descrivere situazioni in cui un individuo, una volta infetto, non può mai recuperare o tornare suscettibile (come nel caso di una malattia permanente).
# 1.	Suscettibili (S): Gli individui sono vulnerabili all'infezione e possono diventare infetti.
# 2.	Infetti (I): Gli individui infetti possono trasmettere l'infezione ad altri suscettibili.
# 3.	Dinamica: Gli individui infetti contagiano i suscettibili con una probabilità β\beta.
# La dinamica dell'infezione è modellata con una probabilità β\beta che descrive il rischio che un suscettibile venga infettato da un vicino infetto. Una volta infetti, i nodi non tornano suscettibili, ma continuano a diffondere l'infezione.
# Equazione:
# •	La probabilità di infettare un vicino suscettibile SS da un infetto II è descritta da: dSdt=−β⋅S⋅I\frac{dS}{dt} = -\beta \cdot S \cdot I dIdt=β⋅S⋅I\frac{dI}{dt} = \beta \cdot S \cdot I
# Applicazioni: Questo modello è utilizzato quando non si vuole considerare la fase di recupero, come ad esempio in alcune epidemie acute (es. HIV, dove una volta che una persona è infetta non diventa mai suscettibile).
# Implementazione: Nel codice, la funzione simulate_si modella il flusso da "suscettibile" a "infetto" nei nodi di una rete. I nodi iniziano come suscettibili e diventano infetti quando interagiscono con nodi infetti, con una probabilità β\beta.
# """

import random


def simulate_si(graph, beta, steps):
    states = {node: "S" for node in graph.nodes}
    infected = random.choice(list(graph.nodes))
    states[infected] = "I"

    results = []
    for _ in range(steps):
        new_states = states.copy()
        for node in graph.nodes:
            if states[node] == "S":
                for neighbor in graph.neighbors(node):
                    if states[neighbor] == "I" and random.random() < beta:
                        new_states[node] = "I"
                        break
        states = new_states
        results.append(states.copy())
    return results
