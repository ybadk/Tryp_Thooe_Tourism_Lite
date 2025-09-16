"""
Data Processing Module for Tshwane Tourism Application
Integrates with existing AI agents for comprehensive data analysis
"""

import pandas as pd
import json
import os
import sys
from pathlib import Path
import streamlit as st
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TshwaneDataProcessor:
    """Main data processor for Tshwane Tourism data"""
    
    def __init__(self):
        self.base_url = "http://www.visittshwane.co.za"
        self.data_folder = "processed_data"
        self.ensure_data_folder()
        
        # Initialize Hugging Face models
        self.sentiment_analyzer = None
        self.text_classifier = None
        self.load_models()
    
    def ensure_data_folder(self):
        """Create data folder if it doesn't exist"""
        Path(self.data_folder).mkdir(exist_ok=True)
    
    def load_models(self):
        """Load Hugging Face models for processing"""
        try:
            # Load sentiment analysis model
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )
            
            # Load text classification model
            self.text_classifier = pipeline(
                "text-classification",
                model="facebook/bart-large-mnli"
            )
            
            logger.info("✅ Hugging Face models loaded successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not load some models: {e}")
    
    def scrape_website_comprehensive(self):
        """Comprehensive website scraping with data categorization"""
        try:
            logger.info("🌐 Starting comprehensive website scraping...")
            
            # Main page scraping
            main_data = self.scrape_page(self.base_url)
            
            # Discover additional pages
            additional_pages = self.discover_pages(main_data.get('links', []))
            
            # Scrape additional pages
            all_data = {'main': main_data, 'pages': {}}
            
            for page_url in additional_pages[:10]:  # Limit to 10 additional pages
                try:
                    page_data = self.scrape_page(page_url)
                    page_name = self.extract_page_name(page_url)
                    all_data['pages'][page_name] = page_data
                    logger.info(f"✅ Scraped: {page_name}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to scrape {page_url}: {e}")
            
            # Process and categorize data
            processed_data = self.process_scraped_data(all_data)
            
            # Save processed data
            self.save_processed_data(processed_data)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"❌ Error in comprehensive scraping: {e}")
            return None
    
    def scrape_page(self, url):
        """Scrape a single page"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'url': url,
            'title': soup.find('title').text if soup.find('title') else '',
            'content': soup.get_text(),
            'links': [link.get('href') for link in soup.find_all('a', href=True)],
            'images': [img.get('src') for img in soup.find_all('img', src=True)],
            'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
            'paragraphs': [p.get_text(strip=True) for p in soup.find_all('p')],
            'scraped_at': datetime.now().isoformat()
        }
    
    def discover_pages(self, links):
        """Discover relevant pages from links"""
        relevant_pages = []
        base_domain = "visittshwane.co.za"
        
        for link in links:
            if link and base_domain in str(link):
                if not any(skip in str(link).lower() for skip in ['javascript:', 'mailto:', '#']):
                    if link.startswith('/'):
                        link = self.base_url + link
                    relevant_pages.append(link)
        
        return list(set(relevant_pages))  # Remove duplicates
    
    def extract_page_name(self, url):
        """Extract a clean page name from URL"""
        return url.split('/')[-1].replace('.html', '').replace('.php', '') or 'home'
    
    def process_scraped_data(self, all_data):
        """Process and categorize scraped data using AI models"""
        logger.info("🤖 Processing data with AI models...")
        
        processed = {
            'places': [],
            'restaurants': [],
            'events': [],
            'accommodations': [],
            'activities': [],
            'contact_info': {},
            'social_links': [],
            'images': [],
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'total_pages': len(all_data.get('pages', {})) + 1
            }
        }
        
        # Process all content
        all_content = []
        all_content.extend(all_data['main'].get('paragraphs', []))
        all_content.extend(all_data['main'].get('headings', []))
        
        for page_data in all_data.get('pages', {}).values():
            all_content.extend(page_data.get('paragraphs', []))
            all_content.extend(page_data.get('headings', []))
        
        # Categorize content using AI
        for content in all_content:
            if len(content.strip()) < 10:  # Skip very short content
                continue
                
            category = self.categorize_content(content)
            processed[category].append({
                'text': content,
                'sentiment': self.analyze_sentiment(content),
                'category': category,
                'processed_at': datetime.now().isoformat()
            })
        
        # Extract specific information
        processed['contact_info'] = self.extract_contact_information(all_content)
        processed['social_links'] = self.extract_social_media_links(all_data)
        processed['images'] = self.collect_images(all_data)
        
        return processed
    
    def categorize_content(self, text):
        """Categorize content using AI classification"""
        if not self.text_classifier:
            return self.simple_categorize(text)
        
        try:
            # Define categories for classification
            categories = [
                "places and attractions",
                "restaurants and dining",
                "events and activities", 
                "accommodations and hotels",
                "general information"
            ]
            
            # Use zero-shot classification
            result = self.text_classifier(text, categories)
            
            # Map to our category structure
            category_mapping = {
                "places and attractions": "places",
                "restaurants and dining": "restaurants", 
                "events and activities": "events",
                "accommodations and hotels": "accommodations",
                "general information": "activities"
            }
            
            predicted_category = result['labels'][0]
            return category_mapping.get(predicted_category, "activities")
            
        except Exception as e:
            logger.warning(f"AI categorization failed: {e}")
            return self.simple_categorize(text)
    
    def simple_categorize(self, text):
        """Simple rule-based categorization as fallback"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['restaurant', 'cafe', 'dining', 'food', 'cuisine']):
            return 'restaurants'
        elif any(word in text_lower for word in ['hotel', 'accommodation', 'lodge', 'guesthouse']):
            return 'accommodations'
        elif any(word in text_lower for word in ['event', 'festival', 'concert', 'show']):
            return 'events'
        elif any(word in text_lower for word in ['museum', 'park', 'monument', 'attraction']):
            return 'places'
        else:
            return 'activities'
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        if not self.sentiment_analyzer:
            return {'label': 'NEUTRAL', 'score': 0.5}
        
        try:
            result = self.sentiment_analyzer(text[:512])  # Limit text length
            return result[0] if result else {'label': 'NEUTRAL', 'score': 0.5}
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5}
    
    def extract_contact_information(self, content_list):
        """Extract contact information from content"""
        contact_info = {
            'emails': [],
            'phones': [],
            'addresses': [],
            'websites': []
        }
        
        all_text = ' '.join(content_list)
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        contact_info['emails'] = list(set(re.findall(email_pattern, all_text)))
        
        # Phone pattern (South African)
        phone_pattern = r'(\+27|0)[0-9\s\-\(\)]{8,15}'
        contact_info['phones'] = list(set(re.findall(phone_pattern, all_text)))
        
        # Website pattern
        website_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        contact_info['websites'] = list(set(re.findall(website_pattern, all_text)))
        
        return contact_info
    
    def extract_social_media_links(self, all_data):
        """Extract social media links"""
        social_links = []
        social_platforms = {
            'facebook': r'facebook\.com',
            'twitter': r'twitter\.com',
            'instagram': r'instagram\.com',
            'linkedin': r'linkedin\.com',
            'youtube': r'youtube\.com',
            'tiktok': r'tiktok\.com'
        }
        
        # Collect all links
        all_links = []
        all_links.extend(all_data['main'].get('links', []))
        for page_data in all_data.get('pages', {}).values():
            all_links.extend(page_data.get('links', []))
        
        for link in all_links:
            if not link:
                continue
                
            for platform, pattern in social_platforms.items():
                if re.search(pattern, str(link), re.IGNORECASE):
                    social_links.append({
                        'platform': platform,
                        'url': link,
                        'found_at': datetime.now().isoformat()
                    })
        
        return social_links
    
    def collect_images(self, all_data):
        """Collect and categorize images"""
        images = []
        
        # Collect all image URLs
        all_images = []
        all_images.extend(all_data['main'].get('images', []))
        for page_data in all_data.get('pages', {}).values():
            all_images.extend(page_data.get('images', []))
        
        for img_url in all_images:
            if img_url:
                images.append({
                    'url': img_url,
                    'type': self.categorize_image(img_url),
                    'collected_at': datetime.now().isoformat()
                })
        
        return images
    
    def categorize_image(self, img_url):
        """Simple image categorization based on URL/filename"""
        img_lower = str(img_url).lower()
        
        if any(word in img_lower for word in ['logo', 'brand']):
            return 'logo'
        elif any(word in img_lower for word in ['gallery', 'photo', 'image']):
            return 'gallery'
        elif any(word in img_lower for word in ['banner', 'header', 'hero']):
            return 'banner'
        else:
            return 'general'
    
    def save_processed_data(self, processed_data):
        """Save processed data to various formats"""
        try:
            # Save as JSON
            with open(f"{self.data_folder}/processed_tshwane_data.json", 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2, ensure_ascii=False)
            
            # Save individual categories as CSV
            for category in ['places', 'restaurants', 'events', 'accommodations', 'activities']:
                if processed_data[category]:
                    df = pd.DataFrame(processed_data[category])
                    df.to_csv(f"{self.data_folder}/tshwane_{category}.csv", index=False)
            
            # Save contact info as CSV
            if processed_data['contact_info']:
                contact_df = pd.DataFrame([processed_data['contact_info']])
                contact_df.to_csv(f"{self.data_folder}/tshwane_contacts.csv", index=False)
            
            # Save social links as CSV
            if processed_data['social_links']:
                social_df = pd.DataFrame(processed_data['social_links'])
                social_df.to_csv(f"{self.data_folder}/tshwane_social_links.csv", index=False)
            
            logger.info(f"✅ Data saved to {self.data_folder}/")
            
        except Exception as e:
            logger.error(f"❌ Error saving data: {e}")
    
    def analyze_with_existing_agents(self, data_file):
        """Integrate with existing AI agents for analysis"""
        try:
            # This would integrate with your existing agents
            # For now, we'll create a summary analysis
            
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                analysis = {
                    'summary': {
                        'total_places': len(data.get('places', [])),
                        'total_restaurants': len(data.get('restaurants', [])),
                        'total_events': len(data.get('events', [])),
                        'total_accommodations': len(data.get('accommodations', [])),
                        'sentiment_distribution': self.calculate_sentiment_distribution(data)
                    },
                    'recommendations': self.generate_recommendations(data),
                    'analysis_date': datetime.now().isoformat()
                }
                
                # Save analysis
                with open(f"{self.data_folder}/data_analysis.json", 'w') as f:
                    json.dump(analysis, f, indent=2)
                
                return analysis
            
        except Exception as e:
            logger.error(f"❌ Error in analysis: {e}")
            return None
    
    def calculate_sentiment_distribution(self, data):
        """Calculate sentiment distribution across content"""
        sentiments = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
        
        for category in ['places', 'restaurants', 'events', 'accommodations', 'activities']:
            for item in data.get(category, []):
                sentiment = item.get('sentiment', {}).get('label', 'NEUTRAL')
                if sentiment in sentiments:
                    sentiments[sentiment] += 1
        
        return sentiments
    
    def generate_recommendations(self, data):
        """Generate recommendations based on processed data"""
        recommendations = []
        
        # Find highly positive places
        positive_places = []
        for place in data.get('places', []):
            sentiment = place.get('sentiment', {})
            if sentiment.get('label') == 'POSITIVE' and sentiment.get('score', 0) > 0.8:
                positive_places.append(place['text'])
        
        if positive_places:
            recommendations.append({
                'type': 'top_places',
                'title': 'Highly Recommended Places',
                'items': positive_places[:5]
            })
        
        # Find popular restaurants
        restaurants = [r['text'] for r in data.get('restaurants', [])]
        if restaurants:
            recommendations.append({
                'type': 'dining',
                'title': 'Dining Options',
                'items': restaurants[:5]
            })
        
        return recommendations

def main():
    """Main function for testing the data processor"""
    processor = TshwaneDataProcessor()
    
    # Process website data
    processed_data = processor.scrape_website_comprehensive()
    
    if processed_data:
        print("✅ Data processing completed successfully!")
        
        # Analyze with existing agents
        analysis = processor.analyze_with_existing_agents(
            f"{processor.data_folder}/processed_tshwane_data.json"
        )
        
        if analysis:
            print("✅ Analysis completed!")
            print(f"Summary: {analysis['summary']}")
    else:
        print("❌ Data processing failed!")

if __name__ == "__main__":
    main()
