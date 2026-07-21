from langchain_groq import ChatGroq
from core.config import GROQ_MODEL


def get_llm():
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0.2
    )
