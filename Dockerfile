FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    curl \
    gcc \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV ANONYMIZED_TELEMETRY=False
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

EXPOSE 8501
EXPOSE 11434

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

CMD curl -fsSL https://ollama.com/install.sh | sh && \
    ollama serve & \
    sleep 10 && \
    ollama pull mistral && \
    streamlit run app.py --server.port $STREAMLIT_SERVER_PORT --server.address $STREAMLIT_SERVER_ADDRESS