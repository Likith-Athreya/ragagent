import streamlit as st
from agent import RAGAgent

# Initialize agent
@st.cache_resource
def get_agent():
    return RAGAgent()

agent = get_agent()

# UI
st.title("Local RAG with Ollama")
query = st.text_input("Ask a question about your documents:")

if query:
    with st.spinner("Thinking..."):
        result = agent.run(query)
    
    # Display results
    st.subheader("Answer")
    st.success(result["answer"])
    
    if result["mode"] == "rag":
        with st.expander("Retrieved Context"):
            for i, ctx in enumerate(result["context"], 1):
                st.markdown(f"**Chunk {i}**")
                st.info(ctx)
    
    st.caption(f"Mode: {result['mode'].upper()}")