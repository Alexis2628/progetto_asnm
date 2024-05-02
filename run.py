from threads_interface import ThreadsInterface
import pandas as pd

class Retriever:

    def __init__(self):
        self.ti = ThreadsInterface()
        self.df_replies = pd.DataFrame()
        self.df_threads = pd.DataFrame()
        self.list_user = []

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
        self.df_replies=pd.concat([self.df_replies, df])
        # post_user_profile_pic_url
        # post_user_username
        # post_user_pk   /id degli utenti
        # post_pk     /user_id
        # post_has_audio
        # post_text_post_app_info_reply_to_author_username
        # post_caption_text   /testo della risposta
        # post_taken_at    /timestamp di quando è stato pubblicato
        # post_like_count
        # post_code   / non so cosa sia
        # post_id


    def run_threads(self,id=314216):
        data = self.ti.retrieve_user_threads(id)
        threads = data['data']['mediaData']['threads']
        flattened_data = [self.flatten_dict(item) for thread in threads for item in thread['thread_items']]
        df = pd.DataFrame(flattened_data)#,columns=["post_user_profile_pic_url",
                                         #         "post_user_username",
                                         #         "post_user_pk",
                                         #          "post_pk",
                                         #          "post_has_audio",
                                         #          "post_text_post_app_info_reply_to_author_username",
                                         #          "post_caption_text",
                                         #          "post_taken_at",
                                         #          "post_like_count",
                                         #          "post_code",
                                         #          "post_id"])
        self.df_threads=pd.concat([self.df_threads, df])


    def to_csv(self):
        self.df_replies.to_csv("var/replies.csv",sep=",")
        self.df_threads.to_csv("var/threads.csv",sep=",")

    def to_json(self):
        self.df_replies.to_json("var/replies.json")
        self.df_threads.to_json("var/threads.json")


ret = Retriever()
ret.run_threads()
ret.to_json()
print(str(ret.df_threads.columns.values))
