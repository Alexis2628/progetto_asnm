from .linear_threshold_model import linear_threshold_model
from .independent_cascade_model import independent_cascade_model
from .simulate_si import simulate_si
from .simulate_sir import simulate_sir
from .simulate_sis import simulate_sis
from .simulate_sirs import simulate_sirs
from .simulate_gt import simulate_gt
from .simulate_gc import simulate_gc
from .simulate_tr import simulate_tr
from .simulate_dc import simulate_dc
from .friend_foe_model import friend_foe_dynamic_linear_threshold

class Models:
    def __init__(self, graph):
        """
        Costruttore della classe Models.
        :param graph: Il grafo su cui eseguire i modelli di diffusione.
        """
        self.graph = graph

    # Modelli con semi
    def run_linear_threshold(self, seed_nodes):
        """Esegue il modello Linear Threshold con semi iniziali."""
        return linear_threshold_model(self.graph, seed_nodes)

    def run_independent_cascade(self, seed_nodes, p=0.1):
        """Esegue il modello Independent Cascade con semi iniziali."""
        return independent_cascade_model(self.graph, seed_nodes, p)

    # Modelli epidemiologici
    def run_si(self, beta=0.1, steps=100):
        """Esegue il modello SI con parametri beta e numero di passi."""
        return simulate_si(self.graph, beta, steps)

    def run_sir(self, beta=0.1, gamma=0.05, steps=100):
        """Esegue il modello SIR con parametri beta, gamma e numero di passi."""
        return simulate_sir(self.graph, beta, gamma, steps)

    def run_sis(self, beta=0.1, gamma=0.05, steps=100):
        """Esegue il modello SIS con parametri beta, gamma e numero di passi."""
        return simulate_sis(self.graph, beta, gamma, steps)

    def run_sirs(self, beta=0.1, gamma=0.05, lambda_=0.01, steps=100):
        """Esegue il modello SIRS con parametri beta, gamma, lambda e numero di passi."""
        return simulate_sirs(self.graph, beta, gamma, lambda_, steps)

    # Modelli basati su soglie
    def run_gt(self, thresholds, steps=100):
        """Esegue il modello General Threshold con soglie specificate."""
        return simulate_gt(self.graph, thresholds, steps)

    # Modelli stocastici
    def run_gc(self, prob=0.1, steps=100):
        """Esegue il modello General Cascade con probabilità di attivazione."""
        return simulate_gc(self.graph, prob, steps)

    def run_tr(self, steps=100):
        """Esegue il modello Threshold Reversibile con probabilità e numero di passi."""
        return simulate_tr(self.graph, steps)

    def run_dc(self, initial_prob=0.1, decay_factor=0.95, steps=100):
        """Esegue il modello Deterministic and Chaotic Diffusion con parametri di inizializzazione e decadimento."""
        return simulate_dc(self.graph, initial_prob, decay_factor, steps)

    # Modello Friend-Foe
    def run_friend_foe(self, seed_nodes, trust_function):
        """Esegue il modello Friend-Foe con semi iniziali e funzione di fiducia specificata."""
        return friend_foe_dynamic_linear_threshold(self.graph, seed_nodes, trust_function)

    def run_all(self, seed_nodes=None, **kwargs):
        """
        Esegue tutti i modelli di diffusione disponibili con i parametri specificati.
        :param seed_nodes: Lista di nodi iniziali per modelli con semi.
        :param thresholds: Dizionario delle soglie per i modelli basati su soglie.
        :param kwargs: Parametri aggiuntivi per specificare i dettagli dei modelli.
        :return: Dizionario con i risultati di tutti i modelli eseguiti.
        """
        results = {}

        # Modelli con semi
        if seed_nodes is not None:
            results['Linear Threshold'] = self.run_linear_threshold(seed_nodes)
            results['Independent Cascade'] = self.run_independent_cascade(seed_nodes, kwargs.get('p', 0.1))

        # Modelli epidemiologici
        results['SI'] = self.run_si(kwargs.get('beta', 0.1), kwargs.get('steps', 100))
        results['SIR'] = self.run_sir(kwargs.get('beta', 0.1), kwargs.get('gamma', 0.05), kwargs.get('steps', 100))
        results['SIS'] = self.run_sis(kwargs.get('beta', 0.1), kwargs.get('gamma', 0.05), kwargs.get('steps', 100))
        results['SIRS'] = self.run_sirs(kwargs.get('beta', 0.1), kwargs.get('gamma', 0.05), kwargs.get('lambda_', 0.01), kwargs.get('steps', 100))

        
        results['General Threshold'] = self.run_gt(kwargs.get('steps', 100))

        # Modelli stocastici
        results['General Cascade'] = self.run_gc(kwargs.get('prob', 0.1), kwargs.get('steps', 100))
        results['Threshold Reversibile'] = self.run_tr(kwargs.get('steps', 100))
        results['Deterministic and Chaotic Diffusion'] = self.run_dc(kwargs.get('initial_prob', 0.1), kwargs.get('decay_factor', 0.95), kwargs.get('steps', 100))

        # Modello Friend-Foe
        if seed_nodes is not None and 'trust_function' in kwargs:
            results['Friend-Foe'] = self.run_friend_foe(seed_nodes, kwargs['trust_function'])

        return results