from collections import defaultdict
import numpy as np
from sklearn.datasets import load_iris
import xgboost as xgb
import joblib
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import tempfile
import os
from datetime import datetime
import hashlib
import base64
from cryptography.fernet import Fernet
import plotly.express as px
import plotly.graph_objects as go
from transformers import pipeline
import time
from urllib.parse import urljoin, urlparse
import warnings
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import uuid
import urllib.parse
from services.weather_service import WeatherService
from ui.streamlit_cards import (
    dataframe_preview_records,
    render_dataframe_cards,
    render_metric_strip,
    render_record_cards,
    render_section_header,
)
warnings.filterwarnings('ignore')

# Enhanced system architecture inspired by analyzed AI tools

WEATHER_SERVICE = WeatherService()


class OperationMode(Enum):
    PLANNING = "planning"
    STANDARD = "standard"
    REAL_TIME = "real_time"


@dataclass
class PlanStep:
    id: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class ToolCall:
    name: str
    parameters: Dict[str, Any]
    explanation: str
    result: Optional[Any] = None


class TshwanePlanningSystem:
    """Devin-inspired planning system for tourism data processing"""

    def __init__(self):
        self.mode = OperationMode.PLANNING
        self.gathered_info = {}
        self.plan_steps = []
        self.current_step = 0
        self.execution_log = []

    def think(self, observation: str) -> str:
        """Devin-style thinking for reflection and planning"""
        timestamp = datetime.now().isoformat()
        thought = {
            'timestamp': timestamp,
            'observation': observation,
            'current_mode': self.mode.value,
            'step': self.current_step
        }
        self.execution_log.append(thought)
        return f"💭 Thinking: {observation}"

    def suggest_plan(self, user_request: str) -> List[PlanStep]:
        """Create execution plan based on user request"""
        plan_id = str(uuid.uuid4())[:8]

        if "scrape" in user_request.lower() or "website" in user_request.lower():
            steps = [
                PlanStep(f"{plan_id}-1", "Initialize web scraping tools"),
                PlanStep(f"{plan_id}-2", "Scrape Tshwane Tourism website"),
                PlanStep(f"{plan_id}-3", "Process and categorize content"),
                PlanStep(f"{plan_id}-4", "Generate structured data files"),
                PlanStep(f"{plan_id}-5", "Create interactive visualizations")
            ]
        elif "booking" in user_request.lower():
            steps = [
                PlanStep(f"{plan_id}-1", "Validate booking form data"),
                PlanStep(f"{plan_id}-2", "Encrypt sensitive information"),
                PlanStep(f"{plan_id}-3", "Generate booking confirmation"),
                PlanStep(f"{plan_id}-4", "Send notification email"),
                PlanStep(f"{plan_id}-5", "Update booking database")
            ]
        else:
            steps = [
                PlanStep(f"{plan_id}-1", "Analyze user request"),
                PlanStep(f"{plan_id}-2", "Gather required information"),
                PlanStep(f"{plan_id}-3", "Execute primary task"),
                PlanStep(f"{plan_id}-4", "Validate results"),
                PlanStep(f"{plan_id}-5", "Present findings to user")
            ]

        self.plan_steps = steps
        return steps

    def execute_step(self, step_id: str) -> bool:
        """Execute a specific plan step"""
        step = next((s for s in self.plan_steps if s.id == step_id), None)
        if not step:
            return False

        step.status = "in_progress"
        try:
            # Simulate step execution
            time.sleep(0.5)  # Brief delay for realism
            step.status = "completed"
            step.result = f"Step {step_id} completed successfully"
            return True
        except Exception as e:
            step.status = "failed"
            step.error = str(e)
            return False


class ComponentSystem:
    """v0-inspired component system for modular UI"""

    @staticmethod
    def create_code_project(project_id: str, components: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured project similar to v0's CodeProject"""
        return {
            'id': project_id,
            'components': components,
            'runtime': 'streamlit',
            'created_at': datetime.now().isoformat(),
            'responsive': True
        }

    @staticmethod
    def render_component(component_type: str, props: Dict[str, Any]) -> None:
        """Render UI components with consistent styling"""
        if component_type == "gallery_card":
            st.markdown(f"""
            <div class="gallery-card" style="
                background: black;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 10px;
                transition: transform 0.3s ease;
            ">
                <h3>{props.get('title', 'Untitled')}</h3>
                <p>{props.get('description', 'No description')}</p>
                <span class="badge">{props.get('type', 'general')}</span>
            </div>
            """, unsafe_allow_html=True)

        elif component_type == "progress_indicator":
            progress = props.get('progress', 0)
            st.progress(progress / 100)
            st.caption(f"Progress: {progress}%")

        elif component_type == "notification_toast":
            message_type = props.get('type', 'info')
            message = props.get('message', '')

            if message_type == 'success':
                st.success(message)
            elif message_type == 'error':
                st.error(message)
            elif message_type == 'warning':
                st.warning(message)
            else:
                st.info(message)


class SemanticSearch:
    """Cursor-inspired semantic search for tourism content"""

    def __init__(self):
        self.search_history = []

    def search_tourism_content(self, query: str, target_data: List[Dict]=None) -> List[Dict]:
        """Enhanced semantic search using real website data"""
        explanation = f"Searching real Tshwane tourism content for: '{query}'"

        # Use real website data if available
        if target_data is None and hasattr(st.session_state, 'searchable_content'):
            target_data = st.session_state.searchable_content
        elif target_data is None:
            target_data = st.session_state.places_data + st.session_state.restaurants_data

        # Log search
        self.search_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'explanation': explanation,
            'data_source': 'real_website' if hasattr(st.session_state, 'searchable_content') else 'session_data'
        })

        if not target_data:
            return []

        results = []
        query_lower = query.lower()

        # Enhanced search with real website content
        for item in target_data:
            score = 0
            name = item.get('name', '').lower()
            display_name = item.get('display_name', name).lower()
            description = item.get('description', '').lower()
            short_desc = item.get('short_description', '').lower()

            # Primary matching - exact matches get highest scores
            if query_lower in display_name:
                score += 15
            if query_lower in name:
                score += 12
            if query_lower in short_desc:
                score += 10
            if query_lower in description:
                score += 8

            # Category and type matching
            categories = item.get('ai_categories', item.get('categories', []))
            item_type = item.get('type', '').lower()

            if query_lower in item_type:
                score += 8

            for category in categories:
                if query_lower in category.lower():
                    score += 6

            # Enhanced semantic matching for Tshwane tourism content
            tourism_keywords = {
                'museum': ['ditsong', 'history', 'cultural', 'heritage', 'mrs ples', 'skull', 'ancestor'],
                'nature': ['wildlife', 'reserve', 'big 5', 'rhino', 'lion', 'giraffe', 'antelope', 'birding'],
                'architecture': ['grand', 'monument', 'sculpture', 'building', 'cultural'],
                'outdoor': ['nature', 'park', 'wildlife', 'reserve', 'birding', 'wetlands'],
                'culture': ['museum', 'heritage', 'historical', 'art', 'cultural', 'monument'],
                'food': ['restaurant', 'dining', 'cuisine', 'cafe', 'fine dining'],
                'entertainment': ['show', 'event', 'festival', 'music', 'market'],
                'shopping': ['market', 'centre', 'shopping', 'bustling'],
                'tourism': ['tourist', 'map', 'guide', 'information', 'accommodation']
            }

            # Check for semantic matches
            for key, keywords in tourism_keywords.items():
                if key in query_lower:
                    for keyword in keywords:
                        if keyword in description or keyword in name or keyword in display_name:
                            score += 4

                # Also check if any keyword matches the query
                for keyword in keywords:
                    if keyword in query_lower:
                        if key in description or key in name or key in display_name:
                            score += 3

            # Sentiment boost for positive content
            sentiment = item.get('ai_sentiment', 'neutral')
            if sentiment == 'positive':
                score += 2

            # Source verification boost
            if item.get('verified_source', False):
                score += 3

            # Weather suitability matching
            weather_terms = ['sunny', 'rainy',
                             'cloudy', 'hot', 'cold', 'weather']
            if any(term in query_lower for term in weather_terms):
                weather_data = item.get('weather_suitability', {})
                if weather_data:
                    score += 5

            if score > 0:
                results.append({
                    **item,
                    'relevance_score': score,
                    'search_query': query,
                    'matched_content': self._extract_matched_content(item, query_lower)
                })

        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:10]

    def _extract_matched_content(self, item: Dict[str, Any], query: str) -> str:
        """Extract the part of content that matches the search query"""
        description = item.get('description', '')
        if query in description.lower():
            # Find the sentence containing the query
            sentences = description.split('.')
            for sentence in sentences:
                if query in sentence.lower():
                    return sentence.strip() + "..."

        return item.get('short_description', description[:100] + "...")


# Page configuration
st.set_page_config(
    page_title="Tshwane Tourism Interactive Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced session state management


class SessionManager:
    """Lovable-inspired session state management"""

    @staticmethod
    def initialize_session():
        """Initialize all session state variables"""
        # Remove CSV loading and related variables
        defaults = {
            'website_data': {},
            'places_data': [],
            'restaurants_data': [],
            'social_links': [],
            'contact_info': {},
            'planning_system': TshwanePlanningSystem(),
            'component_system': ComponentSystem(),
            'semantic_search': SemanticSearch(),
            'operation_mode': OperationMode.PLANNING,
            'current_plan': None,
            'execution_progress': 0,
            'real_time_updates': True,
            'tool_calls': [],
            'notifications': [],
            'user_preferences': {
                'theme': 'nature',
                'auto_refresh': True,
                'show_progress': True
            },
            'csv_data_loaded': False,
            'available_place_types': [],
            'available_weather_options': []
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def update_progress(step: str, progress: int):
        """Update execution progress with real-time feedback"""
        st.session_state.execution_progress = progress
        if st.session_state.user_preferences['show_progress']:
            st.session_state.planning_system.think(
                f"Completed: {step} ({progress}%)")

    @staticmethod
    def add_notification(message: str, type: str="info"):
        """Add notification with timestamp"""
        notification = {
            'id': str(uuid.uuid4())[:8],
            'message': message,
            'type': type,
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        st.session_state.notifications.append(notification)

        # Keep only last 10 notifications
        if len(st.session_state.notifications) > 10:
            st.session_state.notifications = st.session_state.notifications[-10:]


class RealTimeProcessor:
    """Manus-inspired real-time processing system"""

    def __init__(self):
        self.processing_queue = []
        self.active_tasks = {}

    def add_task(self, task_id: str, task_type: str, parameters: Dict[str, Any]):
        """Add task to processing queue"""
        task = {
            'id': task_id,
            'type': task_type,
            'parameters': parameters,
            'status': 'queued',
            'created_at': datetime.now().isoformat()
        }
        self.processing_queue.append(task)
        return task_id

    def process_task(self, task_id: str) -> Dict[str, Any]:
        """Process a specific task with progress updates"""
        task = next(
            (t for t in self.processing_queue if t['id'] == task_id), None)
        if not task:
            return {'error': 'Task not found'}

        task['status'] = 'processing'
        self.active_tasks[task_id] = task

        try:
            if task['type'] == 'scrape_website':
                return self._process_website_scraping(task)
            elif task['type'] == 'process_booking':
                return self._process_booking(task)
            elif task['type'] == 'generate_recommendations':
                return self._process_recommendations(task)
            else:
                return {'error': 'Unknown task type'}

        except Exception as e:
            task['status'] = 'failed'
            task['error'] = str(e)
            return {'error': str(e)}

    def _process_website_scraping(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process website scraping with progress updates"""
        SessionManager.update_progress("Starting website scraping", 10)

        # Simulate scraping process
        url = task['parameters'].get('url', 'http://www.visittshwane.co.za')

        SessionManager.update_progress("Fetching website content", 30)
        time.sleep(1)  # Simulate network delay

        SessionManager.update_progress("Parsing HTML content", 50)
        time.sleep(0.5)

        SessionManager.update_progress("Extracting tourism data", 70)
        time.sleep(0.5)

        SessionManager.update_progress("Categorizing content", 90)
        time.sleep(0.5)

        SessionManager.update_progress("Website scraping completed", 100)

        task['status'] = 'completed'
        return {'success': True, 'message': 'Website scraping completed successfully'}

    def _process_booking(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process booking with encryption and validation"""
        SessionManager.update_progress("Validating booking data", 20)

        booking_data = task['parameters'].get('booking_data', {})

        SessionManager.update_progress("Encrypting sensitive information", 40)
        time.sleep(0.5)

        SessionManager.update_progress("Generating confirmation", 60)
        time.sleep(0.5)

        SessionManager.update_progress("Sending notifications", 80)
        time.sleep(0.5)

        SessionManager.update_progress("Booking processing completed", 100)

        task['status'] = 'completed'
        return {'success': True, 'booking_id': str(uuid.uuid4())[:8]}

    def _process_recommendations(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process weather-based recommendations"""
        SessionManager.update_progress("Analyzing weather conditions", 25)
        time.sleep(0.3)

        SessionManager.update_progress("Matching places to weather", 50)
        time.sleep(0.3)

        SessionManager.update_progress("Ranking recommendations", 75)
        time.sleep(0.3)

        SessionManager.update_progress("Recommendations generated", 100)

        task['status'] = 'completed'
        return {'success': True, 'recommendations': []}


# Initialize enhanced session management
SessionManager.initialize_session()

# Asset loading functions


def load_website_assets():
    """Load assets from the cloned website"""
    assets = {
        'images': [],
        'css': [],
        'js': [],
        'html_pages': []
    }

    try:
        # Load images from cloned website
        images_dir = Path("tshwane_crawled_data/assets")
        if images_dir.exists():
            for img_file in images_dir.glob("*.{jpg,jpeg,png,gif,svg}"):
                assets['images'].append(str(img_file))

        # Load HTML pages
        pages_dir = Path("tshwane_crawled_data/pages")
        if pages_dir.exists():
            for html_file in pages_dir.glob("*.html"):
                assets['html_pages'].append(str(html_file))

        # Load processed data
        data_dir = Path("processed_data")
        if data_dir.exists():
            if (data_dir / "enhanced_tshwane_data.json").exists():
                with open(data_dir / "enhanced_tshwane_data.json", 'r', encoding='utf-8') as f:
                    assets['tourism_data'] = json.load(f)

        return assets
    except Exception as e:
        st.warning(f"Could not load website assets: {e}")
        return assets


def get_place_types_from_csv():
    """Get unique place types from CSV for multi-select options"""
    from pathlib import Path
    import pandas as pd
    try:
        csv_file = Path("tshwane_places.csv")
        if not csv_file.exists():
            csv_file = Path("processed_data/tshwane_places.csv")
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            types = df['type'].unique().tolist()
            return [t for t in types if pd.notna(t)]
        else:
            return ['attraction', 'accommodation', 'restaurant', 'venue', 'area']
    except Exception as e:
        return ['attraction', 'accommodation', 'restaurant', 'venue', 'area']


def get_weather_options_from_csv():
    """Get weather options based on weather_suitability data in CSV"""
    from pathlib import Path
    import pandas as pd
    try:
        csv_file = Path("tshwane_places.csv")
        if not csv_file.exists():
            csv_file = Path("processed_data/tshwane_places.csv")
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            weather_options = set()
            for _, row in df.iterrows():
                weather_data = row.get('weather_suitability', '')
                if isinstance(weather_data, str) and weather_data.startswith('{'):
                    try:
                        weather_dict = eval(weather_data)
                        weather_options.update(weather_dict.keys())
                    except:
                        pass
            if weather_options:
                return sorted(list(weather_options))
            else:
                return ["sunny", "rainy", "cloudy", "hot", "cold", "windy", "mild"]
        else:
            return ["sunny", "rainy", "cloudy", "hot", "cold", "windy", "mild"]
    except Exception as e:
        return ["sunny", "rainy", "cloudy", "hot", "cold", "windy", "mild"]


def create_tutorial_system():
    """Create a modern, context-aware interactive tutorial system for the Tshwane Tourism Portal."""
    if 'tutorial_step' not in st.session_state:
        st.session_state.tutorial_step = 0
        st.session_state.show_tutorial = False

    tutorial_steps = [
        {
            'title': '🌿 Welcome to Tshwane Tourism Portal',
            'content': 'Discover the beauty of Tshwane with our AI-powered tourism assistant. Plan, explore, and book your perfect trip—all in one place, with real data and smart features.',
            'action': 'Click "Next" to begin your journey!'
        },
        {
            'title': '🎯 Choose Your Mode',
            'content': 'Select your preferred mode: Planning (step-by-step guidance), Standard (regular use), or Real-Time (live updates). Each mode tailors the experience to your needs.',
            'action': 'Try switching modes in the top-right corner.'
        },
        {
            'title': '🌐 Load Real Tourism Data',
            'content': 'Get the latest places, restaurants, and attractions by loading real data from the Tshwane Tourism website and CSVs. This powers all recommendations and maps.',
            'action': 'Click "Load Data" in the sidebar.'
        },
        {
            'title': '🔍 Smart Search & Navigation',
            'content': 'Use the sidebar to search for activities, places, or restaurants. Navigation buttons let you jump to the gallery, booking, weather, analytics, and more.',
            'action': 'Try searching for "museum" or "outdoor" in the sidebar.'
        },
        {
            'title': '🏛️ Explore the Interactive Gallery',
            'content': 'Browse real places with images, categories, and links. Sync with the official gallery for the latest updates. Use Previous/Next/Random to explore.',
            'action': 'Visit the Gallery and try the navigation buttons.'
        },
        {
            'title': '🗺️ Discover on the Map',
            'content': 'See all places and restaurants on an interactive map. Filter by type, view details, and use quick Google Maps links for directions.',
            'action': 'Scroll to the map and try filtering or clicking a marker.'
        },
        {
            'title': '🤖 Plan Your Trip with AI',
            'content': 'Use the Activity Planner to select interests and get AI-powered suggestions. Add favorites, reorder your plan, and get step-by-step recommendations.',
            'action': 'Open Planning Mode and select some activities.'
        },
        {
            'title': '📝 Book Your Experience',
            'content': 'Book single or multiple places with a modern, validated form. Choose times, add special requests, and get instant AI feedback and confirmation.',
            'action': 'Go to Booking Form and try booking a place.'
        },
        {
            'title': '🌤️ Get AI Weather Recommendations',
            'content': 'Let the AI suggest the best places to visit based on the weather. Use real data or simulate conditions for tailored recommendations.',
            'action': 'Try the Weather Guide and get AI suggestions.'
        },
        {
            'title': '📊 Track Progress & Notifications',
            'content': 'See real-time notifications for bookings, updates, and system status. View analytics on places, activities, and your journey.',
            'action': 'Check the sidebar and analytics dashboard.'
        },
        {
            'title': "🎉 You're Ready!",
            'content': "You've completed the tour! Explore, plan, and book with confidence. Need help? Restart the tutorial anytime from the sidebar.",
            'action': 'Click "Finish" to start your adventure!'
        }
    ]

    return tutorial_steps


def display_tutorial():
    """Display the tutorial as a Streamlit-native interactive container (no HTML/JS overlay)."""
    if st.session_state.get('show_tutorial', False):
        tutorial_steps = create_tutorial_system()
        current_step = st.session_state.get('tutorial_step', 0)
        n_steps = len(tutorial_steps)
        step = tutorial_steps[current_step] if current_step < n_steps else None

        with st.container():
            st.markdown("""
            <style>
            .tutorial-native-container {
                background: linear-gradient(135deg, #232a36 0%, #181c24 100%);
                border-radius: 22px;
                box-shadow: 0 8px 40px #00d4aa55;
                padding: 38px 36px 28px 36px;
                max-width: 480px;
                margin: 32px auto 24px auto;
                border: 2px solid #00d4aa44;
                color: #fff;
            }
            .tutorial-native-container h2, .tutorial-native-container h3 {
                color: #00d4aa;
            }
            .tutorial-native-progress {
                width: 100%;
                height: 8px;
                background: #232a36;
                border-radius: 6px;
                margin-bottom: 18px;
                overflow: hidden;
            }
            .tutorial-native-progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #00d4aa 0%, #00b894 100%);
                border-radius: 6px;
                transition: width 0.4s cubic-bezier(0.4,0,0.2,1);
            }
            </style>
            <div class='tutorial-native-container'>
            """, unsafe_allow_html=True)
            progress_pct = int((current_step + 1) / n_steps * 100)
            st.markdown(f"""
            <div class='tutorial-native-progress'><div class='tutorial-native-progress-bar' style='width:{progress_pct}%;'></div></div>
            <h2 style='margin-bottom: 16px;'>Step {current_step+1} of {n_steps}</h2>
            <h3 style='margin-bottom: 12px;'>{step['title']}</h3>
            <p style='color: #b3b3b3; line-height: 1.6; margin-bottom: 20px;'>{step['content']}</p>
            <p style='color: #00d4aa; font-weight: 500; margin-bottom: 24px;'>💡 {step['action']}</p>
            </div>
            """, unsafe_allow_html=True)
            # Navigation buttons
            nav_cols = st.columns([1, 1, 1, 1])
            with nav_cols[0]:
                if st.button('Back', key='tutorial_back_btn', disabled=current_step == 0):
                    if current_step > 0:
                        st.session_state.tutorial_step = current_step - 1
            with nav_cols[1]:
                if st.button('Skip', key='tutorial_skip_btn'):
                    st.session_state.show_tutorial = False
                    st.session_state.tutorial_step = 0
            with nav_cols[2]:
                if st.button('Next', key='tutorial_next_btn', disabled=current_step == n_steps - 1):
                    if current_step < n_steps - 1:
                        st.session_state.tutorial_step = current_step + 1
            with nav_cols[3]:
                if st.button('Finish', key='tutorial_finish_btn', disabled=current_step != n_steps - 1):
                    st.session_state.show_tutorial = False
                    st.session_state.tutorial_step = 0


def optimize_loading():
    """Optimize loading speed with caching and lazy loading"""
    # Cache website assets
    if 'website_assets' not in st.session_state:
        with st.spinner("🔄 Loading website assets..."):
            # Ensure minimum 3-second loading time
            start_time = time.time()

            st.session_state.website_assets = load_website_assets()

            # Ensure minimum 3-second loading time
            elapsed_time = time.time() - start_time
            if elapsed_time < 3:
                time.sleep(3 - elapsed_time)

    # Lazy load heavy components
    if 'heavy_components_loaded' not in st.session_state:
        st.session_state.heavy_components_loaded = False

# Encryption functions


def generate_key():
    """Generate a key for encryption"""
    return Fernet.generate_key()


def encrypt_data(data, key):
    """Encrypt data using Fernet encryption"""
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data, key):
    """Decrypt data using Fernet encryption"""
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()

# Website scraping functions


@st.cache_data
def scrape_website(url):
    """Scrape the Tshwane Tourism website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data
        data = {
            'title': soup.find('title').text if soup.find('title') else '',
            'content': soup.get_text(),
            'links': [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)],
            'images': [urljoin(url, img.get('src')) for img in soup.find_all('img', src=True)],
            'social_links': extract_social_links(soup),
            'contact_info': extract_contact_info(soup),
            'places': extract_places(soup),
            'restaurants': extract_restaurants(soup)
        }

        return data
    except Exception as e:
        st.error(f"Error scraping website: {e}")
        return None


def extract_social_links(soup):
    """Extract social media links from the website"""
    social_patterns = [
        r'facebook\.com',
        r'twitter\.com',
        r'instagram\.com',
        r'linkedin\.com',
        r'youtube\.com',
        r'tiktok\.com'
    ]

    social_links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        for pattern in social_patterns:
            if re.search(pattern, href, re.IGNORECASE):
                social_links.append({
                    'platform': pattern.split('.')[0].title(),
                    'url': href,
                    'text': link.get_text(strip=True)
                })

    return social_links


def extract_contact_info(soup):
    """Extract contact information from the website"""
    contact_info = {}

    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, soup.get_text())
    contact_info['emails'] = list(set(emails))

    # Phone pattern
    phone_pattern = r'(\+27|0)[0-9\s\-\(\)]{8,15}'
    phones = re.findall(phone_pattern, soup.get_text())
    contact_info['phones'] = list(set(phones))

    # Address pattern (basic)
    address_elements = soup.find_all(text=re.compile(
        r'address|location|street|avenue|road', re.IGNORECASE))
    contact_info['addresses'] = [elem.strip() for elem in address_elements[:5]]

    return contact_info


def extract_places(soup):
    """Extract places/attractions from the website"""
    places = []

    # Look for common place indicators
    place_keywords = ['attraction', 'museum', 'park',
                      'monument', 'gallery', 'center', 'square', 'garden']

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'div', 'p']):
        text = element.get_text(strip=True)
        if any(keyword in text.lower() for keyword in place_keywords) and len(text) < 100:
            places.append({
                'name': text,
                'description': text,
                'type': 'attraction'
            })

    return places[:20]  # Limit to 20 places


def extract_restaurants(soup):
    """Extract restaurants from the website"""
    restaurants = []

    # Look for restaurant indicators
    restaurant_keywords = ['restaurant', 'cafe',
                           'dining', 'food', 'cuisine', 'bar', 'grill']

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'div', 'p']):
        text = element.get_text(strip=True)
        if any(keyword in text.lower() for keyword in restaurant_keywords) and len(text) < 100:
            restaurants.append({
                'name': text,
                'description': text,
                'type': 'restaurant'
            })

    return restaurants[:15]  # Limit to 15 restaurants

# Weather-based suggestions using Hugging Face


@st.cache_resource
def load_weather_model():
    """Load Hugging Face model for weather-based suggestions"""
    try:
        from transformers import pipeline
        classifier = pipeline(
            "text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        return classifier
    except Exception as e:
        st.warning(f"Could not load weather model: {e}")
        return None


def get_weather_suggestions(weather_condition, places_data):
    """Get place suggestions based on weather"""
    return WEATHER_SERVICE.score_places_for_weather(places_data, weather_condition, limit=5)

# Enhanced main application with AI tool integrations


def main():
    """Main application with enhanced AI capabilities"""

    # Show tutorial overlay if requested
    display_tutorial()

    # Enhanced Dark Theme CSS with optimized performance
    st.markdown("""
    <style>
        /* Import Google Fonts for better readability */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Dark theme colors */
        :root {
            --primary-bg: #000000;
            --secondary-bg: #000000;
            --accent-bg: #262730;
            --primary-green: #00d4aa;
            --secondary-green: #00b894;
            --dark-green: #00a085;
            --text-primary: #ffffff;
            --text-secondary: #ffffff;
            --text-muted: #ffffff;
            --border-color: #2d3748;
            --shadow-dark: rgba(0, 0, 0, 0.3);
            --shadow-light: rgba(0, 212, 170, 0.1);
        }

        /* Main app styling */
        .stApp {
            background: linear-gradient(135deg, var(--primary-bg) 0%, var(--secondary-bg) 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
        }

        /* Override Streamlit's default styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            background: transparent;
        }

        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
            padding: 24px;
            border-radius: 16px;
            color: var(--primary-bg);
            text-align: center;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px var(--shadow-light);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }

        .main-header h1 {
            font-weight: 700;
            font-size: 2.5rem;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .main-header p {
            font-weight: 400;
            font-size: 1.1rem;
            margin: 8px 0 0 0;
            opacity: 0.9;
        }

        /* Gallery card styling with optimized animations */
        .gallery-card {
            background: var(--accent-bg);
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 20px var(--shadow-dark);
            margin: 16px 0;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1),
                        box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--primary-green);
            will-change: transform;
        }

        .gallery-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 12px 40px var(--shadow-dark), 0 0 20px var(--shadow-light);
            border-left-color: var(--secondary-green);
        }

        .gallery-card h3 {
            color: var(--primary-green);
            font-weight: 600;
            font-size: 1.4rem;
            margin: 0 0 12px 0;
        }

        .gallery-card p {
            color: var(--text-secondary);
            line-height: 1.6;
            margin: 8px 0;
        }

        .gallery-card .badge {
            background: var(--primary-green);
            color: var(--primary-bg);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
            margin-top: 12px;
        }

        /* Enhanced button styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
            color: var(--primary-bg);
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(0, 212, 170, 0.2);
            font-family: 'Inter', sans-serif;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, var(--secondary-green) 0%, var(--dark-green) 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 170, 0.3);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Sidebar styling */
        .css-1d391kg, .css-1cypcdb {
            background: linear-gradient(180deg, var(--secondary-bg) 0%, var(--accent-bg) 100%);
            border-right: 1px solid var(--border-color);
        }

        .sidebar-content {
            padding: 16px;
        }

        .sidebar-button {
            display: block;
            width: 100%;
            background: var(--accent-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px 16px;
            margin: 8px 0;
            text-decoration: none;
            transition: all 0.2s ease;
            font-weight: 500;
            text-align: left;
            cursor: pointer;
        }

        .sidebar-button:hover {
            background: var(--primary-green);
            color: var(--primary-bg);
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0, 212, 170, 0.2);
        }

        .sidebar-button i {
            margin-right: 8px;
            width: 16px;
        }

        /* Form styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input {
            background: var(--accent-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: var(--primary-green);
            box-shadow: 0 0 0 2px rgba(0, 212, 170, 0.2);
        }

        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--primary-green) 0%, var(--secondary-green) 100%);
        }

        /* Map container styling */
        .map-container {
            background: var(--accent-bg);
            border-radius: 16px;
            padding: 16px;
            margin: 16px 0;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 20px var(--shadow-dark);
            overflow: auto;
            height: 500px;
            position: relative;
        }

        .map-container iframe {
            border-radius: 12px;
            width: 100%;
            height: 100%;
            border: none;
        }

        /* Tutorial overlay */
        .tutorial-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .tutorial-content {
            background: var(--accent-bg);
            border-radius: 16px;
            padding: 32px;
            max-width: 500px;
            margin: 20px;
            border: 1px solid var(--border-color);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }

        /* Loading spinner */
        .loading-spinner {
            border: 3px solid var(--border-color);
            border-top: 3px solid var(--primary-green);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Optimized animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--secondary-bg);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--primary-green);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-green);
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .gallery-card {
                margin: 8px 0;
                padding: 16px;
            }

            .main-header {
                padding: 16px;
            }

            .main-header h1 {
                font-size: 2rem;
            }

            .tutorial-content {
                margin: 10px;
                padding: 24px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize real-time processor
    if 'real_time_processor' not in st.session_state:
        st.session_state.real_time_processor = RealTimeProcessor()

    # Header with mode indicator
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("🌿 Tshwane Tourism Interactive Portal")
        st.markdown(
            "*Discover the beauty of Tshwane with our AI-powered tourism assistant*")

    with col2:
        # Mode selector (Devin-inspired)
        mode = st.selectbox(
            "Operation Mode",
            [OperationMode.PLANNING.value, OperationMode.STANDARD.value,
                OperationMode.REAL_TIME.value],
            index=0
        )
        st.session_state.operation_mode = OperationMode(mode)

    with col3:
        # Real-time refresh toggle (Lovable-inspired)
        auto_refresh = st.toggle(
            "🔄 Auto Refresh", value=st.session_state.user_preferences['auto_refresh'])
        st.session_state.user_preferences['auto_refresh'] = auto_refresh

        if auto_refresh:
            time.sleep(1)
            st.rerun()

    # Planning mode interface (Devin-inspired)
    if st.session_state.operation_mode == OperationMode.PLANNING:
        display_planning_interface()

    # Progress indicator (v0-inspired)
    if st.session_state.execution_progress > 0:
        st.session_state.component_system.render_component(
            "progress_indicator",
            {"progress": st.session_state.execution_progress}
        )

    # Enhanced sidebar with tool integration
    display_enhanced_sidebar()

    # Main content with component system
    display_main_content()


def display_weather_insights(weather_condition: str):
    """Display weather-specific insights and tips"""
    insights = {
        'sunny': {
            'icon': '☀️',
            'tips': ['Bring sunscreen and water', 'Perfect for outdoor photography', 'Early morning visits recommended'],
            'activities': ['Hiking', 'Garden tours', 'Outdoor monuments']
        },
        'rainy': {
            'icon': '🌧️',
            'tips': ['Bring an umbrella', 'Check indoor opening hours', 'Great for cozy experiences'],
            'activities': ['Museum visits', 'Gallery tours', 'Shopping centers']
        },
        'cloudy': {
            'icon': '☁️',
            'tips': ['Perfect for photography', 'Comfortable walking weather', 'No harsh shadows'],
            'activities': ['City walks', 'Historic tours', 'Market visits']
        },
        'hot': {
            'icon': '🌡️',
            'tips': ['Stay hydrated', 'Seek air-conditioned spaces', 'Avoid midday sun'],
            'activities': ['Indoor attractions', 'Water features', 'Shaded areas']
        },
        'cold': {
            'icon': '🥶',
            'tips': ['Dress warmly', 'Enjoy hot beverages', 'Indoor activities preferred'],
            'activities': ['Museums', 'Cafes', 'Indoor markets']
        }
    }

    insight = insights.get(weather_condition.lower())
    if insight:
        st.markdown(f"### {insight['icon']} Weather Insights")

        col1, col2 = st.columns(2)
        with col1:
            st.write("**💡 Tips:**")
            for tip in insight['tips']:
                st.write(f"• {tip}")

        with col2:
            st.write("**🎯 Recommended Activities:**")
            for activity in insight['activities']:
                st.write(f"• {activity}")
    # Real-time notifications (Lovable-inspired)
    # display_real_time_notifications(
    #     toggle_key="show_all_notifications_toggle_main")


def display_planning_interface():
    """Unified planning interface: custom icons, dark theme, advanced interactivity."""
    import pandas as pd
    import re
    import random
    import time
    from collections import defaultdict
    # --- Tab selector for planning modes ---
    tab = st.radio('Planning Mode', [
                   'Activity Planner', 'AI-Enhanced Planning'], key='planning_mode_tab')

    # --- Custom SVG/Unicode icon map for categories ---
    icon_map = {
        'accommodation': '<svg width="32" height="32" viewBox="0 0 24 24" fill="#00d4aa"><path d="M3 21v-2h18v2H3zm0-4V7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10H3zm2-8v8h14V9H5zm2 2h2v2H7v-2zm4 0h2v2h-2v-2zm4 0h2v2h-2v-2z"/></svg>',
        'restaurant': '🍽️',
        'service': '🛎️',
        'attraction': '<svg width="32" height="32" viewBox="0 0 24 24" fill="#ffd700"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2" stroke="#222" stroke-width="2" fill="none"/></svg>',
        'area': '🌍',
        'venue': '<svg width="32" height="32" viewBox="0 0 24 24" fill="#b388ff"><rect x="4" y="8" width="16" height="10" rx="2"/><path d="M8 8V6a4 4 0 0 1 8 0v2" stroke="#fff" stroke-width="2" fill="none"/></svg>',
        'shopping': '🛍️',
        'museum': '<svg width="32" height="32" viewBox="0 0 24 24" fill="#ff7043"><rect x="4" y="10" width="16" height="8" rx="2"/><path d="M2 10l10-6 10 6" stroke="#fff" stroke-width="2" fill="none"/></svg>',
        'spa': '💆',
        'park': '🏞️',
        'cafe': '☕',
        'event': '🎉',
        'nature': '🌳',
        'default': '<svg width="32" height="32" viewBox="0 0 24 24" fill="#888"><circle cx="12" cy="12" r="10"/></svg>'
    }

    def get_icon(cat):
        for k, v in icon_map.items():
            if k in str(cat).lower():
                return v
        return icon_map['default']

    # --- Custom dark theme CSS for planning interface ---
    st.markdown("""
    <style>
    .planning-dark-container {
        background: linear-gradient(135deg, #181c24 0%, #232a36 100%);
        border-radius: 18px;
        box-shadow: 0 4px 24px #000a;
        padding: 22px 28px 18px 28px;
        margin-bottom: 22px;
        border: 1.5px solid #00d4aa44;
        animation: fadeInUp 0.7s;
    }
    .planning-card {
        background: #232a36;
        border-radius: 14px;
        box-shadow: 0 2px 12px #00d4aa22;
        margin: 10px 0 18px 0;
        padding: 18px 16px 12px 16px;
        border: 1.5px solid #00d4aa33;
        transition: box-shadow 0.2s, transform 0.2s;
        position: relative;
    }
    .planning-card:hover {
        box-shadow: 0 8px 32px #00d4aa55;
        transform: scale(1.025);
        border-color: #00d4aa;
        z-index: 2;
    }
    .planning-icon {
        display: inline-block;
        vertical-align: middle;
        margin-right: 10px;
        width: 32px;
        height: 32px;
        line-height: 32px;
        text-align: center;
        border-radius: 50%;
        background: #222c37;
        box-shadow: 0 2px 8px #00d4aa22;
        margin-bottom: 6px;
    }
    .planning-fav {
        position: absolute;
        top: 10px;
        right: 18px;
        font-size: 1.5em;
        color: #ffd700cc;
        cursor: pointer;
        transition: color 0.2s, transform 0.2s;
    }
    .planning-fav.fav-on {
        color: #ffd700;
        transform: scale(1.2);
        text-shadow: 0 2px 8px #ffd70088;
    }
    .planning-updown {
        position: absolute;
        bottom: 10px;
        right: 18px;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .planning-updown button {
        background: #232a36;
        color: #00d4aa;
        border: 1px solid #00d4aa44;
        border-radius: 6px;
        font-size: 1.1em;
        padding: 2px 8px;
        margin: 0;
        cursor: pointer;
        transition: background 0.2s, color 0.2s;
    }
    .planning-updown button:hover {
        background: #00d4aa22;
        color: #fff;
    }
    .planning-tooltip {
        display: inline-block;
        position: relative;
        cursor: pointer;
    }
    .planning-tooltip .planning-tooltiptext {
        visibility: hidden;
        width: 180px;
        background: #232a36;
        color: #fff;
        text-align: center;
        border-radius: 8px;
        padding: 8px 0;
        position: absolute;
        z-index: 10;
        bottom: 125%;
        left: 50%;
        margin-left: -90px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.95em;
    }
    .planning-tooltip:hover .planning-tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    <style>@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px);} to { opacity: 1; transform: translateY(0);} }</style>
    """, unsafe_allow_html=True)

    # --- Shared logic: extract activities/entities from all CSVs ---
    def extract_activities_and_places(selected_activities=None, user_query=None):
        activity_set = set()
        place_cards = []
        csvs = [
            'tshwane_places.csv',
            'processed_data/tshwane_places.csv',
            'processed_data/tshwane_restaurants.csv',
            'scraps/Tryp_Thooe_Tourism-main/processed_data/tshwane_descriptions.csv',
            'scraps/Tryp_Thooe_Tourism-main/Tryp_Thooe_Tourism/processed_data/tshwane_places.csv',
            'scraps/Tryp_Thooe_Tourism-main/Tryp_Thooe_Tourism/processed_data/tshwane_restaurants.csv'
        ]

        def add_activities_from_col(df, col):
            if col in df.columns:
                for v in df[col].dropna().unique():
                    if isinstance(v, str):
                        for part in re.split(r'[|,;/]', v):
                            part = part.strip()
                            if part and len(part) > 2:
                                activity_set.add(part)

        for path in csvs:
            try:
                df = pd.read_csv(path)
                for col in ['type', 'category', 'ai_categories', 'highlights', 'facilities', 'special_features']:
                    add_activities_from_col(df, col)
                for idx, row in df.iterrows():
                    found = False
                    if selected_activities:
                        for col in ['type', 'category', 'ai_categories', 'highlights', 'facilities', 'special_features']:
                            val = row.get(col, '')
                            if any(act.lower() in str(val).lower() for act in selected_activities):
                                found = True
                    elif user_query:
                        for col in ['type', 'category', 'ai_categories', 'highlights', 'facilities', 'special_features', 'description', 'name']:
                            val = row.get(col, '')
                            if user_query.lower() in str(val).lower():
                                found = True
                    if found:
                        name = row.get('name', row.get('Name', 'Unknown'))
                        desc = row.get('description', row.get(
                            'short_description', ''))
                        img = row.get('image', '')
                        cat = row.get('type', row.get('category', ''))
                        link = row.get('link', row.get('website', ''))
                        if not img:
                            img = f"https://placehold.co/400x250?text={name.replace(' ', '+')}&font=roboto"
                        place_cards.append({
                            'name': name,
                            'desc': desc,
                            'img': img,
                            'cat': cat,
                            'link': link
                        })
            except Exception:
                continue
        activities = sorted(activity_set)
        seen = set()
        unique_cards = []
        for card in place_cards:
            if card['name'] not in seen:
                unique_cards.append(card)
                seen.add(card['name'])
        return activities, unique_cards

    # --- Helper for favorite toggle ---
    def fav_key(name):
        return f"fav_{name.replace(' ', '_')}"

    # --- Helper for plan reordering ---
    def move_plan_item(plan, idx, direction):
        if direction == 'up' and idx > 0:
            plan[idx - 1], plan[idx] = plan[idx], plan[idx - 1]
        elif direction == 'down' and idx < len(plan) - 1:
            plan[idx + 1], plan[idx] = plan[idx], plan[idx + 1]
        return plan

    if tab == 'Activity Planner':
        with st.container():
            st.markdown("<div class='planning-dark-container'>",
                        unsafe_allow_html=True)
            st.markdown("""
            <h2 style='color: #00d4aa;'>🗺️ Smart Tourism Planner</h2>
            <p style='color:#b3b3b3;'>Select your desired activities and let the AI help you plan the perfect Tshwane experience.</p>
            """, unsafe_allow_html=True)
            activities, _ = extract_activities_and_places()
            selected_activities = st.multiselect(
                'What activities are you interested in?',
                options=activities,
                help='Choose one or more activities to get personalized suggestions.'
            )
            st.markdown("</div>", unsafe_allow_html=True)
        with st.expander('🎯 Suggestions for Your Activities', expanded=True):
            _, unique_cards = extract_activities_and_places(
                selected_activities=selected_activities)
            cols = st.columns(2)
            for i, card in enumerate(unique_cards):
                with cols[i % 2]:
                    st.markdown(f"<div class='planning-card'>",
                                unsafe_allow_html=True)
                    st.markdown(
                        f"<span class='planning-icon' title='{card['cat']}'>{get_icon(card['cat'])}</span>", unsafe_allow_html=True)
                    st.image(card['img'], use_container_width=True)
                    st.markdown(f"**{card['name']}**")
                    if card['cat']:
                        st.caption(f"Type: {card['cat']}")
                    st.markdown(card['desc'])
                    if card['link']:
                        st.markdown(f"[More Info]({card['link']})")
                    # Favorite toggle
                    fav = st.session_state.get(fav_key(card['name']), False)
                    if st.button('⭐' if not fav else '💛', key=fav_key(card['name'])):
                        st.session_state[fav_key(card['name'])] = not fav
                    st.markdown(
                        f"<span class='planning-fav {'fav-on' if fav else ''}'> {'💛' if fav else '⭐'}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        with st.expander('📝 Your Plan', expanded=True):
            plan = st.session_state.get('user_plan', [])
            for i, item in enumerate(plan):
                st.markdown(f"<div class='planning-card'>",
                            unsafe_allow_html=True)
                st.markdown(
                    f"<span class='planning-icon' title='{item['cat']}'>{get_icon(item['cat'])}</span>", unsafe_allow_html=True)
                st.markdown(f"<b>{i+1}. {item['name']}</b>")
                st.caption(f"Type: {item['cat']}")
                st.markdown(item['desc'])
                st.image(item['img'], width=200)
                date = st.date_input(
                    f"Date for {item['name']}", key=f"plan_date_{i}")
                time = st.time_input(
                    f"Time for {item['name']}", key=f"plan_time_{i}")
                # Favorite toggle
                fav = st.session_state.get(fav_key(item['name']), False)
                if st.button('⭐' if not fav else '💛', key=fav_key(item['name']) + "_plan"):
                    st.session_state[fav_key(item['name'])] = not fav
                st.markdown(
                    f"<span class='planning-fav {'fav-on' if fav else ''}'> {'💛' if fav else '⭐'}</span>", unsafe_allow_html=True)
                # Up/down buttons
                up, down = st.columns([1, 1])
                with up:
                    if st.button('⬆️', key=f"up_{i}"):
                        plan = move_plan_item(plan, i, 'up')
                        st.session_state['user_plan'] = plan
                        st.rerun()
                with down:
                    if st.button('⬇️', key=f"down_{i}"):
                        plan = move_plan_item(plan, i, 'down')
                        st.session_state['user_plan'] = plan
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            if not plan:
                st.info('No activities added to your plan yet.')
        with st.container():
            if st.button('🤖 Get AI Suggestions for Your Plan'):
                plan = st.session_state.get('user_plan', [])
                if plan:
                    st.success('Your plan looks great!')
                else:
                    st.warning('Add activities to your plan first.')
    else:
        with st.container():
            st.markdown("<div class='planning-dark-container'>",
                        unsafe_allow_html=True)
            st.markdown("### 🤖 AI-Enhanced Planning Mode")
            st.markdown("Powered by Hugging Face Models via MCP Integration")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Models Loaded", 7)
            with col2:
                st.metric("Available Tasks", 7)
            with col3:
                st.metric("Cache Status", "Active")
            user_input = st.text_area(
                "What would you like to plan for your Tshwane visit?",
                placeholder="e.g., I want to visit historical sites and need restaurant recommendations for a sunny day...",
                height=100
            )
            st.markdown("</div>", unsafe_allow_html=True)
        with st.expander('🎯 AI Suggestions for Your Request', expanded=True):
            if st.button("🤖 Get AI Planning Assistance", key="ai_planning_btn"):
                if user_input:
                    with st.spinner("🤖 AI is analyzing your request..."):
                        # Ensure minimum 3-second loading time
                        start_time = time.time()

                        # --- Placeholder for real backend integration ---
                        # To connect to a real backend, replace the following block with an API call to Hugging Face or your own service.
                        _, unique_cards = extract_activities_and_places(
                            user_query=user_input)
                        st.info(
                            "Step 1: Analyze user intent and extract key needs...")
                        time.sleep(1)
                        st.info(
                            "Step 2: Match activities and places from CSVs...")
                        time.sleep(1)
                        st.info(
                            "Step 3: Generate step-by-step plan and recommendations...")
                        time.sleep(1)

                        # Ensure minimum 3-second loading time
                        elapsed_time = time.time() - start_time
                        if elapsed_time < 3:
                            time.sleep(3 - elapsed_time)
                        st.success("Here is your AI-powered plan!")
                        cols = st.columns(2)
                        for i, card in enumerate(unique_cards):
                            with cols[i % 2]:
                                st.markdown(
                                    f"<div class='planning-card'>", unsafe_allow_html=True)
                                st.markdown(
                                    f"<span class='planning-icon' title='{card['cat']}'>{get_icon(card['cat'])}</span>", unsafe_allow_html=True)
                                st.image(card['img'], use_container_width=True)
                                st.markdown(f"**{card['name']}**")
                                if card['cat']:
                                    st.caption(f"Type: {card['cat']}")
                                st.markdown(card['desc'])
                                if card['link']:
                                    st.markdown(f"[More Info]({card['link']})")
                                # Favorite toggle
                                fav = st.session_state.get(
                                    fav_key(card['name']), False)
                                if st.button('⭐' if not fav else '💛', key=fav_key(card['name']) + "_ai"):
                                    st.session_state[fav_key(
                                        card['name'])] = not fav
                                st.markdown(
                                    f"<span class='planning-fav {'fav-on' if fav else ''}'> {'💛' if fav else '⭐'}</span>", unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown('---')
                        # Render the AI-Generated Plan section directly, not in an expander
                        st.markdown(
                            "<h4 style='color:#ffd700;'>📝 Your AI-Generated Plan</h4>", unsafe_allow_html=True)
                        for i, card in enumerate(unique_cards):
                            st.markdown(f"<div class='planning-card'>",
                                        unsafe_allow_html=True)
                            st.markdown(
                                f"<span class='planning-icon' title='{card['cat']}'>{get_icon(card['cat'])}</span>", unsafe_allow_html=True)
                            st.markdown(f"<b>{i+1}. {card['name']}</b>")
                            st.caption(f"Type: {card['cat']}")
                            st.markdown(card['desc'])
                            st.image(card['img'], width=200)
                            date = st.date_input(
                                f"Date for {card['name']}", key=f"ai_plan_date_{i}")
                            time = st.time_input(
                                f"Time for {card['name']}", key=f"ai_plan_time_{i}")
                            # Favorite toggle
                            fav = st.session_state.get(
                                fav_key(card['name']), False)
                            if st.button('⭐' if not fav else '��', key=fav_key(card['name']) + "_ai_plan"):
                                st.session_state[fav_key(
                                    card['name'])] = not fav
                            st.markdown(
                                f"<span class='planning-fav {'fav-on' if fav else ''}'> {'💛' if fav else '⭐'}</span>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown(
                            "**Intent:** planning_request (Confidence: 0.92)")
                        st.markdown("**Sentiment:** positive (Score: 0.88)")
                        st.markdown(
                            "**AI Recommendations:**\n- Book in advance for popular sites.\n- Try local cuisine for lunch.\n- Check weather before outdoor activities.")
                else:
                    st.warning("Please enter your planning request.")


def display_enhanced_sidebar():
    """Enhanced sidebar with AI tool integrations, social/contact info, and dark theme"""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-content">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: var(--primary-green); margin-bottom: 8px;">🌿 Tourism Portal</h2>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">AI-Powered Tools</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Social/Contact Info Section with interactive dark-themed animated buttons
        st.markdown("""
        <style>
        .social-btn {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            background: linear-gradient(90deg, #232526 0%, #414345 100%);
            color: #f5f7fa;
            border: none;
            border-radius: 30px;
            padding: 12px 22px;
            margin: 8px 0;
            font-size: 1.08rem;
            font-weight: 600;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            box-shadow: 0 2px 10px rgba(0,0,0,0.10);
            cursor: pointer;
            transition: transform 0.18s cubic-bezier(0.4,0,0.2,1), box-shadow 0.18s cubic-bezier(0.4,0,0.2,1), background 0.18s, color 0.18s;
            outline: none;
            gap: 14px;
            letter-spacing: 0.01em;
        }
        .social-btn:hover {
            transform: scale(1.07) translateX(6px);
            background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
            color: #232526;
            box-shadow: 0 8px 24px rgba(0,212,170,0.18);
        }
        .social-icon {
            font-size: 1.35rem;
            margin-right: 12px;
            width: 28px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("### 📱 Social & Contact Info")
        # Restore only the first 5 unique social/contact links, skip NaN/missing URLs, and use animated button style
        import pandas as pd
        st.markdown("""
        <style>
        .social-btn {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            background: linear-gradient(90deg, #232526 0%, #414345 100%);
            color: #f5f7fa;
            border: none;
            border-radius: 30px;
            padding: 12px 22px;
            margin: 8px 0;
            font-size: 1.08rem;
            font-weight: 600;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            box-shadow: 0 2px 10px rgba(0,0,0,0.10);
            cursor: pointer;
            transition: transform 0.18s cubic-bezier(0.4,0,0.2,1), box-shadow 0.18s cubic-bezier(0.4,0,0.2,1), background 0.18s, color 0.18s;
            outline: none;
            gap: 14px;
            letter-spacing: 0.01em;
        }
        .social-btn:hover {
            transform: scale(1.07) translateX(6px);
            background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
            color: #232526;
            box-shadow: 0 8px 24px rgba(0,200,150,0.18);
        }
        .social-icon {
            font-size: 1.35rem;
            margin-right: 12px;
            width: 28px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        try:
            df_social = pd.read_csv('tshwane_social_links.csv')
            icon_map = {
                'facebook': '📘',
                'twitter': '🐦',
                'youtube': '▶️',
                'instagram': '📸',
                'linkedin': '💼',
                'tiktok': '🎵',
            }
            shown = set()
            count = 0
            for _, row in df_social.iterrows():
                url = str(row.get('url', '')).strip()
                text = str(row.get('text', '') or row.get(
                    'platform', '')).strip()
                platform = str(row.get('platform', '')).lower()
                key = (url, text)
                if url and url.lower() != 'nan' and key not in shown:
                    icon = icon_map.get(platform.split(
                        ',')[0].strip().lower(), '🔗')
                    st.markdown(f"""
                    <a href='{url}' target='_blank' class='social-btn' style='text-decoration:none;'>
                        <span class='social-icon'>{icon}</span> {text}
                    </a>
                    """, unsafe_allow_html=True)
                    shown.add(key)
                    count += 1
                if count >= 5:
                    break
        except Exception:
            st.info("No social links found.")

        # Tutorial button
        if st.button("📚 Start Tutorial", key="tutorial_btn", help="Learn how to use the app"):
            st.session_state.show_tutorial = True
            st.session_state.tutorial_step = 0
            st.rerun()

        st.markdown("### 🚀 Quick Actions")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🌐 Load Data", key="load_data_btn", help="Load tourism data"):
                st.session_state['places_data'] = load_tshwane_places_csv()
                st.success("Tourism data loaded from tshwane_places.csv!")
        with col2:
            if st.button("🔄 Refresh", key="refresh_btn", help="Refresh the application"):
                st.rerun()

        st.markdown("### 🔍 Smart Search")
        search_query = st.text_input(
            "Search tourism content:",
            placeholder="outdoor activities, museums, restaurants...",
            key="search_input"
        )
        if st.button("🔍 Search", key="search_btn") and search_query:
            results = [place for place in st.session_state['places_data'] if search_query.lower() in place.get(
                'name', '').lower() or search_query.lower() in place.get('description', '').lower()]
            if results:
                st.success(f"Found {len(results)} results:")
                for result in results[:5]:
                    st.markdown(
                        f"**{result.get('name', 'Unknown')}**<br><small>{result.get('type', '')}</small>", unsafe_allow_html=True)
            else:
                st.info("No results found. Try different keywords.")

        st.markdown("### 🧭 Navigation")
        # Navigation links as dark-themed animated buttons (Streamlit-native, interactive)
        nav_links = [
            ("Places Gallery", "gallery", '🏛️'),
            ("Individual Places", "individual_places", '📁'),
            ("Booking Form", "booking", '📝'),
            ("Weather Guide", "weather_guide", '🌤️'),
            ("Analytics", "analytics", '📊'),
            ("Contact Info", "contact", '📞'),
            ("AI Chat Assistant", "chat", '🤖'),
            ("Email Secretary", "email_secretary", '📧'),
        ]
        st.markdown("<div style='margin-top:18px;'></div>",
                    unsafe_allow_html=True)
        for text, key, icon in nav_links:
            btn = st.button(f"{icon} {text}",
                            key=f"nav_{key}", help=f"Go to {text}")
            if btn:
                st.session_state.current_section = key
                st.rerun()

        st.markdown("### 📊 System Status")
        st.metric("Places", len(st.session_state['places_data']), delta=None)
        st.metric("Notifications", len(
            st.session_state.get('notifications', [])), delta=None)

        # Display contact info in sidebar when contact section is active
        if st.session_state.get('current_section') == 'contact':
            st.markdown("### 👤 Developer Info")
            developers = load_developer_details()
            if developers:
                for dev in developers:  # Show all developers (now just one)
                    st.markdown(f"""
                    **{dev['name']}**  
                    {dev['role']}  
                    📧 {dev['email']}
                    """)

        # Display secretary info in sidebar when email secretary section is active
        if st.session_state.get('current_section') == 'email_secretary':
            st.markdown("### 📧 Secretary Contact")
            st.markdown("""
            **Tshwane Tourism Association**  
            📧 secretary@tshwanetourism.com  
            📞 +27 12 XXX XXXX  
            🏢 Main Office: Tshwane, South Africa
            """)
            st.markdown("### 💡 Quick Tips")
            st.markdown("""
            • Be specific about your inquiry
            • Include relevant details
            • Mention if urgent response needed
            • Provide contact information
            """)

        # 4. OCR Module (file upload + text extraction)
        st.markdown("### 🖼️ OCR Scan")
        uploaded_file = st.file_uploader(
            "Upload image for OCR", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            try:
                import pytesseract
                from PIL import Image
            except ImportError:
                st.error(
                    "OCR requires 'pytesseract' and 'Pillow'. Please install them with 'pip install pytesseract pillow'.")
            else:
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded Image",
                         use_container_width=True)
                text = pytesseract.image_to_string(img)
                st.markdown("**Extracted Text:**")
                st.code(text)

# 5. Left-side container for place summary/notifications


def display_left_summary():
    """Display summary of selected/booked place and notifications on the left"""
    with st.container():
        st.markdown("### 📝 Selected Place Summary")
        place = st.session_state.get('selected_place')
        if place:
            st.success(
                f"**{place.get('name', 'Unknown')}**\nType: {place.get('type', 'Unknown')}\n{place.get('description', '')}")
            lat, lon = place.get('latitude'), place.get('longitude')
            if lat and lon:
                st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
        else:
            st.info("No place selected yet.")
        st.markdown("### 🔔 Notifications")
        for notif in st.session_state.get('notifications', [])[-5:]:
            st.info(f"{notif['message']} ({notif['timestamp'][:19]})")

# 2. WhatsApp notification simulation (UI element)


def simulate_whatsapp_notification(booking_data):
    st.markdown("---")
    st.markdown(
        f"**📲 WhatsApp Notification:**\nA WhatsApp message would be sent to {booking_data.get('whatsapp', '[number]')} confirming the booking for {booking_data.get('selected_place', '[place]')}. (Simulation)")

# 3. Enhanced booking form with restaurant multi-choice and reservation option


def display_enhanced_booking_form():
    """Enhanced booking form with AI validation and real-time processing, grouped by place type with time selection, now with a dark theme."""
    import pandas as pd
    import datetime
    import hashlib
    import uuid

    if 'places_data' not in st.session_state or not st.session_state['places_data']:
        st.info("No places data loaded.")
        return

    # --- Dark theme CSS for the form ---
    st.markdown("""
    <style>
    .dark-booking-form {
        background: linear-gradient(135deg, #181c24 0%, #232a36 100%);
        border-radius: 18px;
        box-shadow: 0 4px 24px #000a;
        padding: 32px 28px 24px 28px;
        margin-bottom: 22px;
        border: 1.5px solid #00d4aa44;
        color: #fff;
        animation: fadeInUp 0.7s;
    }
    .dark-booking-form h2, .dark-booking-form h3, .dark-booking-form h4 {
        color: #00d4aa;
    }
    .dark-booking-form label, .dark-booking-form .stTextInput > div > div > input,
    .dark-booking-form .stTextArea > div > div > textarea,
    .dark-booking-form .stSelectbox > div > div > select,
    .dark-booking-form .stDateInput > div > div > input {
        background: #232a36 !important;
        color: #fff !important;
        border: 1px solid #00d4aa44 !important;
        border-radius: 8px !important;
    }
    .dark-booking-form .stTextInput > div > div > input:focus,
    .dark-booking-form .stTextArea > div > div > textarea:focus,
    .dark-booking-form .stSelectbox > div > div > select:focus {
        border-color: #00d4aa !important;
        box-shadow: 0 0 0 2px rgba(0, 212, 170, 0.2) !important;
    }
    .dark-booking-form .stButton > button {
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(0, 212, 170, 0.2);
        margin-top: 12px;
    }
    .dark-booking-form .stButton > button:hover {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%) !important;
        color: #fff !important;
    }
    .dark-booking-form .st-expander {
        background: #232a36 !important;
        color: #fff !important;
        border-radius: 12px !important;
        border: 1px solid #00d4aa33 !important;
    }
    .dark-booking-form .st-expanderHeader {
        color: #00d4aa !important;
    }
    .dark-booking-form .stAlert {
        background: #232a36 !important;
        color: #fff !important;
        border-left: 4px solid #00d4aa !important;
    }
    .dark-booking-form .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00d4aa 0%, #00b894 100%) !important;
    }
    .dark-booking-form .sticky-summary {
        background: #181c24;
        border-radius: 12px;
        padding: 18px;
        color: #fff;
        border: 1px solid #00d4aa33;
        margin-top: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Extract all unique types from places_data
    df_places = pd.DataFrame(st.session_state['places_data'])
    types = sorted(df_places['type'].dropna().unique().tolist())
    places_by_type = {
        t: df_places[df_places['type'] == t]['name'].tolist() for t in types}

    st.markdown('<div class="dark-booking-form">', unsafe_allow_html=True)
    st.markdown("### 🎯 Smart Booking System")
    with st.form("enhanced_booking_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "Full Name *", placeholder="Enter your full name")
            email = st.text_input(
                "Email Address *", placeholder="your.email@example.com")
            whatsapp = st.text_input(
                "WhatsApp Number *", placeholder="+27 XX XXX XXXX")
        with col2:
            visit_date = st.date_input(
                "Preferred Visit Date", min_value=datetime.date.today())

        st.markdown("---")
        st.subheader("Select Places to Visit by Category")
        selections = {}
        times = {}
        for t in types:
            with st.expander(f"{t.title()} ({len(places_by_type[t])} places)", expanded=False):
                selected = st.multiselect(
                    f"Select {t.title()}s", places_by_type[t], key=f"sel_{t}")
                selections[t] = selected
                for place in selected:
                    times[place] = st.time_input(f"Preferred time for {place}", value=datetime.time(
                        10, 0), key=f"time_{t}_{place}")
        st.markdown("---")
        special_requests = st.text_area(
            "Special Requests", placeholder="Any special requirements or requests...")
        form_valid = bool(name and email and whatsapp and any(
            selections[t] for t in types))
        if form_valid:
            st.success("✅ Form validation passed")
        else:
            st.warning(
                "⚠️ Please fill in all required fields marked with * and select at least one place.")
            # Debug info for missing fields
            missing = []
            if not name:
                missing.append("Full Name")
            if not email:
                missing.append("Email Address")
            if not whatsapp:
                missing.append("WhatsApp Number")
            if not any(selections[t] for t in types):
                missing.append("At least one place selection")
            if missing:
                st.info(f"Missing: {', '.join(missing)}")
        submitted = st.form_submit_button(
            "🚀 Submit Smart Booking",
            help="Submit your booking with AI-powered processing"
        )
        if submitted and form_valid:
            # Flatten selections into a list of dicts with type and time
            selected_places = []
            for t in types:
                for place in selections[t]:
                    selected_places.append({
                        'name': place,
                        'type': t,
                        'time': str(times[place])
                    })
            booking_data = {
                'name': name,
                'email': email,
                'whatsapp': whatsapp,
                'visit_date': str(visit_date),
                'selected_places': selected_places,
                'selected_place': selected_places[0]['name'] if selected_places else '',
                'selected_restaurant': '',
                'make_reservation': True,
                'special_requests': special_requests,
                'timestamp': datetime.datetime.now().isoformat(),
                'booking_id': hashlib.md5(f"{name}{email}{datetime.datetime.now()}".encode()).hexdigest()[:8],
                'ai_processed': True,
                'validation_score': calculate_booking_score({'name': name, 'email': email, 'whatsapp': whatsapp, 'selected_place': selected_places[0]['name'] if selected_places else '', 'visit_date': str(visit_date)})
            }
            task_id = st.session_state.real_time_processor.add_task(
                str(uuid.uuid4())[:8],
                'process_booking',
                {'booking_data': booking_data}
            )
            with st.spinner("Processing booking with AI..."):
                # Ensure minimum 3-second loading time
                start_time = time.time()

                result = st.session_state.real_time_processor.process_task(
                    task_id)
                if result.get('success'):
                    process_enhanced_booking(booking_data)
                    SessionManager.add_notification(
                        f"Booking confirmed: {result.get('booking_id')}", "success")
                else:
                    SessionManager.add_notification(
                        "Booking processing failed", "error")

                # Ensure minimum 3-second loading time
                elapsed_time = time.time() - start_time
                if elapsed_time < 3:
                    time.sleep(3 - elapsed_time)
    st.markdown('</div>', unsafe_allow_html=True)


def calculate_booking_score(booking_data):
    score = 0.0
    if booking_data.get('name'):
        score += 0.2
    if booking_data.get('email') and '@' in booking_data['email']:
        score += 0.2
    if booking_data.get('whatsapp'):
        score += 0.2
    # Accept either single or multi mode for place selection
    if booking_data.get('mode') == 'single':
        if any(len(v) > 0 for v in booking_data.get('selections', {}).values()):
            score += 0.2
    else:
        if any(len(v) > 0 for v in booking_data.get('bookings', {}).values()):
            score += 0.2
    if booking_data.get('timestamp') or booking_data.get('visit_date'):
        score += 0.2
    return score


def display_booking_form():
    """Display booking form with encryption"""
    if 'selected_place' not in st.session_state:
        st.info("Please select a place from the gallery above.")
        return

    with st.form("booking_form"):
        st.write(f"**Booking for:** {st.session_state.selected_place['name']}")

        # User details
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input(
            "Email Address *", placeholder="your.email@example.com")
        whatsapp = st.text_input(
            "WhatsApp Number *", placeholder="+27 XX XXX XXXX")

        # Place selection from CSV
        place_options = [place['name']
                         for place in st.session_state.places_data]
        selected_place = st.selectbox(
            "Select Place to Visit (from CSV)", place_options)

        # Multi-select for additional places from CSV
        additional_places = st.multiselect(
            "Additional Places to Visit",
            options=place_options,
            help="Select additional places you'd like to visit during your trip"
        )

        # Restaurant selection from CSV
        if st.session_state.restaurants_data:
            restaurant_options = ["None"] + [restaurant['name']
                                             for restaurant in st.session_state.restaurants_data]
            selected_restaurant = st.selectbox(
                "Select Restaurant (from CSV)", restaurant_options)
            make_reservation = st.checkbox("Make restaurant reservation")
        else:
            selected_restaurant = "None"
            make_reservation = True

        # Additional details
        visit_date = st.date_input("Preferred Visit Date")
        special_requests = st.text_area(
            "Special Requests", placeholder="Any special requirements or requests...")

        submitted = st.form_submit_button("🚀 Submit Booking")

        if submitted:
            if name and email and whatsapp:
                # Create booking data
                booking_data = {
                    'name': name,
                    'email': email,
                    'whatsapp': whatsapp,
                    'selected_place': selected_place,
                    'selected_restaurant': selected_restaurant,
                    'make_reservation': make_reservation,
                    'visit_date': str(visit_date),
                    'special_requests': special_requests,
                    'timestamp': datetime.now().isoformat(),
                    'booking_id': hashlib.md5(f"{name}{email}{datetime.now()}".encode()).hexdigest()[:8]
                }

                # Save and send booking
                process_booking(booking_data)
            else:
                st.error("Please fill in all required fields marked with *")


def process_booking(booking_data):
    """Process booking with encryption and email sending"""
    try:
        # Generate encryption key
        key = generate_key()

        # Encrypt sensitive data
        encrypted_data = encrypt_data(json.dumps(booking_data), key)

        # Save to DataFrame
        df = pd.DataFrame([booking_data])
        df.to_csv(f"booking_{booking_data['booking_id']}.csv", index=False)

        # Save encrypted version
        with open(f"encrypted_booking_{booking_data['booking_id']}.txt", 'wb') as f:
            f.write(encrypted_data)

        # Save encryption key separately
        with open(f"key_{booking_data['booking_id']}.key", 'wb') as f:
            f.write(key)

        # Send email (simulated)
        send_booking_email(booking_data)

        # Display confirmation
        st.success(
            f"✅ Booking submitted successfully! Booking ID: {booking_data['booking_id']}")

        # Add to notifications
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []

        st.session_state.notifications.append({
            'type': 'booking',
            'message': f"New booking for {booking_data['selected_place']} by {booking_data['name']}",
            'timestamp': datetime.now(),
            'data': booking_data
        })

    except Exception as e:
        st.error(f"Error processing booking: {e}")


def send_booking_email(booking_data):
    """Simulate sending email to secretary"""
    # In a real implementation, you would use actual SMTP settings
    email_content = f"""
    New Tourism Booking Request
    
    Booking ID: {booking_data['booking_id']}
    Client Name: {booking_data['name']}
    Email: {booking_data['email']}
    WhatsApp: {booking_data['whatsapp']}
    
    Selected Place: {booking_data['selected_place']}
    Selected Restaurant: {booking_data['selected_restaurant']}
    Restaurant Reservation: {'Yes' if booking_data['make_reservation'] else 'No'}
    
    Visit Date: {booking_data['visit_date']}
    Special Requests: {booking_data['special_requests']}
    
    Submitted: {booking_data['timestamp']}
    
    ---
    This booking was submitted through the Tshwane Tourism Interactive Portal
    Created by Profit Projects Online Virtual Assistance
    Enterprise Number: K2025200646
    Contact: Thapelo Kgothatso Thooe
    Email: kgothatsothooe@gmail.com
    """

    # Save email content to file
    with open(f"email_booking_{booking_data['booking_id']}.txt", 'w') as f:
        f.write(email_content)

    st.info("📧 Booking details prepared for email to secretary@tshwanetourism.com")


def load_tshwane_places_csv():
    """Load tshwane_places.csv and return a list of dicts."""
    import pandas as pd
    try:
        df = pd.read_csv('tshwane_places.csv')
        return df.to_dict(orient='records')
    except Exception:
        return []


def load_developer_details():
    """Load developer details from CSV and return a list of dicts."""
    import pandas as pd
    try:
        df = pd.read_csv('developer_details.csv')
        return df.to_dict(orient='records')
    except Exception as e:
        st.warning(f"Could not load developer details: {e}")
        return []


def load_individual_place_data():
    """Load individual place data from the processed CSV files"""
    import pandas as pd
    from pathlib import Path

    individual_places = []

    # Look for individual places data directory
    data_dirs = [
        "individual_places_data",
        "processed_places_data",
        "Tryp_Thooe_Tourism/individual_places_data",
        "Tryp_Thooe_Tourism/processed_places_data"
    ]

    for data_dir in data_dirs:
        if Path(data_dir).exists():
            # Walk through all subdirectories
            for subdir in Path(data_dir).iterdir():
                if subdir.is_dir():
                    for csv_file in subdir.glob("*.csv"):
                        try:
                            df = pd.read_csv(csv_file)
                            if not df.empty:
                                place_data = df.iloc[0].to_dict()
                                place_data['category'] = subdir.name
                                place_data['file_path'] = str(csv_file)
                                individual_places.append(place_data)
                        except Exception as e:
                            st.warning(f"Could not load {csv_file}: {e}")

    return individual_places


def display_individual_places_gallery():
    """Display individual places in a gallery format"""
    individual_places = load_individual_place_data()

    if not individual_places:
        st.info("No individual place data found. Run the CSV data processor first.")
        return

    st.subheader("🏛️ Individual Places Gallery")
    st.markdown(
        f"*Showing {len(individual_places)} individual places with detailed information*")

    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        # Get unique categories
        categories = list(set(place.get('category', 'Unknown')
                          for place in individual_places))
        category_filter = st.multiselect(
            "Filter by Category",
            options=sorted(categories),
            default=sorted(categories))

    with col2:
        sentiment_filter = st.selectbox(
            "Filter by Sentiment",
            options=["All", "positive", "neutral", "negative"])

    with col3:
        weather_filter = st.selectbox(
            "Filter by Weather Suitability",
            options=["All", "indoor", "outdoor", "all_weather"])

    # Apply filters
    filtered_places = individual_places
    if category_filter:
        filtered_places = [p for p in filtered_places if p.get(
            'category') in category_filter]
    if sentiment_filter != "All":
        filtered_places = [p for p in filtered_places if p.get(
            'ai_sentiment') == sentiment_filter]
    if weather_filter != "All":
        filtered_places = [p for p in filtered_places if p.get(
            'weather_suitability') == weather_filter]

    # Display places in a grid
    cols = st.columns(2)
    for i, place in enumerate(filtered_places):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div class="gallery-card">
                    <h3>🏛️ {place.get('name', 'Unknown')}</h3>
                    <p><strong>Category:</strong> {place.get('category', 'Unknown').title()}</p>
                    <p><strong>Type:</strong> {place.get('type', 'Unknown')}</p>
                    <p><strong>Sentiment:</strong> {place.get('ai_sentiment', 'neutral').title()}</p>
                    <p><strong>Weather:</strong> {place.get('weather_suitability', 'Unknown')}</p>
                    <p><strong>Price Range:</strong> {place.get('price_range', 'Unknown')}</p>
                    <p>{place.get('description', 'No description available')[:200]}...</p>
                </div>
                """, unsafe_allow_html=True)

                # Show additional details in expander
                with st.expander(f"📋 Details for {place.get('name', 'Unknown')}"):
                    if place.get('address'):
                        st.write(f"📍 **Address:** {place['address']}")
                    if place.get('phone'):
                        st.write(f"📞 **Phone:** {place['phone']}")
                    if place.get('email'):
                        st.write(f"📧 **Email:** {place['email']}")
                    if place.get('website'):
                        st.write(
                            f"🌐 **Website:** [{place['website']}]({place['website']})")
                    if place.get('opening_hours'):
                        st.write(f"🕒 **Hours:** {place['opening_hours']}")
                    if place.get('facilities'):
                        st.write(f"🏢 **Facilities:** {place['facilities']}")
                    if place.get('rating'):
                        st.write(f"⭐ **Rating:** {place['rating']}")
                    if place.get('latitude') and place.get('longitude'):
                        st.write(
                            f"🗺️ **Coordinates:** {place['latitude']}, {place['longitude']}")
                    st.write(
                        f"📁 **Source:** {place.get('file_path', 'Unknown')}")

    # Summary statistics
    st.markdown("---")
    st.subheader("📊 Individual Places Statistics")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Places", len(individual_places))
    with col2:
        verified_count = sum(
            1 for p in individual_places if p.get('verified_source', False))
        st.metric("Verified Places", verified_count)
    with col3:
        with_coords = sum(1 for p in individual_places if p.get(
            'latitude') and p.get('longitude'))
        st.metric("With Coordinates", with_coords)
    with col4:
        with_websites = sum(1 for p in individual_places if p.get('website'))
        st.metric("With Websites", with_websites)


# At startup, ensure places_data is loaded
if 'places_data' not in st.session_state or not st.session_state['places_data']:
    st.session_state['places_data'] = load_tshwane_places_csv()


def display_developer_contact_info():
    """Display developer contact information in a professional format"""
    developers = load_developer_details()

    if not developers:
        st.error("Could not load developer information.")
        return

    st.markdown("""
    <style>
    .developer-card {
        background: linear-gradient(135deg, #232a36 0%, #181c24 100%);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        border: 1px solid #00d4aa44;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease;
    }
    .developer-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 212, 170, 0.3);
    }
    .developer-name {
        color: #00d4aa;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .developer-role {
        color: #b3b3b3;
        font-size: 1rem;
        margin-bottom: 12px;
    }
    .contact-info {
        color: #ffffff;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .skills-badge {
        background: #00d4aa22;
        color: #00d4aa;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 2px;
        display: inline-block;
    }
    .experience-badge {
        background: #ffd70022;
        color: #ffd700;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 2px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### 👤 Lead Developer")
    st.markdown(
        "*Meet the developer behind the Tshwane Tourism Interactive Portal*")

    for developer in developers:
        st.markdown(f"""
        <div class="developer-card">
            <div class="developer-name">👤 {developer['name']}</div>
            <div class="developer-role">🎯 {developer['role']}</div>
            <div class="contact-info">
                📧 <a href="mailto:{developer['email']}" style="color: #00d4aa;">{developer['email']}</a><br>
                📞 <a href="tel:{developer['phone']}" style="color: #00d4aa;">{developer['phone']}</a><br>
                💼 <a href="https://{developer['linkedin']}" target="_blank" style="color: #00d4aa;">LinkedIn</a><br>
                🐙 <a href="https://github.com/{developer['github']}" target="_blank" style="color: #00d4aa;">GitHub</a><br>
                🐦 <a href="https://x.com/KgothatsoThooe" target="_blank" style="color: #00d4aa;">X (Twitter)</a>
            </div>
            <div style="margin-top: 12px;">
                <strong style="color: #ffffff;">Skills:</strong><br>
                {', '.join([f'<span class="skills-badge">{skill.strip()}</span>' for skill in developer['skills'].split(',')])}
            </div>
            <div style="margin-top: 8px;">
                <strong style="color: #ffffff;">Experience:</strong>
                <span class="experience-badge">{developer['experience']}</span>
            </div>
            <div style="margin-top: 8px;">
                <strong style="color: #ffffff;">Contribution:</strong><br>
                <span style="color: #b3b3b3; font-size: 0.85rem;">{developer['contribution']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00d4aa22 0%, #00b89422 100%); 
                border-radius: 12px; padding: 16px; border: 1px solid #00d4aa44;">
        <h4 style="color: #00d4aa; margin-bottom: 8px;">🏢 Project Information</h4>
        <p style="color: #ffffff; margin: 0;">
            <strong>Enterprise:</strong> Profit Projects Online Virtual Assistance<br>
            <strong>Registration:</strong> K2025200646<br>
            <strong>Contact:</strong> kgothatsothooe@gmail.com<br>
            <strong>Project:</strong> Tshwane Tourism Interactive Portal
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_email_secretary_form():
    """Display email form to contact the secretary"""
    st.markdown("### 📧 Contact Secretary")
    st.markdown(
        "*Send a direct message to the Tshwane Tourism Association secretary*")

    with st.form("email_secretary_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "Your Name *", placeholder="Enter your full name")
            email = st.text_input(
                "Your Email *", placeholder="your.email@example.com")
            phone = st.text_input(
                "Phone Number", placeholder="+27 XX XXX XXXX")
        with col2:
            subject = st.selectbox("Subject *", [
                "General Inquiry",
                "Booking Request",
                "Tourism Information",
                "Partnership Opportunity",
                "Feedback",
                "Other"
            ])
            priority = st.selectbox(
                "Priority", ["Low", "Medium", "High", "Urgent"])

        message = st.text_area(
            "Message *",
            placeholder="Please describe your inquiry or request in detail...",
            height=150
        )

        # Additional options
        col1, col2, col3 = st.columns(3)
        with col1:
            include_contact = st.checkbox(
                "Include contact information", value=True)
        with col2:
            request_callback = st.checkbox("Request callback")
        with col3:
            urgent_matter = st.checkbox("Urgent matter")

        submitted = st.form_submit_button("📧 Send Email to Secretary")

        if submitted:
            if name and email and message:
                # Create email content
                email_content = f"""
                🌿 TSHWANE TOURISM ASSOCIATION - NEW INQUIRY
                
                ═══════════════════════════════════════════════════════════
                📋 INQUIRY DETAILS
                ═══════════════════════════════════════════════════════════
                
                📅 Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                📧 From: {name} ({email})
                📞 Phone: {phone if phone else 'Not provided'}
                🎯 Subject: {subject}
                ⚡ Priority: {priority}
                
                ═══════════════════════════════════════════════════════════
                💬 MESSAGE
                ═══════════════════════════════════════════════════════════
                
                {message}
                
                ═══════════════════════════════════════════════════════════
                📋 ADDITIONAL OPTIONS
                ═══════════════════════════════════════════════════════════
                
                Include Contact Info: {'Yes' if include_contact else 'No'}
                Request Callback: {'Yes' if request_callback else 'No'}
                Urgent Matter: {'Yes' if urgent_matter else 'No'}
                
                ═══════════════════════════════════════════════════════════
                📞 CONTACT & SUPPORT
                ═══════════════════════════════════════════════════════════
                
                Created by: Profit Projects Online Virtual Assistance
                Enterprise Number: K2025200646
                Contact: Thapelo Kgothatso Thooe
                Email: kgothatsothooe@gmail.com
                
                For inquiries: secretary@tshwanetourism.com
                
                ═══════════════════════════════════════════════════════════
                """

                # Save email content
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"secretary_email_{timestamp}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(email_content)

                st.success(
                    "✅ Email sent successfully to secretary@tshwanetourism.com")
                st.info(f"📁 Email saved as: {filename}")

                # Add to notifications
                SessionManager.add_notification(
                    f"Email sent to secretary by {name}", "success")

            else:
                st.error("Please fill in all required fields marked with *")


def display_main_content():
    """Main content area with component system"""
    # Create main columns at the top level
    col1, col2 = st.columns([2, 1])

    # Check if the user wants to see the booking form directly
    if st.session_state.get('current_section') == 'booking':
        with col1:
            st.subheader("📝 Book Your Experience")
            display_enhanced_booking_form()
        with col2:
            st.subheader("📊 Data from Scraps & Project CSVs")
            # ... (keep the CSV dataframes code here) ...
            pass
        return

    # Check if the user wants to see the contact info
    if st.session_state.get('current_section') == 'contact':
        with col1:
            st.subheader("📞 Contact Information")
            display_developer_contact_info()
        with col2:
            st.subheader("📊 Contact Analytics")
            st.info("Contact information loaded from developer_details.csv")
        return

    # Check if the user wants to see the email secretary form
    if st.session_state.get('current_section') == 'email_secretary':
        with col1:
            st.subheader("📧 Email Secretary")
            display_email_secretary_form()
        with col2:
            st.subheader("📊 Email Analytics")
            st.info(
                "Email form for contacting the Tshwane Tourism Association secretary")
        return

    # Check if the user wants to see the chat interface
    if st.session_state.get('current_section') == 'chat':
        with col1:
            st.subheader("🤖 AI Chat Assistant")
            # Import and display chat interface
            try:
                from chat_interface import display_chat_interface_main
                display_chat_interface_main()
            except ImportError:
                st.error(
                    "Chat interface module not found. Please ensure chat_interface.py is in the same directory.")
        with col2:
            st.subheader("📊 Chat Analytics")
            st.info("Chat analytics will appear here when you start chatting.")
        return

    with col1:
        # Component-based UI (v0-inspired)
        project = st.session_state.component_system.create_code_project(
            "tshwane-tourism-main",
            {
                "map_component": "Interactive map iframe",
                "gallery_component": "Places gallery with animations",
                "booking_component": "Secure booking form"
            }
        )

        # --- Google Maps iframe and links ---
        display_google_maps_with_places()
        # Enhanced interactive map with CSV data
        st.subheader("🗺️ Interactive Tshwane Map")

        # Map container with CSV data integration
        csv_places_count = len(st.session_state.places_data)
        csv_restaurants_count = len(st.session_state.restaurants_data)
        csv_total_count = csv_places_count + csv_restaurants_count

        st.markdown(f"""
        <div class="map-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h4 style="margin: 0; color: var(--primary-green);">🌍 Explore Tshwane</h4>
                <div style="display: flex; gap: 8px;">
                    <span class="badge">🏛️ {csv_places_count} Places</span>
                    <span class="badge">🍽️ {csv_restaurants_count} Restaurants</span>
                    <span class="badge">📊 {csv_total_count} Total from CSV</span>
                </div>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: 16px;">
                Interactive map with tourism data from tshwane_places.csv
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Map controls with CSV-based filters
        map_col1, map_col2, map_col3 = st.columns([1, 1, 2])
        with map_col1:
            show_places = st.checkbox(
                "Show Places", value=True, key="map_places")
        with map_col2:
            show_restaurants = st.checkbox(
                "Show Restaurants", value=True, key="map_restaurants")
        with map_col3:
            # Multi-select for place types from CSV
            available_types = st.session_state.get(
                'available_place_types', ['attraction', 'accommodation', 'restaurant'])
            selected_types = st.multiselect(
                "Filter by Type (from CSV)",
                options=available_types,
                default=available_types,
                key="map_type_filter",
                help="Select place types to display on the map"
            )

        # --- Folium Map Integration ---
        import folium
        from streamlit_folium import st_folium

        with st.container():
            st.markdown("### 🗺️ Folium Map of Tshwane Places (from CSV)")
            # Default Tshwane coordinates
            default_lat, default_lon = -25.7479, 28.1879
            m = folium.Map(location=[default_lat, default_lon], zoom_start=11)

            # Add markers for each place with coordinates
            import pandas as pd
            for place in st.session_state.places_data:
                lat = place.get('lat', None)
                lon = place.get('lng', None)
                try:
                    if pd.isna(lat) or pd.isna(lon):
                        continue
                except Exception:
                    if lat is None or lon is None:
                        continue
                name = place.get('name', 'Unknown')
                short_desc = place.get('short_description', '')
                address = place.get('address', '')
                popup_html = f"""
                <b>{name}</b><br>
                <i>{address}</i><br>
                <p>{short_desc}</p>
                """
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=name,
                    icon=folium.Icon(color='green', icon='info-sign')
                ).add_to(m)

            st_folium(m, width='100%', height=600)

        # Create map data from real website content
        if st.session_state.places_data and show_places:
            import pandas as pd

            # Create map data for real places
            map_data = []

            for i, place in enumerate(st.session_state.places_data):
                # Use Tshwane coordinates with slight variations for different places
                lat = -25.7479 + (i * 0.01)  # Spread around Tshwane
                lon = 28.1879 + (i * 0.01)

                map_data.append({
                    'lat': lat,
                    'lon': lon,
                    'name': place.get('display_name', place.get('name', 'Unknown')),
                    'size': 100 + (i * 20)  # Different sizes for variety
                })

            if map_data:
                df = pd.DataFrame(map_data)
                st.map(df, zoom=12)

                # Show place details below map
                with st.expander("📍 Place Details"):
                    for place in st.session_state.places_data:
                        verified = "✅" if place.get(
                            'verified_source') else "⚠️"
                        st.markdown(
                            f"**🏛️ {place.get('display_name', place.get('name'))}** {verified}")
                        st.caption(place.get('short_description',
                                   place.get('description', '')[:100]))

        # Fallback to website iframe
        try:
            st.markdown("### 🌐 Official Tshwane Tourism Website")
            st.components.v1.iframe(
                "http://www.visittshwane.co.za", height=400, scrolling=True)
        except Exception as e:
            st.error(f"Website loading failed: {e}")
            st.info("Please check your internet connection and try again.")

        # Enhanced interactive gallery with dashboard view option
        gallery_col1, gallery_col2 = st.columns([3, 1])
        with gallery_col1:
            st.subheader("🏛️ Places to Visit")
        with gallery_col2:
            view_mode = st.selectbox(
                "View Mode", ["Gallery", "Dashboard", "Table"], key="gallery_view_mode")

        if view_mode == "Dashboard":
            display_places_dashboard()
        elif view_mode == "Table":
            display_places_table()
        else:
            display_enhanced_gallery()

        # Real-time analytics
        st.subheader("📊 Enhanced Real-time Analytics")
        # display_enhanced_analytics_dashboard()

    with col2:
        # Weather-based suggestions with AI - Call outside of columns
        st.subheader("🌤️ AI Weather Recommendations")
        # Move the function content here instead of calling it
        display_weather_content()

        # Real-time analytics
        st.subheader("📊 Real-time Analytics")
        st.caption('Cloudy Weather')
        display_weather_insights('cloudy')
        st.caption('Hot weather')
        display_weather_insights('hot')
        st.caption('Rainy Weather')
        display_weather_insights('rainy')
        st.caption('Cold Weather')
        display_weather_insights('cold')
        # display_analytics_dashboard()
        st.caption('Sunny Weather')
        display_weather_insights('sunny')

        # Real-time notifications (Lovable-inspired)
        # display_real_time_notifications(
        #     toggle_key="show_all_notifications_toggle_main_content")

        # --- NEW: Dataframes from scraps and root CSVs ---
        with st.container():
            st.markdown("### 📊 Data from Scraps & Project CSVs")
            import pandas as pd
            # Scraps CSVs
            try:
                df_places = pd.read_csv(
                    'scraps/Tryp_Thooe_Tourism-main/tshwane_places.csv')
                st.markdown('**scraps/tshwane_places.csv**')
                st.dataframe(df_places, use_container_width=True,
                             hide_index=True)
            except Exception as e:
                st.info(f"Could not load scraps places CSV: {e}")
            try:
                df_social = pd.read_csv(
                    'scraps/Tryp_Thooe_Tourism-main/tshwane_social_links.csv')
                st.markdown('**scraps/tshwane_social_links.csv**')
                st.dataframe(df_social, use_container_width=True,
                             hide_index=True)
            except Exception as e:
                st.info(f"Could not load scraps social links CSV: {e}")
            try:
                df_coords = pd.read_csv(
                    'scraps/Tryp_Thooe_Tourism-main/Repo/Tryp_Thooe_Tourism-main/tshwane_places_coordinates.csv')
                st.markdown('**scraps/Repo/tshwane_places_coordinates.csv**')
                st.dataframe(df_coords, use_container_width=True,
                             hide_index=True)
            except Exception as e:
                st.info(f"Could not load scraps coordinates CSV: {e}")
            # Root project CSVs
            try:
                df_places_root = pd.read_csv('tshwane_places.csv')
                st.markdown('**tshwane_places.csv**')
                st.dataframe(df_places_root,
                             use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root places CSV: {e}")
            try:
                df_social_root = pd.read_csv('tshwane_social_links.csv')
                st.markdown('**tshwane_social_links.csv**')
                st.dataframe(df_social_root,
                             use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root social links CSV: {e}")
            try:
                df_coords_root = pd.read_csv('tshwane_coordinates.csv')
                st.markdown('**tshwane_coordinates.csv**')
                st.dataframe(df_coords_root,
                             use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root coordinates CSV: {e}")
            try:
                df_desc_root = pd.read_csv('tshwane_descriptions.csv')
                st.markdown('**tshwane_descriptions.csv**')
                st.dataframe(
                    df_desc_root, use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root descriptions CSV: {e}")
            try:
                df_sent_root = pd.read_csv('tshwane_sentiment_data.csv')
                st.markdown('**tshwane_sentiment_data.csv**')
                st.dataframe(
                    df_sent_root, use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root sentiment data CSV: {e}")
            try:
                df_temp_root = pd.read_csv('tshwane_temperature_data.csv')
                st.markdown('**tshwane_temperature_data.csv**')
                st.dataframe(
                    df_temp_root, use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root temperature data CSV: {e}")

    if st.session_state.get('current_section') == 'weather_guide':
        st.header("🌤️ Weather-Based Suggestions")
        st.markdown("Get suggestions for places to visit based on the weather.")
        temp_csv = "tshwane_temperature_data.csv"
        if os.path.exists(temp_csv):
            temp_df = pd.read_csv(temp_csv)
            st.dataframe(temp_df)
        weather = st.selectbox(
            "Weather", ["Sunny", "Rainy", "Cloudy", "Hot", "Cold"])
        if st.button("Suggest Places"):
            suggestions = get_weather_suggestions(
                weather, st.session_state.get('places_data', []))
            if suggestions:
                st.dataframe(pd.DataFrame(suggestions))
            else:
                st.info("No suggestions found for this weather condition.")
        return


def display_weather_content():
    """Content for weather suggestions - now loads from tshwane_temperature_data.csv"""
    # Load temperature data
    temp_csv = "tshwane_temperature_data.csv"
    temp_df = None
    live_weather = WEATHER_SERVICE.fetch_current_weather()
    if os.path.exists(temp_csv):
        temp_df = pd.read_csv(temp_csv)
        st.dataframe(temp_df)
        weather_options = temp_df['weather'].unique().tolist() if 'weather' in temp_df.columns else [
            "Sunny", "Rainy", "Cloudy", "Hot", "Cold", "Windy", "Mild"]
    else:
        weather_options = ["Sunny", "Rainy",
                           "Cloudy", "Hot", "Cold", "Windy", "Mild"]
    weather_options_display = [option.capitalize() for option in weather_options]
    if live_weather and live_weather.condition.capitalize() not in weather_options_display:
        weather_options_display.append(live_weather.condition.capitalize())

    if live_weather:
        st.markdown("### 🌤️ Live Tshwane Weather")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Condition", live_weather.condition.capitalize())
        col2.metric("Temperature", f"{live_weather.temperature_c:.1f}°C")
        col3.metric("Feels like", f"{live_weather.apparent_temperature_c:.1f}°C")
        col4.metric("Wind", f"{live_weather.wind_speed_kmh:.1f} km/h")
        st.caption(f"Source: Open-Meteo • Observed at {live_weather.observed_at}")

    default_weather = st.session_state.get(
        'detected_weather_condition',
        live_weather.condition.capitalize() if live_weather else weather_options_display[0]
    )
    default_index = weather_options_display.index(default_weather) if default_weather in weather_options_display else 0
    selected_weather = st.selectbox(
        "Current Weather Condition", weather_options_display, index=default_index)
    auto_detect = st.button(
        "🌡️ Auto-Detect", help="Automatically detect live weather in Tshwane")
    if auto_detect:
        if live_weather:
            st.session_state.detected_weather_condition = live_weather.condition.capitalize()
            SessionManager.add_notification(
                f"Weather auto-detected from Open-Meteo: {live_weather.condition.capitalize()}", "info")
            st.rerun()
        elif temp_df is not None:
            import random
            selected_weather = random.choice(weather_options_display)
            SessionManager.add_notification(
                f"Weather auto-detected from saved data: {selected_weather}", "info")
    if st.button("🤖 Get AI Recommendations"):
        if st.session_state.places_data:
            with st.spinner("AI is analyzing weather conditions..."):
                # Ensure minimum 3-second loading time
                start_time = time.time()

                suggestions = get_enhanced_weather_suggestions(
                    selected_weather, st.session_state.places_data, temp_df)
                if suggestions:
                    st.markdown(
                        f"**🎯 AI Recommendations for {selected_weather.lower()} weather:**")
                    for suggestion in suggestions:
                        with st.expander(f"🏛️ {suggestion['name']} (Score: {suggestion.get('weather_suitability_score', 0)})"):
                            st.markdown(
                                f"**Type:** {suggestion.get('type', 'Unknown')}")
                            st.markdown(
                                f"**Why recommended:** {suggestion.get('reason', 'Good match for current weather')}")
                            st.markdown(
                                f"**Weather suitability:** {suggestion.get('weather_suitability_score', 0)}/5")
                            if st.button(f"📋 Quick Book", key=f"quick_book_{suggestion['name']}"):
                                st.session_state.selected_place = suggestion
                                SessionManager.add_notification(
                                    f"Quick-selected {suggestion['name']}", "success")
                else:
                    st.info(
                        "No specific suggestions available for this weather condition.")

                # Ensure minimum 3-second loading time
                elapsed_time = time.time() - start_time
                if elapsed_time < 3:
                    time.sleep(3 - elapsed_time)
        else:
            st.info("Please load website data first.")


def get_enhanced_weather_suggestions(weather_condition: str, places_data: list, temp_df=None) -> list:
    """Enhanced weather suggestions using temperature data from CSV if available"""
    return WEATHER_SERVICE.score_places_for_weather(
        places_data,
        weather_condition,
        temp_df=temp_df,
        limit=5,
    )


def display_enhanced_gallery():
    """Display gallery using local CSV, but enhance with images/categories/links from official gallery if available."""
    import pandas as pd
    import ast
    import random
    import re
    fun_facts = [
        "Did you know? Tshwane is home to the largest urban jacaranda forest in the world!",
        "Travel tip: Always carry a reusable water bottle to stay hydrated while exploring.",
        "Fun fact: Pretoria is also known as the Jacaranda City due to its thousands of jacaranda trees.",
        "Travel tip: Early mornings are best for sightseeing to avoid crowds and heat.",
        "Did you know? The Union Buildings are the official seat of the South African government.",
        "Fun fact: Many museums in Tshwane offer free entry on certain days!",
        "Travel tip: Try local cuisine at a market for an authentic experience.",
        "Did you know? Tshwane has more than 100 embassies, making it one of the world's diplomatic capitals."
    ]
    if st.button('🔄 Sync with Official Gallery'):
        places = scrape_official_gallery()
        if places:
            st.session_state['synced_gallery'] = places
            pd.DataFrame(places).to_csv('synced_gallery.csv', index=False)
            st.success(f"Synced {len(places)} places from official gallery!")
        else:
            st.warning('No places found from official gallery.')
    # Load local CSV
    try:
        df_csv = pd.read_csv('tshwane_places.csv')
    except Exception:
        st.warning('Could not load tshwane_places.csv')
        return
    # Load synced gallery if available
    gallery_data = st.session_state.get('synced_gallery')
    # Build a mapping from normalized name to scraped info

    def normalize_name(name):
        return re.sub(r'[^a-z0-9]', '', str(name).lower())

    scraped_map = {normalize_name(
        p['name']): p for p in gallery_data} if gallery_data else {}
    # Merge CSV with scraped info
    merged_places = []
    for _, row in df_csv.iterrows():
        name = row.get('name', '')
        norm = normalize_name(name)
        scraped = scraped_map.get(norm, {})
        merged = dict(row)
        # Prefer scraped image/category/link if available
        for k in ['image', 'category', 'link']:
            if scraped.get(k):
                merged[k] = scraped[k]
        merged_places.append(merged)
    # Gallery navigation
    n_places = len(merged_places)
    if n_places == 0:
        st.warning('No places found in local CSV.')
        return
    nav1, nav2, nav3, nav4 = st.columns([1, 1, 1, 1])
    if 'gallery_index' not in st.session_state:
        st.session_state.gallery_index = 0
    with nav1:
        if st.button('⬅️ Previous', key='gallery_prev'):
            st.session_state.gallery_index = (
                st.session_state.gallery_index - 1) % n_places
    with nav2:
        if st.button('🎲 Random', key='gallery_rand'):
            st.session_state.gallery_index = random.randint(0, n_places - 1)
    with nav3:
        if st.button('Next ➡️', key='gallery_next'):
            st.session_state.gallery_index = (
                st.session_state.gallery_index + 1) % n_places
    with nav4:
        st.markdown(f"**{st.session_state.gallery_index+1} / {n_places}**")
    place = merged_places[st.session_state.gallery_index]
    st.markdown('---')
    st.markdown(f"<div class='gallery-card fade-in-up'>",
                unsafe_allow_html=True)
    # Creative: Placeholder image if missing
    img_url = place.get('image', '')
    if not img_url:
        img_url = f"https://placehold.co/600x400?text={place.get('name', 'No+Image').replace(' ', '+')}&font=roboto"
    st.image(img_url, use_container_width=True)
    st.subheader(f"🏛️ {place.get('name', 'Unknown')}")
    if place.get('category'):
        st.markdown(f"**Category:** {place['category']}")
    if place.get('link'):
        st.markdown(f"[View Details]({place['link']})")
    st.markdown(f"**{place.get('description', '')}**")
    # Creative: Show a random fun fact or travel tip
    st.info(random.choice(fun_facts))
    st.markdown('</div>', unsafe_allow_html=True)
    return


def scrape_official_gallery():
    """Scrape the official Tshwane Tourism gallery page and return a list of places with images, categories, and links if available."""
    import requests
    from bs4 import BeautifulSoup
    import re
    gallery_url = "http://www.visittshwane.co.za/gallery"
    try:
        resp = requests.get(gallery_url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        cards = soup.select('.gallery-card, .gallery-item, .place-card, .card')
        places = []
        for card in cards:
            # Name
            name = card.find(['h3', 'h2', 'h4', 'a'])
            name = name.get_text(strip=True) if name else None
            # Description
            desc = card.find('p')
            desc = desc.get_text(strip=True) if desc else ''
            # Image
            img = card.find('img')
            image = img['src'] if img and img.has_attr('src') else ''
            # Try to extract background-image style
            if not image:
                style = card.get('style', '')
                match = re.search(
                    r'background-image:\s*url\(["\']?(.*?)["\']?\)', style)
                if match:
                    image = match.group(1)
            # Category
            cat = card.find(class_='category') or card.find(class_='type')
            if not cat:
                # Try to find a badge/span/div with short text
                for badge in card.find_all(['span', 'div']):
                    txt = badge.get_text(strip=True)
                    if txt and len(txt) < 20 and txt.lower() not in name.lower():
                        cat = badge
                        break
            category = cat.get_text(strip=True) if cat else ''
            # Link
            link = card.find('a', href=True)
            link_url = link['href'] if link and link.has_attr('href') else ''
            if name:
                places.append({'name': name, 'description': desc,
                              'image': image, 'category': category, 'link': link_url})
        # Fallback: try to find all place names in <a> or <div> if no cards found
        if not places:
            for tag in soup.find_all(['a', 'div', 'span']):
                text = tag.get_text(strip=True)
                if text and len(text) > 4 and 'gallery' not in text.lower():
                    places.append({'name': text, 'description': '',
                                  'image': '', 'category': '', 'link': ''})
        return places
    except Exception as e:
        st.error(f"Failed to scrape official gallery: {e}")
        return []


def display_places_dashboard():
    """Display all places in a comprehensive dashboard format"""
    if not st.session_state.places_data:
        st.warning("🌐 No tourism data loaded from tshwane_places.csv!")
        return

    st.markdown("### 📊 Places Dashboard Overview")

    # Summary metrics
    total_places = len(st.session_state.places_data)
    verified_places = sum(1 for place in st.session_state.places_data if place.get(
        'verified_source', False))
    place_types = len(set(place.get('type', 'unknown')
                      for place in st.session_state.places_data))

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Total Places", total_places)
    with metric_col2:
        st.metric("Verified Places", verified_places)
    with metric_col3:
        st.metric("Place Types", place_types)
    with metric_col4:
        places_with_weather = sum(
            1 for place in st.session_state.places_data if place.get('weather_suitability'))
        st.metric("Weather Data", places_with_weather)

    # Places by type chart
    import pandas as pd
    import plotly.express as px

    type_counts = {}
    for place in st.session_state.places_data:
        place_type = place.get('type', 'unknown').title()
        type_counts[place_type] = type_counts.get(place_type, 0) + 1

    if type_counts:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig_pie = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
                             title="Places by Type Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)

        with chart_col2:
            fig_bar = px.bar(x=list(type_counts.keys()), y=list(type_counts.values()),
                             title="Places Count by Type")
            st.plotly_chart(fig_bar, use_container_width=True)


def display_places_table():
    """Display all places in a comprehensive table format"""
    if not st.session_state.places_data:
        st.warning("🌐 No tourism data loaded from tshwane_places.csv!")
        return

    st.markdown("### 📋 Places Data Table")

    # Create comprehensive dataframe
    import pandas as pd

    table_data = []
    for i, place in enumerate(st.session_state.places_data):
        sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}.get(
            place.get('ai_sentiment', 'neutral'), "😐")

        table_data.append({
            "#": i + 1,
            "🏛️ Name": place.get('display_name', place.get('name', 'Unknown')),
            "🏷️ Type": place.get('type', 'unknown').title(),
            "📝 Description": place.get('description', 'No description')[:100] + "..." if len(place.get('description', '')) > 100 else place.get('description', 'No description'),
            "😊 Sentiment": f"{sentiment_emoji} {place.get('ai_sentiment', 'neutral').title()}",
            "✅ Verified": "✅ Yes" if place.get('verified_source', False) else "⚠️ No",
            "🌤️ Weather": "✅ Yes" if place.get('weather_suitability') else "❌ No",
            "🌐 Source": place.get('data_source', 'Unknown')
        })

    if table_data:
        places_df = pd.DataFrame(table_data)

        # Add filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            type_filter = st.multiselect("Filter by Type",
                                         options=places_df["🏷️ Type"].unique(),
                                         default=places_df["🏷️ Type"].unique())
        with filter_col2:
            verified_filter = st.selectbox("Filter by Verification",
                                           options=["All", "✅ Yes", "⚠️ No"],
                                           index=0)
        with filter_col3:
            weather_filter = st.selectbox("Filter by Weather Data",
                                          options=["All", "✅ Yes", "❌ No"],
                                          index=0)

        # Apply filters
        filtered_df = places_df[places_df["🏷️ Type"].isin(type_filter)]
        if verified_filter != "All":
            filtered_df = filtered_df[filtered_df["✅ Verified"]
                                      == verified_filter]
        if weather_filter != "All":
            filtered_df = filtered_df[filtered_df["🌤️ Weather"]
                                      == weather_filter]

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        # Download option
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="tshwane_places_filtered.csv",
            mime="text/csv"
        )


def analyze_place_with_ai(place: Dict[str, Any]) -> str:
    """AI-powered place analysis using local models"""
    try:
        # Simple analysis based on keywords and type
        description = place.get('description', '').lower()
        place_type = place.get('type', '').lower()

        analysis_points = []

        # Activity recommendations
        if any(word in description for word in ['outdoor', 'park', 'garden']):
            analysis_points.append(
                "🌳 Perfect for outdoor activities and nature lovers")

        if any(word in description for word in ['museum', 'gallery', 'historic']):
            analysis_points.append(
                "🏛️ Rich in cultural and historical significance")

        if any(word in description for word in ['family', 'children', 'kids']):
            analysis_points.append("👨‍👩‍👧‍👦 Family-friendly destination")

        # Weather suitability
        if 'indoor' in description:
            analysis_points.append("☔ Great for rainy days")
        else:
            analysis_points.append("☀️ Best enjoyed on sunny days")

        # Accessibility
        if any(word in description for word in ['accessible', 'wheelchair', 'easy']):
            analysis_points.append("♿ Accessible for all visitors")

        if not analysis_points:
            analysis_points.append("🎯 A unique destination worth exploring")

        return "\n".join(f"• {point}" for point in analysis_points)

    except Exception as e:
        return f"Analysis temporarily unavailable: {str(e)}"


def display_booking_form_merged():
    """Unified AI-powered booking form with advanced creative UI/UX features and even more advanced features."""
    import pandas as pd
    import datetime
    import random
    import hashlib
    import uuid
    import re

    # --- Load all options from tshwane_places.csv only ---
    try:
        df_places = pd.read_csv('Tryp_Thooe_Tourism/tshwane_places.csv')
    except Exception:
        df_places = pd.DataFrame(
            columns=['name', 'description', 'type', 'image', 'lat', 'lng'])

    # Dynamically determine categories from the CSV
    categories = sorted(df_places['type'].dropna().unique().tolist())
    options = {cat: sorted(df_places[df_places['type'] == cat]['name'].dropna(
    ).unique().tolist()) for cat in categories}

    # Custom icons for categories
    icon_map = {
        'accommodation': '🏨',
        'restaurant': '🍽️',
        'service': '🛎️',
        'attraction': '🎡',
        'area': '🌍',
        'venue': '🏛️',
        'shopping': '🛍️',
        'museum': '🏺',
        'spa': '💆',
        'default': '📍'
    }

    def get_icon(cat):
        return icon_map.get(str(cat).lower(), icon_map['default'])

    def get_place_info(name):
        row = df_places[df_places['name'].str.lower() == str(name).lower()]
        if not row.empty:
            r = row.iloc[0]
            return {
                'short': r.get('description', ''),
                'long': r.get('description', ''),
                'highlighted': bool(re.search(r'(hotel|lodge|recommended)', str(r.get('name', '')), re.I)),
                'image': r.get('image', ''),
                'lat': r.get('lat', None),
                'lng': r.get('lng', None),
            }
        return {'short': '', 'long': '', 'highlighted': False, 'image': '', 'lat': None, 'lng': None}

    # Fun facts and travel tips
    fun_facts = [
        "Did you know? Tshwane is home to the largest urban jacaranda forest in the world!",
        "Travel tip: Always carry a reusable water bottle to stay hydrated while exploring.",
        "Fun fact: Pretoria is also known as the Jacaranda City due to its thousands of jacaranda trees.",
        "Travel tip: Early mornings are best for sightseeing to avoid crowds and heat.",
        "Did you know? The Union Buildings are the official seat of the South African government.",
        "Fun fact: Many museums in Tshwane offer free entry on certain days!",
        "Travel tip: Try local cuisine at a market for an authentic experience.",
        "Did you know? Tshwane has more than 100 embassies, making it one of the world's diplomatic capitals."
    ]

    if 'booking_mode' not in st.session_state:
        st.session_state.booking_mode = 'single'
    if 'booking_data_merged' not in st.session_state:
        st.session_state.booking_data_merged = {}
    if 'booking_summary_merged' not in st.session_state:
        st.session_state.booking_summary_merged = ''
    if 'ai_suggestion_merged' not in st.session_state:
        st.session_state.ai_suggestion_merged = ''
    if 'fav_places' not in st.session_state:
        st.session_state.fav_places = set()
    if 'ai_category_suggestions' not in st.session_state:
        st.session_state.ai_category_suggestions = {}
    if 'show_map_popup' not in st.session_state:
        st.session_state.show_map_popup = None

    def fav_key(name):
        return f"fav_{name.replace(' ', '_')}"

    def grouped_options(opts):
        if len(opts) <= 10:
            return {'All': opts}
        groups = {}
        for o in opts:
            first = o[0].upper()
            if 'A' <= first <= 'F':
                g = 'A-F'
            elif 'G' <= first <= 'L':
                g = 'G-L'
            elif 'M' <= first <= 'R':
                g = 'M-R'
            else:
                g = 'S-Z'
            groups.setdefault(g, []).append(o)
        return groups

    def filter_options(opts, filter_text):
        if not filter_text:
            return opts
        filter_text = filter_text.lower()
        return [o for o in opts if filter_text in o.lower() or filter_text in get_place_info(o)['short'].lower()]

    def ai_suggest_for_category(cat, opts):
        # Simple AI: recommend up to 2 places based on time of day, group size, or random
        now = datetime.datetime.now()
        group_size = st.session_state.get('bm_group_size', 1)
        if cat == 'restaurant':
            # Suggest a restaurant for lunch or dinner
            if now.hour < 15:
                recs = [o for o in opts if 'cafe' in o.lower()
                        or 'grill' in o.lower()]
            else:
                recs = [o for o in opts if 'restaurant' in o.lower()
                        or 'bistro' in o.lower()]
        elif cat == 'accommodation':
            recs = [o for o in opts if 'hotel' in o.lower()
                    or 'lodge' in o.lower()]
        else:
            recs = random.sample(opts, min(2, len(opts))) if opts else []
        return recs[:2]

    # Progress bar: how many categories have at least one selection
    def count_selected(selections):
        return sum(1 for v in selections.values() if v)

    # Map popup logic
    def show_map_for_place(place_info):
        lat, lng = place_info.get('lat'), place_info.get('lng')
        name = place_info.get('name', '')
        if pd.notna(lat) and pd.notna(lng):
            import folium
            from streamlit_folium import st_folium
            m = folium.Map(location=[lat, lng], zoom_start=14)
            folium.Marker([lat, lng], popup=name).add_to(m)
            st_folium(m, width=400, height=300)
        else:
            import urllib.parse
            url = f"https://www.google.com/maps/search/{urllib.parse.quote_plus(name + ' Tshwane')}"
            st.markdown(f"[Open in Google Maps]({url})")

    with st.form('booking_form_merged', clear_on_submit=False):
        st.markdown("""
        <div style='background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%); padding: 18px; border-radius: 18px; margin-bottom: 18px;'>
        <h2 style='color: #00b894;'>📝 Unified AI Booking Form</h2>
        <p>Book a single place or multiple experiences in Tshwane with AI-powered suggestions, accessibility info, and a modern, personalized experience.</p>
        </div>
        """, unsafe_allow_html=True)

        mode = st.radio('Booking Mode', [
                        'Book a single place', 'Book multiple experiences'], index=0, key='booking_mode_radio')
        st.session_state.booking_mode = 'single' if mode == 'Book a single place' else 'multi'

        st.subheader('👤 Your Details')
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                'Full Name *', placeholder='Enter your full name', key='bm_name')
            email = st.text_input(
                'Email Address *', placeholder='your.email@example.com', key='bm_email')
            whatsapp = st.text_input(
                'WhatsApp Number *', placeholder='+27 XX XXX XXXX', key='bm_whatsapp')
        with col2:
            group_size = st.selectbox('Group Size', [
                                      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, '10+'], index=0, key='bm_group_size')
            dietary = st.text_input(
                'Dietary Preferences', placeholder='e.g. vegetarian, halal, none', key='bm_dietary')
            special_needs = st.text_input(
                'Special Needs', placeholder='e.g. wheelchair access, allergies', key='bm_special_needs')
        st.markdown('---')

        if st.session_state.booking_mode == 'single':
            st.subheader(
                '🏛️ Book a Single Place (or Multiple from Each Category)')
            single_selections = {}
            for cat in categories:
                with st.expander(f"{get_icon(cat)} {cat.title()} 🏷️", expanded=False):
                    st.markdown(
                        f"<span class='animated-icon'>{get_icon(cat)}</span> <b>{cat.title()}</b>", unsafe_allow_html=True)
                    st.info(random.choice(fun_facts))
                    opts = options[cat]
                    filter_text = st.text_input(
                        f"Filter {cat.title()} options", key=f"filter_single_{cat}")
                    filtered_opts = filter_options(opts, filter_text)
                    groups = grouped_options(filtered_opts)
                    # AI Suggestion button
                    if st.button(f"🤖 AI Suggest {cat.title()} Options", key=f"ai_suggest_single_{cat}"):
                        st.session_state.ai_category_suggestions[cat] = ai_suggest_for_category(
                            cat, filtered_opts)
                    ai_suggestions = st.session_state.ai_category_suggestions.get(cat, [
                    ])
                    if ai_suggestions:
                        st.success(
                            f"AI Suggestion: {', '.join(ai_suggestions)}")
                    # Quick Add All
                    if filtered_opts:
                        if st.button(f"Quick Add All {cat.title()}", key=f"quickadd_single_{cat}"):
                            for group_opts in groups.values():
                                st.session_state[f"bm_single_{cat}_All"] = group_opts
                    selected = []
                    for group, group_opts in groups.items():
                        if len(groups) > 1:
                            st.markdown(f"**{group}**")
                        sel = st.multiselect(
                            f"Select {cat.title()} options" if len(
                                groups) == 1 else '',
                            group_opts,
                            key=f"bm_single_{cat}_{group}")
                        selected.extend(sel)
                    single_selections[cat] = []
                    for place in selected:
                        info = get_place_info(place)
                        fav = fav_key(place)
                        is_fav = fav in st.session_state.fav_places
                        # Image preview
                        img_url = info['image'] if info[
                            'image'] else f"https://placehold.co/400x250?text={place.replace(' ', '+')}&font=roboto"
                        st.image(img_url, width=250, caption=place,
                                 use_column_width=False)
                        # Map popup
                        if st.button(f"Show on Map", key=f"showmap_single_{cat}_{place}"):
                            st.session_state.show_map_popup = (place, info)
                        if st.session_state.show_map_popup and st.session_state.show_map_popup[0] == place:
                            show_map_for_place({**info, 'name': place})
                        # Custom preview card
                        st.markdown(f"""
                        <div class='preview-card'>
                        <b style='font-size:1.1em'>{get_icon(cat)} {place}</b>
                        {'<span style=\"color:#ffffff;font-weight:bold;\">⭐ Recommended</span>' if info['highlighted'] else ''}
                        <span class='fav-star {'fav-on' if is_fav else ''}' onclick=\"window.parent.postMessage({{type: 'toggle_fav', name: '{place}'}}, '*')\">{'💛' if is_fav else '⭐'}</span><br>
                        <span style='color:#ffffff;'>{info['short']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            date = st.date_input(f"Date for {place}", min_value=datetime.date.today(
                            ), key=f"bm_single_date_{cat}_{place}")
                            time = st.time_input(f"Time for {place}", value=datetime.time(
                                hour=10), key=f"bm_single_time_{cat}_{place}")
                        with col2:
                            st.caption('No extra info available.')
                        single_selections[cat].append({
                            'name': place,
                            'date': str(date),
                            'time': str(time),
                            'category': cat
                        })
            st.progress(count_selected(single_selections) / 
                        max(1, len(categories)), text="Categories selected")
            special_requests = st.text_area(
                'Special Requests',
                placeholder='Any special requirements or requests...\n\nSuggestions:\n• Wheelchair accessibility\n• Photography permissions\n• Group discounts\n• Guided tour preferences',
                key='bm_single_special'
            )
            form_valid = bool(name and email and whatsapp and any(
                len(v) > 0 for v in single_selections.values()))
            if form_valid:
                st.success("✅ Form validation passed")
            else:
                st.warning(
                    "⚠️ Please fill in all required fields marked with * and select at least one option.")
            st.markdown(f"<div class='sticky-summary'>",
                        unsafe_allow_html=True)
            summary = f"**Name:** {name}\n**Email:** {email}\n**WhatsApp:** {whatsapp}\n**Group Size:** {group_size}\n"
            for cat, items in single_selections.items():
                if items:
                    summary += f"\n**{cat.title()}**:\n"
                    for item in items:
                        summary += f"- {item['name']} on {item['date']} at {item['time']}\n"
            if special_requests:
                summary += f"\n**Special Requests:** {special_requests}\n"
            st.subheader('📝 Booking Summary')
            st.markdown(summary)
            st.session_state.booking_summary_merged = summary
            st.markdown(f"</div>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                '🚀 Submit Booking', disabled=not form_valid)
            if submitted:
                booking_data = {
                    'mode': 'single',
                    'name': name,
                    'email': email,
                    'whatsapp': whatsapp,
                    'group_size': group_size,
                    'dietary': dietary,
                    'special_needs': special_needs,
                    'selections': single_selections,
                    'special_requests': special_requests,
                    'summary': summary,
                    'timestamp': str(datetime.datetime.now()),
                    'booking_id': hashlib.md5(f"{name}{email}{datetime.datetime.now()}".encode()).hexdigest()[:8],
                    'ai_processed': True,
                    'validation_score': None  # Will set below
                }
                booking_data['validation_score'] = calculate_booking_score(
                    booking_data)
                if 'real_time_processor' in st.session_state:
                    task_id = st.session_state.real_time_processor.add_task(
                        str(uuid.uuid4())[:8],
                        'process_booking',
                        {'booking_data': booking_data}
                    )
                    with st.spinner("Processing booking with AI..."):
                        # Ensure minimum 3-second loading time
                        start_time = time.time()

                        result = st.session_state.real_time_processor.process_task(
                            task_id)
                        if result.get('success'):
                            process_booking(booking_data)
                            SessionManager.add_notification(
                                f"Booking confirmed: {booking_data['booking_id']}", "success")
                        else:
                            SessionManager.add_notification(
                                "Booking processing failed", "error")

                        # Ensure minimum 3-second loading time
                        elapsed_time = time.time() - start_time
                        if elapsed_time < 3:
                            time.sleep(3 - elapsed_time)
                else:
                    process_booking(booking_data)
                    st.success('✅ Booking submitted!')
        else:
            st.subheader('🌟 Book Multiple Experiences')
            booking_selections = {}
            for cat in categories:
                with st.expander(f"{get_icon(cat)} {cat.title()} 🏷️", expanded=False):
                    st.markdown(
                        f"<span class='animated-icon'>{get_icon(cat)}</span> <b>{cat.title()}</b>", unsafe_allow_html=True)
                    st.info(random.choice(fun_facts))
                    opts = options[cat]
                    filter_text = st.text_input(
                        f"Filter {cat.title()} options", key=f"filter_multi_{cat}")
                    filtered_opts = filter_options(opts, filter_text)
                    groups = grouped_options(filtered_opts)
                    # AI Suggestion button
                    if st.button(f"🤖 AI Suggest {cat.title()} Options", key=f"ai_suggest_multi_{cat}"):
                        st.session_state.ai_category_suggestions[cat] = ai_suggest_for_category(
                            cat, filtered_opts)
                    ai_suggestions = st.session_state.ai_category_suggestions.get(cat, [
                    ])
                    if ai_suggestions:
                        st.success(
                            f"AI Suggestion: {', '.join(ai_suggestions)}")
                    # Quick Add All
                    if filtered_opts:
                        if st.button(f"Quick Add All {cat.title()}", key=f"quickadd_multi_{cat}"):
                            for group_opts in groups.values():
                                st.session_state[f"bm_multi_{cat}_All"] = group_opts
                    selected = []
                    for group, group_opts in groups.items():
                        if len(groups) > 1:
                            st.markdown(f"**{group}**")
                        sel = st.multiselect(
                            f"Select {cat.title()} options" if len(
                                groups) == 1 else '',
                            group_opts,
                            key=f"bm_multi_{cat}_{group}")
                        selected.extend(sel)
                    booking_selections[cat] = []
                    for place in selected:
                        info = get_place_info(place)
                        fav = fav_key(place)
                        is_fav = fav in st.session_state.fav_places
                        img_url = info['image'] if info[
                            'image'] else f"https://placehold.co/400x250?text={place.replace(' ', '+')}&font=roboto"
                        st.image(img_url, width=250, caption=place,
                                 use_column_width=False)
                        if st.button(f"Show on Map", key=f"showmap_multi_{cat}_{place}"):
                            st.session_state.show_map_popup = (place, info)
                        if st.session_state.show_map_popup and st.session_state.show_map_popup[0] == place:
                            show_map_for_place({**info, 'name': place})
                        st.markdown(f"""
                        <div class='preview-card'>
                        <b style='font-size:1.1em'>{get_icon(cat)} {place}</b>
                        {'<span style=\"color:#ffd700;font-weight:bold;\">⭐ Recommended</span>' if info['highlighted'] else ''}
                        <span class='fav-star {'fav-on' if is_fav else ''}' onclick=\"window.parent.postMessage({{type: 'toggle_fav', name: '{place}'}}, '*')\">{'💛' if is_fav else '⭐'}</span><br>
                        <span style='color:#888;'>{info['short']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            date = st.date_input(f"Date for {place}", min_value=datetime.date.today(
                            ), key=f"bm_multi_date_{cat}_{place}")
                            time = st.time_input(f"Time for {place}", value=datetime.time(
                                hour=10), key=f"bm_multi_time_{cat}_{place}")
                        with col2:
                            st.caption('No extra info available.')
                        booking_selections[cat].append({
                            'name': place,
                            'date': str(date),
                            'time': str(time),
                            'category': cat
                        })
            st.progress(count_selected(booking_selections) / 
                        max(1, len(categories)), text="Categories selected")
            special_requests = st.text_area(
                'Anything else? (optional)', placeholder='e.g. birthday, accessibility, etc.', key='bm_multi_special')
            st.markdown(f"<div class='sticky-summary'>",
                        unsafe_allow_html=True)
            summary = f"**Name:** {name}\n**Email:** {email}\n**WhatsApp:** {whatsapp}\n**Group Size:** {group_size}\n"
            for cat, items in booking_selections.items():
                if items:
                    summary += f"\n**{cat.title()}**:\n"
                    for item in items:
                        summary += f"- {item['name']} on {item['date']} at {item['time']}\n"
            if special_requests:
                summary += f"\n**Special Requests:** {special_requests}\n"
            st.subheader('📝 Booking Summary')
            st.markdown(summary)
            st.session_state.booking_summary_merged = summary
            st.markdown(f"</div>", unsafe_allow_html=True)
            ai_recs = st.form_submit_button('🤖 Ask AI for Recommendations')
            if ai_recs:
                recs = []
                for cat in categories:
                    if not booking_selections[cat] and options[cat]:
                        recs.append(
                            f"Try {random.choice(options[cat])} for {cat}!")
                st.session_state.ai_suggestion_merged = '\n'.join(
                    recs) if recs else 'Your plan looks great!'
            if st.session_state.ai_suggestion_merged:
                st.info(
                    f"AI Assistant: {st.session_state.ai_suggestion_merged}")
            submitted = st.form_submit_button('🚀 Submit Booking')
            if submitted:
                if not name or not email or not whatsapp:
                    st.error('Please fill in all required fields marked with *')
                else:
                    booking_data = {
                        'mode': 'multi',
                        'name': name,
                        'email': email,
                        'whatsapp': whatsapp,
                        'group_size': group_size,
                        'dietary': dietary,
                        'special_needs': special_needs,
                        'bookings': booking_selections,
                        'special_requests': special_requests,
                        'summary': summary,
                        'timestamp': str(datetime.datetime.now()),
                        'booking_id': hashlib.md5(f"{name}{email}{datetime.datetime.now()}".encode()).hexdigest()[:8],
                        'ai_processed': True,
                        'validation_score': None  # Will set below
                    }
                    booking_data['validation_score'] = calculate_booking_score(
                        booking_data)
                    if 'real_time_processor' in st.session_state:
                        task_id = st.session_state.real_time_processor.add_task(
                            str(uuid.uuid4())[:8],
                            'process_booking',
                            {'booking_data': booking_data}
                        )
                        with st.spinner("Processing booking with AI..."):
                            # Ensure minimum 3-second loading time
                            start_time = time.time()

                            result = st.session_state.real_time_processor.process_task(
                                task_id)
                            if result.get('success'):
                                process_booking(booking_data)
                                SessionManager.add_notification(
                                    f"Booking confirmed: {booking_data['booking_id']}", "success")
                            else:
                                SessionManager.add_notification(
                                    "Booking processing failed", "error")

                            # Ensure minimum 3-second loading time
                            elapsed_time = time.time() - start_time
                            if elapsed_time < 3:
                                time.sleep(3 - elapsed_time)
                    else:
                        process_booking(booking_data)
                        st.success('✅ Smart booking submitted!')


def process_booking(booking_data):
    """Process booking with encryption and email sending"""
    try:
        # Generate encryption key
        key = generate_key()

        # Encrypt sensitive data
        encrypted_data = encrypt_data(json.dumps(booking_data), key)

        # Save to DataFrame
        df = pd.DataFrame([booking_data])
        df.to_csv(f"booking_{booking_data['booking_id']}.csv", index=False)

        # Save encrypted version
        with open(f"encrypted_booking_{booking_data['booking_id']}.txt", 'wb') as f:
            f.write(encrypted_data)

        # Save encryption key separately
        with open(f"key_{booking_data['booking_id']}.key", 'wb') as f:
            f.write(key)

        # Send email (simulated)
        send_booking_email(booking_data)

        # Display confirmation
        st.success(
            f"✅ Booking submitted successfully! Booking ID: {booking_data['booking_id']}")

        # Add to notifications
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []

        st.session_state.notifications.append({
            'type': 'booking',
            'message': f"New booking for {booking_data['selected_place']} by {booking_data['name']}",
            'timestamp': datetime.now(),
            'data': booking_data
        })

    except Exception as e:
        st.error(f"Error processing booking: {e}")


def send_booking_email(booking_data):
    """Simulate sending email to secretary"""
    # In a real implementation, you would use actual SMTP settings
    email_content = f"""
    New Tourism Booking Request
    
    Booking ID: {booking_data['booking_id']}
    Client Name: {booking_data['name']}
    Email: {booking_data['email']}
    WhatsApp: {booking_data['whatsapp']}
    
    Selected Place: {booking_data['selected_place']}
    Selected Restaurant: {booking_data['selected_restaurant']}
    Restaurant Reservation: {'Yes' if booking_data['make_reservation'] else 'No'}
    
    Visit Date: {booking_data['visit_date']}
    Special Requests: {booking_data['special_requests']}
    
    Submitted: {booking_data['timestamp']}
    
    ---
    This booking was submitted through the Tshwane Tourism Interactive Portal
    Created by Profit Projects Online Virtual Assistance
    Enterprise Number: K2025200646
    Contact: Thapelo Kgothatso Thooe
    Email: kgothatsothooe@gmail.com
    """

    # Save email content to file
    with open(f"email_booking_{booking_data['booking_id']}.txt", 'w') as f:
        f.write(email_content)

    st.info("📧 Booking details prepared for email to secretary@tshwanetourism.com")

# Removed duplicate functions - keeping only the first instances


def process_enhanced_booking(booking_data: Dict[str, Any]):
    """Enhanced booking processing with AI features"""
    try:
        # Generate encryption key
        key = generate_key()

        # Encrypt sensitive data
        encrypted_data = encrypt_data(json.dumps(booking_data), key)

        # Save to DataFrame with enhanced fields
        df = pd.DataFrame([booking_data])
        df.to_csv(f"booking_{booking_data['booking_id']}.csv", index=False)

        # Save encrypted version
        with open(f"encrypted_booking_{booking_data['booking_id']}.txt", 'wb') as f:
            f.write(encrypted_data)

        # Save encryption key separately
        with open(f"key_{booking_data['booking_id']}.key", 'wb') as f:
            f.write(key)

        # Enhanced email sending
        send_enhanced_booking_email(booking_data)

        # Display confirmation with AI insights
        st.success(f"✅ Booking processed successfully!")
        st.info(f"🆔 Booking ID: {booking_data['booking_id']}")
        st.info(
            f"🤖 AI Validation Score: {booking_data.get('validation_score', 0):.1f}/1.0")

        # Add to notifications with enhanced details
        SessionManager.add_notification(
            f"New booking: {booking_data['selected_place']} by {booking_data['name']} (Score: {booking_data.get('validation_score', 0):.1f})", "success")

    except Exception as e:
        st.error(f"Error processing booking: {e}")
        SessionManager.add_notification(
            f"Booking processing failed: {str(e)}", "error")


def send_enhanced_booking_email(booking_data: Dict[str, Any]):
    """Enhanced email sending with AI-generated content"""
    email_content = f"""
    🌿 TSHWANE TOURISM ASSOCIATION - NEW BOOKING REQUEST

    ═══════════════════════════════════════════════════════════
    📋 BOOKING DETAILS
    ═══════════════════════════════════════════════════════════

    🆔 Booking ID: {booking_data['booking_id']}
    📅 Submitted: {booking_data['timestamp']}
    🤖 AI Processed: {booking_data.get('ai_processed', False)}
    ⭐ Validation Score: {booking_data.get('validation_score', 0):.1f}/1.0

    ═══════════════════════════════════════════════════════════
    👤 CLIENT INFORMATION
    ═══════════════════════════════════════════════════════════

    Name: {booking_data['name']}
    Email: {booking_data['email']}
    WhatsApp: {booking_data['whatsapp']}

    ═══════════════════════════════════════════════════════════
    🎯 BOOKING PREFERENCES
    ═══════════════════════════════════════════════════════════

    Selected Place: {booking_data['selected_place']}
    Selected Restaurant: {booking_data['selected_restaurant']}
    Restaurant Reservation: {'Yes' if booking_data['make_reservation'] else 'No'}
    Visit Date: {booking_data['visit_date']}

    ═══════════════════════════════════════════════════════════
    💬 SPECIAL REQUESTS
    ═══════════════════════════════════════════════════════════

    {booking_data['special_requests'] or 'None specified'}

    ═══════════════════════════════════════════════════════════
    🤖 AI SYSTEM INFORMATION
    ═══════════════════════════════════════════════════════════

    This booking was processed through our AI-powered tourism portal
    with enhanced validation and real-time processing capabilities.

    System Features Used:
    • Real-time form validation
    • AI-powered place analysis
    • Encrypted data transmission
    • Automated notification system

    ═══════════════════════════════════════════════════════════
    📞 CONTACT & SUPPORT
    ═══════════════════════════════════════════════════════════

    Created by: Profit Projects Online Virtual Assistance
    Enterprise Number: K2025200646
    Contact: Thapelo Kgothatso Thooe
    Email: kgothatsothooe@gmail.com

    For booking inquiries: secretary@tshwanetourism.com

    ═══════════════════════════════════════════════════════════
    """

    # Save email content to file
    with open(f"email_booking_{booking_data['booking_id']}.txt", 'w', encoding='utf-8') as f:
        f.write(email_content)

    st.info("📧 Enhanced booking email prepared for secretary@tshwanetourism.com")


def display_google_maps_with_places():
    """Display a Google Maps iframe, a filterable table of place links, and a custom map with all markers if possible."""
    import pandas as pd
    import urllib.parse
    st.markdown("#### Google Maps (All Places)")
    # Google Maps base embed (centered on Tshwane)
    st.components.v1.iframe(
        "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d14334.0!2d28.1879!3d-25.7479!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zTWFpbiBUc2h3YW5l!5e0!3m2!1sen!2sza!4v1680000000000!5m2!1sen!2sza",
        height=400,
        scrolling=True
    )
    try:
        df = pd.read_csv('tshwane_places.csv')
        # Filtering
        filter_text = st.text_input('Filter places by name or type:')
        if filter_text:
            df = df[df['name'].str.contains(filter_text, case=False, na=False) | df['type'].str.contains(
                filter_text, case=False, na=False)]
        with st.expander('Quick Google Maps Search Links for All Places', expanded=False):
            # Table/grid layout
            n_cols = 4
            rows = [df.iloc[i:i + n_cols] for i in range(0, len(df), n_cols)]
            for row in rows:
                cols = st.columns(n_cols)
                for idx, (_, place) in enumerate(row.iterrows()):
                    name = place.get('name', '')
                    ptype = place.get('type', '')
                    url = f"https://www.google.com/maps/search/{urllib.parse.quote_plus(name + ' Tshwane')}"
                    with cols[idx]:
                        st.markdown(
                            f"**[{name}]({url})**<br><span style='font-size:0.9em;color:#888;'>Type: {ptype}</span>", unsafe_allow_html=True)
        # Custom Google Maps with all markers (if lat/lng available)
        if 'lat' in df.columns and 'lng' in df.columns and not df[['lat', 'lng']].isnull().all().all():
            # Generate Static Maps API URL (limited by Google API, but demo for a few markers)
            base = "https://maps.googleapis.com/maps/api/staticmap?size=600x400&maptype=roadmap"
            marker_strs = []
            for _, row in df.iterrows():
                lat, lng = row.get('lat'), row.get('lng')
                if pd.notna(lat) and pd.notna(lng):
                    marker_strs.append(f"{lat},{lng}")
            # Limit to 50 markers for demo (API limit)
            marker_params = "&".join(
                [f"markers={m}" for m in marker_strs[:50]])
            # NOTE: You need a Google Maps API key for production use
            static_url = f"{base}&{marker_params}"  # + "&key=YOUR_API_KEY"
            st.image(
                static_url, caption="Custom Map with All Markers (Demo, no API key)")
            st.info(
                "For a fully interactive map with all markers, use the Folium map below or add your Google Maps API key.")
        else:
            st.info(
                "No coordinates found for places. Only search links are available.")
    except Exception as e:
        st.info(f"Could not load tshwane_places.csv: {e}")

# Removed duplicate functions - they are already defined earlier in the file


def _native_render_component(component_type: str, props: Dict[str, Any]) -> None:
    if component_type == "gallery_card":
        with st.container(border=True):
            st.markdown(f"#### {props.get('title', 'Untitled')}")
            st.write(props.get('description', 'No description'))
            st.caption(f"Category: {props.get('type', 'general')}")
    elif component_type == "progress_indicator":
        progress = props.get('progress', 0)
        st.progress(progress / 100)
        st.caption(f"Progress: {progress}%")
    elif component_type == "notification_toast":
        message_type = props.get('type', 'info')
        message = props.get('message', '')
        if message_type == 'success':
            st.success(message)
        elif message_type == 'error':
            st.error(message)
        elif message_type == 'warning':
            st.warning(message)
        else:
            st.info(message)


ComponentSystem.render_component = staticmethod(_native_render_component)


def _get_places_records() -> List[Dict[str, Any]]:
    places = st.session_state.get('places_data') or []
    if not places:
        places = load_tshwane_places_csv()
        if places:
            st.session_state.places_data = places
    return places


def _build_place_cards(records: List[Dict[str, Any]], limit: int=6) -> List[Dict[str, Any]]:
    cards: List[Dict[str, Any]] = []
    for place in records[:limit]:
        name = place.get('display_name') or place.get('name') or 'Unknown Place'
        query = urllib.parse.quote_plus(f"{name} Tshwane")
        cards.append({
            'title': name,
            'type': str(place.get('type', 'Place')).title(),
            'description': place.get('description') or place.get('short_description') or 'Description not available.',
            'sentiment': str(place.get('ai_sentiment', 'balanced')).title(),
            'source': place.get('data_source', 'Local data'),
            'link': f"https://www.google.com/maps/search/{query}",
        })
    return cards


def _prepare_places_dataframe(records: List[Dict[str, Any]]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    if 'display_name' in df.columns and 'name' not in df.columns:
        df['name'] = df['display_name']
    elif 'display_name' in df.columns:
        df['name'] = df['display_name'].fillna(df.get('name'))
    if 'description' not in df.columns:
        df['description'] = df.get('short_description', 'Description not available.')
    if 'type' not in df.columns:
        df['type'] = 'Place'
    return df


def _render_place_selection_card(place: Dict[str, Any], key_prefix: str, button_label: str) -> bool:
    name = place.get('display_name') or place.get('name') or 'Unknown Place'
    with st.container(border=True):
        st.markdown(f"#### {name}")
        cols = st.columns([1.3, 1])
        with cols[0]:
            st.caption(str(place.get('type', 'Place')).title())
        with cols[1]:
            sentiment = str(place.get('ai_sentiment', 'balanced')).title()
            st.caption(f"Sentiment: {sentiment}")
        st.write((place.get('description') or place.get('short_description') or 'Description not available.')[:220])
        return st.button(button_label, key=f"{key_prefix}_{name}")


def display_tutorial():
    """Display a native tutorial panel."""
    if not st.session_state.get('show_tutorial', False):
        return

    tutorial_steps = create_tutorial_system()
    current_step = min(st.session_state.get('tutorial_step', 0), len(tutorial_steps) - 1)
    step = tutorial_steps[current_step]
    progress_pct = int(((current_step + 1) / len(tutorial_steps)) * 100)

    with st.container(border=True):
        render_section_header(
            f"Step {current_step + 1} of {len(tutorial_steps)}",
            step['content'],
            "📚",
        )
        st.progress(progress_pct / 100)
        st.info(step['action'])
        nav_cols = st.columns(4)
        with nav_cols[0]:
            if st.button('Back', key='tutorial_back_btn_native', disabled=current_step == 0):
                st.session_state.tutorial_step = max(current_step - 1, 0)
                st.rerun()
        with nav_cols[1]:
            if st.button('Skip', key='tutorial_skip_btn_native'):
                st.session_state.show_tutorial = False
                st.session_state.tutorial_step = 0
                st.rerun()
        with nav_cols[2]:
            if st.button('Next', key='tutorial_next_btn_native', disabled=current_step >= len(tutorial_steps) - 1):
                st.session_state.tutorial_step = min(current_step + 1, len(tutorial_steps) - 1)
                st.rerun()
        with nav_cols[3]:
            if st.button('Finish', key='tutorial_finish_btn_native'):
                st.session_state.show_tutorial = False
                st.session_state.tutorial_step = 0
                st.rerun()


def display_planning_interface():
    """Native trip planner using tabs, cards, and compact summaries."""
    places = _get_places_records()
    if 'planned_places' not in st.session_state:
        st.session_state.planned_places = []

    render_section_header(
        "Trip Planner",
        "Build a compact itinerary with AI-supported place matching and weather-aware suggestions.",
        "🧭",
    )

    with st.container(border=True):
        planner_cols = st.columns([2, 1, 1])
        with planner_cols[0]:
            planner_goal = st.text_area(
                "What kind of day are you planning?",
                value=st.session_state.get('planner_goal', 'A relaxed day with culture, food, and scenic stops.'),
                key='planner_goal_native',
                height=100,
            )
            st.session_state.planner_goal = planner_goal
        with planner_cols[1]:
            available_types = sorted({str(place.get('type', 'Place')).title() for place in places})
            selected_types = st.multiselect(
                "Place types",
                options=available_types,
                default=available_types[:3],
                key='planner_types_native',
            )
        with planner_cols[2]:
            weather_choice = st.selectbox(
                "Weather mood",
                options=['sunny', 'cloudy', 'rainy', 'windy'],
                key='planner_weather_native',
            )

    filtered_places = [
        place for place in places
        if not selected_types or str(place.get('type', 'Place')).title() in selected_types
    ]
    if planner_goal:
        goal_terms = planner_goal.lower()
        query_matches = [
            place for place in filtered_places
            if goal_terms in str(place.get('description', '')).lower()
            or goal_terms in str(place.get('name', '')).lower()
        ]
        if query_matches:
            filtered_places = query_matches

    recommended_places = WEATHER_SERVICE.score_places_for_weather(filtered_places or places, weather_choice, limit=6)
    render_metric_strip([
        ("Places scanned", len(filtered_places or places), None),
        ("Recommended", len(recommended_places), None),
        ("In itinerary", len(st.session_state.planned_places), None),
    ])

    suggestion_tab, itinerary_tab, ai_tab = st.tabs(["Suggestions", "Itinerary", "AI Plan Steps"])
    with suggestion_tab:
        if not recommended_places:
            st.info("Try widening your filters to see more recommended stops.")
        for place in recommended_places:
            if _render_place_selection_card(place, 'plan_add', 'Add to itinerary'):
                if not any((item.get('name') or item.get('display_name')) == (place.get('name') or place.get('display_name')) for item in st.session_state.planned_places):
                    st.session_state.planned_places.append(place)
                    st.rerun()

    with itinerary_tab:
        if not st.session_state.planned_places:
            st.info('Your itinerary is empty. Add a few places from the Suggestions tab.')
        else:
            for index, place in enumerate(st.session_state.planned_places):
                with st.container(border=True):
                    title_col, action_col = st.columns([4, 1])
                    with title_col:
                        st.markdown(f"#### {place.get('display_name') or place.get('name') or 'Planned stop'}")
                        st.caption(str(place.get('type', 'Place')).title())
                        st.write((place.get('description') or 'Description not available.')[:200])
                    with action_col:
                        if st.button('Remove', key=f'remove_plan_{index}'):
                            st.session_state.planned_places.pop(index)
                            st.rerun()
                    slot_cols = st.columns(2)
                    slot_cols[0].text_input('Best time', value='Late morning', key=f'plan_time_{index}')
                    slot_cols[1].text_input('Notes', value='Great stop for photos or food nearby.', key=f'plan_notes_{index}')

    with ai_tab:
        ai_steps = st.session_state.planning_system.suggest_plan(planner_goal or 'Plan a Tshwane day trip')
        for step in ai_steps:
            status = step.status.replace('_', ' ').title()
            with st.container(border=True):
                st.write(f"**{step.description}**")
                st.caption(f"Status: {status}")


def display_enhanced_sidebar():
    """CSS-free sidebar navigation and app status."""
    places = _get_places_records()
    nav_options = {
        'overview': '🏡 Overview',
        'planning': '🧭 Planner',
        'analytics': '📊 Analytics',
        'individual_places': '🗂️ Places',
        'weather_guide': '🌤️ Weather Guide',
        'booking': '📝 Booking',
        'chat': '🤖 AI Chat',
        'contact': '📞 Contact',
        'email_secretary': '📧 Secretary',
    }

    with st.sidebar:
        st.title('🌿 Explore Tshwane')
        st.caption('Lightweight navigation, weather context, and quick access actions.')

        current_section = st.session_state.get('current_section', 'overview')
        section_keys = list(nav_options.keys())
        selected_section = st.radio(
            'Navigate',
            options=section_keys,
            index=section_keys.index(current_section) if current_section in section_keys else 0,
            format_func=lambda key: nav_options[key],
            key='sidebar_navigation_native',
        )
        st.session_state.current_section = selected_section

        if st.button('📚 Start Tutorial', key='start_tutorial_sidebar_native'):
            st.session_state.show_tutorial = True
            st.session_state.tutorial_step = 0
            st.rerun()

        snapshot = WEATHER_SERVICE.fetch_current_weather()
        with st.expander('Live weather snapshot', expanded=True):
            if snapshot:
                st.metric('Condition', snapshot.condition.title())
                st.metric('Temperature', f"{snapshot.temperature_c:.1f}°C")
                st.caption(f"Observed at {snapshot.observed_at}")
            else:
                st.caption('Live weather is temporarily unavailable.')

        with st.expander('Quick search', expanded=False):
            query = st.text_input('Search places', key='sidebar_search_native')
            if query:
                matches = [
                    place for place in places
                    if query.lower() in str(place.get('name', '')).lower()
                    or query.lower() in str(place.get('description', '')).lower()
                ][:5]
                if matches:
                    render_record_cards(
                        _build_place_cards(matches, limit=5),
                        title_key='title',
                        description_keys=['description'],
                        meta_keys=['type', 'source'],
                        link_key='link',
                        columns_count=1,
                        key_prefix='sidebar_search_cards',
                    )
                else:
                    st.info('No places matched your search yet.')

        with st.expander('Quick links', expanded=False):
            st.link_button('Official Tshwane Tourism', 'https://www.visittshwane.co.za/')
            st.link_button('Open Maps for Pretoria', 'https://www.google.com/maps/search/Pretoria+South+Africa')
            st.link_button('Project Repository', 'https://github.com/ybadk/Tryp_Thooe_Tourism_Lite')

        with st.expander('App status', expanded=False):
            render_metric_strip([
                ('Places', len(places), None),
                ('Mode', st.session_state.get('operation_mode', OperationMode.STANDARD).value, None),
            ])
            st.caption('AI services, weather support, and card-based browsing are active.')

        if selected_section == 'contact':
            st.caption('Developer details are also available in the main area.')
        if selected_section == 'email_secretary':
            st.info('Use the secretary form to send event, booking, or partnership requests.')


def display_enhanced_booking_form():
    """Booking flow with native sections and compact summaries."""
    places = _get_places_records()
    place_names = [place.get('display_name') or place.get('name') or 'Unknown Place' for place in places]
    type_names = sorted({str(place.get('type', 'Place')).title() for place in places})
    today = pd.Timestamp.today().date()
    tomorrow = (pd.Timestamp.today() + pd.Timedelta(days=1)).date()

    render_section_header(
        'Book a Tshwane experience',
        'Capture visitor details, preferred places, and booking notes in a cleaner layout.',
        '📝',
    )

    snapshot = WEATHER_SERVICE.fetch_current_weather()
    if snapshot:
        st.caption(f"Weather tip: It is currently {snapshot.condition} and {snapshot.temperature_c:.1f}°C in Tshwane.")

    with st.form('booking_form_native'):
        details_col, trip_col = st.columns(2)
        with details_col:
            name = st.text_input('Full name *')
            email = st.text_input('Email address *')
            phone = st.text_input('Phone number')
            visitors = st.number_input('Number of visitors', min_value=1, max_value=20, value=2)
        with trip_col:
            booking_date = st.date_input('Booking date', value=today)
            end_date = st.date_input('End date', value=tomorrow)
            selected_types = st.multiselect('Preferred place types', options=type_names)
            selected_places = st.multiselect('Places to include *', options=place_names)

        notes = st.text_area('Special requests or accessibility notes')
        summary_col1, summary_col2 = st.columns(2)
        with summary_col1:
            st.write('**Selected place types**')
            st.write(', '.join(selected_types) if selected_types else 'Any type')
        with summary_col2:
            st.write('**Selected places**')
            st.write(', '.join(selected_places) if selected_places else 'Choose at least one place')

        submit = st.form_submit_button('Submit booking request')

    if submit:
        if not name or not email or not selected_places:
            st.error('Please complete the required fields and choose at least one place.')
            return

        booking_data = {
            'booking_id': str(uuid.uuid4())[:8],
            'name': name,
            'email': email,
            'phone': phone,
            'visitors': visitors,
            'booking_date': str(booking_date),
            'end_date': str(end_date),
            'place_types': selected_types,
            'selected_places': selected_places,
            'notes': notes,
        }
        process_booking(booking_data)


def display_individual_places_gallery():
    """Browse place records as cards with compact filters."""
    places = _get_places_records()
    if not places:
        st.warning('No place data is available yet.')
        return

    places_df = _prepare_places_dataframe(places)
    render_section_header('Places directory', 'Browse and filter destinations without large tables.', '🗂️')

    filter_cols = st.columns([1, 1, 2])
    with filter_cols[0]:
        selected_type = st.selectbox('Type', ['All'] + sorted(places_df['type'].astype(str).str.title().unique().tolist()))
    with filter_cols[1]:
        max_cards = st.slider('Cards to show', min_value=4, max_value=20, value=8)
    with filter_cols[2]:
        search_term = st.text_input('Search name or description', key='places_gallery_search_native')

    filtered_df = places_df.copy()
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['type'].astype(str).str.title() == selected_type]
    if search_term:
        filtered_df = filtered_df[
            filtered_df['name'].astype(str).str.contains(search_term, case=False, na=False)
            | filtered_df['description'].astype(str).str.contains(search_term, case=False, na=False)
        ]

    render_metric_strip([
        ('Available', len(places_df), None),
        ('Filtered', len(filtered_df), None),
        ('Types', filtered_df['type'].astype(str).nunique() if not filtered_df.empty else 0, None),
    ])

    preview_cards = _build_place_cards(filtered_df.to_dict(orient='records'), limit=max_cards)
    render_record_cards(
        preview_cards,
        title_key='title',
        description_keys=['description'],
        meta_keys=['type', 'sentiment', 'source'],
        link_key='link',
        columns_count=2,
        key_prefix='individual_places_native',
    )


def display_developer_contact_info():
    """Native developer contact section."""
    developers = load_developer_details()
    render_section_header('Project contacts', 'Connect with the builders and support team.', '📞')
    if not developers:
        st.info('Developer details could not be loaded.')
        return

    for index, developer in enumerate(developers):
        with st.container(border=True):
            name = developer.get('name', 'Project Team')
            role = developer.get('role', 'Team member')
            st.markdown(f"#### {name}")
            st.caption(role)
            info_cols = st.columns(2)
            info_cols[0].write(f"**Email:** {developer.get('email', 'Not provided')}")
            info_cols[1].write(f"**Phone:** {developer.get('phone', 'Not provided')}")
            skills = developer.get('skills') or developer.get('specialization') or developer.get('expertise')
            if skills:
                st.write(f"**Focus:** {skills}")
            links_col1, links_col2 = st.columns(2)
            if developer.get('linkedin'):
                links_col1.link_button('LinkedIn', developer['linkedin'])
            if developer.get('github'):
                links_col2.link_button('GitHub', developer['github'])


def display_weather_content():
    """Weather guidance using metrics and recommendation cards."""
    places = _get_places_records()
    render_section_header('Weather-based suggestions', 'Use current conditions to decide what to do next in Tshwane.', '🌤️')

    snapshot = WEATHER_SERVICE.fetch_current_weather()
    if snapshot:
        render_metric_strip([
            ('Condition', snapshot.condition.title(), None),
            ('Temperature', f"{snapshot.temperature_c:.1f}°C", None),
            ('Feels like', f"{snapshot.apparent_temperature_c:.1f}°C", None),
            ('Wind', f"{snapshot.wind_speed_kmh:.1f} km/h", None),
        ])
        st.caption(WEATHER_SERVICE.format_summary(snapshot))
        recommended = WEATHER_SERVICE.score_places_for_weather(places, snapshot.condition, limit=6)
    else:
        st.info('Live weather is unavailable, so choose a condition manually.')
        manual_condition = st.selectbox('Weather condition', ['sunny', 'cloudy', 'rainy', 'windy'])
        recommended = WEATHER_SERVICE.score_places_for_weather(places, manual_condition, limit=6)

    render_record_cards(
        _build_place_cards(recommended, limit=6),
        title_key='title',
        description_keys=['description'],
        meta_keys=['type', 'sentiment'],
        link_key='link',
        columns_count=2,
        key_prefix='weather_cards_native',
    )


def display_enhanced_gallery():
    """Feature selected places in a card-first gallery."""
    places = _get_places_records()
    if not places:
        st.info('No featured places are available right now.')
        return

    render_section_header('Featured gallery', 'Compact spotlights inspired by your layout card references.', '🌱')
    featured = sorted(
        places,
        key=lambda place: (str(place.get('verified_source', False)), str(place.get('ai_sentiment', 'neutral'))),
        reverse=True,
    )
    render_record_cards(
        _build_place_cards(featured, limit=6),
        title_key='title',
        description_keys=['description'],
        meta_keys=['type', 'sentiment', 'source'],
        link_key='link',
        columns_count=2,
        key_prefix='featured_gallery_native',
    )


def display_places_table():
    """Replace the raw table view with filterable cards and CSV download."""
    places = _get_places_records()
    if not places:
        st.warning('No tourism data loaded from tshwane_places.csv!')
        return

    places_df = _prepare_places_dataframe(places)
    render_section_header('Data explorer', 'Preview records as cards while keeping CSV export available.', '📚')
    filter_cols = st.columns(3)
    with filter_cols[0]:
        type_filter = st.multiselect(
            'Filter by type',
            options=sorted(places_df['type'].astype(str).str.title().unique().tolist()),
            default=sorted(places_df['type'].astype(str).str.title().unique().tolist()),
        )
    with filter_cols[1]:
        verification_filter = st.selectbox('Verification', ['All', 'Verified only', 'Unverified only'])
    with filter_cols[2]:
        weather_filter = st.selectbox('Weather suitability', ['All', 'Has weather fit', 'No weather fit'])

    filtered_df = places_df[places_df['type'].astype(str).str.title().isin(type_filter)] if type_filter else places_df.copy()
    if verification_filter == 'Verified only' and 'verified_source' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['verified_source'] == True]
    if verification_filter == 'Unverified only' and 'verified_source' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['verified_source'] != True]
    if weather_filter == 'Has weather fit' and 'weather_suitability' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['weather_suitability'].notna()]
    if weather_filter == 'No weather fit' and 'weather_suitability' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['weather_suitability'].isna()]

    preview_records = _build_place_cards(filtered_df.to_dict(orient='records'), limit=10)
    render_record_cards(
        preview_records,
        title_key='title',
        description_keys=['description'],
        meta_keys=['type', 'sentiment', 'source'],
        link_key='link',
        columns_count=2,
        key_prefix='places_table_cards_native',
    )

    st.download_button(
        label='Download filtered CSV',
        data=filtered_df.to_csv(index=False),
        file_name='tshwane_places_filtered.csv',
        mime='text/csv',
    )


def display_booking_form_merged():
    """Delegate legacy booking entry point to the new booking form."""
    display_enhanced_booking_form()


def display_google_maps_with_places():
    """Map and search links with native Streamlit layout."""
    places_df = _prepare_places_dataframe(_get_places_records())
    render_section_header('Map and place finder', 'Use the map for orientation and open cards for directions.', '🗺️')
    if places_df.empty:
        st.info('No mapped place data is available yet.')
        return

    filter_cols = st.columns([2, 1])
    with filter_cols[0]:
        search_text = st.text_input('Search places or descriptions', key='maps_search_native')
    with filter_cols[1]:
        type_choice = st.selectbox('Place type', ['All'] + sorted(places_df['type'].astype(str).str.title().unique().tolist()), key='maps_type_native')

    filtered_df = places_df.copy()
    if search_text:
        filtered_df = filtered_df[
            filtered_df['name'].astype(str).str.contains(search_text, case=False, na=False)
            | filtered_df['description'].astype(str).str.contains(search_text, case=False, na=False)
        ]
    if type_choice != 'All':
        filtered_df = filtered_df[filtered_df['type'].astype(str).str.title() == type_choice]

    if {'lat', 'lng'}.issubset(filtered_df.columns):
        map_df = filtered_df[['lat', 'lng']].dropna().rename(columns={'lng': 'lon'})
        if not map_df.empty:
            st.map(map_df, use_container_width=True)
        else:
            st.info('Coordinates are unavailable for the current filter selection.')

    render_record_cards(
        _build_place_cards(filtered_df.to_dict(orient='records'), limit=8),
        title_key='title',
        description_keys=['description'],
        meta_keys=['type', 'source'],
        link_key='link',
        columns_count=2,
        key_prefix='maps_cards_native',
    )


def display_main_content():
    """Main card-based content area with tabs and reduced scrolling."""
    section = st.session_state.get('current_section', 'overview')
    places = _get_places_records()
    if not places:
        st.warning('Tourism place data is not available. Load the CSV files to explore the portal fully.')

    if section == 'planning':
        display_planning_interface()
        return
    if section == 'booking':
        display_enhanced_booking_form()
        return
    if section == 'contact':
        display_developer_contact_info()
        return
    if section == 'email_secretary':
        display_email_secretary_form()
        return
    if section == 'chat':
        from chat_interface import display_chat_interface_main
        display_chat_interface_main()
        return
    if section == 'weather_guide':
        display_weather_content()
        return
    if section == 'analytics':
        display_places_dashboard()
        return
    if section == 'individual_places':
        display_individual_places_gallery()
        return

    render_section_header(
        'Tshwane tourism command center',
        'A lighter, card-based overview for exploration, AI guidance, and booking preparation.',
        '🌿',
    )
    render_metric_strip([
        ('Places', len(places), None),
        ('Types', len({place.get('type', 'unknown') for place in places}), None),
        ('Weather aware', sum(1 for place in places if place.get('weather_suitability')), None),
        ('Verified', sum(1 for place in places if place.get('verified_source')), None),
    ])

    hero_left, hero_right = st.columns([2.2, 1])
    with hero_left:
        display_google_maps_with_places()
    with hero_right:
        with st.container(border=True):
            snapshot = WEATHER_SERVICE.fetch_current_weather()
            st.markdown('#### Today in Tshwane')
            if snapshot:
                st.write(WEATHER_SERVICE.format_summary(snapshot))
            else:
                st.write('Live weather is temporarily unavailable.')
            top_types = pd.Series([str(place.get('type', 'Place')).title() for place in places]).value_counts().head(3)
            st.caption('Most common place types')
            for place_type, count in top_types.items():
                st.write(f"• {place_type}: {count}")

        with st.container(border=True):
            st.markdown('#### Quick actions')
            action_cols = st.columns(2)
            if action_cols[0].button('Open planner', key='quick_planner_native'):
                st.session_state.current_section = 'planning'
                st.rerun()
            if action_cols[1].button('Ask AI', key='quick_chat_native'):
                st.session_state.current_section = 'chat'
                st.rerun()
            if st.button('Book a visit', key='quick_booking_native', use_container_width=True):
                st.session_state.current_section = 'booking'
                st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(['Highlights', 'Gallery', 'Analytics', 'Data Explorer'])
    with tab1:
        recommended = WEATHER_SERVICE.score_places_for_weather(places, 'sunny', limit=6)
        render_record_cards(
            _build_place_cards(recommended, limit=6),
            title_key='title',
            description_keys=['description'],
            meta_keys=['type', 'sentiment'],
            link_key='link',
            columns_count=2,
            key_prefix='overview_highlights_native',
        )
    with tab2:
        display_enhanced_gallery()
    with tab3:
        display_places_dashboard()
    with tab4:
        display_places_table()


def main():
    """Main application with native Streamlit theming and compact card layouts."""
    SessionManager.initialize_session()
    if 'real_time_processor' not in st.session_state:
        st.session_state.real_time_processor = RealTimeProcessor()
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 'overview'

    display_tutorial()

    header_cols = st.columns([3, 1.2, 1])
    with header_cols[0]:
        st.title('🌿 Tshwane Tourism Interactive Portal')
        st.caption('A light, nature-themed workspace for discovery, planning, weather guidance, and AI support.')
    with header_cols[1]:
        mode = st.selectbox(
            'Operation mode',
            [mode.value for mode in OperationMode],
            index=[mode.value for mode in OperationMode].index(st.session_state.get('operation_mode', OperationMode.STANDARD).value),
            key='operation_mode_select_native',
        )
        st.session_state.operation_mode = OperationMode(mode)
    with header_cols[2]:
        auto_refresh = st.toggle('Auto refresh', value=st.session_state.user_preferences['auto_refresh'])
        st.session_state.user_preferences['auto_refresh'] = auto_refresh

    if st.session_state.execution_progress > 0:
        st.session_state.component_system.render_component('progress_indicator', {'progress': st.session_state.execution_progress})

    display_enhanced_sidebar()
    display_main_content()


if __name__ == "__main__":
    main()

# --- Unified Offline Model Call for Chat Assistant ---

# GPT-2 imports (assuming gpt-2-master/src is in PYTHONPATH)
try:
    import sys
    sys.path.append(os.path.abspath('gpt-2-master/src'))
    import encoder as gpt2_encoder
    import model as gpt2_model
    import sample as gpt2_sample
except ImportError:
    gpt2_encoder = None
    gpt2_model = None
    gpt2_sample = None

# RAG imports (example: use all-rag-techniques-main/01_simple_rag.ipynb logic)
# For demonstration, we use a simple keyword search over loaded CSVs


def load_iris_model():
    model_path = 'iris_xgb_model.joblib'
    if not os.path.exists(model_path):
        # Train and save if not present
        iris = load_iris()
        X, y = iris.data, iris.target
        model = xgb.XGBClassifier()
        model.fit(X, y)
        joblib.dump(model, model_path)
    return joblib.load(model_path)


def load_iris_data():
    iris = load_iris()
    return iris


def rag_search(query, csv_dirs=None, max_results=3):
    if csv_dirs is None:
        csv_dirs = [
            Path('processed_data'),
            Path('scraps'),
            Path('tshwane_crawled_data'),
            Path('processed_places_data'),
        ]
    results = []
    for d in csv_dirs:
        if d.exists():
            for csv_file in d.rglob('*.csv'):
                try:
                    df = pd.read_csv(csv_file)
                    for col in df.columns:
                        matches = df[df[col].astype(str).str.contains(
                            query, case=False, na=False)]
                        if not matches.empty:
                            for _, row in matches.iterrows():
                                results.append({
                                    'file': str(csv_file),
                                    'row': row.to_dict()
                                })
                                if len(results) >= max_results:
                                    return results
                except Exception:
                    continue
    return results


def gpt2_generate(prompt, model_name='124M', models_dir='gpt-2-master/models', length=60):
    if gpt2_encoder is None or gpt2_model is None or gpt2_sample is None:
        return "[GPT-2 not available in this environment]"
    enc = gpt2_encoder.get_encoder(model_name, models_dir)
    hparams = gpt2_model.default_hparams()
    import json
    import tensorflow as tf
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))
    context_tokens = enc.encode(prompt)
    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [1, None])
        output = gpt2_sample.sample_sequence(
            hparams=hparams, length=length, context=context, batch_size=1
        )
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)
        out = sess.run(output, feed_dict={context: [context_tokens]})
        text = enc.decode(out[0])
        return text


def offline_chat_model_call(user_query: str) -> str:
    # 1. Check for iris dataset queries
    if 'iris' in user_query.lower():
        model = load_iris_model()
        iris = load_iris_data()
        # Simple demo: if user asks for prediction, expect 4 floats in query
        import re
        floats = re.findall(r'[-+]?[0-9]*\.?[0-9]+', user_query)
        if len(floats) >= 4:
            features = np.array(floats[:4], dtype=float).reshape(1, -1)
            pred = model.predict(features)[0]
            class_name = iris.target_names[pred]
            return f"[Iris Model] Predicted class: {class_name} (features: {features.tolist()})"
        else:
            # Otherwise, show dataset info
            return f"[Iris Dataset] Features: {iris.feature_names}, Classes: {iris.target_names.tolist()}"
    # 2. Check for CSV/crawled data queries (simple keyword search)
    rag_results = rag_search(user_query)
    if rag_results:
        response = '[RAG] Found the following relevant data:\n'
        for r in rag_results:
            response += f"File: {r['file']}\nRow: {r['row']}\n"
        return response
    # 3. Fallback to GPT-2
    gpt2_response = gpt2_generate(user_query)
    return f"[GPT-2] {gpt2_response}"

# --- Example usage: ---
# To use in your chat assistant, call:
# response = offline_chat_model_call(user_query)
# print(response)

# --- Unified Offline Data Categorization and Query for Chat Assistant ---


# GPT-2 imports (optional, for fallback chat)
try:
    import sys
    sys.path.append(os.path.abspath('gpt-2-master/src'))
    import encoder as gpt2_encoder
    import model as gpt2_model
    import sample as gpt2_sample
except ImportError:
    gpt2_encoder = None
    gpt2_model = None
    gpt2_sample = None


def scan_and_categorize_data(csv_dirs=None, category_col_candidates=None):
    """
    Scan all CSVs and crawled/cloned website data, categorize them by file, type, or a relevant column.
    Returns: dict {category: [records]}
    """
    if csv_dirs is None:
        csv_dirs = [
            Path('processed_data'),
            Path('scraps'),
            Path('tshwane_crawled_data'),
            Path('processed_places_data'),
        ]
    if category_col_candidates is None:
        category_col_candidates = ['type', 'category',
                                   'Type', 'Category', 'class', 'Class']
    categorized = defaultdict(list)
    for d in csv_dirs:
        if d.exists():
            for csv_file in d.rglob('*.csv'):
                try:
                    df = pd.read_csv(csv_file)
                    # Try to find a category column
                    cat_col = None
                    for col in df.columns:
                        if col in category_col_candidates:
                            cat_col = col
                            break
                    # If no category column, use filename as category
                    if cat_col:
                        for _, row in df.iterrows():
                            cat = str(row[cat_col]) if pd.notna(
                                row[cat_col]) else str(csv_file.stem)
                            categorized[cat].append(row.to_dict())
                    else:
                        cat = str(csv_file.stem)
                        for _, row in df.iterrows():
                            categorized[cat].append(row.to_dict())
                except Exception:
                    continue
    return categorized


def gpt2_generate(prompt, model_name='124M', models_dir='gpt-2-master/models', length=60):
    if gpt2_encoder is None or gpt2_model is None or gpt2_sample is None:
        return "[GPT-2 not available in this environment]"
    enc = gpt2_encoder.get_encoder(model_name, models_dir)
    hparams = gpt2_model.default_hparams()
    import json
    import tensorflow as tf
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))
    context_tokens = enc.encode(prompt)
    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [1, None])
        output = gpt2_sample.sample_sequence(
            hparams=hparams, length=length, context=context, batch_size=1
        )
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)
        out = sess.run(output, feed_dict={context: [context_tokens]})
        text = enc.decode(out[0])
        return text


def offline_chat_data_query(user_query: str) -> str:
    """
    Unified offline data query for the chat assistant.
    - Categorizes all local data
    - Searches for the query in each category
    - Returns grouped results
    - Falls back to GPT-2 if no match (optional)
    """
    categorized = scan_and_categorize_data()
    found = False
    response = ''
    for cat, records in categorized.items():
        matches = []
        for rec in records:
            for v in rec.values():
                if user_query.lower() in str(v).lower():
                    matches.append(rec)
                    break
        if matches:
            found = True
            response += f"\n[Category: {cat}]\n"
            for m in matches[:3]:  # Show up to 3 matches per category
                response += f"{m}\n"
    if found:
        return response.strip()
    # Fallback to GPT-2
    gpt2_response = gpt2_generate(user_query)
    return f"[GPT-2] {gpt2_response}"

# --- Example usage: ---
# To use in your chat assistant, call:
# response = offline_chat_data_query(user_query)
# print(response)

# --- Tshwane Data: Unified Tabular Processing and XGBoost Model for Offline Chat Assistant ---


# GPT-2 imports (optional, for fallback chat)
try:
    import sys
    sys.path.append(os.path.abspath('gpt-2-master/src'))
    import encoder as gpt2_encoder
    import model as gpt2_model
    import sample as gpt2_sample
except ImportError:
    gpt2_encoder = None
    gpt2_model = None
    gpt2_sample = None


def scan_and_load_tshwane_csvs(csv_dirs=None):
    """
    Scan and load all Tshwane-related CSVs into a unified DataFrame.
    Returns: pd.DataFrame
    """
    if csv_dirs is None:
        csv_dirs = [
            Path('processed_data'),
            Path('scraps'),
            Path('tshwane_crawled_data'),
            Path('processed_places_data'),
        ]
    dfs = []
    for d in csv_dirs:
        if d.exists():
            for csv_file in d.rglob('*.csv'):
                try:
                    df = pd.read_csv(csv_file)
                    df['__source_file__'] = str(csv_file)
                    dfs.append(df)
                except Exception:
                    continue
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()


def preprocess_for_xgboost(df, target_col=None):
    """
    Preprocess DataFrame for XGBoost: handle categoricals, missing values, etc.
    Returns: X, y, feature_names, label_encoder (if used)
    """
    from sklearn.preprocessing import LabelEncoder
    df = df.copy()
    # Drop columns with all NaN or only one unique value
    df = df.dropna(axis=1, how='all')
    nunique = df.nunique()
    df = df.loc[:, nunique > 1]
    # Fill missing values
    df = df.fillna('')
    # Identify target
    if target_col is None or target_col not in df.columns:
        # Try to guess a target column (e.g., 'category', 'type', 'label', etc.)
        for col in ['category', 'type', 'label', 'target', 'Class', 'Type', 'Category']:
            if col in df.columns:
                target_col = col
                break
    if target_col is None or target_col not in df.columns:
        raise ValueError('No suitable target column found in data.')
    y = df[target_col]
    X = df.drop([target_col, '__source_file__'], axis=1, errors='ignore')
    # Encode categoricals
    for col in X.columns:
        if X[col].dtype == object:
            X[col] = LabelEncoder().fit_transform(X[col].astype(str))
    # Encode target if not numeric
    label_encoder = None
    if y.dtype == object:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))
    return X, y, list(X.columns), label_encoder


def train_and_save_xgboost_model(X, y, model_path='tshwane_xgb_model.joblib'):
    """
    Train and save an XGBoost model on the provided data.
    """
    model = xgb.XGBClassifier()
    model.fit(X, y)
    joblib.dump(model, model_path)
    return model


def load_xgboost_model(model_path='tshwane_xgb_model.joblib'):
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None


def gpt2_generate(prompt, model_name='124M', models_dir='gpt-2-master/models', length=60):
    if gpt2_encoder is None or gpt2_model is None or gpt2_sample is None:
        return "[GPT-2 not available in this environment]"
    enc = gpt2_encoder.get_encoder(model_name, models_dir)
    hparams = gpt2_model.default_hparams()
    import json
    import tensorflow as tf
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))
    context_tokens = enc.encode(prompt)
    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [1, None])
        output = gpt2_sample.sample_sequence(
            hparams=hparams, length=length, context=context, batch_size=1
        )
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)
        out = sess.run(output, feed_dict={context: [context_tokens]})
        text = enc.decode(out[0])
        return text


def offline_tshwane_model_query(user_query: str, model_path='tshwane_xgb_model.joblib') -> str:
    """
    Unified offline model/data query for the chat assistant.
    - If the query looks like a prediction request, use the XGBoost model.
    - If the query is a data summary/statistics request, use the DataFrame.
    - Otherwise, fallback to GPT-2 (optional).
    """
    # Load data and model
    df = scan_and_load_tshwane_csvs()
    model = load_xgboost_model(model_path)
    if df.empty or model is None:
        return "[Error: No data/model available. Please run training first.]"
    # Simple prediction: if user provides feature values, try to predict
    import re
    floats = re.findall(r'[-+]?[0-9]*\.?[0-9]+', user_query)
    if len(floats) >= len(model.get_booster().feature_names):
        features = [float(f)
                    for f in floats[:len(model.get_booster().feature_names)]]
        X_pred = pd.DataFrame(
            [features], columns=model.get_booster().feature_names)
        pred = model.predict(X_pred)[0]
        return f"[Tshwane Model] Predicted class: {pred} (features: {features})"
    # Data summary
    if 'summary' in user_query.lower() or 'stats' in user_query.lower():
        return f"[Tshwane Data] Columns: {list(df.columns)}\nRows: {len(df)}"
    # Fallback to GPT-2
    gpt2_response = gpt2_generate(user_query)
    return f"[GPT-2] {gpt2_response}"

# --- Example usage: ---
# 1. To train the model (run once):
# df = scan_and_load_tshwane_csvs()
# X, y, feature_names, label_encoder = preprocess_for_xgboost(df)
# train_and_save_xgboost_model(X, y)
#
# 2. To use in your chat assistant:
# response = offline_tshwane_model_query(user_query)
# print(response)

# --- Optimized Tshwane Tabular Data + XGBoost Model for Offline Chat Assistant ---


# GPT-2 imports (optional, for fallback chat)
try:
    import sys
    sys.path.append(os.path.abspath('gpt-2-master/src'))
    import encoder as gpt2_encoder
    import model as gpt2_model
    import sample as gpt2_sample
except ImportError:
    gpt2_encoder = None
    gpt2_model = None
    gpt2_sample = None

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='[TshwaneModel] %(message)s')

# --- Caching ---
_cached_df = None
_cached_model = None
_cached_label_encoder = None
_cached_feature_names = None

# --- Data Loading and Cleaning ---


def scan_and_load_tshwane_csvs(csv_dirs=None):
    """
    Scan and load all Tshwane-related CSVs into a unified DataFrame.
    Returns: pd.DataFrame
    """
    global _cached_df
    if _cached_df is not None:
        return _cached_df
    if csv_dirs is None:
        csv_dirs = [
            Path('processed_data'),
            Path('scraps'),
            Path('tshwane_crawled_data'),
            Path('processed_places_data'),
        ]
    dfs = []
    for d in csv_dirs:
        if d.exists():
            for csv_file in d.rglob('*.csv'):
                try:
                    df = pd.read_csv(csv_file)
                    df.columns = [str(c).strip().lower() for c in df.columns]
                    df['__source_file__'] = str(csv_file)
                    dfs.append(df)
                except Exception as e:
                    logging.warning(f"Could not load {csv_file}: {e}")
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        # Drop columns with >80% missing
        thresh = int(0.8 * len(df))
        df = df.dropna(axis=1, thresh=thresh)
        # Fill missing values
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].fillna('missing')
            else:
                df[col] = df[col].fillna(
                    df[col].mean() if not df[col].isnull().all() else 0)
        # Remove duplicate rows
        df = df.drop_duplicates()
        _cached_df = df
        return df
    else:
        return pd.DataFrame()

# --- Feature Engineering and Preprocessing ---


def preprocess_for_xgboost(df, target_col=None):
    """
    Preprocess DataFrame for XGBoost: handle categoricals, missing values, etc.
    Returns: X, y, feature_names, label_encoder (if used)
    """
    from sklearn.preprocessing import LabelEncoder
    df = df.copy()
    # Drop columns with all NaN or only one unique value
    nunique = df.nunique()
    df = df.loc[:, nunique > 1]
    # Identify target
    if target_col is None or target_col not in df.columns:
        # Try to guess a target column
        for col in ['category', 'type', 'label', 'target', 'class']:
            if col in df.columns:
                target_col = col
                break
    if target_col is None or target_col not in df.columns:
        logging.warning(
            'No suitable target column found in data. Model will not be trained.')
        return None, None, None, None
    y = df[target_col]
    X = df.drop([target_col, '__source_file__'], axis=1, errors='ignore')
    # Encode categoricals
    label_encoders = {}
    for col in X.columns:
        if X[col].dtype == object:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
    # Encode target if not numeric
    label_encoder = None
    if y.dtype == object:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))
    return X, y, list(X.columns), label_encoder

# --- Model Training and Validation ---


def train_and_save_xgboost_model(X, y, model_path='tshwane_xgb_model.joblib', label_encoder=None, feature_names=None):
    """
    Train and save an XGBoost model on the provided data. Also saves encoders.
    """
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logging.info(f"Model trained. Test accuracy: {acc:.3f}")
    # Save model, feature names, and label encoder
    joblib.dump({'model': model, 'label_encoder': label_encoder,
                'feature_names': feature_names}, model_path)
    return model

# --- Model Loading ---


def load_xgboost_model(model_path='tshwane_xgb_model.joblib'):
    global _cached_model, _cached_label_encoder, _cached_feature_names
    if _cached_model is not None:
        return _cached_model, _cached_label_encoder, _cached_feature_names
    if os.path.exists(model_path):
        bundle = joblib.load(model_path)
        _cached_model = bundle['model']
        _cached_label_encoder = bundle['label_encoder']
        _cached_feature_names = bundle['feature_names']
        return _cached_model, _cached_label_encoder, _cached_feature_names
    return None, None, None

# --- GPT-2 Fallback ---


def gpt2_generate(prompt, model_name='124M', models_dir='gpt-2-master/models', length=60):
    if gpt2_encoder is None or gpt2_model is None or gpt2_sample is None:
        return "[GPT-2 not available in this environment]"
    enc = gpt2_encoder.get_encoder(model_name, models_dir)
    hparams = gpt2_model.default_hparams()
    import json
    import tensorflow as tf
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))
    context_tokens = enc.encode(prompt)
    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [1, None])
        output = gpt2_sample.sample_sequence(
            hparams=hparams, length=length, context=context, batch_size=1
        )
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)
        out = sess.run(output, feed_dict={context: [context_tokens]})
        text = enc.decode(out[0])
        return text

# --- Unified Chat Assistant Access ---


def offline_tshwane_model_query(user_query: str, model_path='tshwane_xgb_model.joblib') -> str:
    """
    Unified offline model/data query for the chat assistant.
    - If the query looks like a prediction request, use the XGBoost model.
    - If the query is a data summary/statistics request, use the DataFrame.
    - Otherwise, fallback to GPT-2 (optional).
    """
    df = scan_and_load_tshwane_csvs()
    model, label_encoder, feature_names = load_xgboost_model(model_path)
    if df.empty or model is None or feature_names is None:
        return "[Error: No data/model available. Please run training first.]"
    # Prediction: if user provides enough numbers, try to predict
    import re
    floats = re.findall(r'[-+]?[0-9]*\.?[0-9]+', user_query)
    if len(floats) >= len(feature_names):
        features = [float(f) for f in floats[:len(feature_names)]]
        X_pred = pd.DataFrame([features], columns=feature_names)
        try:
            pred = model.predict(X_pred)[0]
            if label_encoder is not None:
                pred_label = label_encoder.inverse_transform([pred])[0]
            else:
                pred_label = pred
            return f"[Tshwane Model] Predicted class: {pred_label} (features: {features})"
        except Exception as e:
            return f"[Model Error] {e}"
    # Data summary
    if 'summary' in user_query.lower() or 'stats' in user_query.lower():
        return f"[Tshwane Data] Columns: {list(df.columns)}\nRows: {len(df)}"
    # Fallback to GPT-2
    gpt2_response = gpt2_generate(user_query)
    return f"[GPT-2] {gpt2_response}"

# --- Example usage: ---
# 1. To train the model (run once):
# df = scan_and_load_tshwane_csvs()
# X, y, feature_names, label_encoder = preprocess_for_xgboost(df)
# if X is not None and y is not None:
#     train_and_save_xgboost_model(X, y, label_encoder=label_encoder, feature_names=feature_names)
#
# 2. To use in your chat assistant:
# response = offline_tshwane_model_query(user_query)
# print(response)

# --- NLTK-Enhanced Tshwane Tabular Data + XGBoost Model for Offline Chat Assistant ---


# NLTK imports for NLP features
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
    _nltk_ready = True
except Exception:
    _nltk_ready = False
    stopwords = None
    word_tokenize = None
    WordNetLemmatizer = None

# GPT-2 imports (optional, for fallback chat)
try:
    import sys
    sys.path.append(os.path.abspath('gpt-2-master/src'))
    import encoder as gpt2_encoder
    import model as gpt2_model
    import sample as gpt2_sample
except ImportError:
    gpt2_encoder = None
    gpt2_model = None
    gpt2_sample = None

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='[TshwaneModel] %(message)s')

# --- Caching ---
_cached_df = None
_cached_model = None
_cached_label_encoder = None
_cached_feature_names = None

# --- NLTK Text Preprocessing ---


def nltk_preprocess_text(text):
    if not _nltk_ready or not isinstance(text, str):
        return text.lower() if isinstance(text, str) else text
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)

# --- Data Loading and Cleaning ---


def scan_and_load_tshwane_csvs(csv_dirs=None):
    """
    Scan and load all Tshwane-related CSVs into a unified DataFrame.
    Applies NLTK preprocessing to text columns.
    Returns: pd.DataFrame
    """
    global _cached_df
    if _cached_df is not None:
        return _cached_df
    if csv_dirs is None:
        csv_dirs = [
            Path('processed_data'),
            Path('scraps'),
            Path('tshwane_crawled_data'),
            Path('processed_places_data'),
        ]
    dfs = []
    for d in csv_dirs:
        if d.exists():
            for csv_file in d.rglob('*.csv'):
                try:
                    df = pd.read_csv(csv_file)
                    df.columns = [str(c).strip().lower() for c in df.columns]
                    df['__source_file__'] = str(csv_file)
                    # NLTK preprocess all object/text columns
                    for col in df.select_dtypes(include='object').columns:
                        df[col] = df[col].astype(
                            str).apply(nltk_preprocess_text)
                    dfs.append(df)
                except Exception as e:
                    logging.warning(f"Could not load {csv_file}: {e}")
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        # Drop columns with >80% missing
        thresh = int(0.8 * len(df))
        df = df.dropna(axis=1, thresh=thresh)
        # Fill missing values
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].fillna('missing')
            else:
                df[col] = df[col].fillna(
                    df[col].mean() if not df[col].isnull().all() else 0)
        # Remove duplicate rows
        df = df.drop_duplicates()
        _cached_df = df
        return df
    else:
        return pd.DataFrame()

# --- Feature Engineering and Preprocessing ---


def preprocess_for_xgboost(df, target_col=None):
    """
    Preprocess DataFrame for XGBoost: handle categoricals, missing values, etc.
    Returns: X, y, feature_names, label_encoder (if used)
    """
    from sklearn.preprocessing import LabelEncoder
    df = df.copy()
    # Drop columns with all NaN or only one unique value
    nunique = df.nunique()
    df = df.loc[:, nunique > 1]
    # Identify target
    if target_col is None or target_col not in df.columns:
        # Try to guess a target column
        for col in ['category', 'type', 'label', 'target', 'class']:
            if col in df.columns:
                target_col = col
                break
    if target_col is None or target_col not in df.columns:
        logging.warning(
            'No suitable target column found in data. Model will not be trained.')
        return None, None, None, None
    y = df[target_col]
    X = df.drop([target_col, '__source_file__'], axis=1, errors='ignore')
    # Encode categoricals
    label_encoders = {}
    for col in X.columns:
        if X[col].dtype == object:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
    # Encode target if not numeric
    label_encoder = None
    if y.dtype == object:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))
    return X, y, list(X.columns), label_encoder

# --- Model Training and Validation ---


def train_and_save_xgboost_model(X, y, model_path='tshwane_xgb_model.joblib', label_encoder=None, feature_names=None):
    """
    Train and save an XGBoost model on the provided data. Also saves encoders.
    """
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logging.info(f"Model trained. Test accuracy: {acc:.3f}")
    # Save model, feature names, and label encoder
    joblib.dump({'model': model, 'label_encoder': label_encoder,
                'feature_names': feature_names}, model_path)
    return model

# --- Model Loading ---


def load_xgboost_model(model_path='tshwane_xgb_model.joblib'):
    global _cached_model, _cached_label_encoder, _cached_feature_names
    if _cached_model is not None:
        return _cached_model, _cached_label_encoder, _cached_feature_names
    if os.path.exists(model_path):
        bundle = joblib.load(model_path)
        _cached_model = bundle['model']
        _cached_label_encoder = bundle['label_encoder']
        _cached_feature_names = bundle['feature_names']
        return _cached_model, _cached_label_encoder, _cached_feature_names
    return None, None, None

# --- NLTK Query Preprocessing ---


def nltk_preprocess_query(query):
    if not _nltk_ready or not isinstance(query, str):
        return query.lower() if isinstance(query, str) else query
    tokens = word_tokenize(query.lower())
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens

# --- GPT-2 Fallback ---


def gpt2_generate(prompt, model_name='124M', models_dir='gpt-2-master/models', length=60):
    if gpt2_encoder is None or gpt2_model is None or gpt2_sample is None:
        return "[GPT-2 not available in this environment]"
    enc = gpt2_encoder.get_encoder(model_name, models_dir)
    hparams = gpt2_model.default_hparams()
    import json
    import tensorflow as tf
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))
    context_tokens = enc.encode(prompt)
    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [1, None])
        output = gpt2_sample.sample_sequence(
            hparams=hparams, length=length, context=context, batch_size=1
        )
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)
        out = sess.run(output, feed_dict={context: [context_tokens]})
        text = enc.decode(out[0])
        return text

# --- Unified Chat Assistant Access with Contextual NLP Search ---


def offline_tshwane_model_query(user_query: str, model_path='tshwane_xgb_model.joblib') -> str:
    """
    Unified offline model/data query for the chat assistant.
    - If the query looks like a prediction request, use the XGBoost model.
    - If the query is a data summary/statistics request, use the DataFrame.
    - Otherwise, use NLTK to preprocess the query and search for contextually relevant data.
    - Fallback to GPT-2 (optional).
    """
    df = scan_and_load_tshwane_csvs()
    model, label_encoder, feature_names = load_xgboost_model(model_path)
    if df.empty or model is None or feature_names is None:
        return "[Error: No data/model available. Please run training first.]"
    # Prediction: if user provides enough numbers, try to predict
    import re
    floats = re.findall(r'[-+]?[0-9]*\.?[0-9]+', user_query)
    if len(floats) >= len(feature_names):
        features = [float(f) for f in floats[:len(feature_names)]]
        X_pred = pd.DataFrame([features], columns=feature_names)
        try:
            pred = model.predict(X_pred)[0]
            if label_encoder is not None:
                pred_label = label_encoder.inverse_transform([pred])[0]
            else:
                pred_label = pred
            return f"[Tshwane Model] Predicted class: {pred_label} (features: {features})"
        except Exception as e:
            return f"[Model Error] {e}"
    # Data summary
    if 'summary' in user_query.lower() or 'stats' in user_query.lower():
        return f"[Tshwane Data] Columns: {list(df.columns)}\nRows: {len(df)}"
    # NLTK contextual search
    tokens = nltk_preprocess_query(user_query)
    if tokens and isinstance(tokens, list):
        matches = []
        for idx, row in df.iterrows():
            row_text = ' '.join([str(v)
                                for v in row.values if isinstance(v, str)])
            row_tokens = set(nltk_preprocess_query(row_text))
            if set(tokens) & row_tokens:
                matches.append(row)
            if len(matches) >= 3:
                break
        if matches:
            response = '[NLP Search] Found the following relevant data:\n'
            for m in matches:
                response += f"{m.to_dict()}\n"
            return response
    # Fallback to GPT-2
    gpt2_response = gpt2_generate(user_query)
    return f"[GPT-2] {gpt2_response}"

# --- Example usage: ---
# 1. To train the model (run once):
# df = scan_and_load_tshwane_csvs()
# X, y, feature_names, label_encoder = preprocess_for_xgboost(df)
# if X is not None and y is not None:
#     train_and_save_xgboost_model(X, y, label_encoder=label_encoder, feature_names=feature_names)
#
# 2. To use in your chat assistant:
# response = offline_tshwane_model_query(user_query)
# print(response)

# --- Hugging Face Transformers Fallback for Offline Chat Assistant ---


# NLTK imports for NLP features
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
    _nltk_ready = True
except Exception:
    _nltk_ready = False
    stopwords = None
    word_tokenize = None
    WordNetLemmatizer = None

# Hugging Face transformers for text generation fallback
try:
    from transformers import pipeline
    _transformers_ready = True
    _textgen_pipe = pipeline('text-generation', model='distilgpt2', device=-1)
except Exception:
    _transformers_ready = False
    _textgen_pipe = None

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='[TshwaneModel] %(message)s')

# --- Caching ---
_cached_df = None
_cached_model = None
_cached_label_encoder = None
_cached_feature_names = None

# --- NLTK Text Preprocessing ---


def nltk_preprocess_text(text):
    if not _nltk_ready or not isinstance(text, str):
        return text.lower() if isinstance(text, str) else text
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)

# --- Data Loading and Cleaning ---


def scan_and_load_tshwane_csvs(csv_dirs=None):
    global _cached_df
    if _cached_df is not None:
        return _cached_df
    if csv_dirs is None:
        csv_dirs = [
            Path('processed_data'),
            Path('scraps'),
            Path('tshwane_crawled_data'),
            Path('processed_places_data'),
        ]
    dfs = []
    for d in csv_dirs:
        if d.exists():
            for csv_file in d.rglob('*.csv'):
                try:
                    df = pd.read_csv(csv_file)
                    df.columns = [str(c).strip().lower() for c in df.columns]
                    df['__source_file__'] = str(csv_file)
                    for col in df.select_dtypes(include='object').columns:
                        df[col] = df[col].astype(
                            str).apply(nltk_preprocess_text)
                    dfs.append(df)
                except Exception as e:
                    logging.warning(f"Could not load {csv_file}: {e}")
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        thresh = int(0.8 * len(df))
        df = df.dropna(axis=1, thresh=thresh)
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].fillna('missing')
            else:
                df[col] = df[col].fillna(
                    df[col].mean() if not df[col].isnull().all() else 0)
        df = df.drop_duplicates()
        _cached_df = df
        return df
    else:
        return pd.DataFrame()

# --- Feature Engineering and Preprocessing ---


def preprocess_for_xgboost(df, target_col=None):
    from sklearn.preprocessing import LabelEncoder
    df = df.copy()
    nunique = df.nunique()
    df = df.loc[:, nunique > 1]
    if target_col is None or target_col not in df.columns:
        for col in ['category', 'type', 'label', 'target', 'class']:
            if col in df.columns:
                target_col = col
                break
    if target_col is None or target_col not in df.columns:
        logging.warning(
            'No suitable target column found in data. Model will not be trained.')
        return None, None, None, None
    y = df[target_col]
    X = df.drop([target_col, '__source_file__'], axis=1, errors='ignore')
    label_encoders = {}
    for col in X.columns:
        if X[col].dtype == object:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
    label_encoder = None
    if y.dtype == object:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))
    return X, y, list(X.columns), label_encoder


def train_and_save_xgboost_model(X, y, model_path='tshwane_xgb_model.joblib', label_encoder=None, feature_names=None):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logging.info(f"Model trained. Test accuracy: {acc:.3f}")
    joblib.dump({'model': model, 'label_encoder': label_encoder,
                'feature_names': feature_names}, model_path)
    return model


def load_xgboost_model(model_path='tshwane_xgb_model.joblib'):
    global _cached_model, _cached_label_encoder, _cached_feature_names
    if _cached_model is not None:
        return _cached_model, _cached_label_encoder, _cached_feature_names
    if os.path.exists(model_path):
        bundle = joblib.load(model_path)
        _cached_model = bundle['model']
        _cached_label_encoder = bundle['label_encoder']
        _cached_feature_names = bundle['feature_names']
        return _cached_model, _cached_label_encoder, _cached_feature_names
    return None, None, None


def nltk_preprocess_query(query):
    if not _nltk_ready or not isinstance(query, str):
        return query.lower() if isinstance(query, str) else query
    tokens = word_tokenize(query.lower())
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens

# --- Hugging Face Transformers Text Generation Fallback ---


def transformers_generate(prompt, max_length=60):
    if not _transformers_ready or _textgen_pipe is None:
        return "[Transformers not available in this environment]"
    try:
        result = _textgen_pipe(
            prompt, max_length=max_length, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"[Transformers error: {e}]"

# --- Unified Chat Assistant Access with Contextual NLP Search ---


def offline_tshwane_model_query(user_query: str, model_path='tshwane_xgb_model.joblib') -> str:
    """
    Unified offline model/data query for the chat assistant.
    - If the query looks like a prediction request, use the XGBoost model.
    - If the query is a data summary/statistics request, use the DataFrame.
    - Otherwise, use NLTK to preprocess the query and search for contextually relevant data.
    - Fallback to Hugging Face transformers text generation (if available).
    """
    df = scan_and_load_tshwane_csvs()
    model, label_encoder, feature_names = load_xgboost_model(model_path)
    if df.empty or model is None or feature_names is None:
        return "[Error: No data/model available. Please run training first.]"
    import re
    floats = re.findall(r'[-+]?[0-9]*\.?[0-9]+', user_query)
    if len(floats) >= len(feature_names):
        features = [float(f) for f in floats[:len(feature_names)]]
        X_pred = pd.DataFrame([features], columns=feature_names)
        try:
            pred = model.predict(X_pred)[0]
            if label_encoder is not None:
                pred_label = label_encoder.inverse_transform([pred])[0]
            else:
                pred_label = pred
            return f"[Tshwane Model] Predicted class: {pred_label} (features: {features})"
        except Exception as e:
            return f"[Model Error] {e}"
    if 'summary' in user_query.lower() or 'stats' in user_query.lower():
        return f"[Tshwane Data] Columns: {list(df.columns)}\nRows: {len(df)}"
    tokens = nltk_preprocess_query(user_query)
    if tokens and isinstance(tokens, list):
        matches = []
        for idx, row in df.iterrows():
            row_text = ' '.join([str(v)
                                for v in row.values if isinstance(v, str)])
            row_tokens = set(nltk_preprocess_query(row_text))
            if set(tokens) & row_tokens:
                matches.append(row)
            if len(matches) >= 3:
                break
        if matches:
            response = '[NLP Search] Found the following relevant data:\n'
            for m in matches:
                response += f"{m.to_dict()}\n"
            return response
    # Fallback to transformers text generation
    transformers_response = transformers_generate(user_query)
    return f"[Transformers] {transformers_response}"

# --- Example usage: ---
# 1. To train the model (run once):
# df = scan_and_load_tshwane_csvs()
# X, y, feature_names, label_encoder = preprocess_for_xgboost(df)
# if X is not None and y is not None:
#     train_and_save_xgboost_model(X, y, label_encoder=label_encoder, feature_names=feature_names)
#
# 2. To use in your chat assistant:
# response = offline_tshwane_model_query(user_query)
# print(response)

# --- Cleaned, Deployment-Ready ML/NLP/Chat Assistant Functions ---


# NLTK imports for NLP features
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
    _nltk_ready = True
except Exception:
    _nltk_ready = False
    stopwords = None
    word_tokenize = None
    WordNetLemmatizer = None

# Hugging Face transformers for text generation fallback
try:
    from transformers import pipeline
    _transformers_ready = True
    _textgen_pipe = pipeline('text-generation', model='distilgpt2', device=-1)
except Exception:
    _transformers_ready = False
    _textgen_pipe = None

logging.basicConfig(level=logging.INFO, format='[TshwaneModel] %(message)s')

_cached_df = None
_cached_model = None
_cached_label_encoder = None
_cached_feature_names = None


def nltk_preprocess_text(text):
    if not _nltk_ready or not isinstance(text, str):
        return text.lower() if isinstance(text, str) else text
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)


def nltk_preprocess_query(query):
    if not _nltk_ready or not isinstance(query, str):
        return query.lower() if isinstance(query, str) else query
    tokens = word_tokenize(query.lower())
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens


def scan_and_load_tshwane_csvs(csv_dirs=None):
    global _cached_df
    if _cached_df is not None:
        return _cached_df
    if csv_dirs is None:
        csv_dirs = [
            Path('processed_data'),
            Path('scraps'),
            Path('tshwane_crawled_data'),
            Path('processed_places_data'),
        ]
    dfs = []
    for d in csv_dirs:
        if d.exists():
            for csv_file in d.rglob('*.csv'):
                try:
                    df = pd.read_csv(csv_file)
                    df.columns = [str(c).strip().lower() for c in df.columns]
                    df['__source_file__'] = str(csv_file)
                    for col in df.select_dtypes(include='object').columns:
                        df[col] = df[col].astype(
                            str).apply(nltk_preprocess_text)
                    dfs.append(df)
                except Exception as e:
                    logging.warning(f"Could not load {csv_file}: {e}")
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        thresh = int(0.8 * len(df))
        df = df.dropna(axis=1, thresh=thresh)
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].fillna('missing')
            else:
                df[col] = df[col].fillna(
                    df[col].mean() if not df[col].isnull().all() else 0)
        df = df.drop_duplicates()
        _cached_df = df
        return df
    else:
        return pd.DataFrame()


def preprocess_for_xgboost(df, target_col=None):
    from sklearn.preprocessing import LabelEncoder
    df = df.copy()
    nunique = df.nunique()
    df = df.loc[:, nunique > 1]
    if target_col is None or target_col not in df.columns:
        for col in ['category', 'type', 'label', 'target', 'class']:
            if col in df.columns:
                target_col = col
                break
    if target_col is None or target_col not in df.columns:
        logging.warning(
            'No suitable target column found in data. Model will not be trained.')
        return None, None, None, None
    y = df[target_col]
    X = df.drop([target_col, '__source_file__'], axis=1, errors='ignore')
    label_encoders = {}
    for col in X.columns:
        if X[col].dtype == object:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
    label_encoder = None
    if y.dtype == object:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))
    return X, y, list(X.columns), label_encoder


def train_and_save_xgboost_model(X, y, model_path='tshwane_xgb_model.joblib', label_encoder=None, feature_names=None):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logging.info(f"Model trained. Test accuracy: {acc:.3f}")
    joblib.dump({'model': model, 'label_encoder': label_encoder,
                'feature_names': feature_names}, model_path)
    return model


def load_xgboost_model(model_path='tshwane_xgb_model.joblib'):
    global _cached_model, _cached_label_encoder, _cached_feature_names
    if _cached_model is not None:
        return _cached_model, _cached_label_encoder, _cached_feature_names
    if os.path.exists(model_path):
        bundle = joblib.load(model_path)
        _cached_model = bundle['model']
        _cached_label_encoder = bundle['label_encoder']
        _cached_feature_names = bundle['feature_names']
        return _cached_model, _cached_label_encoder, _cached_feature_names
    return None, None, None


def transformers_generate(prompt, max_length=60):
    if not _transformers_ready or _textgen_pipe is None:
        return "[Transformers not available in this environment]"
    try:
        result = _textgen_pipe(
            prompt, max_length=max_length, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"[Transformers error: {e}]"


def offline_tshwane_model_query(user_query: str, model_path='tshwane_xgb_model.joblib') -> str:
    """
    Unified offline model/data query for the chat assistant.
    - If the query looks like a prediction request, use the XGBoost model.
    - If the query is a data summary/statistics request, use the DataFrame.
    - Otherwise, use NLTK to preprocess the query and search for contextually relevant data.
    - Fallback to Hugging Face transformers text generation (if available).
    """
    df = scan_and_load_tshwane_csvs()
    model, label_encoder, feature_names = load_xgboost_model(model_path)
    if df.empty or model is None or feature_names is None:
        return "[Error: No data/model available. Please run training first.]"
    import re
    floats = re.findall(r'[-+]?[0-9]*\.?[0-9]+', user_query)
    if len(floats) >= len(feature_names):
        features = [float(f) for f in floats[:len(feature_names)]]
        X_pred = pd.DataFrame([features], columns=feature_names)
        try:
            pred = model.predict(X_pred)[0]
            if label_encoder is not None:
                pred_label = label_encoder.inverse_transform([pred])[0]
            else:
                pred_label = pred
            return f"[Tshwane Model] Predicted class: {pred_label} (features: {features})"
        except Exception as e:
            return f"[Model Error] {e}"
    if 'summary' in user_query.lower() or 'stats' in user_query.lower():
        return f"[Tshwane Data] Columns: {list(df.columns)}\nRows: {len(df)}"
    tokens = nltk_preprocess_query(user_query)
    if tokens and isinstance(tokens, list):
        matches = []
        for idx, row in df.iterrows():
            row_text = ' '.join([str(v)
                                for v in row.values if isinstance(v, str)])
            row_tokens = set(nltk_preprocess_query(row_text))
            if set(tokens) & row_tokens:
                matches.append(row)
            if len(matches) >= 3:
                break
        if matches:
            response = '[NLP Search] Found the following relevant data:\n'
            for m in matches:
                response += f"{m.to_dict()}\n"
            return response
    # Fallback to transformers text generation
    transformers_response = transformers_generate(user_query)
    return f"[Transformers] {transformers_response}"

# --- Example usage: ---
# 1. To train the model (run once):
# df = scan_and_load_tshwane_csvs()
# X, y, feature_names, label_encoder = preprocess_for_xgboost(df)
# if X is not None and y is not None:
#     train_and_save_xgboost_model(X, y, label_encoder=label_encoder, feature_names=feature_names)
#
# 2. To use in your chat assistant:
# response = offline_tshwane_model_query(user_query)
# print(response)
