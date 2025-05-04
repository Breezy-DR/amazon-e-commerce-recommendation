import streamlit as st
from backend.recommender import initialize_database

# Load ChromaDB database that consists of products data embedding
@st.cache_resource
def load_database():
    db, df = initialize_database()
    return db, df

db, df = load_database()