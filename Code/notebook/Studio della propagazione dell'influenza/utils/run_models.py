from models.models import Models
from utils.file_utils import save_results_to_file, convert_sets_in_dict
from utils.plotter import Plotter
import os

def run_models_on_different_seed_lengths(graph_builder,top_influencers,save_to_file,save_fig,steps,seed_lengths):
    graph = graph_builder.graph
    all_results = {}
    output_dir = r"Code\notebook\Studio della propagazione dell'influenza\output/model_output"
    for seed_length in seed_lengths:
        seed_nodes = [node for node, _ in top_influencers[:seed_length]]
    # Esecuzione dei modelli
        models = Models(graph)
        model_results = models.run_all(
            seed_nodes=seed_nodes,
            p=0.4,
            beta=0.3,
            gamma=0.03,
            lambda_=0.1,
            steps=steps,
            prob=0.4,
            initial_prob=0.1,
            decay_factor=0.95,
            trust_function=graph_builder.trust_function,
        )
        all_results[seed_length] = model_results
        # Salvataggio e visualizzazione risultati
            
        if save_to_file:
            save_results_to_file(model_results, os.path.join(output_dir, f"steps_{seed_length}"))
    if save_fig:
        plotter = Plotter(output_dir+"/plot_comparative_seed_length")
        # plotter.plot_model_results(model_results)
        plotter.plot_all_results(all_results, seed_lengths)


def run_models_on_differnt_centralities(centralities, graph_builder, save_to_file, save_fig,seed_length,steps):
    centrality_metrics = ["Degree Centrality", "Closeness Centrality", "Betweenness Centrality",
                          "PageRank", "Katz Centrality","Eigenvector Centrality","HITS Hub Scores","HITS Authority Scores"]
    graph = graph_builder.graph
    seed_nodes_by_centrality = {}

    for metric in centrality_metrics:
        sorted_nodes = sorted(centralities[metric].items(), key=lambda x: x[1], reverse=True)
        seed_nodes_by_centrality[metric] = [node for node, _ in sorted_nodes[:seed_length]]

        all_results_by_centrality = {}
        output_dir = r"Code\notebook\Studio della propagazione dell'influenza\output\model_output"

        for metric, seed_nodes in seed_nodes_by_centrality.items():
            # Esecuzione dei modelli
            models = Models(graph)
            model_results = models.run_all(
                seed_nodes=seed_nodes,
                p=0.4,
                beta=0.3,
                gamma=0.03,
                lambda_=0.1,
                steps=steps,
                prob=0.4,
                initial_prob=0.1,
                decay_factor=0.95,
                trust_function=graph_builder.trust_function,
            )
            all_results_by_centrality[metric] = model_results

            # Salvataggio dei risultati
            if save_to_file:
                save_results_to_file(model_results, os.path.join(output_dir, f"{metric}_steps_{seed_length}"))

        # Visualizzazione dei risultati
    if save_fig:
        plotter = Plotter(output_dir + "/plot_centrality_comparison")
        plotter.plot_all_results(all_results_by_centrality, centrality_metrics,use_centrality_labels=True)