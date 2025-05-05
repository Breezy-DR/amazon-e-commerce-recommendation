from typing import Optional
from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def gemini_genetare_content(
        query: str,
        model: str = "gemini-2.0-flash",
    ) -> str:
    """
    Generate an educational AI response using Gemini API
    
    Args:
        question: The user's question text
        context: Optional context about the current material/chapter the user is viewing
        model: The model to use for generating the response (default is "gemini-2.0-flash")
        
    Returns:
        str: The generated response text from the Gemini model
    """
    try:
        response = client.models.generate_content(
            model=model,
            contents=query
        )
        return response.text
            
    except Exception as e:
        return f"Error: {str(e)}"

def construct_educational_voice_prompt(question: str, context: str = None) -> str:
    """Construct an appropriate prompt for the Gemini model"""
    
    system_prompt = """
    Kamu adalah voice assistant android. berikan jawaban yang baik dibaca oleh TextToSpeech lib.Kamu adalah asisten pendidikan yang membantu siswa. Berikan jawaban yang Akurat secara pendidikan
    
    Jika ditanya tentang topik yang tidak kamu ketahui, jujurlah tentang batasan pengetahuanmu.
    """
    
    if context:
        return f"{system_prompt}\n\nKonteks materi: {context}\n\nPertanyaan: {question}"
    else:
        return f"{system_prompt}\n\nPertanyaan: {question}"

