import json
from utils import makecsv
from threads_interface import ThreadsInterface
import pandas as pd
import os
class Retriever:

    def __init__(self):
        self.ti = ThreadsInterface()
        path_to_replies = 'var/replies.json'
        path_to_threads = 'var/threads.json'

        # Controlla se i file esistono e carica i DataFrame
        if os.path.exists(path_to_replies):
            self.df_replies = pd.read_json(path_to_replies)
        else:
            self.df_replies = pd.DataFrame()

        if os.path.exists(path_to_threads):
            self.df_threads = pd.read_json(path_to_threads)
        else:
            self.df_threads = pd.DataFrame()
    

    def flatten_dict(self,base, parent_key='', sep='_'):
        items = []
        for k, v in base.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    items.extend(self.flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def run_replies(self,id=314216):
        if self.df_replies.empty or id not in self.df_replies["post_user_pk"]:
            data = self.ti.retrieve_user_replies(id)
            threads = data['data']['mediaData']['threads']
            flattened_data = [self.flatten_dict(item) for thread in threads for item in thread['thread_items']]
            df = pd.DataFrame(flattened_data,columns=["post_user_profile_pic_url",
                                                    "post_user_username",
                                                    "post_user_pk",
                                                    "post_pk",
                                                    "post_has_audio",
                                                    "post_text_post_app_info_reply_to_author_username",
                                                    "post_caption_text",
                                                    "post_taken_at",
                                                    "post_like_count",
                                                    "post_code",
                                                    "post_id"])
            self.df_replies=pd.concat([self.df_replies, df],ignore_index=True)

    def retrieve_thread_by_id(self,id):
        return self.ti.retrieve_thread(thread_id=id)
    def run_threads(self,id=314216):
        
        if self.df_threads.empty or id not in self.df_threads["post_user_pk"]:
            data = self.ti.retrieve_user_threads(id)
            threads = data['data']['mediaData']['threads']
            flattened_data = [self.flatten_dict(item) for thread in threads for item in thread['thread_items']]
            df = pd.DataFrame(flattened_data,columns=[ "post_user_profile_pic_url",
                                                    "post_user_username",
                                                    "post_user_pk",
                                                    "post_pk",
                                                    "post_has_audio",
                                                    "post_text_post_app_info_reply_to_author_username",
                                                    "post_caption_text",
                                                    "post_taken_at",
                                                    "post_like_count",
                                                    "post_code",
                                                    "post_id"])
            self.df_threads=pd.concat([self.df_threads, df],ignore_index=True)


    def to_csv(self):
        self.df_replies.to_csv("var/replies.csv",sep=",")
        self.df_threads.to_csv("var/threads.csv",sep=",")

    def to_json(self):
        self.df_replies.to_json("var/replies.json",indent=10)
        self.df_threads.to_json("var/threads.json",indent=10)

    def retrieve_thread_by_query(self, id):
        dati = self.ti.retrieve_thread_by_query(id)
        df = pd.DataFrame(columns=['Post ID', 'User ID', 'Thread Type', 'Username', 'Profile Picture URL', 'Text Post', 'Tags', 'Is Reply', 'Like Count', 'Quote Count', 'Caption Text', 'Caption Created At (UTC)', 'Direct Reply Count', 'Repost Count'])
        for edges in dati["data"]["searchResults"]["edges"]:
            thread_type = edges["node"]["thread"]["thread_type"]
            for threads_item in edges["node"]["thread"]["thread_items"]:
                data:dict = threads_item["post"]    
                post_id = data.get('pk')
                user_id = data['user'].get('id')
                is_reply = data['text_post_app_info'].get("is_reply")
                username = data['user'].get('username')
                profile_pic_url = data['user'].get('profile_pic_url')
                text_post = data['text_post_app_info']['text_fragments']['fragments'][0]['plaintext']
                tags = ' '.join(fragment['plaintext'] for fragment in data['text_post_app_info']['text_fragments']['fragments'][1:])
                #image_url = data['image_versions2']['candidates'][0]['url']
                like_count = data.get('like_count')
                quote_count = data["text_post_app_info"].get('quote_count')
                caption_text = data['caption'].get('text')
                caption_created_at = data.get('taken_at')
                direct_reply_count = data.get('direct_reply_count')  # Nuovo campo
                repost_count = data["text_post_app_info"].get('repost_count')  # Nuovo campo
                likers = data.get('likers') 
                # Crea un DataFrame con i dati estratti
                new_df = pd.DataFrame({
                    'Post ID': [post_id],
                    'User ID': [user_id],
                    "Thread Type" :[thread_type],
                    'Username': [username],
                    'Profile Picture URL': [profile_pic_url],
                    'Text Post': [text_post],
                    'Tags': [tags],
                    "Is Reply" :[is_reply],
                    'Like Count': [like_count],
                    "Quote Count": [quote_count],
                    'Caption Text': [caption_text],
                    'Caption Created At (UTC)': [caption_created_at],
                    'Direct Reply Count': [direct_reply_count],  # Nuovo campo
                    'Repost Count': [repost_count],
                })
                df = pd.concat([df, new_df], ignore_index=True)
        return df


# ret = Retriever()
# df = pd.DataFrame()
# df2 = ret.retrieve_thread_by_query("olimpiadi")

# for id in df2["User ID"]:
#     ret.run_threads(id)
#     ret.run_replies(id)
# df=pd.concat([df,df2],ignore_index=True)

# df.to_json("var/threads_by_query.json",indent=10)
# ret.to_json()

makecsv('var/replies.json','var/threads.json',"var/threads_by_query.json")