from dotenv import load_dotenv
import os
from google import genai
from backend.recommender import recommend_similar_products
from backend.database import db, df
import streamlit as st
from google.genai import types

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai_client = genai.Client(api_key=GOOGLE_API_KEY)

# Prompt template
prompt = """You are a product recommendation system that is used to suggest the best matching products
based on the customer's product requests. Answer by recommending EXACTLY two products that fits the criteria
from the user's requests according to the products available. Answer it with the following format for each product, 
with each number INCLUDING A NEWLINE:
1. Product name: {product name}
2. Price: {price}
3. Ratings: {ratings (ratings above 4 are preferred)}
4. Reasons: {Reasons why user should by from either a price or quality standpoint (with detailed explanation)}.
5. Product link: {Clickable product link}
Make sure to structure everything cleanly with newlines and bullet points."""

config = types.GenerateContentConfig(
    system_instruction = prompt,
    temperature = 1.4,
    top_p = 0.6
)

def format_history(messages):
    gemini_history = []
    for msg in messages:
        role = msg["role"]
        if role == "assistant":
            role = "model"

        gemini_history.append({
            "role": role,
            "parts": [{"text": msg["content"]}],
        })
    return gemini_history

def generate_response(query, model_name):

    gemini_history = format_history(st.session_state.messages)

    chat_model = genai_client.chats.create(
        model=model_name,
        history=gemini_history,
        config=config
    )

    user_messages = [m for m in st.session_state.messages if m["role"] == "user"]

    if len(user_messages) == 1:
        recommendation = recommend_similar_products(db, df, query, 11)
        recommendation = recommendation.iloc[1:]
        parsed_prods = recommendation.to_json(orient='records')

        chat_message = f"""{prompt}

        User query:
        {query}
        
        Candidate products (JSON format):
        {parsed_prods}
        """
    else:
        chat_message = query

    response = chat_model.send_message(chat_message)
    return response.text


