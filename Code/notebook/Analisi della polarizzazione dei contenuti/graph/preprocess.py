import json

# Parametri configurabili
MIN_FOLLOWERS = 10  # Numero minimo di follower per conservare un utente
MAX_NODES = 5000  # Numero massimo di nodi nel dataset ridotto
MAX_FOLLOWERS_PER_USER = 5000  # Numero massimo di follower per utente

# Carica il file JSON
with open('final_dataset.json', 'rb') as file:
    data = json.load(file)

# Funzione per rimuovere duplicati dei post basandosi sull'ID del post
def remove_duplicate_posts(posts):
    unique_posts = {}
    for post in posts:
        post_id = post.get("Post ID", "")
        if post_id and post_id not in unique_posts:
            unique_posts[post_id] = post
    return list(unique_posts.values())

# Funzione per verificare se un nodo contiene testo significativo
def has_text(posts):
    for post in posts:
        if post.get("Caption Text", "").strip():  # Controlla se il testo non è vuoto
            return True
    return False

# Prepara il dataset ridotto
reduced_data = {}
total_nodes = 0

for user_id, user_info in data.items():
    # Pulisci e rimuovi duplicati nei post
    user_info['user_data_translated'] = remove_duplicate_posts(
        user_info.get('user_data_translated', [])
    )
    followers = user_info.get("followers", [])
    
    # Filtra utenti con un numero sufficiente di follower
    if len(followers) >= MIN_FOLLOWERS:
        # Pulisci e rimuovi duplicati nei post dei follower
        filtered_followers = []
        for follower in followers:
            follower['user_data_translated'] = remove_duplicate_posts(
                follower.get('user_data_translated', [])
            )
            if has_text(follower['user_data_translated']):
                filtered_followers.append(follower)
        
        # Limita il numero massimo di follower per utente
        filtered_followers = filtered_followers[:MAX_FOLLOWERS_PER_USER]

        # Aggiungi l'utente al dataset ridotto
        reduced_data[user_id] = {
            "username": user_info.get("username", ""),
            "followers": filtered_followers,
            "user_data_translated": user_info.get("user_data_translated", [])
        }

        # Aggiorna il conteggio dei nodi
        total_nodes += 1 + len(filtered_followers)
        
        # Smetti di aggiungere nuovi nodi se il limite totale è raggiunto
        if total_nodes >= MAX_NODES:
            break

# Rimuovi i post dagli utenti meno significativi per raggiungere il limite
if total_nodes > MAX_NODES:
    for user_id, user_info in list(reduced_data.items()):
        if total_nodes <= MAX_NODES:
            break
        # Rimuovi i post dell'utente ma mantieni i follower
        if user_info.get("user_data_translated"):
            user_info["user_data_translated"] = []
            total_nodes -= 1

# Salva il nuovo dataset in formato JSON
with open('dataset.json', 'w') as output_file:
    json.dump(reduced_data, output_file, indent=4)

print("Dataset ridotto salvato in 'dataset.json'.")
