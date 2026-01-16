import fitz  # PymuPDF
import os 
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def ask_groq_llm(prompt,max_tokens=1000):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content