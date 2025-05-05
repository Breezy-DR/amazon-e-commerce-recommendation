from google import genai

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
# Create .env file inside the routes folder with variable API_KEY and your API key
API_KEY = os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY)

sample_text = "I want to open chapter 8 mathemathics 2 SMA."

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=f"Classify this text into one of the following actions: 'speak', 'pause', 'navigate', 'convert pdf', 'show list', 'show content', 'show chapter'. Only answer the action. The text is: '{sample_text}'",
)
print(response.text)