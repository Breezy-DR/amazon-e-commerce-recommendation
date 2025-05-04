import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import pandas as pd
from google import genai
from google.genai import types
from google.api_core import retry
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini client
genai_client = genai.Client(api_key=GOOGLE_API_KEY)

# Retry setup for API calls
is_retriable_error = lambda e: isinstance(e, genai.errors.APIError) and e.code in {429, 503}
genai.models.Models.generate_content = retry.Retry(predicate=is_retriable_error)(genai.models.Models.generate_content)

# Embedding Function using Gemini API
class GeminiEmbedding(EmbeddingFunction):
    def __init__(self, is_document=True):
        self.is_document = is_document

    @retry.Retry(predicate=is_retriable_error)
    def __call__(self, inputs: Documents) -> Embeddings:
        task_type = "retrieval_document" if self.is_document else "retrieval_query"
        response = genai_client.models.embed_content(
            model="models/text-embedding-004",
            contents=inputs,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        return [embedding.values for embedding in response.embeddings]

# Constants
DB_NAME = "amazon_product_db"
SELECTED_COLUMNS = ['final_category', 'product_name', 'actual_price', 'discounted_price', 'rating', 'rating_count',
                    'product_link']

def initialize_database():
    """Initialize ChromaDB and load embeddings from CSV."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(base_dir, "..", "data", "amazon_cleaned.csv")
    products_df = pd.read_csv(csv_file_path)

    chroma_client = chromadb.Client()
    embedding_function = GeminiEmbedding()
    collection = chroma_client.get_or_create_collection(name=DB_NAME, embedding_function=embedding_function)

    batch_size = 80
    document_batch = []
    id_batch = []

    for idx, row in products_df.iterrows():
        document = f"""
        PRODUCT NAME: {row['product_name']}
        DESCRIPTION: {row['about_product']}
        PRICE: {row['discounted_price']}
        RATING: {row['rating']}
        RATING COUNT: {row['rating_count']}
        """
        document_batch.append(document)
        id_batch.append(str(idx))

        if len(document_batch) >= batch_size:
            collection.add(documents=document_batch, ids=id_batch)
            document_batch.clear()
            id_batch.clear()

    # Add any remaining documents
    if document_batch:
        collection.add(documents=document_batch, ids=id_batch)

    return collection, products_df

def recommend_similar_products(collection, products_df, user_query: str, top_k: int = 20):
    """Recommend similar products based on a query."""
    search_results = collection.query(query_texts=[user_query], n_results=top_k)
    matching_indices = [int(doc_id) for doc_id in search_results['ids'][0]]
    return products_df.loc[matching_indices, SELECTED_COLUMNS]