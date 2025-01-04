from utils.logger import setup_logger
from graph.GraphConstructor import GraphConstructor
from utils.plotter import Plotter
from utils.file_utils import save_results_to_file, convert_sets_in_dict
import os
from utils.run_models import run_models_on_different_seed_lengths,run_models_on_differnt_centralities
import random
random.seed(42)
from models.models import Models
from optimizers.optimizer import Optimizer


if __name__ == "__main__":
    # Configurazione del logger
    setup_logger()

    # Parametri
    run_models = True
    run_optimizers = False
    print_centrality = False
    save_to_file = False
    save_fig = True
    steps = 100
    seed_lengths = [10, 50, 100, 200]  # Varie lunghezze di seed_nodes

    # Creazione del grafo
    graph_builder = GraphConstructor(followers_path="dataset/dataset_cleaned.json")
    graph_builder.build_graph()
    graph = graph_builder.graph

    # Logging del grafo
    graph_builder.log_graph_info()

    # Calcolo delle centralità
    centralities = graph_builder.calculate_centralities()
    if print_centrality:
        graph_builder.print_top_centralities(centralities)

    if run_models:
        # Estrazione dei nodi seed
        run_models_on_differnt_centralities(centralities, graph_builder, save_to_file, save_fig,100,steps)
        top_influencers = sorted(centralities["Katz Centrality"].items(), key=lambda x: x[1], reverse=True)
        run_models_on_different_seed_lengths(graph_builder,top_influencers,save_to_file,save_fig,steps,seed_lengths)

    if run_optimizers:
        # Esecuzione degli algoritmi di ottimizzazione
        optimizer = Optimizer(graph)
        optimization_results = optimizer.run_all(k=10, p=0.1, path_limit=3, threshold=0.5, rr_sets=100)

        # Salvataggio dei risultati
        if save_to_file:
            output_dir = r"Code\notebook\Studio della propagazione dell'influenza\output/algo_output"
            save_results_to_file(optimization_results, os.path.join(output_dir, "steps"))
