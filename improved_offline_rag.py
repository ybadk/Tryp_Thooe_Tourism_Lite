import os
import re
from typing import List, Dict, Any
from langchain.chains import LLMChain, RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings, Model2vecEmbeddings
from langchain.schema import Document
from langchain_community.document_loaders import TextLoader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from services.tourism_ai_service import (
    DEFAULT_GENERATION_CONFIG,
    rerank_documents,
    split_documents,
)


class ImprovedOfflineRAG:

    def __init__(self,
                 documents_path: str,
                 chunk_size: int=500,
                 chunk_overlap: int=100,
                 max_tokens: int=500,
                 model_name: str="gpt2",
                 device: int=0):
        """
        Initialize the improved offline RAG system with dual embeddings.
        
        Args:
            documents_path: Path to the directory containing text documents
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
            max_tokens: Maximum tokens for context truncation
            model_name: Name of the language model to use
            device: Device to run the model on (0 for GPU, -1 for CPU)
        """
        self.documents_path = documents_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_tokens = max_tokens
        self.model_name = model_name
        self.device = device
        
        # Initialize embeddings
        self.hf_embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.model2vec_embeddings = Model2vecEmbeddings("minishlab/potion-base-8M")
        
        # Initialize LLM
        self.llm_pipeline = pipeline(
            "text-generation",
            model=model_name,
            device=device,
            max_new_tokens=DEFAULT_GENERATION_CONFIG.max_new_tokens,
            temperature=DEFAULT_GENERATION_CONFIG.temperature,
            top_k=DEFAULT_GENERATION_CONFIG.top_k,
            do_sample=True,
        )
        self.llm = HuggingFacePipeline(pipeline=self.llm_pipeline)
        
        # Initialize vector stores
        self.hf_vectorstore = None
        self.model2vec_vectorstore = None
        self.retriever = None
        
        # Initialize prompt template
        self.prompt_template = """Answer the following question based on the provided context. 
        If the context doesn't contain enough information to answer the question, say so.
        
        Context: {context}
        
        Question: {query}
        
        Answer:"""
        
        self.prompt = PromptTemplate(
            input_variables=["query", "context"],
            template=self.prompt_template
        )
        
        # Initialize chains
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)
        self.retrieval_qa = None
        
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing special characters and normalizing whitespace.
        """
        # Remove special characters but keep alphanumeric and whitespace
        pattern = r'[^a-zA-Z0-9\s]'
        text = re.sub(pattern, '', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_unique_words(self, text: str) -> Dict[str, int]:
        """
        Extract unique words and their frequencies from text.
        """
        words = text.lower().split()
        word_freq = {}
        for word in words:
            clean_word = self.clean_text(word)
            if clean_word:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        return word_freq
    
    def load_and_process_documents(self) -> List[Document]:
        """
        Load documents from the specified path and process them.
        """
        documents = []
        
        if os.path.isdir(self.documents_path):
            for filename in os.listdir(self.documents_path):
                if filename.endswith(".txt"):
                    file_path = os.path.join(self.documents_path, filename)
                    try:
                        loader = TextLoader(file_path)
                        documents.extend(loader.load())
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
        elif os.path.isfile(self.documents_path):
            try:
                loader = TextLoader(self.documents_path)
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading document: {e}")
        
        # Clean and process documents
        processed_docs = []
        for doc in documents:
            cleaned_content = self.clean_text(doc.page_content)
            if cleaned_content:
                processed_docs.append(Document(
                    page_content=cleaned_content,
                    metadata=doc.metadata
                ))
        
        return processed_docs
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks for better processing.
        """
        return split_documents(
            documents,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
    
    def create_vector_stores(self, documents: List[Document]):
        """
        Create vector stores using both embedding models.
        """
        print("Creating HuggingFace embeddings vector store...")
        self.hf_vectorstore = FAISS.from_documents(documents, self.hf_embeddings)
        
        print("Creating Model2Vec embeddings vector store...")
        self.model2vec_vectorstore = FAISS.from_documents(documents, self.model2vec_embeddings)
        
        # Use HF embeddings as primary retriever
        self.retriever = self.hf_vectorstore.as_retriever()
        
        # Initialize retrieval QA chain
        self.retrieval_qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            verbose=True
        )
    
    def truncate_to_max_tokens(self, text: str) -> str:
        """
        Truncate text to maximum token limit.
        """
        tokens = text.split()
        if len(tokens) > self.max_tokens:
            return " ".join(tokens[:self.max_tokens])
        return text
    
    def hybrid_retrieval(self, query: str, k: int=3) -> List[Document]:
        """
        Perform hybrid retrieval using both embedding models.
        """
        # Get documents from both vector stores
        hf_docs = self.hf_vectorstore.similarity_search(query, k=k)
        model2vec_docs = self.model2vec_vectorstore.similarity_search(query, k=k)
        
        # Combine and deduplicate documents
        all_docs = hf_docs + model2vec_docs
        unique_docs = []
        seen_contents = set()
        
        for doc in all_docs:
            if doc.page_content not in seen_contents:
                unique_docs.append(doc)
                seen_contents.add(doc.page_content)
        
        return rerank_documents(query, unique_docs, limit=k)
    
    def answer_question(self, query: str, use_hybrid: bool=True) -> Dict[str, Any]:
        """
        Answer a question using the RAG system.
        
        Args:
            query: The question to answer
            use_hybrid: Whether to use hybrid retrieval (both embedding models)
        
        Returns:
            Dictionary containing the answer and metadata
        """
        try:
            if use_hybrid:
                # Use hybrid retrieval
                retrieved_docs = self.hybrid_retrieval(query, k=3)
            else:
                # Use standard retrieval
                retrieved_docs = self.retriever.get_relevant_documents(query)[:3]
            
            # Prepare context
            context = " ".join([doc.page_content for doc in retrieved_docs])
            context = self.truncate_to_max_tokens(context)
            
            # Generate answer using the reranked context directly
            response = self.llm_chain.run(query=query, context=context)
            
            return {
                "answer": response,
                "context": context,
                "sources": [doc.metadata for doc in retrieved_docs],
                "num_sources": len(retrieved_docs)
            }
            
        except Exception as e:
            return {
                "answer": f"Error generating answer: {str(e)}",
                "context": "",
                "sources": [],
                "num_sources": 0
            }
    
    def analyze_corpus(self) -> Dict[str, Any]:
        """
        Analyze the document corpus for insights.
        """
        documents = self.load_and_process_documents()
        
        # Combine all text
        all_text = " ".join([doc.page_content for doc in documents])
        
        # Extract word frequencies
        word_freq = self.extract_unique_words(all_text)
        
        # Get top words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        top_words = sorted_words[:10]
        
        # Get longest words
        longest_words = sorted(word_freq.keys(), key=len, reverse=True)[:10]
        
        return {
            "total_documents": len(documents),
            "total_words": len(word_freq),
            "top_words": top_words,
            "longest_words": longest_words,
            "average_doc_length": len(all_text) / len(documents) if documents else 0
        }
    
    def setup(self):
        """
        Complete setup of the RAG system.
        """
        print("Loading and processing documents...")
        documents = self.load_and_process_documents()
        
        print(f"Processing {len(documents)} documents...")
        chunked_docs = self.chunk_documents(documents)
        
        print(f"Created {len(chunked_docs)} chunks...")
        self.create_vector_stores(chunked_docs)
        
        print("RAG system setup complete!")
        
        # Analyze corpus
        analysis = self.analyze_corpus()
        print(f"Corpus analysis: {analysis['total_documents']} documents, {analysis['total_words']} unique words")


# Example usage
if __name__ == "__main__":
    # Initialize the RAG system
    rag = ImprovedOfflineRAG(
        documents_path="your_documents_folder",  # Replace with your documents path
        chunk_size=500,
        chunk_overlap=100,
        max_tokens=500
    )
    
    # Setup the system
    rag.setup()
    
    # Example queries
    queries = [
        "What is the main topic of the documents?",
        "Can you summarize the key points?",
        "What are the most important concepts discussed?"
    ]
    
    for query in queries:
        print(f"\nQuestion: {query}")
        result = rag.answer_question(query, use_hybrid=True)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['num_sources']} documents used") 
