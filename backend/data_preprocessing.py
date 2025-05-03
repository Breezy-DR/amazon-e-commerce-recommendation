import pandas as pd
import numpy as np

products_df = pd.read_csv('../data/amazon.csv')

products_df.loc[:, 'rating_count'] = products_df['rating_count'].fillna(0)

products_df_cleaned = products_df.drop_duplicates(subset=['user_id', 'product_id'])

products_df_cleaned.insert(3, 'final_category', products_df_cleaned['category'].str.split('|').str[-1])

products_df_cleaned.to_csv("../data/amazon_cleaned.csv", index=False)