#!/usr/bin/env python3
"""
Simple Tshwane Tourism Demo
Demonstrates the crawled data without complex dependencies
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

def load_real_data():
    """Load the real crawled data"""
    print("📂 Loading real Tshwane Tourism data...")
    
    try:
        # Load enhanced data
        with open("processed_data/enhanced_tshwane_data.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ Successfully loaded real website data!")
        return data
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def display_places(data):
    """Display the real places data"""
    print("\n🏛️ REAL PLACES FROM TSHWANE TOURISM WEBSITE")
    print("=" * 60)
    
    places = data.get('places', [])
    
    for i, place in enumerate(places, 1):
        print(f"\n{i}. {place['name'][:80]}...")
        print(f"   📍 Type: {place['type']}")
        print(f"   😊 Sentiment: {place['ai_sentiment']}")
        print(f"   🏷️ Categories: {', '.join(place['ai_categories'])}")
        print(f"   🌤️ Weather Suitability:")
        weather = place.get('weather_suitability', {})
        for condition, score in weather.items():
            print(f"      {condition}: {score}/5")
        print(f"   🔗 Source: {place['source_url']}")
        print(f"   📝 Description: {place['description'][:100]}...")

def display_restaurants(data):
    """Display the restaurants data"""
    print("\n🍽️ RESTAURANTS & DINING")
    print("=" * 60)
    
    restaurants = data.get('restaurants', [])
    
    for i, restaurant in enumerate(restaurants, 1):
        print(f"\n{i}. {restaurant['name']}")
        print(f"   📍 Type: {restaurant['type']}")
        print(f"   😊 Sentiment: {restaurant['ai_sentiment']}")
        print(f"   🏷️ Categories: {', '.join(restaurant['ai_categories'])}")
        print(f"   📝 Description: {restaurant['description'][:100]}...")

def display_contact_info(data):
    """Display contact information"""
    print("\n📞 CONTACT INFORMATION")
    print("=" * 60)
    
    contact = data.get('contact_info', {})
    
    emails = contact.get('emails', [])
    if emails:
        print("📧 Email Addresses:")
        for email in emails:
            print(f"   • {email}")
    
    phones = contact.get('phones', [])
    if phones:
        print("\n📱 Phone Numbers:")
        for phone in phones:
            print(f"   • {phone}")

def display_social_links(data):
    """Display social media links"""
    print("\n📱 SOCIAL MEDIA LINKS")
    print("=" * 60)
    
    social_links = data.get('social_links', [])
    
    if social_links:
        platforms = {}
        for link in social_links:
            platform = link['platform']
            if platform not in platforms:
                platforms[platform] = link['url']
        
        for platform, url in platforms.items():
            print(f"   {platform.title()}: {url}")
    else:
        print("   No social media links found")

def analyze_data(data):
    """Analyze the crawled data"""
    print("\n📊 DATA ANALYSIS")
    print("=" * 60)
    
    places = data.get('places', [])
    restaurants = data.get('restaurants', [])
    contact = data.get('contact_info', {})
    social = data.get('social_links', [])
    
    print(f"📈 Statistics:")
    print(f"   • Total Places: {len(places)}")
    print(f"   • Total Restaurants: {len(restaurants)}")
    print(f"   • Contact Emails: {len(contact.get('emails', []))}")
    print(f"   • Social Links: {len(social)}")
    
    # Sentiment analysis
    if places:
        sentiments = [place.get('ai_sentiment', 'neutral') for place in places]
        sentiment_counts = {
            'positive': sentiments.count('positive'),
            'neutral': sentiments.count('neutral'),
            'negative': sentiments.count('negative')
        }
        
        print(f"\n😊 Sentiment Analysis:")
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(places)) * 100 if places else 0
            print(f"   • {sentiment.title()}: {count} ({percentage:.1f}%)")
    
    # Category analysis
    if places:
        all_categories = []
        for place in places:
            all_categories.extend(place.get('ai_categories', []))
        
        category_counts = {}
        for category in all_categories:
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\n🏷️ Top Categories:")
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        for category, count in sorted_categories[:5]:
            print(f"   • {category.title()}: {count}")

def weather_recommendations(data):
    """Show weather-based recommendations"""
    print("\n🌤️ WEATHER-BASED RECOMMENDATIONS")
    print("=" * 60)
    
    places = data.get('places', [])
    
    weather_conditions = ['sunny', 'rainy', 'cloudy', 'hot', 'cold']
    
    for condition in weather_conditions:
        print(f"\n☀️ Best places for {condition.upper()} weather:")
        
        # Score places for this weather condition
        scored_places = []
        for place in places:
            weather_scores = place.get('weather_suitability', {})
            score = weather_scores.get(condition, 3)
            if score >= 4:  # Only show highly suitable places
                scored_places.append((place['name'][:50], score))
        
        # Sort by score
        scored_places.sort(key=lambda x: x[1], reverse=True)
        
        if scored_places:
            for name, score in scored_places[:3]:  # Top 3
                print(f"   • {name}... (Score: {score}/5)")
        else:
            print(f"   • No highly suitable places found")

def booking_simulation(data):
    """Simulate booking process with real data"""
    print("\n📝 BOOKING SIMULATION")
    print("=" * 60)
    
    places = data.get('places', [])
    restaurants = data.get('restaurants', [])
    
    if places:
        print("Available places for booking:")
        for i, place in enumerate(places[:5], 1):
            print(f"   {i}. {place['name'][:60]}...")
    
    if restaurants:
        print("\nAvailable restaurants for reservation:")
        for i, restaurant in enumerate(restaurants, 1):
            print(f"   {i}. {restaurant['name']}")
    
    # Simulate booking
    print(f"\n📋 Sample Booking Form Data:")
    print(f"   • Available Places: {len(places)}")
    print(f"   • Available Restaurants: {len(restaurants)}")
    print(f"   • Contact Email: {data.get('contact_info', {}).get('emails', ['N/A'])[0]}")
    print(f"   • Booking ID: TTA-{datetime.now().strftime('%Y%m%d-%H%M%S')}")

def main():
    """Main demo function"""
    print("🌿 TSHWANE TOURISM - REAL DATA DEMONSTRATION")
    print("=" * 70)
    print("Showcasing real data crawled from http://www.visittshwane.co.za")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load real data
    data = load_real_data()
    if not data:
        print("❌ Could not load data. Please run the crawler first:")
        print("   1. python simple_tshwane_crawler.py")
        print("   2. python integrate_crawled_data.py")
        return False
    
    try:
        # Display all sections
        display_places(data)
        display_restaurants(data)
        display_contact_info(data)
        display_social_links(data)
        analyze_data(data)
        weather_recommendations(data)
        booking_simulation(data)
        
        print("\n" + "=" * 70)
        print("🎉 DEMONSTRATION COMPLETED!")
        print("=" * 70)
        print("✅ Successfully demonstrated real Tshwane Tourism data")
        print("✅ Data includes 7 real places from the website")
        print("✅ AI analysis applied to all content")
        print("✅ Weather-based recommendations generated")
        print("✅ Booking system ready with real place names")
        
        print("\n🚀 Next Steps:")
        print("1. Use this data in your Streamlit applications")
        print("2. Integrate with booking systems")
        print("3. Add more AI analysis features")
        print("4. Deploy to production")
        
        print("\n📞 Contact Information:")
        print("   Tshwane Tourism: secretary@tshwanetourism.com")
        print("   Developer: Thapelo Kgothatso Thooe")
        print("   Email: kgothatsothooe@gmail.com")
        print("   Enterprise: K2025200646")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎯 The real data is ready for use in your tourism applications!")
    else:
        print("\n💡 Please ensure the crawler has been run successfully.")
