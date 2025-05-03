import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from backend.recommender import recommend_similar_products, GeminiEmbedding
from website import db, df

st.markdown("# Batch Evaluation: Mean Similarity & Precision@k")

# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "amazon_cleaned.csv")
choice_df = pd.read_csv(csv_path)

csv_output_path = os.path.join(BASE_DIR, "..", "data", "evaluation_recommendation_output.csv")
txt_output_path = os.path.join(BASE_DIR, "..", "data", "evaluation_recommendation_score.txt")

# Filter categories with at least 11 unique products
category_counts = choice_df.groupby("final_category")["product_name"].nunique()
valid_categories = category_counts[category_counts >= 20].index.tolist()

st.write(f"Total valid categories with ≥20 unique products: {len(valid_categories)}")
st.write("Relevant recommended products have the same category as the queried product, and name similarity score ≥ 0.7.")

embedding_fn = GeminiEmbedding(is_document=False)

results = []

if os.path.exists(csv_output_path) and os.path.exists(txt_output_path):
    # Load and display from file
    st.write("Files exist. Showing results")
    result_df = pd.read_csv(csv_output_path)
    st.subheader("Evaluation Results (Loaded from File)")
    st.dataframe(result_df)

    st.subheader("Summary Statistics (Loaded from File)")
    with open(txt_output_path, "r", encoding="utf-8") as f:
        summary = f.read()
    st.text(summary)

else:
    st.write("Files don't exist. Calculating evaluation.")
    category_stats = {}

    for category in valid_categories:
        category_df = choice_df[choice_df["final_category"] == category].dropna(subset=["product_name"])
        unique_products = category_df["product_name"].unique()

        total_similarity = 0
        total_precision = 0
        total_relevant = 0
        evaluated_products = 0
        total_products = 0

        for product in unique_products:
            try:
                recdf = recommend_similar_products(db, df, f"I want a product similar to {product}", top_k=11)
                recdf = recdf[recdf["product_name"] != product].reset_index(drop=True)

                query_embedding = embedding_fn([product])[0]
                rec_embeddings = embedding_fn(recdf["product_name"].tolist())
                name_sim = cosine_similarity([query_embedding], rec_embeddings)[0]
                recdf["name_similarity"] = name_sim
                mean_name_similarity = np.mean(name_sim)

                recdf["is_relevant"] = (
                        (recdf["name_similarity"] >= 0.7) &
                        (recdf["final_category"] == category)
                )

                precision_at_k = recdf["is_relevant"].sum() / len(recdf)

                total_similarity += mean_name_similarity
                total_precision += precision_at_k
                total_relevant += recdf["is_relevant"].sum()
                evaluated_products += 1
                total_products += len(recdf)

            except Exception as e:
                print(f"Skipping {product} in {category} due to error: {e}")

        if evaluated_products > 0:
            category_stats[category] = {
                "mean_name_similarity": total_similarity / evaluated_products,
                "precision_at_k": total_precision / evaluated_products,
                "relevant_percentage": total_relevant / total_products
            }

    result_df = pd.DataFrame.from_dict(category_stats, orient="index").reset_index().rename(columns={"index": "category"})

    st.subheader("Evaluation Results")
    st.dataframe(result_df)

    mean_name_similarity = round(result_df["mean_name_similarity"].mean(), 4)
    precision_at_k = round(result_df["precision_at_k"].mean(), 4)

    st.subheader("Summary Statistics")
    st.write("Average Mean Similarity:", mean_name_similarity)
    st.write("Average Precision@k:", precision_at_k)

    result_df.to_csv(csv_output_path, index=False)

    with open(txt_output_path, "w", encoding="utf-8") as f:
        f.write(f"Average mean similarity: {mean_name_similarity}\n\n")
        f.write(f"Average Precision@k: {precision_at_k}\n\n")

