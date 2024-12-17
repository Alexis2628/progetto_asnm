import numpy as np
import pandas as pd
import json

class DataProcessor:
    def __init__(self, posts_path, replies_path, followers_path):
        self.posts_path = posts_path
        self.replies_path = replies_path
        self.followers_path = followers_path

    def load_data(self):
        df_posts = pd.read_csv(self.posts_path)
        df_replies = pd.read_csv(self.replies_path)
        with open(self.followers_path, "r", encoding="utf-8") as file:
            followers_data = json.load(file)

        return df_posts, df_replies, followers_data

    def preprocess_data(self, df_posts, df_replies):
        missing_columns = [col for col in df_replies.columns if col not in df_posts.columns]
        for col in missing_columns:
            df_posts[col] = np.nan

        df_combined = pd.concat([df_posts, df_replies], ignore_index=True)
        df_combined.columns = [col.lower().replace(" ", "_") for col in df_combined.columns]
        df_combined.drop(columns=[
            "parent_post_id", "direct_reply_count", "repost_count", "following", "followed_by",
            "can_reply", "reply_control", "reshare_count", "is_verified"
        ], axis=1, inplace=True)

        df_combined['like_count'] = df_combined['like_count'].fillna(0).astype(int)
        df_combined['quote_count'] = df_combined['quote_count'].fillna(0).astype(int)
        return df_combined.drop_duplicates()