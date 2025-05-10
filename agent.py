from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGAgent:
    def __init__(self):
        # Initialize Ollama LLM
        self.llm = Ollama(
            model="mistral",
            temperature=0.1,
            num_ctx=2048,
            base_url="http://localhost:11434"  # Explicit connection
        )
        
        # Initialize embeddings and vector store
        self.embeddings = OllamaEmbeddings(model="mistral")
        self.vector_store = Chroma(
            persist_directory="db",
            embedding_function=self.embeddings
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
    
    def retrieve(self, query: str) -> List[str]:
        """Retrieve relevant document chunks"""
        docs = self.retriever.get_relevant_documents(query)
        return [doc.page_content for doc in docs]
    
    def generate_answer(self, query: str, context: List[str]) -> str:
        """Generate answer using LLM"""
        prompt = ChatPromptTemplate.from_template(
            """Answer the question based only on the following context:
            {context}
            Question: {question}"""
        )
        chain = prompt | self.llm
        return chain.invoke({
            "context": "\n\n".join(context),
            "question": query
        })
    
    def run(self, query: str) -> dict:
        """Full RAG pipeline"""
        try:
            # Special cases
            if "calculate" in query.lower():
                return {"mode": "calc", "answer": "Use Python's eval() for calculations"}
            
            if "define" in query.lower():
                return {"mode": "define", "answer": "Use dictionary APIs for definitions"}
            
            # Standard RAG flow
            context = self.retrieve(query)
            answer = self.generate_answer(query, context)
            return {
                "mode": "rag",
                "context": context,
                "answer": answer
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"mode": "error", "answer": str(e)}