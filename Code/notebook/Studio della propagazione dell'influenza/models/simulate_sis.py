# """
# Modello SIS (Susceptible-Infected-Susceptible)
# Teoria: Il modello SIS è una variazione del modello SIR, ma non esiste uno stato recuperato permanente. Gli individui che si guariscono tornano suscettibili e possono essere nuovamente infettati. Questo modello è adatto per malattie che non conferiscono immunità permanente.
# Dinamiche:
# •	Gli individui Suscettibili (S) possono diventare Infetti (I) se vengono esposti a un vicino infetto.
# •	Gli individui Infetti (I) possono tornare Suscettibili (S) dopo essersi "recuperati" (senza immunità permanente).
# Equazioni:
# •	Le dinamiche del modello SIS sono descritte dalle seguenti equazioni differenziali: dSdt=−β⋅S⋅I+γ⋅I\frac{dS}{dt} = -\beta \cdot S \cdot I + \gamma \cdot I dIdt=β⋅S⋅I−γ⋅I\frac{dI}{dt} = \beta \cdot S \cdot I - \gamma \cdot I
# Applicazioni:
# •	Malattie infettive senza immunità: Infezioni come l'influenza, dove l'immunità dura solo per un periodo limitato.
# •	Comportamenti ad alta diffusione: Comportamenti sociali che tornano frequentemente a diffondersi in una rete, come tendenze di moda.
# Implementazione: Nel codice, i nodi passano dallo stato infetto a suscettibile e viceversa, creando una dinamica continua di attivazione e guarigione.
# """

import random


def simulate_sis(graph, beta, gamma, steps):
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
            elif states[node] == "I" and random.random() < gamma:
                new_states[node] = "S"
        states = new_states
        results.append(states.copy())
    return results
