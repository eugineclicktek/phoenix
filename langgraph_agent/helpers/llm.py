from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
import os


OPENAI_API_MODEL_NAME = os.getenv("OPENAI_API_MODEL_NAME", "gpt-4.1")
OPENAI_API_DEPLOYMENT = os.getenv("OPENAI_API_DEPLOYMENT", "gpt-4.1")
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY", "67gPB9yATTShkDXrXR1JcCHVvqZShOLTuOZIYDXUYoMKfK5hwdaAJQQJ99BCACHYHv6XJ3w3AAAAACOGPAMG"
)
OPEN_API_ENDPOINT = os.getenv("OPEN_API_ENDPOINT", "https://pocmckupler4829061145.openai.azure.com/")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-12-01-preview")


azure_llm = AzureChatOpenAI(
    model=OPENAI_API_MODEL_NAME,
    temperature=0.5,
    azure_deployment=OPENAI_API_DEPLOYMENT,
    api_version=OPENAI_API_VERSION,
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPEN_API_ENDPOINT,
)


llm_ollama = ChatOllama(
    model="cogito:14b",
    temperature=0.5,
    base_url="http://localhost:11434",
)

chat_llm = azure_llm
