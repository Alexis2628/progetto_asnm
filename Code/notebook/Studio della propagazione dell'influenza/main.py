import json  # Aggiungi questa importazione
from utils.DataProcessor import DataProcessor
from utils.GraphConstructor import GraphConstructor
from models.models import Models
from optimizers.optimizer import Optimizer
import random
import os

if __name__ == "__main__":
    # Parametri per eseguire modelli e ottimizzatori
    run_models = True
    run_optimizers = False
    save_to_file = False
    steps = 100
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
    
    # Centrality calculation (for seed nodes)
    centralities = graph_builder.calculate_centralities()
    top_influencers = sorted(
        centralities["PageRank"].items(), key=lambda x: x[1], reverse=True
    )[:10]
    seed_nodes = [node for node, _ in top_influencers]

    if run_models:
        # Inizializzazione dei modelli
        models = Models(graph)

        # Esecuzione di tutti i modelli di diffusione con i parametri aggiornati
        model_results = models.run_all(
            seed_nodes=seed_nodes,
            beta=0.5,  # Incrementa il tasso di infezione
            gamma=0.01,  # Diminuisci il tasso di recupero
            lambda_=0.2,  # Incrementa il tasso di ri-suscettibilità
            steps=steps,  # Numero di passi per simulare più iterazioni
            prob=0.5,  # Probabilità di attivazione per modelli probabilistici
            initial_prob=0.5,  # Probabilità iniziale di attivazione
            decay_factor=0.99,  # Rallenta il decadimento delle probabilità
            trust_function=graph_builder.trust_function,  # Imposta una fiducia statica tra i nodi
        )

        # Stampa dei risultati dei modelli
        print("Risultati dei modelli (ultima iterazione):")
        for model_name, result in model_results.items():
            if result and isinstance(result, dict):
                last_step = result[list(result.keys())[-1]]  # ultima iterazione
                if isinstance(last_step, set):
                    print(f"{model_name}: {len(last_step)} nodi attivi")
                elif isinstance(last_step, dict):
                    print(f"{model_name}: {len(last_step)} nodi attivi (o altre informazioni)")
                elif isinstance(last_step, tuple):
                    # Specifico per modelli come SIR che restituiscono tuple (S, I, R)
                    _, I, _ = last_step
                    print(f"{model_name}: {len(I)} nodi infetti nell'ultima iterazione")
            elif isinstance(result, set):
                print(f"{model_name}: {len(result)} nodi attivi")
            else:
                print(f"{model_name}: {len(result)}")

        if save_to_file:
            output_dir = "output/model_output"
            os.makedirs(output_dir, exist_ok=True)
            for model_name, result in model_results.items():
                result_file_path = os.path.join(output_dir, f"{model_name}_results.json" if isinstance(result, dict) else f"{model_name}_results.txt")
                with open(result_file_path, "w") as f:
                    if isinstance(result, dict):
                        json.dump(result, f, indent=4)  # Salva come JSON
                    else:
                        f.write(f"{model_name}: {result}\n")

    if run_optimizers:
        # Inizializzazione dell'ottimizzatore
        optimizer = Optimizer(graph)

        # Esecuzione di tutti gli algoritmi di ottimizzazione con i parametri forniti
        optimization_results = optimizer.run_all(
            k=10,  # Numero di nodi da selezionare
            p=0.1,  # Probabilità di attivazione
            path_limit=3,  # Limite del numero di passi (profondità del cammino)
            threshold=0.5,  # Soglia di attivazione per i nodi
            rr_sets=100,  # Numero di set da utilizzare nell'ottimizzazione
        )

        # Stampa dei risultati degli algoritmi di ottimizzazione
        print("\nRisultati degli algoritmi di ottimizzazione:")
        for algo_name, result in optimization_results.items():
            print(f"{algo_name}: {result}")

        if save_to_file:
            output_dir = "output/algo_output"
            os.makedirs(output_dir, exist_ok=True)
            for algo_name, result in optimization_results.items():
                result_file_path = os.path.join(output_dir, f"{algo_name}_results.json" if isinstance(result, dict) else f"{algo_name}_results.txt")
                with open(result_file_path, "w") as f:
                    if isinstance(result, dict):
                        json.dump(result, f, indent=4)  # Salva come JSON
                    else:
                        f.write(f"{algo_name}: {result}\n")
