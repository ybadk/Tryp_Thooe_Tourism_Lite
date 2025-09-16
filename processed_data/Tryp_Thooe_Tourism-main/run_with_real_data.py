#!/usr/bin/env python3
"""
Launch Tshwane Tourism Applications with Real Crawled Data
Runs the enhanced tourism applications using the actual website data
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def check_data_availability():
    """Check if crawled data is available"""
    print("🔍 Checking for crawled data...")
    
    required_files = [
        "processed_data/enhanced_tshwane_data.json",
        "processed_data/tshwane_places.csv",
        "processed_data/tshwane_contacts.json",
        "processed_data/integration_report.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n💡 Please run the crawler and integration first:")
        print("   1. python simple_tshwane_crawler.py")
        print("   2. python integrate_crawled_data.py")
        return False
    
    print("✅ All required data files found!")
    return True

def display_data_summary():
    """Display summary of available data"""
    print("\n📊 AVAILABLE REAL DATA SUMMARY")
    print("=" * 50)
    
    try:
        # Load integration report
        with open("processed_data/integration_report.json", 'r') as f:
            report = json.load(f)
        
        stats = report['statistics']
        quality = report['data_quality']
        
        print(f"🏛️ Places: {stats['total_places']}")
        print(f"🍽️ Restaurants: {stats['total_restaurants']}")
        print(f"🎉 Events: {stats['total_events']}")
        print(f"📧 Contact Emails: {stats['contact_emails']}")
        print(f"📱 Social Links: {stats['social_links']}")
        
        print(f"\n📈 Data Quality:")
        print(f"   - Places with descriptions: {quality['places_with_descriptions']}")
        print(f"   - Places with categories: {quality['places_with_categories']}")
        print(f"   - Positive sentiment: {quality['sentiment_distribution']['positive']}")
        print(f"   - Neutral sentiment: {quality['sentiment_distribution']['neutral']}")
        
        print(f"\n🌐 Data Source: {report['data_sources']['main_website']}")
        print(f"📅 Last Updated: {report['integration_timestamp'][:19]}")
        
    except Exception as e:
        print(f"❌ Error reading data summary: {e}")

def show_sample_data():
    """Show sample of the real data"""
    print("\n📋 SAMPLE REAL DATA")
    print("=" * 50)
    
    try:
        # Show sample places
        with open("processed_data/enhanced_tshwane_data.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data['places']:
            print("🏛️ Sample Places:")
            for i, place in enumerate(data['places'][:3], 1):
                print(f"   {i}. {place['name'][:60]}...")
                print(f"      Type: {place['type']}")
                print(f"      Sentiment: {place['ai_sentiment']}")
                print(f"      Categories: {place['ai_categories']}")
                print()
        
        if data['contact_info']:
            print("📞 Contact Information:")
            emails = data['contact_info'].get('emails', [])
            if emails:
                print(f"   📧 Email: {emails[0]}")
            
            phones = data['contact_info'].get('phones', [])
            if phones:
                print(f"   📱 Phone: {phones[0]}")
        
        if data['social_links']:
            print(f"\n📱 Social Media Links: {len(data['social_links'])} found")
            for link in data['social_links'][:3]:
                print(f"   - {link['platform']}: {link['url']}")
        
    except Exception as e:
        print(f"❌ Error reading sample data: {e}")

def launch_applications():
    """Launch the tourism applications"""
    print("\n🚀 LAUNCH OPTIONS")
    print("=" * 50)
    
    apps = [
        {
            'name': '🌿 Enhanced Tourism App (Main)',
            'file': 'tshwane_tourism_app.py',
            'description': 'Main tourism portal with real data integration'
        },
        {
            'name': '🤖 Enhanced Data Processor',
            'file': 'enhanced_integrated_processor.py',
            'description': 'AI-powered data processor with real data'
        },
        {
            'name': '📊 Original Data Processor',
            'file': 'integrated_data_processor.py',
            'description': 'Original processor for comparison'
        }
    ]
    
    print("Available applications:")
    for i, app in enumerate(apps, 1):
        print(f"{i}. {app['name']}")
        print(f"   File: {app['file']}")
        print(f"   Description: {app['description']}")
        print()
    
    try:
        choice = input("Select application to launch (1-3): ").strip()
        
        if choice in ['1', '2', '3']:
            app_index = int(choice) - 1
            selected_app = apps[app_index]
            
            print(f"\n🚀 Launching {selected_app['name']}...")
            print(f"📁 File: {selected_app['file']}")
            print("🌐 The application will open in your default web browser.")
            print("⏹️ Press Ctrl+C to stop the application.")
            print()
            
            # Check if file exists
            if not Path(selected_app['file']).exists():
                print(f"❌ Error: {selected_app['file']} not found!")
                return False
            
            # Launch the application
            try:
                subprocess.run([
                    sys.executable, "-m", "streamlit", "run", 
                    selected_app['file'],
                    "--server.headless=false"
                ])
                return True
            except FileNotFoundError:
                print("❌ Streamlit not found. Please install it with: pip install streamlit")
                return False
            except KeyboardInterrupt:
                print("\n👋 Application stopped by user.")
                return True
        
        else:
            print("❌ Invalid choice. Please select 1-3.")
            return False
            
    except KeyboardInterrupt:
        print("\n👋 Launch cancelled by user.")
        return True
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return False

def show_usage_instructions():
    """Show instructions for using the applications"""
    print("\n📖 USAGE INSTRUCTIONS")
    print("=" * 50)
    print("Once the application launches, you can:")
    print()
    print("🌿 In the Main Tourism App:")
    print("   1. Click 'Load Tshwane Tourism Data' to load real website data")
    print("   2. Browse the interactive gallery with real places")
    print("   3. Use the semantic search to find specific content")
    print("   4. Get AI-powered weather recommendations")
    print("   5. Submit real booking requests")
    print()
    print("🤖 In the Enhanced Data Processor:")
    print("   1. Upload CSV files for processing")
    print("   2. Use AI models for content analysis")
    print("   3. Generate visualizations from real data")
    print("   4. Export processed data in multiple formats")
    print()
    print("📊 Features with Real Data:")
    print("   ✅ 7 real places from Tshwane Tourism website")
    print("   ✅ Real contact information (secretary@tshwanetourism.com)")
    print("   ✅ 9 social media links")
    print("   ✅ AI sentiment analysis on real content")
    print("   ✅ Weather-based recommendations using real place data")
    print("   ✅ Enhanced booking system with real place names")

def main():
    """Main execution function"""
    print("🌿 TSHWANE TOURISM - LAUNCH WITH REAL DATA")
    print("=" * 60)
    print("Launch enhanced tourism applications using real website data")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Check data availability
        if not check_data_availability():
            return False
        
        # Display data summary
        display_data_summary()
        
        # Show sample data
        show_sample_data()
        
        # Show usage instructions
        show_usage_instructions()
        
        # Launch applications
        success = launch_applications()
        
        if success:
            print("\n✅ Application launched successfully!")
            print("🎉 Enjoy exploring Tshwane with real data!")
        
        return success
        
    except KeyboardInterrupt:
        print("\n👋 Launch cancelled by user.")
        return True
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n💡 Troubleshooting:")
        print("1. Ensure you've run: python simple_tshwane_crawler.py")
        print("2. Ensure you've run: python integrate_crawled_data.py")
        print("3. Check your internet connection")
        print("4. Install missing dependencies: pip install -r requirements.txt")
    
    sys.exit(0 if success else 1)
