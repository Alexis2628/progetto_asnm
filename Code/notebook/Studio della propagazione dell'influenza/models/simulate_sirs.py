# """
# Modello SIRS (Susceptible-Infected-Recovered-Susceptible)
# Teoria: Il modello SIRS è una variante del modello SIR che considera che la guarigione non conferisce un'immunità permanente. Gli individui che si sono ripresi dalla malattia possono tornare suscettibili dopo un certo periodo.
# Dinamiche:
# •	Gli individui Recuperati (R) tornano a essere Suscettibili (S) con una probabilità λ\lambda, rappresentando il decadimento dell'immunità.
# Equazioni:
# •	Le dinamiche del modello SIRS sono rappresentate da: dSdt=−β⋅S⋅I+λ⋅R\frac{dS}{dt} = -\beta \cdot S \cdot I + \lambda \cdot R dIdt=β⋅S⋅I−γ⋅I\frac{dI}{dt} = \beta \cdot S \cdot I - \gamma \cdot I dRdt=γ⋅I−λ⋅R\frac{dR}{dt} = \gamma \cdot I - \lambda \cdot R
# Applicazioni:
# •	Malattie con immunità temporanea: Ad esempio, infezioni dove una persona può tornare suscettibile dopo un po' di tempo (come alcune malattie stagionali).
# Implementazione: Nel codice, il nodo infetto può diventare recuperato, e dopo un po', può tornare suscettibile, creando una dinamica ciclica.
# """

import random


def simulate_sirs(graph, beta, gamma, lambda_, steps):
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
            elif states[node] == "I":
                if random.random() < gamma:
                    new_states[node] = "R"
            elif states[node] == "R":
                if random.random() < lambda_:
                    new_states[node] = "S"
        states = new_states
        results.append(states.copy())
    return results
