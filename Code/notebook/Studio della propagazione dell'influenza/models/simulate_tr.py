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

from models.simulate_gc import simulate_gc


def simulate_tr(graph, prob, steps):
    return simulate_gc(graph, prob, steps)
