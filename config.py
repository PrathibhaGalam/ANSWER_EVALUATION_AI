import os
from langchain_groq import ChatGroq


#setting Api Key
#Setting the Groq api key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from dotenv import load_dotenv
load_dotenv() 
#initialzing the llm's
llm=ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant"
)