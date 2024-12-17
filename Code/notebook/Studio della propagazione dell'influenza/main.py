from utils.DataProcessor import DataProcessor
from utils.GraphConstructor import GraphConstructor
import random
from models import (
    linear_threshold_model,
    independent_cascade_model,
    simulate_si,
    simulate_sir,
    simulate_sis,
    simulate_sirs,
    simulate_gt,
    simulate_gc,
    simulate_tr,
    simulate_dc,
    friend_foe_dynamic_linear_threshold,
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
    lt_model = linear_threshold_model(graph, seed_nodes)
    print("Number of nodes activated (LT Model):", len(lt_model))

    # Independent Cascade Model
    ic_model = independent_cascade_model(graph, seed_nodes, p=0.2)
    print("Number of nodes activated (IC Model):", len(ic_model))

    # Simulate SI (Susceptible-Infected)
    si_results = simulate_si(graph, beta=0.1, steps=100)
    # print("SI Model Results (first step):", si_results[0])

    # Simulate SIR (Susceptible-Infected-Recovered)
    sir_results = simulate_sir(graph, beta=0.1, gamma=0.05, steps=100)
    # print("SIR Model Results (first step):", sir_results[0])

    # Simulate SIS (Susceptible-Infected-Susceptible)
    sis_results = simulate_sis(graph, beta=0.1, gamma=0.05, steps=100)
    # print("SIS Model Results (first step):", sis_results[0])

    # Simulate SIRS (Susceptible-Infected-Recovered-Susceptible)
    sirs_results = simulate_sirs(graph, beta=0.1, gamma=0.05, lambda_=0.01, steps=100)
    # print("SIRS Model Results (first step):", sirs_results[0])

    # Simulate GT (General Threshold)
    gt_results = simulate_gt(
        graph,
        thresholds={node: random.uniform(0, 1) for node in graph.nodes()},
        steps=100,
    )
    # print("GT Model Results (first step):", gt_results[0])

    # Simulate GC (General Cascade)
    gc_results = simulate_gc(graph, prob=0.1, steps=100)
    # print("GC Model Results (first step):", gc_results[0])

    # Simulate TR (Threshold Random)
    tr_results = simulate_tr(graph, prob=0.1, steps=100)
    # print("TR Model Results (first step):", tr_results[0])

    # Simulate DC (Decay Cascade)
    dc_results = simulate_dc(graph, initial_prob=0.1, decay_factor=0.95, steps=100)
    # print("DC Model Results (first step):", dc_results[0])

    # Friend-Foe Dynamic Linear Threshold Model
    def trust_function(neighbor, node):
        # A simple trust function: return 1 for all neighbors (can be customized)
        return 1

    friend_foe_results = friend_foe_dynamic_linear_threshold(
        graph, seed_nodes, trust_function
    )
    # print("Friend-Foe Dynamic Linear Threshold Model Results:", len(friend_foe_results))

    # Print Top Influencers by PageRank
    print("Top Influencers by PageRank:", top_influencers)
