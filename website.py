import streamlit as st
import warnings
from backend.database import db, df
warnings.filterwarnings('ignore')

recommender = st.Page(
    "pages/recommendation_page.py", title="Product Recommender", icon=":material/shopping_bag:"
)
chatbot = st.Page(
    "pages/chatbot_page.py", title="Chatbot", icon=":material/chat:"
)
evaluation = st.Page(
    "pages/eval_page.py", title="Evaluation"
)

pg = st.navigation(
        {
            "Choose how you want to recommend items": [recommender, chatbot, evaluation],
        }
    )

pg.run()