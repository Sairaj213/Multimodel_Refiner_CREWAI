import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from langchain_community.vectorstores import Chroma

# --- NEW: Import local embeddings ---
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

os.environ["OPENAI_API_KEY"] = "lm-studio"
os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
os.environ["OPENAI_BASE_URL"] = "http://localhost:1234/v1" 

# --- NEW: Use a local embedding model instead of LM Studio ---
# This runs locally on your CPU and doesn't bother LM Studio at all.
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    collection_name="session_memory",
    embedding_function=embedding_model
)

class MemoryTools(BaseTool):
    name: str = "Session Memory Tool"
    description: str = (
        "A tool with methods to save and retrieve information from the session's memory. "
        "Use the 'save_memory' method to remember key insights or final answers. "
        "Use the 'retrieve_memory' method to get context from past conversations before starting a new task."
    )

    def _run(self, argument: str) -> str:
        return "Please use a specific method like 'save_memory' or 'retrieve_memory'."

    @classmethod
    def save_memory(cls, text: str) -> str:
        try:
            vectorstore.add_texts([text])
            return f"Successfully saved to memory."
        except Exception as e:
            return f"Error saving to memory: {e}"

    @classmethod
    def retrieve_memory(cls, query: str) -> str:
        try:
            docs = vectorstore.similarity_search(query, k=3)
            if not docs:
                return "No past context found. This is a new topic."
            context = "\n".join([doc.page_content for doc in docs])
            return f"Past Conversation Context:\n---\n{context}\n---"
        except Exception as e:
            return f"Error retrieving from memory: {e}"

    @classmethod
    def clear_memory(cls) -> str:
        """Completely wipes the session memory."""
        try:
            vectorstore.delete_collection()
            return "Memory wiped."
        except Exception:
            return "Memory already empty."

# Instantiate the tool for easy import
memory_tool = MemoryTools()