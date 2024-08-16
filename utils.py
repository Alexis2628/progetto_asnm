import pandas as pd

def makecsv(replies,threads,threads_by_query):

    # Carica i file JSON
    replies_df = pd.read_json(replies)
    threads_df = pd.read_json(threads)
    threads_by_query_df = pd.read_json(threads_by_query)

    # Mappatura delle colonne per unificare i nomi
    replies_df.rename(columns={
        'post_user_profile_pic_url': 'Profile Picture URL',
        'post_user_username': 'Username',
        'post_user_pk': 'User ID',
        'post_pk': 'Post ID',
        'post_caption_text': 'Caption Text',
        'post_taken_at': 'Caption Created At (UTC)',
        'post_like_count': 'Like Count'
    }, inplace=True)

    threads_df.rename(columns={
        'post_user_profile_pic_url': 'Profile Picture URL',
        'post_user_username': 'Username',
        'post_user_pk': 'User ID',
        'post_pk': 'Post ID',
        'post_caption_text': 'Caption Text',
        'post_taken_at': 'Caption Created At (UTC)',
        'post_like_count': 'Like Count'
    }, inplace=True)

    # Aggiungi la colonna 'Source' per identificare la provenienza
    replies_df['Source'] = 'reply'
    threads_df['Source'] = 'thread'
    threads_by_query_df['Source'] = 'thread_by_query'

    # Concatenare i DataFrame
    merged_df = pd.concat([replies_df, threads_df, threads_by_query_df], ignore_index=True)

    # Esportare il DataFrame in un file CSV
    output_path = 'var/merged_data.csv'
    merged_df.to_csv(output_path, index=False)

    print(f"File CSV creato con successo: {output_path}")
