# """
# Modello SIR (Susceptible-Infected-Recovered)
# Teoria: Il modello SIR è uno dei modelli epidemiologici più usati per simulare la diffusione di malattie in una popolazione. Esso assume che ogni individuo possa essere in uno dei tre stati:
# 1.	Suscettibile (S): L'individuo è vulnerabile alla malattia.
# 2.	Infetto (I): L'individuo ha la malattia e può trasmetterla.
# 3.	Recuperato (R): L'individuo si è ripreso dalla malattia e non può più trasmetterla né essere infettato.
# Dinamiche:
# •	Ogni individuo suscettibile ha una probabilità β\beta di essere infettato da un vicino infetto.
# •	Un individuo infetto può passare a recuperato con probabilità γ\gamma.
# Equazioni:
# •	La velocità di cambiamento delle proporzioni di individui nei vari stati è data da: dSdt=−β⋅S⋅I\frac{dS}{dt} = -\beta \cdot S \cdot I dIdt=β⋅S⋅I−γ⋅I\frac{dI}{dt} = \beta \cdot S \cdot I - \gamma \cdot I dRdt=γ⋅I\frac{dR}{dt} = \gamma \cdot I
# Dove SS, II, e RR sono le frazioni di individui suscettibili, infetti e recuperati, rispettivamente, in un dato momento.
# Applicazioni:
# •	Malattie infettive: Simula la diffusione di epidemie come influenza o Covid-19.
# •	Comportamenti virali: Modella il comportamento virale di una campagna di marketing o di un messaggio.
# •	Strategie di immunizzazione: Analizza l'efficacia delle vaccinazioni e delle misure di contenimento.
# Implementazione: Nel codice, i nodi possono passare da uno stato all'altro (Suscettibile, Infetto, Recuperato) a seconda delle probabilità di contagio β\beta e guarigione γ\gamma.
# """


import random


def simulate_sir(graph, beta, gamma, steps):
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
                new_states[node] = "R"
        states = new_states
        results.append(states.copy())
    return results
