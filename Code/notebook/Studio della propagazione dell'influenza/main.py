import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from utils.logger import setup_logger
from Code.notebook.graph.GraphConstructor import GraphConstructor
from utils.plotter import Plotter
from utils.file_utils import save_results_to_file, convert_sets_in_dict
import os
from utils.run_models import run_models_on_different_seed_lengths,run_models_on_differnt_centralities,run_models_on_differnt_optimizer
import random
random.seed(42)
from models.models import Models
from optimizers.optimizer import Optimizer
import logging

setup_logger()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting the influence propagation analysis script.")

    # Parameters
    run_models = True
    run_optimizers = True
    print_centrality = True
    save_to_file = True
    save_fig = True
    steps = 100
    seed_lengths = [10, 50, 100, 200]  # Various seed_node lengths

    logger.info("Parameters set. Run models: %s, Run optimizers: %s", run_models, run_optimizers)

    # Graph construction
    followers_path = "dataset/dataset_cleaned.json"
    logger.info("Initializing GraphConstructor with followers_path: %s", followers_path)
    graph_builder = GraphConstructor(followers_path=followers_path)

    logger.info("Building the graph...")
    graph_builder.build_graph()
    graph = graph_builder.graph
    logger.info("Graph built successfully")

    # Log graph information
    logger.info("Logging graph information...")
    graph_builder.log_graph_info()

    # Centrality calculation
    logger.info("Calculating centralities...")
    centralities = graph_builder.calculate_centralities()
    logger.info("Centralities calculated successfully.")

    if print_centrality:
        logger.info("Printing top centralities...")
        graph_builder.print_top_centralities(centralities)

    if run_models:
        logger.info("Running models on different centralities...")
        run_models_on_differnt_centralities(centralities, graph_builder, save_to_file, save_fig, 100, steps)

        logger.info("Sorting top influencers by Katz Centrality...")
        top_influencers = sorted(centralities["Katz Centrality"].items(), key=lambda x: x[1], reverse=True)

        logger.info("Running models on different seed lengths...")
        run_models_on_different_seed_lengths(graph_builder, top_influencers, save_to_file, save_fig, steps, seed_lengths)

    if run_optimizers:
        logger.info("Running optimizers...")
        optimizer = Optimizer(graph)
        optimization_results = optimizer.run_all(k=10, p=0.1, path_limit=3, threshold=0.5, rr_sets=100)
        logger.info("Optimization completed successfully.")
        run_models_on_differnt_optimizer(optimization_results, graph_builder, save_fig, steps)
        if save_to_file:
            output_dir = r"Code\notebook\Studio della propagazione dell'influenza\output/optimizer_output"
            logger.info("Saving optimization results to directory: %s", output_dir)
            save_results_to_file(optimization_results, os.path.join(output_dir, "save"))
            logger.info("Results saved successfully.")
            
    logger.info("Script execution completed.")