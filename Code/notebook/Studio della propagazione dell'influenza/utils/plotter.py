import matplotlib.pyplot as plt
import os
import logging
class Plotter:
    def __init__(self, output_dir):
        self.output_dir = os.path.join(output_dir, "figure")
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_model_results(self, model_results):
        for model_name, result in model_results.items():
            logging.info(f"Salvataggio figura : {model_name}")
            steps = list(result.keys())
            active_counts = []
            for step in steps:
                if isinstance(result[step], tuple):
                    _, I, _ = result[step]
                    active_counts.append(len(I))
                else:
                    active_counts.append(len(result[step]))
            # active_counts = [len(result[step]) for step in steps]
            plt.figure()
            plt.plot(steps, active_counts, marker="o", label=model_name)
            plt.title(f"{model_name} - Nodi attivi per step")
            plt.xlabel("Step")
            plt.ylabel("Numero di nodi attivi")
            plt.grid(True)
            plt.legend()
            plt.savefig(os.path.join(self.output_dir, f"{model_name}_plot.png"))
            plt.close()

    def plot_all_results(self, all_results, seed_lengths, use_centrality_labels=False):
        for seed_length, model_results in all_results.items():
            for model_name in next(iter(all_results.values())).keys():
                plt.figure(figsize=(10, 6))
                for seed_length in seed_lengths:
                    result = all_results[seed_length][model_name]
                    steps = list(result.keys())
                    active_counts = []

                    for step in steps:
                        if isinstance(result[step], tuple):
                            _, I, _ = result[step]
                            active_counts.append(len(I))
                        else:
                            active_counts.append(len(result[step]))

                    # Cambia l'etichetta in base al flag
                    label = f"Centrality: {seed_length}" if use_centrality_labels else f"Seed Length: {seed_length}"
                    plt.plot(steps, active_counts, marker="o", label=label)

                plt.title(f"{model_name} - Nodi attivi per step")
                plt.xlabel("Step")
                plt.ylabel("Numero di nodi attivi")
                plt.grid(True)
                plt.legend()
                plt.savefig(os.path.join(self.output_dir, f"{model_name}_comparative_plot.png"))
                plt.close()

            