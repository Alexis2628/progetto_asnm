import numpy as np
import random
from DataProcessor import DataProcessor
from GraphConstructor import GraphConstructor


# Class for influence models
class InfluenceModels:

    # """
    # Modello di Soglia Lineare (Linear Threshold Model)
    # Teoria: Il modello di soglia lineare è un modello di diffusione in cui i nodi di una rete (individui) sono soggetti a un meccanismo di attivazione basato su una soglia di influenza. Ogni nodo ha una soglia probabilistica che rappresenta la quantità minima di influenza che deve ricevere dai suoi vicini per attivarsi. Ogni arco (connessione) tra due nodi ha un peso che rappresenta l'intensità dell'influenza che un nodo esercita sull'altro. Quando la somma delle influenze dai vicini supera la soglia di attivazione di un nodo, esso diventa attivo.
    # 1.	Soglia casuale: Ogni nodo ha una soglia generata casualmente (compresa tra 0 e 1).
    # 2.	Attivazione: Un nodo diventa attivo se la somma delle influenze (ovvero, il peso degli archi dai vicini attivi) supera la sua soglia.
    # 3.	Propagazione: Una volta che un nodo diventa attivo, influenza i suoi vicini, i quali potrebbero a loro volta superare la loro soglia di attivazione.
    # Formula: La soglia θi\theta_i per ogni nodo ii è generata casualmente tra 0 e 1. Un nodo ii diventa attivo se:
    # ∑j∈N(i)wijxj≥θi\sum_{j \in N(i)} w_{ij} x_j \geq \theta_i
    # Dove:
    # •	N(i)N(i) è l'insieme dei vicini del nodo ii,
    # •	wijw_{ij} è il peso dell'arco che collega il nodo jj con ii,
    # •	xjx_j è lo stato del nodo jj (1 se attivo, 0 altrimenti),
    # •	θi\theta_i è la soglia di attivazione del nodo ii.
    # Applicazioni:
    # •	Marketing virale: Diffusione di un prodotto o messaggio attraverso una rete sociale.
    # •	Norme sociali: L'adozione di un comportamento da parte di una persona dipende dalle persone intorno a lei che l'hanno già adottato.
    # •	Diffusione di idee: Le idee si diffondono in modo simile a una catena, in cui ogni individuo può influenzare quelli che lo circondano.
    # Implementazione: Nel codice, l'attivazione di un nodo dipende dall'influenza ricevuta dai suoi vicini. Ogni nodo ha una soglia casuale, e la propagazione continua finché ci sono nodi che possono essere attivati.
    # """

    def linear_threshold_model(graph, seed_nodes):
        graph = graph.to_undirected()
        activated = set(seed_nodes)
        newly_activated = set(seed_nodes)

        for node in graph.nodes():
            neighbors = list(graph.neighbors(node))

            if neighbors:
                weight = 1 / len(neighbors)
                for neighbor in neighbors:
                    graph.edges[node, neighbor]["influence"] = weight

        while newly_activated:
            next_activated = set()
            for node in graph.nodes():
                if node not in activated:
                    total_influence = sum(
                        graph.edges[neighbor, node]["influence"]
                        for neighbor in graph.neighbors(node)
                        if neighbor in activated
                    )
                    if total_influence >= graph.nodes[node]["threshold"]:
                        next_activated.add(node)

            newly_activated = next_activated
            activated.update(newly_activated)
        return activated

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
    @staticmethod
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

    # """
    # Simulazione SIR - Susceptible-Infected)
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

    @staticmethod
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
    @staticmethod
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
                elif states[node] == "I":
                    if random.random() < gamma:
                        new_states[node] = "R"
            states = new_states
            results.append(states.copy())
        return results

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
    @staticmethod
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
                elif states[node] == "I":
                    if random.random() < gamma:
                        new_states[node] = "S"
            states = new_states
            results.append(states.copy())
        return results

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
    @staticmethod
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
    @staticmethod
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
    @staticmethod
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

    # """
    # Simulazione con Threshold Reversibile)
    # Teoria: Nel modello Threshold Reversibile, i nodi hanno una soglia di attivazione che può essere influenzata da dinamiche reversibili. Una volta che un nodo diventa attivo, esso può tornare allo stato non attivo se una condizione reversibile è soddisfatta. Questo è simile a un modello SIS, ma con soglie specifiche per l'attivazione e la disattivazione.
    # 1.	Dinamica: Un nodo attivo può diventare di nuovo non attivo se l'influenza ricevuta dai suoi vicini scende al di sotto della sua soglia.
    # 2.	Reversibilità: I nodi non sono permanentemente attivi, ma possono passare avanti e indietro tra gli stati.
    # Condizione:
    # •	Un nodo ii è attivo se la somma dell'influenza dei vicini è maggiore della sua soglia θi\theta_i. Se la somma scende al di sotto di θi\theta_i, il nodo torna non attivo.
    # Applicazioni:
    # •	Comportamenti dinamici: Situazioni dove le persone o gli oggetti possono entrare e uscire dallo stato attivo, come l'adozione di comportamenti che possono essere abbandonati.
    # •	Mercati finanziari: Comportamenti che oscillano tra l'attivo e il non attivo in risposta a cambiamenti nel contesto.
    # Implementazione: Nel codice, simulate_tr implementa la dinamica reversibile, permettendo ai nodi di attivarsi o disattivarsi in base alla soglia e all'influenza ricevuta.
    # """
    @staticmethod
    def simulate_tr(graph, prob, steps):
        return InfluenceModels.simulate_gc(graph, prob, steps)

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
    @staticmethod
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
    @staticmethod
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

    def greedy(self, k, p=0.1):
        """Algoritmo Greedy per la massimizzazione dell'influenza"""
        current_seeds = set()
        for _ in range(k):
            best_node = None
            best_influence = 0
            for node in self.graph.nodes():
                if node not in current_seeds:
                    temp_seeds = current_seeds | {node}
                    influence = len(self.independent_cascade(temp_seeds, p))
                    if influence > best_influence:
                        best_influence = influence
                        best_node = node
            current_seeds.add(best_node)
        return current_seeds

    def celf(self, k, p=0.1):
        """Algoritmo CELF (Cost-Effective Lazy Greedy)"""
        current_seeds = set()
        influence_cache = {}
        heap = []

        for _ in range(k):
            best_node = None
            best_influence = 0
            for node in self.graph.nodes():
                if node not in current_seeds:
                    if node not in influence_cache:
                        influence_cache[node] = len(
                            self.independent_cascade(current_seeds | {node}, p)
                        )
                    influence = influence_cache[node]
                    if influence > best_influence:
                        best_influence = influence
                        best_node = node
            current_seeds.add(best_node)
            heapq.heappush(
                heap, (-best_influence, best_node)
            )  # usiamo il valore negativo per max-heap
        return current_seeds

    def celf_plus(self, k, p=0.1):
        """Algoritmo CELF++ (miglioramento di CELF)"""
        current_seeds = set()
        influence_cache = {}
        heap = []

        for _ in range(k):
            best_node = None
            best_influence = 0
            for node in self.graph.nodes():
                if node not in current_seeds:
                    if node not in influence_cache:
                        influence_cache[node] = len(
                            self.independent_cascade(current_seeds | {node}, p)
                        )
                    influence = influence_cache[node]
                    if influence > best_influence:
                        best_influence = influence
                        best_node = node
            current_seeds.add(best_node)
            heapq.heappush(
                heap, (-best_influence, best_node)
            )  # usiamo il valore negativo per max-heap
        return current_seeds

    def stop_and_go(self, k, p=0.1):
        """Algoritmo Stop-And-Go"""
        current_seeds = set()
        while len(current_seeds) < k:
            best_node = None
            best_influence = 0
            for node in self.graph.nodes():
                if node not in current_seeds:
                    temp_seeds = current_seeds | {node}
                    influence = len(self.independent_cascade(temp_seeds, p))
                    if influence > best_influence:
                        best_influence = influence
                        best_node = node
            current_seeds.add(best_node)
        return current_seeds

    def static(self, k, p=0.1):
        """Algoritmo Static (scelta statica dei nodi)"""
        # Qui si potrebbe implementare un approccio basato su centralità (degree, betweenness, etc.)
        # come esempio userò il grado dei nodi
        current_seeds = set()
        sorted_nodes = sorted(
            self.graph.nodes(), key=lambda node: self.graph.degree(node), reverse=True
        )
        return set(sorted_nodes[:k])

        ### SIMPATH ###

    def simpath(self, k, p=0.1, path_limit=3):
        """Algoritmo SIMPATH basato sui percorsi influenti"""

        def compute_path_influence(node, path_limit):
            visited = set()
            stack = [(node, 0)]
            influence = 0

            while stack:
                current_node, depth = stack.pop()
                if depth > path_limit or current_node in visited:
                    continue
                visited.add(current_node)
                influence += 1
                for neighbor in self.graph.neighbors(current_node):
                    stack.append((neighbor, depth + 1))
            return influence

        seed_set = set()
        for _ in range(k):
            best_node = max(
                self.graph.nodes(), key=lambda n: compute_path_influence(n, path_limit)
            )
            seed_set.add(best_node)
            self.graph.remove_node(best_node)
        return seed_set

    ### LDAG ###
    def ldag(self, k, p=0.1, threshold=0.5):
        """Algoritmo LDAG: Local DAG-based propagation"""

        def build_local_dag(node, threshold):
            local_dag = nx.DiGraph()
            visited = set([node])
            queue = [node]
            while queue:
                current = queue.pop(0)
                for neighbor in self.graph.neighbors(current):
                    if random.random() < threshold:
                        local_dag.add_edge(current, neighbor)
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
            return local_dag

        seed_set = set()
        for _ in range(k):
            best_node = max(
                self.graph.nodes(), key=lambda n: len(build_local_dag(n, threshold))
            )
            seed_set.add(best_node)
        return seed_set

    ### IRIE ###
    def irie(self, k, p=0.1):
        """Algoritmo IRIE basato su Random Walk e Linear Influence"""
        influence_scores = {node: 1 for node in self.graph.nodes()}

        for _ in range(5):  # Itera per stabilizzare i punteggi
            new_scores = {}
            for node in self.graph.nodes():
                new_scores[node] = 1 + sum(
                    influence_scores[neighbor] * p
                    for neighbor in self.graph.predecessors(node)
                )
            influence_scores = new_scores

        seed_set = set(
            sorted(influence_scores, key=influence_scores.get, reverse=True)[:k]
        )
        return seed_set

    ### PMC ###
    def pmc(self, k, p=0.1):
        """PMC: Approssimazione usando grafi ridotti"""
        reduced_graph = self.graph.copy()
        for u, v in self.graph.edges():
            if random.random() > p:
                reduced_graph.remove_edge(u, v)

        seed_set = set(
            sorted(
                reduced_graph.nodes(),
                key=nx.degree_centrality(reduced_graph),
                reverse=True,
            )[:k]
        )
        return seed_set

    ### TIM+ ###
    def tim_plus(self, k, p=0.1, rr_sets=100):
        """TIM+: Reverse Reachable Set Sampling"""

        def generate_rr_set():
            node = random.choice(list(self.graph.nodes()))
            rr_set = set([node])
            queue = [node]
            while queue:
                current = queue.pop(0)
                for neighbor in self.graph.predecessors(current):
                    if neighbor not in rr_set and random.random() < p:
                        rr_set.add(neighbor)
                        queue.append(neighbor)
            return rr_set

        rr_sets_list = [generate_rr_set() for _ in range(rr_sets)]
        seed_set = set()
        for _ in range(k):
            max_node = max(
                self.graph.nodes(),
                key=lambda n: sum(1 for rr in rr_sets_list if n in rr),
            )
            seed_set.add(max_node)
            rr_sets_list = [rr for rr in rr_sets_list if max_node not in rr]
        return seed_set

    ### EaSyIM ###
    def easyim(self, k, p=0.1):
        """EaSyIM: Ottimizzato con Sketching e campioni"""
        sketch = {node: random.uniform(0, 1) for node in self.graph.nodes()}
        seed_set = set(sorted(sketch, key=sketch.get)[:k])
        return seed_set

    ### Sketching ###
    def sketching(self, k, p=0.1):
        """Sketching: Riduzione e selezione ottimizzata"""
        reduced_nodes = sorted(
            self.graph.nodes(), key=lambda n: self.graph.degree(n), reverse=True
        )[: len(self.graph.nodes()) // 2]
        subgraph = self.graph.subgraph(reduced_nodes)
        return set(sorted(subgraph.nodes(), key=subgraph.degree, reverse=True)[:k])

    ### Singles ###
    def singles(self, k, p=0.1):
        """Singles: Valutazione dei singoli nodi"""
        return set(
            sorted(
                self.graph.nodes(),
                key=lambda n: len(self.independent_cascade({n}, p)),
                reverse=True,
            )[:k]
        )


if __name__ == "__main__":

    # Paths to data files
    posts_path = "../../../data/post_data.csv"
    replies_path = "../../../data/replies_data.csv"
    followers_path = "../../../data/output.json"

    # Data processing
    processor = DataProcessor(posts_path, replies_path, followers_path)
    df_posts, df_replies, followers_data = processor.load_data()
    df = processor.preprocess_data(df_posts, df_replies)

    # Graph construction
    graph_builder = GraphConstructor(followers_data, df)
    graph_builder.build_graph()
    graph = graph_builder.graph

    # Adding thresholds to nodes
    for node in graph.nodes():
        graph.nodes[node]["threshold"] = random.uniform(0, 1)

    # Centrality calculation
    centralities = graph_builder.calculate_centralities()
    top_influencers = sorted(
        centralities["PageRank"].items(), key=lambda x: x[1], reverse=True
    )[:10]
    seed_nodes = [node for node, _ in top_influencers]

    # Influence models

    # Linear Threshold Model
    lt_model = InfluenceModels.linear_threshold_model(graph, seed_nodes)
    print("Number of nodes activated (LT Model):", len(lt_model))

    # Independent Cascade Model
    ic_model = InfluenceModels.independent_cascade_model(graph, seed_nodes, p=0.2)
    print("Number of nodes activated (IC Model):", len(ic_model))

    # Simulate SI (Susceptible-Infected)
    si_results = InfluenceModels.simulate_si(graph, beta=0.1, steps=100)
    # print("SI Model Results (first step):", si_results[0])

    # Simulate SIR (Susceptible-Infected-Recovered)
    sir_results = InfluenceModels.simulate_sir(graph, beta=0.1, gamma=0.05, steps=100)
    # print("SIR Model Results (first step):", sir_results[0])

    # Simulate SIS (Susceptible-Infected-Susceptible)
    sis_results = InfluenceModels.simulate_sis(graph, beta=0.1, gamma=0.05, steps=100)
    # print("SIS Model Results (first step):", sis_results[0])

    # Simulate SIRS (Susceptible-Infected-Recovered-Susceptible)
    sirs_results = InfluenceModels.simulate_sirs(
        graph, beta=0.1, gamma=0.05, lambda_=0.01, steps=100
    )
    # print("SIRS Model Results (first step):", sirs_results[0])

    # Simulate GT (General Threshold)
    gt_results = InfluenceModels.simulate_gt(
        graph,
        thresholds={node: random.uniform(0, 1) for node in graph.nodes()},
        steps=100,
    )
    # print("GT Model Results (first step):", gt_results[0])

    # Simulate GC (General Cascade)
    gc_results = InfluenceModels.simulate_gc(graph, prob=0.1, steps=100)
    # print("GC Model Results (first step):", gc_results[0])

    # Simulate TR (Threshold Random)
    tr_results = InfluenceModels.simulate_tr(graph, prob=0.1, steps=100)
    # print("TR Model Results (first step):", tr_results[0])

    # Simulate DC (Decay Cascade)
    dc_results = InfluenceModels.simulate_dc(
        graph, initial_prob=0.1, decay_factor=0.95, steps=100
    )
    # print("DC Model Results (first step):", dc_results[0])

    # Friend-Foe Dynamic Linear Threshold Model
    def trust_function(neighbor, node):
        # A simple trust function: return 1 for all neighbors (can be customized)
        return 1

    friend_foe_results = InfluenceModels.friend_foe_dynamic_linear_threshold(
        graph, seed_nodes, trust_function
    )
    # print("Friend-Foe Dynamic Linear Threshold Model Results:", len(friend_foe_results))

    # Print Top Influencers by PageRank
    print("Top Influencers by PageRank:", top_influencers)
