import os
import pandas as pd
from threads_interface import ThreadsInterface  # Assicurati che questo sia il percorso corretto

def load_existing_data(filename):
    """Carica i dati esistenti da un file CSV."""
    if os.path.exists(filename):
        return pd.read_csv(filename).to_dict(orient='records')
    return []

def main():
    # Inizializza l'interfaccia per i Threads


    # File per salvare i dati
    csv_filename = 'collected_posts.csv'
    existing_posts = load_existing_data(csv_filename)

    # Converti la lista esistente in un set di ID dei post già visti
    seen_post_ids = {post['Post ID'] for post in existing_posts}

    all_posts = existing_posts.copy()  # Inizia dalla lista esistente

    # Liste di query che puoi utilizzare per recuperare vari post
    queries = [
        "#IntelligenzaArtificiale", 
        "AI", 
        "#ArtificialIntelligence", 
        "Machine Learning", 
        "Deep Learning", 
        "#MachineLearning", 
        "#DeepLearning", 
        "Intelligenza Artificiale etica", 
        "AI e futuro del lavoro", 
        "Reti neurali", 
        "#ChatGPT", 
        "#GPT", 
        "Tecnologie AI", 
        "#AITrends", 
        "Sviluppo AI", 
        "AI e salute", 
        "#AIinHealthcare", 
        "Automazione", 
        "#Automation", 
        "Impatto dell'AI sulla società", 
        "#AIImpact", 
        "AI e privacy", 
        "Innovazioni AI", 
        "AI nel business", 
        "#AIBusiness"
    ]

    # Effettua più chiamate per ogni query
    for query in queries:
        for _ in range(5):  # Esegui la query 5 volte per raccogliere più dati
            threads_interface = ThreadsInterface()
            print(f"Recuperando dati per la query: {query}")
            response = threads_interface.retrieve_thread_by_query(query)
            if response is None:
                continue
            if response["data"] is None:
                continue
            # Assicurati di estrarre i dati necessari dalla risposta
            if 'data' in response and 'searchResults' in response['data']:
                for edges in response["data"]["searchResults"]["edges"]:
                    thread_type = edges["node"]["thread"]["thread_type"]

                    for threads_item in edges["node"]["thread"]["thread_items"]:
                        data = threads_item["post"]
                        post_id = data.get('pk')
                        
                        # Ignora i post duplicati
                        if post_id in seen_post_ids:
                            continue

                        seen_post_ids.add(post_id)  # Aggiungi l'ID dei post visti

                        user_id = data['user'].get('id')
                        is_reply = data['text_post_app_info'].get("is_reply")
                        username = data['user'].get('username')
                        profile_pic_url = data['user'].get('profile_pic_url')
                        text_post = data['text_post_app_info']['text_fragments']['fragments'][0]['plaintext']
                        tags = ' '.join(fragment['plaintext'] for fragment in data['text_post_app_info']['text_fragments']['fragments'][1:])
                        like_count = data.get('like_count')
                        quote_count = data["text_post_app_info"].get('quote_count')
                        caption_text = data['caption'].get('text')
                        caption_created_at = data.get('taken_at')
                        direct_reply_count = data.get('direct_reply_count')  # Nuovo campo
                        repost_count = data["text_post_app_info"].get('repost_count')  # Nuovo campo
                        likers = data.get('likers')

                        # Raccogli i dati in un dizionario
                        post_data = {
                            'Post ID': post_id,
                            'User ID': user_id,
                            'Thread Type': thread_type,
                            'Username': username,
                            'Profile Picture URL': profile_pic_url,
                            'Text Post': text_post,
                            'Tags': tags,
                            'Is Reply': is_reply,
                            'Like Count': like_count,
                            'Quote Count': quote_count,
                            'Caption Text': caption_text,
                            'Caption Created At (UTC)': caption_created_at,
                            'Direct Reply Count': direct_reply_count,
                            'Repost Count': repost_count,
                        }
                        all_posts.append(post_data)

    # Stampa il numero totale di post raccolti


    # Salva i dati in CSV
    df = pd.DataFrame(all_posts)
    df.drop_duplicates(inplace=True)
    df.to_csv(csv_filename, index=False)
    print(f"Numero totale di post raccolti: {df["Post ID"].count()}")

if __name__ == "__main__":
    main()