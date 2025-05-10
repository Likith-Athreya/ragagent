RAG-Ollama Knowledge Assistant
A local Retrieval-Augmented Generation (RAG) system powered by Ollama's Mistral/LLaMA3, with document retrieval and natural language answering capabilities.

Features
Document Ingestion: Processes PDFs/TXT files

Local LLM: Uses Ollama-hosted models (Mistral/LLaMA3)

Vector Search: ChromaDB for semantic retrieval

Tool Routing: Handles definitions, calculations, and general queries

Web Interface: Streamlit-based UI

Prerequisites
Docker

Quick Start
Build the Docker image:

bash
docker build -t rag-ollama .
Run the container:

bash
docker run -d \
  -p 8501:8501 \
  -p 11434:11434 \
  --gpus all \
  --name rag-app \
  rag-ollama
Access the UI:

http://localhost:8501
Adding Documents
Place files in the data/ directory:

Supported formats: PDF, TXT

Example structure:

data/
  ├── manual.pdf
  ├── policies.txt
  └── faqs.txt
Usage Examples
"What's our refund policy?" (Document retrieval)

"Calculate 15% of 200" (Math tool)

"Define quantum computing" (Definition tool)

Deployment Options
Local Network Access
bash
docker run -p 0.0.0.0:8501:8501 ...
Access via: http://<your-local-ip>:8501

Cloud Deployment
Push image to container registry:

bash
docker tag rag-ollama your-registry/rag-ollama
docker push your-registry/rag-ollama
Deploy to AWS/Azure/GCP with GPU support

Configuration
Environment variables (set in Docker):

STREAMLIT_SERVER_PORT: Web UI port (default: 8501)

ANONYMIZED_TELEMETRY: Disable ChromaDB analytics (False)

Troubleshooting
Ollama not responding:

bash
docker exec rag-app ollama list
View logs:

bash
docker logs -f rag-app