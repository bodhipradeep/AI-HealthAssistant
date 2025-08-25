from langchain_groq import ChatGroq
from config.settings import settings

llm = ChatGroq(
    model=settings.Llama_MODEL,
    api_key=settings.GROQ_API_KEY,
    verbose=True,
    temperature=0.05
)
