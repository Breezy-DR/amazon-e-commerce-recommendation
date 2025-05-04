import streamlit as st
from backend.recommender import recommend_similar_products
from website import db, df
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from backend.recommender import GeminiEmbedding

st.markdown("# Recommendation Page")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "amazon_cleaned.csv")
choice_df = pd.read_csv(csv_path)

# Pick a product from a category.
if 'recommendation_result' not in st.session_state or 'selected_product' not in st.session_state:
    categories = sorted(choice_df['final_category'].dropna().unique().tolist())
    selected_category = st.selectbox(
        "Select a category",
        ["-- Select a category --"] + categories,
        key='selected_category'
    )

    # Pick a category from the product dataset
    if selected_category != "-- Select a category --":
        filtered_df = choice_df[choice_df['final_category'] == selected_category]
        products_in_category = sorted(filtered_df['product_name'].dropna().unique().tolist())

        # Pick a product from the category selected
        selected_product = st.selectbox(
            "Select a product",
            ["-- Select a product --"] + products_in_category,
            key='selected_product'
        )

        if selected_product != "-- Select a product --":
            # Input the product into the recommendation system
            recdf = recommend_similar_products(db, df, f"I want a product similar to {selected_product}", top_k=11)

            # Remove the row where the recommended product name matches the selected product
            recdf = recdf[recdf["product_name"] != selected_product]

            st.subheader(f"Recommended products for: {selected_product}")
            st.dataframe(recdf)

            embedding_fn = GeminiEmbedding(is_document=False)

            # Get embedding for the selected product name (query)
            query_embedding = embedding_fn([selected_product])[0]

            # Get embeddings for each product name in the recommendations
            product_names = recdf["product_name"].tolist()
            rec_embeddings = embedding_fn(product_names)

            # Compute cosine similarities between query and each recommended product name
            similarities = cosine_similarity([query_embedding], rec_embeddings)[0]

            # Add similarity scores to your DataFrame
            recdf = recdf.copy()
            recdf["name_similarity"] = similarities

            recdf["is_relevant"] = (
                    (recdf["name_similarity"] >= 0.7) &
                    (recdf["final_category"] == selected_category)
            )

            precision_at_k = recdf["is_relevant"].sum() / len(recdf)

            # Optionally sort and show top matches
            recdf = recdf.sort_values(by="name_similarity", ascending=False)

            st.subheader("Cosine Similarity scores based on product name embeddings")
            st.dataframe(recdf[['final_category', 'product_name', 'name_similarity']])

            mean_similarity = round(np.mean(similarities), 4)
            max_similarity = round(np.max(similarities), 4)
            min_similarity = round(np.min(similarities), 4)

            st.write("Average similarity score:", mean_similarity)
            st.write("Max similarity score:", max_similarity)
            st.write("Min similarity score:", min_similarity)
            st.write("Precision@10 score:", precision_at_k)