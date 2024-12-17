import json
import csv

# Carica il file JSON
with open(r"../../data/output.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# File CSV per i nodi
nodes_file = "nodes.csv"
# File CSV per gli archi
edges_file = "edges.csv"

# Set per tenere traccia dei nodi unici
nodes_set = set()

# Liste per memorizzare nodi e archi
nodes_list = []
edges_list = []

# Costruzione dei nodi e degli archi
for user_id, user_info in data.items():
    # Aggiungi il nodo del proprietario
    nodes_set.add(user_id)
    nodes_list.append({
        "Id": user_id,
        "Label": user_info["username"]
    })
    
    # Aggiungi i follower come nodi e crea archi
    for follower in user_info["followers"]:
        follower_id = follower["user_id"]
        if follower_id not in nodes_set:
            nodes_set.add(follower_id)
            nodes_list.append({
                "Id": follower_id,
                "Label": follower["username"]
            })
        # Aggiungi l'arco (da follower al proprietario)
        edges_list.append({
            "Source": follower_id,
            "Target": user_id,
            "Type": "directed"
        })

# Scrittura del file nodes.csv
with open(nodes_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Id", "Label"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(nodes_list)

# Scrittura del file edges.csv
with open(edges_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Source", "Target", "Type"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(edges_list)

print(f"File CSV creati: {nodes_file}, {edges_file}")
