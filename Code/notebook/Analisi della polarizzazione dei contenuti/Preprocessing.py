import json
import tiktoken
from deep_translator import GoogleTranslator
import re
import logging

# Configura il logging
logging.basicConfig(level=logging.INFO)
tokenizer = tiktoken.get_encoding("cl100k_base")
# Funzione di preprocessing
def preprocess_text(text):
    # Rimozione di simboli speciali e trasformazione in minuscolo
    text = re.sub(r'[\^\w\s]', '', text)
    text = text.lower()
    logging.debug(f"Testo preprocessato: {text}")
    return text

def process_user_data(user_data):
    all_texts = []
    translated_posts = []
    for post in user_data:
        if 'Caption Text' in post:
            try:
                translated_text = GoogleTranslator(source='auto', target='en').translate(post['Caption Text'])
                if translated_text:
                    all_texts.append(translated_text)
                    post_copy = post.copy()
                    post_copy['Caption Text'] = translated_text
                    translated_posts.append(post_copy)
                    logging.info(f"Tradotto: {post['Caption Text']} -> {translated_text}")
                else:
                    logging.warning(f"Traduzione fallita per: {post['Caption Text']}")
            except Exception as e:
                logging.error(f"Errore durante la traduzione: {e}")
    
    if not all_texts:
        logging.info("Nessun testo tradotto trovato.")
        return [], []
    
    combined_text = " ".join(all_texts)
    processed_text = preprocess_text(combined_text)
    
    # Tokenizzazione con tiktoken
    
    tokens = tokenizer.encode(processed_text)
    
    logging.info(f"Tokenizzazione completata. Numero di token: {len(tokens)}")
    return translated_posts, tokens

followers_path = "data/final_dataset.json"

with open(followers_path, "rb") as f:
    data = json.load(f)

processed_count = 0
max_process = 20

for user_id, user_info in data.items():
    if processed_count >= max_process:
        logging.info("Limite di processi raggiunto.")
        break
    
    # Verifica se i dati dell'utente principale sono già stati processati
    if "user_data" in user_info and user_info["user_data"] and "user_data_translated" not in user_info and "text_token" not in user_info:
        translated_posts, text_token = process_user_data(user_info["user_data"])
        user_info["user_data_translated"] = translated_posts
        user_info["text_token"] = text_token
        processed_count += 1
        logging.info(f"Dati utente {user_id} processati.")
    
    # Verifica e processa i follower
    for follower in user_info.get("followers", []):
        if processed_count >= max_process:
            logging.info("Limite di processi raggiunto durante la verifica dei follower.")
            break

        if "user_data" in follower and follower["user_data"] and "user_data_translated" not in follower and "text_token" not in follower:
            translated_posts, text_token = process_user_data(follower["user_data"])
            follower["user_data_translated"] = translated_posts
            follower["text_token"] = text_token
            processed_count += 1
            logging.info(f"Dati follower processati per utente {user_id}.")

# Salva il JSON aggiornato
updated_path = "data/final_dataset.json"
with open(updated_path, "w") as f:
    json.dump(data, f, indent=4)

logging.info(f"JSON aggiornato salvato in {updated_path}")
print(f"JSON aggiornato salvato in {updated_path}")

