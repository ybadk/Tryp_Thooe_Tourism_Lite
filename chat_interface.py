"""
🌿 Tshwane Tourism Chat Interface
Integrated RAG-powered chatbot for tourism assistance

This module provides an intelligent chat interface that can:
- Answer questions about Tshwane tourism destinations
- Provide real-time information from tourism websites
- Assist with booking and planning queries
- Offer personalized recommendations

Built with LangChain, Streamlit, and modern AI practices.
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import time
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import urllib.parse
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# LangChain imports (if available)
try:
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_community.document_loaders import WebBaseLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.llms import HuggingFacePipeline
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.chains import create_history_aware_retriever, create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    st.warning(
        "⚠️ LangChain not available. Install with: pip install langchain langchain-community transformers torch")


class ChatMode(Enum):
    """Chat interface modes"""
    TOURISM_ASSISTANT = "tourism_assistant"
    WEBSITE_CHAT = "website_chat"
    BOOKING_HELP = "booking_help"
    PLANNING_GUIDE = "planning_guide"


@dataclass
class ChatMessage:
    """Structured chat message"""
    id: str
    content: str
    sender: str  # "user" or "assistant"
    timestamp: datetime
    message_type: str = "text"
    metadata: Optional[Dict[str, Any]] = None


class TourismChatInterface:
    """Enhanced chat interface for Tshwane Tourism with RAG capabilities"""

    def __init__(self):
        self.chat_history: List[ChatMessage] = []
        self.vector_store = None
        self.current_mode = ChatMode.TOURISM_ASSISTANT
        self.tourism_data = {}
        self.website_urls = [
            "http://www.visittshwane.co.za",
            "https://www.tshwanetourism.com",
            "https://www.pretoria.co.za"
        ]

        # Initialize session state
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        if 'chat_vector_store' not in st.session_state:
            st.session_state.chat_vector_store = None
        if 'chat_mode' not in st.session_state:
            st.session_state.chat_mode = ChatMode.TOURISM_ASSISTANT.value

    def load_tourism_data(self):
        """Load tourism data from CSV files and websites"""
        try:
            # Load CSV data
            csv_files = [
                'tshwane_places.csv',
                'processed_data/tshwane_places.csv',
                'tshwane_restaurants.csv',
                'C:/Users/user/Desktop/Tryp-Thooe-repo/Tryp_Thooe_Tourism/processed_data/tshwane_places.csv',
                'C:/Users/user/Desktop/Tryp-Thooe-repo/Tryp_Thooe_Tourism/processed_data/tshwane_restaurants.csv',
                'C:/Users/user/Desktop/Tryp-Thooe-repo/Tryp_Thooe_Tourism/scraps/Tryp_Thooe_Tourism-main/tshwane_places.csv',
                'C:/Users/user/Desktop/Tryp-Thooe-repo/Tryp_Thooe_Tourism/scraps/Tryp_Thooe_Tourism-main/Tshwane_Tourism_Association/Tryp_Thooe_Tourism/tshwane_places.csv'
            ]

            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    self.tourism_data[csv_file] = df.to_dict('records')
                except Exception as e:
                    st.info(f"Could not load {csv_file}: {e}")

            # Load website data if available
            if hasattr(st.session_state, 'website_data'):
                self.tourism_data['website'] = st.session_state.website_data

        except Exception as e:
            st.error(f"Error loading tourism data: {e}")

    def get_vectorstore_from_url(self, url: str):
        """Create vector store from website URL using LangChain with Hugging Face models"""
        if not LANGCHAIN_AVAILABLE:
            return None

        try:
            # Get the text in document form
            loader = WebBaseLoader(url)
            document = loader.load()

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter()
            document_chunks = text_splitter.split_documents(document)

            # Create embeddings using Hugging Face model
            # Using a smaller, efficient embedding model
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}  # Use CPU for compatibility
            )

            # Create a vectorstore from the chunks
            vector_store = Chroma.from_documents(document_chunks, embeddings)
            return vector_store

        except Exception as e:
            st.error(f"Error creating vector store from {url}: {e}")
            return None

    def get_context_retriever_chain(self, vector_store):
        """Create context-aware retriever chain using Hugging Face models"""
        if not LANGCHAIN_AVAILABLE or not vector_store:
            return None

        try:
            # Load Hugging Face model for text generation
            model_name = "sentence-transformers/all-MiniLM-L6-v2"

            # Check if model is already loaded in session state
            if 'hf_pipeline' not in st.session_state:
                with st.spinner("🔄 Loading Hugging Face model..."):
                    tokenizer = AutoTokenizer.from_pretrained(model_name)
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype=torch.float16,
                        device_map="auto" if torch.cuda.is_available() else "cpu"
                    )

                    # Create pipeline
                    hf_pipeline = pipeline(
                        "text-generation",
                        model=model,
                        tokenizer=tokenizer,
                        max_new_tokens=512,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id
                    )
                    st.session_state.hf_pipeline = hf_pipeline

            # Create LangChain LLM wrapper
            llm = HuggingFacePipeline(
                pipeline=st.session_state.hf_pipeline,
                model_kwargs={"temperature": 0.7, "max_length": 512}
            )

            retriever = vector_store.as_retriever()

            prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
            ])

            retriever_chain = create_history_aware_retriever(
                llm, retriever, prompt)
            return retriever_chain

        except Exception as e:
            st.error(f"Error creating retriever chain: {e}")
            return None

    def get_conversational_rag_chain(self, retriever_chain):
        """Create conversational RAG chain using Hugging Face models"""
        if not LANGCHAIN_AVAILABLE or not retriever_chain:
            return None

        try:
            # Use the same Hugging Face pipeline from session state
            if 'hf_pipeline' not in st.session_state:
                st.error("Hugging Face model not loaded. Please try again.")
                return None

            # Create LangChain LLM wrapper
            llm = HuggingFacePipeline(
                pipeline=st.session_state.hf_pipeline,
                model_kwargs={"temperature": 0.7, "max_length": 512}
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful tourism assistant for Tshwane, South Africa. Answer questions based on the provided context and be friendly, informative, and accurate."),
                ("system", "Context: {context}"),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
            ])

            stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
            return create_retrieval_chain(retriever_chain, stuff_documents_chain)

        except Exception as e:
            st.error(f"Error creating conversational chain: {e}")
            return None

    def get_ai_response(self, user_input: str) -> str:
        """Get AI response using RAG or fallback methods"""
        try:
            # Try RAG first if available
            if LANGCHAIN_AVAILABLE and st.session_state.chat_vector_store:
                retriever_chain = self.get_context_retriever_chain(
                    st.session_state.chat_vector_store)
                if retriever_chain:
                    conversation_rag_chain = self.get_conversational_rag_chain(
                        retriever_chain)
                    if conversation_rag_chain:
                        # Convert chat history to LangChain format
                        chat_history = []
                        # Last 10 messages
                        for msg in st.session_state.chat_messages[-10:]:
                            if msg.sender == "user":
                                chat_history.append(
                                    HumanMessage(content=msg.content))
                            else:
                                chat_history.append(
                                    AIMessage(content=msg.content))

                        response = conversation_rag_chain.invoke({
                            "chat_history": chat_history,
                            "input": user_input
                        })
                        return response['answer']

            # Fallback to rule-based responses
            return self.get_fallback_response(user_input)

        except Exception as e:
            st.error(f"Error getting AI response: {e}")
            return self.get_fallback_response(user_input)

    def get_fallback_response(self, user_input: str) -> str:
        """Fallback response system when AI is not available"""
        user_input_lower = user_input.lower()

        # Tourism-specific responses
        tourism_responses = {
            'museum': "🏛️ Tshwane has several excellent museums! I recommend the Ditsong National Museum of Cultural History, the Pretoria Art Museum, and the Voortrekker Monument. Would you like specific information about any of these?",
            'restaurant': "🍽️ Tshwane offers diverse dining options! From traditional South African cuisine to international flavors, there's something for everyone. Popular areas include Hatfield, Brooklyn, and Menlyn. What type of cuisine are you interested in?",
            'hotel': "🏨 Tshwane has accommodation for every budget! From luxury hotels in the city center to cozy guesthouses in the suburbs. Popular areas include Hatfield, Brooklyn, and Menlyn. What's your budget range?",
            'weather': "🌤️ Tshwane has a pleasant climate! Summers are warm (October-March) and winters are mild (April-September). The best time to visit is during spring (September-November) when the jacaranda trees are in bloom!",
            'transport': "🚗 Getting around Tshwane is easy! You can use Uber, taxis, or rent a car. The Gautrain connects Pretoria to Johannesburg, and there are also local bus services. Where are you planning to visit?",
            'booking': "📝 I can help you with bookings! You can book tours, accommodation, and activities through our portal. Would you like to see our booking form or get specific recommendations?",
            'plan': "🗺️ Let me help you plan your Tshwane visit! I can suggest itineraries based on your interests, time available, and budget. What type of activities interest you most?",
            'cost': "💰 Tshwane offers good value for money! Accommodation ranges from budget-friendly to luxury, and many attractions have reasonable entry fees. What's your budget for this trip?",
            'safety': "🛡️ Tshwane is generally safe for tourists! Like any city, it's best to stay in well-lit areas at night and keep valuables secure. The city center and tourist areas are well-patrolled.",
            'language': "🗣️ English is widely spoken in Tshwane, along with Afrikaans, Zulu, and other South African languages. Most tourist services are available in English."
        }

        # Check for tourism keywords
        for keyword, response in tourism_responses.items():
            if keyword in user_input_lower:
                return response

        # General responses
        general_responses = [
            "I'm here to help you explore Tshwane! What would you like to know about our beautiful city?",
            "Tshwane has so much to offer! From historical sites to modern attractions, there's something for everyone. What interests you most?",
            "I'd be happy to help you plan your Tshwane adventure! What specific information are you looking for?",
            "Tshwane is known for its rich history, beautiful architecture, and warm hospitality. How can I assist you today?",
            "Welcome to Tshwane! I can help you discover the best places to visit, eat, and stay. What would you like to know?"
        ]

        # Return a random general response
        import random
        return random.choice(general_responses)

    def add_message(self, content: str, sender: str, message_type: str = "text", metadata: Optional[Dict[str, Any]] = None):
        """Add a message to the chat history"""
        message = ChatMessage(
            id=str(uuid.uuid4())[:8],
            content=content,
            sender=sender,
            timestamp=datetime.now(),
            message_type=message_type,
            metadata=metadata
        )

        st.session_state.chat_messages.append(message)
        self.chat_history.append(message)

    def display_chat_interface(self):
        """Display the main chat interface"""
        st.markdown("""
        <style>
        .chat-container {
            background: linear-gradient(135deg, #181c24 0%, #232a36 100%);
            border-radius: 18px;
            box-shadow: 0 4px 24px #000a;
            padding: 24px;
            margin-bottom: 20px;
            border: 1.5px solid #00d4aa44;
        }
        .chat-message {
            background: #232a36;
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
            border-left: 4px solid #00d4aa;
            opacity: 1;
            transition: opacity 0.7s ease;
        }
        .chat-message.fade-out {
            opacity: 0.2;
        }
        .chat-message.user {
            border-left-color: #4CAF50;
            background: #1a1d23;
        }
        .chat-message.assistant {
            border-left-color: #00d4aa;
            background: #232a36;
        }
        .chat-input {
            background: #232a36;
            border: 1px solid #00d4aa44;
            border-radius: 12px;
            color: #fff;
        }
        .chat-mode-selector {
            background: #232a36;
            border-radius: 8px;
            padding: 8px;
            margin-bottom: 16px;
        }
        .custom-loader {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 12px 0;
        }
        .dot {
            width: 10px;
            height: 10px;
            background: #00d4aa;
            border-radius: 50%;
            display: inline-block;
            animation: bounce 1.2s infinite alternate;
        }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes bounce {
            0% { transform: translateY(0); }
            100% { transform: translateY(-10px); }
        }
        </style>
        """, unsafe_allow_html=True)

        # Chat mode selector
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown("### 🤖 Tshwane Tourism Chat Assistant")

        # Mode selection
        col1, col2 = st.columns([3, 1])
        with col1:
            mode = st.selectbox(
                "Chat Mode",
                options=[mode.value for mode in ChatMode],
                index=0,
                key="chat_mode_selector"
            )
            st.session_state.chat_mode = mode

        with col2:
            if st.button("🔄 Refresh Data", key="refresh_chat_data"):
                self.load_tourism_data()
                st.success("Tourism data refreshed!")

        st.markdown("</div>", unsafe_allow_html=True)

        # Minimal chat messages display (last 3 only)
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        messages = st.session_state.chat_messages[-3:]
        for i, message in enumerate(messages):
            fade_class = " fade-out" if i == 0 and len(messages) == 3 else ""
            with st.chat_message(message.sender):
                st.markdown(
                    f'<div class="chat-message{fade_class}">{message.content}</div>', unsafe_allow_html=True)
                if message.metadata:
                    st.caption(f"Additional info: {message.metadata}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Chat input
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        user_input = st.chat_input(
            "Ask me about Tshwane tourism...", key="chat_input")

        if user_input:
            # Add user message
            self.add_message(user_input, "user")

            # Show custom loader before AI responds
            with st.container():
                st.markdown('<div class="custom-loader">',
                            unsafe_allow_html=True)
                st.markdown(
                    '<span class="dot"></span><span class="dot"></span><span class="dot"></span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                time.sleep(3)  # Ensure loader lasts at least 3 seconds

            # Get AI response
            ai_response = self.get_ai_response(user_input)

            # Add AI response
            self.add_message(ai_response, "assistant")

            # Rerun to display new messages
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    def display_quick_actions(self):
        """Display quick action buttons for common queries"""
        st.markdown("### ⚡ Quick Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🏛️ Museums", key="quick_museums"):
                self.add_message("Tell me about museums in Tshwane", "user")
                response = self.get_ai_response(
                    "Tell me about museums in Tshwane")
                self.add_message(response, "assistant")
                st.rerun()

        with col2:
            if st.button("🍽️ Restaurants", key="quick_restaurants"):
                self.add_message(
                    "What are the best restaurants in Tshwane?", "user")
                response = self.get_ai_response(
                    "What are the best restaurants in Tshwane?")
                self.add_message(response, "assistant")
                st.rerun()

        with col3:
            if st.button("🏨 Accommodation", key="quick_accommodation"):
                self.add_message("Where should I stay in Tshwane?", "user")
                response = self.get_ai_response(
                    "Where should I stay in Tshwane?")
                self.add_message(response, "assistant")
                st.rerun()

        col4, col5, col6 = st.columns(3)

        with col4:
            if st.button("🗺️ Planning", key="quick_planning"):
                self.add_message("Help me plan my Tshwane trip", "user")
                response = self.get_ai_response("Help me plan my Tshwane trip")
                self.add_message(response, "assistant")
                st.rerun()

        with col5:
            if st.button("🌤️ Weather", key="quick_weather"):
                self.add_message("What's the weather like in Tshwane?", "user")
                response = self.get_ai_response(
                    "What's the weather like in Tshwane?")
                self.add_message(response, "assistant")
                st.rerun()

        with col6:
            if st.button("🚗 Transport", key="quick_transport"):
                self.add_message("How do I get around Tshwane?", "user")
                response = self.get_ai_response("How do I get around Tshwane?")
                self.add_message(response, "assistant")
                st.rerun()

    def display_chat_analytics(self):
        """Display chat analytics and insights"""
        if not st.session_state.chat_messages:
            return

        st.markdown("### 📊 Chat Analytics")

        # Basic analytics
        total_messages = len(st.session_state.chat_messages)
        user_messages = len(
            [m for m in st.session_state.chat_messages if m.sender == "user"])
        assistant_messages = len(
            [m for m in st.session_state.chat_messages if m.sender == "assistant"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", total_messages)
        with col2:
            st.metric("User Messages", user_messages)
        with col3:
            st.metric("Assistant Messages", assistant_messages)

        # Message timeline
        if len(st.session_state.chat_messages) > 1:
            st.markdown("#### 📈 Message Timeline")
            timeline_data = []
            for msg in st.session_state.chat_messages:
                timeline_data.append({
                    "Time": msg.timestamp.strftime("%H:%M"),
                    "Sender": msg.sender.title(),
                    "Message": msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                })

            if timeline_data:
                df_timeline = pd.DataFrame(timeline_data)
                st.dataframe(
                    df_timeline, use_container_width=True, hide_index=True)

    def initialize_vector_store(self):
        """Initialize vector store from tourism websites with Hugging Face models"""
        if not LANGCHAIN_AVAILABLE:
            return

        try:
            with st.spinner("🔄 Initializing AI chat capabilities with Hugging Face models..."):
                # Ensure minimum 3-second loading time
                start_time = time.time()

                # Load Hugging Face model first
                self.load_huggingface_model()

                # Try to create vector store from tourism websites
                for url in self.website_urls:
                    try:
                        vector_store = self.get_vectorstore_from_url(url)
                        if vector_store:
                            st.session_state.chat_vector_store = vector_store
                            st.success(f"✅ Connected to {url}")
                            break
                    except Exception as e:
                        st.info(f"Could not connect to {url}: {e}")
                        continue

                if not st.session_state.chat_vector_store:
                    st.info(
                        "ℹ️ AI chat will use fallback responses. Install LangChain for enhanced capabilities.")

                # Ensure minimum 3-second loading time
                elapsed_time = time.time() - start_time
                if elapsed_time < 3:
                    time.sleep(3 - elapsed_time)

        except Exception as e:
            st.error(f"Error initializing vector store: {e}")

    def load_huggingface_model(self):
        """Load Hugging Face model efficiently"""
        if 'hf_pipeline' in st.session_state:
            return  # Already loaded

        try:
            with st.spinner("🔄 Loading GPT2 model..."):
                # Ensure minimum 3-second loading time
                start_time = time.time()

                model_name = "gpt2"

                # Load tokenizer and model
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    device_map="auto" if torch.cuda.is_available() else "cpu",
                    trust_remote_code=True
                )

                # Create pipeline
                hf_pipeline = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=512,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )

                st.session_state.hf_pipeline = hf_pipeline
                st.success("✅ Hugging Face model loaded successfully!")

                # Ensure minimum 3-second loading time
                elapsed_time = time.time() - start_time
                if elapsed_time < 3:
                    time.sleep(3 - elapsed_time)

        except Exception as e:
            st.error(f"Error loading Hugging Face model: {e}")
            st.info("ℹ️ Falling back to rule-based responses")


def display_chat_interface_main():
    """Main function to display the chat interface"""
    # Initialize chat interface
    if 'chat_interface' not in st.session_state:
        st.session_state.chat_interface = TourismChatInterface()

    chat_interface = st.session_state.chat_interface

    # Load tourism data
    chat_interface.load_tourism_data()

    # Initialize vector store if not already done
    if not st.session_state.get('chat_vector_store_initialized', False):
        chat_interface.initialize_vector_store()
        st.session_state.chat_vector_store_initialized = True

    # Display chat interface
    chat_interface.display_chat_interface()

    # Display quick actions
    chat_interface.display_quick_actions()

    # Display analytics
    chat_interface.display_chat_analytics()


if __name__ == "__main__":
    # Test the chat interface
    st.set_page_config(page_title="Tshwane Tourism Chat", page_icon="🤖")
    st.title("🌿 Tshwane Tourism Chat Assistant")
    display_chat_interface_main()
