# 🌿 Tshwane Tourism Data Processing Suite

A comprehensive data processing solution for the Tshwane Tourism Association that integrates multiple AI agents and uses Hugging Face models to avoid API dependencies.

## 🎯 Overview

This project processes data from the Tshwane Tourism website (http://www.visittshwane.co.za) and creates an interactive tourism portal with the following capabilities:

- **Website Scraping & Data Extraction**
- **AI-Powered Content Analysis** 
- **Interactive Tourism Portal**
- **Booking System with Encryption**
- **Weather-Based Recommendations**
- **Integration with Existing AI Agents**

## 📁 Project Structure

```
Tshwane_Tourism_Association/
├── tshwane_tourism_app.py          # Main Streamlit application
├── data_processor.py               # Core data processing module
├── integrated_data_processor.py    # Integration with existing AI agents
├── requirements.txt                # Python dependencies
├── processed_data/                 # Generated data files
├── ai_data_analysis_agent/         # Existing data analysis agent
├── ai_data_visualisation_agent/    # Existing visualization agent
├── ai_travel_agent/               # Existing travel planning agent
├── customer_support_voice_agent/   # Existing voice support agent
└── opeani_research_agent/         # Existing research agent
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Main Application

```bash
streamlit run tshwane_tourism_app.py
```

### 3. Run the Integrated Data Processor

```bash
streamlit run integrated_data_processor.py
```

## 🔧 Features & Capabilities

### 🌐 Website Data Processing

The system automatically:
- Scrapes the Tshwane Tourism website
- Extracts places, restaurants, events, and accommodations
- Collects contact information and social media links
- Processes images and multimedia content
- Saves data in structured formats (CSV, JSON)

### 🤖 AI-Powered Analysis

Using Hugging Face models (no API keys required):
- **Content Categorization**: Automatically categorizes content into tourism types
- **Sentiment Analysis**: Analyzes visitor sentiment about places and services
- **Entity Recognition**: Extracts important entities (places, people, organizations)
- **Text Summarization**: Creates concise summaries of long content
- **Zero-Shot Classification**: Classifies content without training data

### 📊 Data Integration

Integrates with existing AI agents:
- **Data Analysis Agent**: Processes CSV/Excel files with natural language queries
- **Visualization Agent**: Creates interactive charts and graphs
- **Travel Agent**: Provides travel planning capabilities
- **Research Agent**: Conducts comprehensive research
- **Voice Agent**: Provides voice-powered responses

### 🌤️ Smart Recommendations

Weather-based place suggestions:
- **Sunny**: Outdoor parks, gardens, monuments
- **Rainy**: Museums, galleries, indoor attractions
- **Cloudy**: Walking tours, historic sites
- **Hot**: Shaded areas, air-conditioned venues
- **Cold**: Indoor venues, warm environments

### 📝 Booking System

Secure booking functionality:
- **Form Validation**: Ensures all required fields are completed
- **Data Encryption**: Uses Fernet encryption for sensitive data
- **Email Integration**: Sends booking details to secretary@tshwanetourism.com
- **WhatsApp Integration**: Collects WhatsApp numbers for notifications
- **Booking Tracking**: Generates unique booking IDs

## 🎨 User Interface Features

### Nature-Themed Design
- Gradient backgrounds inspired by outdoor dining
- Smooth animations and transitions
- Responsive layout for all devices
- Interactive gallery with scrolling animations

### Interactive Components
- **Map Integration**: Embedded Tshwane tourism map
- **Gallery Navigation**: Previous/Next buttons with smooth transitions
- **Real-time Notifications**: Booking confirmations and updates
- **Weather Widget**: Dynamic weather-based suggestions

## 📈 Data Output Formats

The system generates multiple data formats:

### CSV Files
- `tshwane_places.csv` - Tourist attractions and places
- `tshwane_restaurants.csv` - Dining establishments
- `tshwane_social_links.csv` - Social media links
- `tshwane_contacts.csv` - Contact information
- `booking_[ID].csv` - Individual booking records

### JSON Files
- `processed_tshwane_data.json` - Complete processed dataset
- `analyzed_content.json` - AI analysis results
- `processing_summary.json` - Processing statistics

### Encrypted Files
- `encrypted_booking_[ID].txt` - Encrypted booking data
- `key_[ID].key` - Encryption keys (stored separately)

## 🔒 Security Features

### Data Encryption
- **Fernet Encryption**: Industry-standard symmetric encryption
- **Separate Key Storage**: Keys stored separately from encrypted data
- **Secure Transmission**: Encrypted data for email transmission

### Privacy Protection
- **Data Anonymization**: Personal data is encrypted before storage
- **Secure Forms**: Form validation and sanitization
- **Network Security**: Protection against data sniffing

## 🌍 Integration Capabilities

### Existing AI Agents
The system seamlessly integrates with your existing agents:

1. **AI Data Analysis Agent**
   - Processes uploaded CSV/Excel files
   - Generates SQL queries from natural language
   - Provides statistical analysis

2. **AI Data Visualization Agent**
   - Creates interactive charts and graphs
   - Supports multiple chart types
   - Generates insights from visualizations

3. **AI Travel Agent**
   - Plans personalized itineraries
   - Researches destinations and activities
   - Provides travel recommendations

4. **Customer Support Voice Agent**
   - Processes documentation queries
   - Provides voice responses
   - Handles customer support requests

5. **Research Agent**
   - Conducts comprehensive web research
   - Generates detailed reports
   - Provides fact-checking capabilities

### Hugging Face Models Used

- **facebook/bart-large-mnli**: Zero-shot classification
- **cardiffnlp/twitter-roberta-base-sentiment-latest**: Sentiment analysis
- **dbmdz/bert-large-cased-finetuned-conll03-english**: Named entity recognition
- **facebook/bart-large-cnn**: Text summarization
- **distilbert-base-uncased**: Fallback classification

## 📊 Usage Examples

### 1. Process Website Data

```python
from data_processor import TshwaneDataProcessor

processor = TshwaneDataProcessor()
processed_data = processor.scrape_website_comprehensive()
```

### 2. Analyze Content with AI

```python
from integrated_data_processor import IntegratedTshwaneProcessor

processor = IntegratedTshwaneProcessor()
analyzed_content = processor.analyze_tourism_content(content_list)
dataframes = processor.create_tourism_dataframes(analyzed_content)
```

### 3. Generate Weather Recommendations

```python
recommendations = processor.generate_weather_recommendations(
    places_df, "sunny"
)
```

## 🎯 Business Impact

### For Tshwane Tourism Association
- **Automated Data Processing**: Reduces manual data entry
- **Enhanced Customer Experience**: Interactive booking system
- **Data-Driven Insights**: AI-powered analytics
- **Secure Operations**: Encrypted data handling

### For Visitors
- **Easy Discovery**: Interactive place gallery
- **Smart Recommendations**: Weather-based suggestions
- **Seamless Booking**: One-click reservation system
- **Real-time Updates**: Instant booking confirmations

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```
ENCRYPTION_KEY=your_encryption_key_here
SMTP_SERVER=your_smtp_server
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_password
```

### Customization Options
- **Color Themes**: Modify CSS in `tshwane_tourism_app.py`
- **AI Models**: Change models in `integrated_data_processor.py`
- **Data Sources**: Update URLs in `data_processor.py`

## 📞 Support & Contact

**Created by:** Profit Projects Online Virtual Assistance  
**Enterprise Number:** K2025200646  
**Contact:** Thapelo Kgothatso Thooe  
**Email:** kgothatsothooe@gmail.com  

**Tshwane Tourism Association**  
**Secretary Email:** secretary@tshwanetourism.com  

## 🚀 Deployment

The application is designed for immediate deployment:

1. **Local Development**: Run with Streamlit
2. **Cloud Deployment**: Compatible with Streamlit Cloud, Heroku, AWS
3. **Docker Support**: Containerization ready
4. **Scalable Architecture**: Handles multiple concurrent users

## 📝 License

This project is created for the Tshwane Tourism Association and Profit Projects Online Virtual Assistance.

---

*Experience the beauty of Tshwane with our AI-powered tourism platform! 🌿*
