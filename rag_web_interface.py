import streamlit as st
import os
import sys
from pathlib import Path
import time
from improved_offline_rag import ImprovedOfflineRAG

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="Improved Offline RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Import the dark theme CSS */
    @import url('dark_theme.css');
    
    /* Streamlit specific overrides */
    .stApp {
        background-color: #121212;
    }
    
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #404040;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #404040;
    }
    
    .stButton > button {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #404040;
    }
    
    .stButton > button:hover {
        background-color: #3d3d3d;
        border-color: #bb86fc;
    }
    
    .stSelectbox > div > div > select {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #404040;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
    
    .stAlert {
        background-color: #1e1e1e;
        border: 1px solid #404040;
    }
    
    /* Custom styling for the main content */
    .main-header {
        background: linear-gradient(90deg, #bb86fc, #03dac6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .info-card {
        background-color: #1e1e1e;
        border: 1px solid #404040;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .response-card {
        background-color: #2d2d2d;
        border: 1px solid #505050;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'is_initialized' not in st.session_state:
    st.session_state.is_initialized = False
if 'documents_path' not in st.session_state:
    st.session_state.documents_path = ""


def initialize_rag_system(documents_path: str, chunk_size: int, chunk_overlap: int, max_tokens: int):
    """Initialize the RAG system with the given parameters."""
    try:
        with st.spinner("Initializing RAG system..."):
            rag = ImprovedOfflineRAG(
                documents_path=documents_path,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                max_tokens=max_tokens
            )
            rag.setup()
            return rag
    except Exception as e:
        st.error(f"Error initializing RAG system: {str(e)}")
        return None


def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Improved Offline RAG System</h1>',
                unsafe_allow_html=True)

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Document path input
        documents_path = st.text_input(
            "Documents Path",
            value=st.session_state.documents_path,
            placeholder="Enter path to your documents folder or file",
            help="Path to the directory containing .txt files or a single .txt file"
        )

        # RAG parameters
        st.subheader("RAG Parameters")
        chunk_size = st.slider("Chunk Size", min_value=100,
                               max_value=1000, value=500, step=50)
        chunk_overlap = st.slider(
            "Chunk Overlap", min_value=0, max_value=200, value=100, step=10)
        max_tokens = st.slider("Max Tokens", min_value=200,
                               max_value=1000, value=500, step=50)

        # Initialize button
        if st.button("🚀 Initialize RAG System", type="primary"):
            if documents_path and os.path.exists(documents_path):
                st.session_state.documents_path = documents_path
                st.session_state.rag_system = initialize_rag_system(
                    documents_path, chunk_size, chunk_overlap, max_tokens
                )
                if st.session_state.rag_system:
                    st.session_state.is_initialized = True
                    st.success("RAG system initialized successfully!")
            else:
                st.error("Please enter a valid documents path.")

        # System status
        st.subheader("📊 System Status")
        if st.session_state.is_initialized:
            st.success("✅ RAG System Ready")

            # Analyze corpus button
            if st.button("📈 Analyze Corpus"):
                with st.spinner("Analyzing corpus..."):
                    analysis = st.session_state.rag_system.analyze_corpus()

                    st.markdown("### Corpus Analysis Results")
                    st.write(
                        f"**Total Documents:** {analysis['total_documents']}")
                    st.write(f"**Unique Words:** {analysis['total_words']}")
                    st.write(
                        f"**Average Document Length:** {analysis['average_doc_length']:.0f} characters")

                    # Top words
                    st.write("**Top 10 Most Frequent Words:**")
                    for word, freq in analysis['top_words']:
                        st.write(f"- {word}: {freq}")

                    # Longest words
                    st.write("**Top 10 Longest Words:**")
                    for word in analysis['longest_words']:
                        st.write(f"- {word}")
        else:
            st.warning("⚠️ RAG System Not Initialized")

    # Main content area
    if st.session_state.is_initialized:
        # Query interface
        st.header("💬 Ask Questions")

        # Query input
        query = st.text_area(
            "Enter your question:",
            placeholder="Ask anything about your documents...",
            height=100
        )

        # Query options
        col1, col2 = st.columns(2)
        with col1:
            use_hybrid = st.checkbox("Use Hybrid Retrieval", value=True,
                                     help="Use both HuggingFace and Model2Vec embeddings for better results")
        with col2:
            if st.button("🔍 Search", type="primary"):
                if query.strip():
                    with st.spinner("Searching for answers..."):
                        result = st.session_state.rag_system.answer_question(
                            query, use_hybrid=use_hybrid)

                        # Display results
                        st.markdown("### 📋 Answer")
                        st.markdown(
                            f'<div class="response-card">{result["answer"]}</div>', unsafe_allow_html=True)

                        # Display metadata
                        with st.expander("📊 Response Details"):
                            st.write(
                                f"**Number of sources used:** {result['num_sources']}")
                            st.write(
                                f"**Retrieval method:** {'Hybrid' if use_hybrid else 'Standard'}")

                            if result['sources']:
                                st.write("**Sources:**")
                                for i, source in enumerate(result['sources'], 1):
                                    st.write(f"{i}. {source}")

                        # Display context
                        with st.expander("📖 Retrieved Context"):
                            st.text(result['context'])

        # Example queries
        st.header("💡 Example Queries")
        example_queries = [
            "What is the main topic of the documents?",
            "Can you summarize the key points?",
            "What are the most important concepts discussed?",
            "What are the main findings or conclusions?",
            "How does this relate to current trends?"
        ]

        for i, example in enumerate(example_queries):
            if st.button(f"Example {i+1}: {example[:50]}...", key=f"example_{i}"):
                st.session_state.example_query = example
                st.rerun()

        # Handle example query
        if 'example_query' in st.session_state:
            query = st.session_state.example_query
            del st.session_state.example_query

            with st.spinner("Searching for answers..."):
                result = st.session_state.rag_system.answer_question(
                    query, use_hybrid=True)

                st.markdown("### 📋 Answer")
                st.markdown(
                    f'<div class="response-card">{result["answer"]}</div>', unsafe_allow_html=True)

                with st.expander("📊 Response Details"):
                    st.write(
                        f"**Number of sources used:** {result['num_sources']}")
                    st.write(f"**Retrieval method:** Hybrid")

                    if result['sources']:
                        st.write("**Sources:**")
                        for i, source in enumerate(result['sources'], 1):
                            st.write(f"{i}. {source}")

                with st.expander("📖 Retrieved Context"):
                    st.text(result['context'])

    else:
        # Welcome message
        st.markdown("""
        <div class="info-card">
            <h3>🎯 Welcome to the Improved Offline RAG System!</h3>
            <p>This system combines the power of:</p>
            <ul>
                <li><strong>Dual Embeddings:</strong> HuggingFace and Model2Vec for better document retrieval</li>
                <li><strong>FAISS Vector Store:</strong> Fast similarity search</li>
                <li><strong>Advanced Text Processing:</strong> Smart chunking and cleaning</li>
                <li><strong>Hybrid Retrieval:</strong> Combine results from multiple embedding models</li>
            </ul>
            <p><strong>To get started:</strong></p>
            <ol>
                <li>Enter the path to your documents folder in the sidebar</li>
                <li>Adjust the RAG parameters if needed</li>
                <li>Click "Initialize RAG System"</li>
                <li>Start asking questions!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        # Features showcase
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="info-card">
                <h4>🔍 Smart Retrieval</h4>
                <p>Uses both HuggingFace and Model2Vec embeddings for comprehensive document search.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="info-card">
                <h4>📊 Corpus Analysis</h4>
                <p>Analyze your document collection for insights and statistics.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="info-card">
                <h4>🧹 Text Processing</h4>
                <p>Advanced text cleaning and chunking for optimal performance.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="info-card">
                <h4>🎨 Dark Theme</h4>
                <p>Beautiful dark interface with white fonts for comfortable reading.</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
