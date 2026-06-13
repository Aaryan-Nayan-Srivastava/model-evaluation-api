from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
def get_llm()->ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")
    if api_key is None:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    
    return ChatGroq(model=model_name, temperature=0.2, api_key=api_key)

async def generate_llm_evaluation_report(prompt: str) -> str:
    llm=get_llm()
    response= await llm.ainvoke(prompt)
    return response.content    
