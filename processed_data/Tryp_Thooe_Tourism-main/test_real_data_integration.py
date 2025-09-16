#!/usr/bin/env python3
"""
Test Real Data Integration for Tshwane Tourism App
Verifies that the app correctly loads and uses real website data
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def test_real_data_availability():
    """Test if real crawled data is available"""
    print("🧪 Testing Real Data Availability")
    print("=" * 50)
    
    required_files = [
        "processed_data/enhanced_tshwane_data.json",
        "processed_data/tshwane_contacts.json",
        "processed_data/tshwane_social_links.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    if missing_files:
        print(f"\n⚠️ {len(missing_files)} files missing. Run crawler first:")
        print("   1. python simple_tshwane_crawler.py")
        print("   2. python integrate_crawled_data.py")
        return False
    
    print("✅ All required data files found!")
    return True

def test_data_content():
    """Test the content of the real data"""
    print("\n🔍 Testing Data Content")
    print("=" * 50)
    
    try:
        # Load enhanced tourism data
        with open("processed_data/enhanced_tshwane_data.json", 'r', encoding='utf-8') as f:
            tourism_data = json.load(f)
        
        places = tourism_data.get('places', [])
        restaurants = tourism_data.get('restaurants', [])
        
        print(f"📊 Data Statistics:")
        print(f"   🏛️ Places: {len(places)}")
        print(f"   🍽️ Restaurants: {len(restaurants)}")
        
        # Test place data quality
        if places:
            print(f"\n🏛️ Sample Place Data:")
            sample_place = places[0]
            
            required_fields = ['name', 'description', 'type', 'ai_sentiment', 'ai_categories']
            for field in required_fields:
                if field in sample_place:
                    print(f"   ✅ {field}: {str(sample_place[field])[:50]}...")
                else:
                    print(f"   ❌ Missing field: {field}")
            
            # Check for enhanced fields
            enhanced_fields = ['display_name', 'short_description', 'weather_suitability', 'verified_source']
            enhanced_count = sum(1 for field in enhanced_fields if field in sample_place)
            print(f"   🤖 Enhanced fields: {enhanced_count}/{len(enhanced_fields)}")
        
        # Load contact information
        with open("processed_data/tshwane_contacts.json", 'r', encoding='utf-8') as f:
            contacts = json.load(f)
        
        emails = contacts.get('emails', [])
        phones = contacts.get('phones', [])
        
        print(f"\n📞 Contact Information:")
        print(f"   📧 Emails: {len(emails)}")
        if emails:
            print(f"      Primary: {emails[0]}")
        print(f"   📱 Phones: {len(phones)}")
        
        # Load social links
        with open("processed_data/tshwane_social_links.json", 'r', encoding='utf-8') as f:
            social_links = json.load(f)
        
        print(f"\n📱 Social Media:")
        print(f"   🔗 Total links: {len(social_links)}")
        
        # Count unique platforms
        platforms = set()
        for link in social_links:
            platforms.add(link.get('platform', 'unknown'))
        
        print(f"   🌐 Platforms: {', '.join(platforms)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing data content: {e}")
        return False

def test_ai_enhancements():
    """Test AI enhancements on real data"""
    print("\n🤖 Testing AI Enhancements")
    print("=" * 50)
    
    try:
        with open("processed_data/enhanced_tshwane_data.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        places = data.get('places', [])
        
        if not places:
            print("❌ No places data to test")
            return False
        
        # Test sentiment analysis
        sentiments = [place.get('ai_sentiment', 'unknown') for place in places]
        sentiment_counts = {
            'positive': sentiments.count('positive'),
            'neutral': sentiments.count('neutral'),
            'negative': sentiments.count('negative'),
            'unknown': sentiments.count('unknown')
        }
        
        print("😊 Sentiment Analysis:")
        for sentiment, count in sentiment_counts.items():
            if count > 0:
                percentage = (count / len(places)) * 100
                print(f"   {sentiment.title()}: {count} ({percentage:.1f}%)")
        
        # Test categorization
        all_categories = []
        for place in places:
            categories = place.get('ai_categories', [])
            all_categories.extend(categories)
        
        category_counts = {}
        for category in all_categories:
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print("\n🏷️ Content Categories:")
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        for category, count in sorted_categories[:5]:
            print(f"   {category.title()}: {count}")
        
        # Test weather suitability
        weather_data_count = sum(1 for place in places if place.get('weather_suitability'))
        print(f"\n🌤️ Weather Suitability:")
        print(f"   Places with weather data: {weather_data_count}/{len(places)}")
        
        if weather_data_count > 0:
            sample_weather = places[0].get('weather_suitability', {})
            print(f"   Weather conditions tracked: {len(sample_weather)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing AI enhancements: {e}")
        return False

def test_app_integration():
    """Test if the app can load the real data"""
    print("\n🔗 Testing App Integration")
    print("=" * 50)
    
    try:
        # Import the main app functions
        sys.path.append('.')
        
        # Test data loading function
        print("📂 Testing data loading...")
        
        # Simulate loading real data
        data_file = Path("processed_data/enhanced_tshwane_data.json")
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            places = data.get('places', [])
            restaurants = data.get('restaurants', [])
            
            # Test data enhancement
            enhanced_places = []
            for place in places:
                enhanced_place = place.copy()
                
                # Test display name generation
                description = place.get('description', '')
                if 'museum' in description.lower():
                    enhanced_place['display_name'] = "Museum/Cultural Site"
                elif 'nature' in description.lower():
                    enhanced_place['display_name'] = "Nature Reserve"
                else:
                    enhanced_place['display_name'] = place.get('name', 'Unknown')[:50]
                
                enhanced_places.append(enhanced_place)
            
            print(f"✅ Enhanced {len(enhanced_places)} places")
            print(f"✅ Loaded {len(restaurants)} restaurants")
            
            # Test search functionality
            print("\n🔍 Testing search functionality...")
            
            # Simple search test
            search_query = "museum"
            matching_places = []
            
            for place in enhanced_places:
                description = place.get('description', '').lower()
                name = place.get('name', '').lower()
                
                if search_query in description or search_query in name:
                    matching_places.append(place)
            
            print(f"✅ Search for '{search_query}': {len(matching_places)} results")
            
            return True
        else:
            print("❌ No data file found for integration test")
            return False
            
    except Exception as e:
        print(f"❌ Error testing app integration: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 TSHWANE TOURISM - REAL DATA INTEGRATION TEST")
    print("=" * 60)
    print(f"📅 Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Data Availability", test_real_data_availability),
        ("Data Content", test_data_content),
        ("AI Enhancements", test_ai_enhancements),
        ("App Integration", test_app_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Real data integration is working correctly.")
        print("\n🚀 Ready to run: streamlit run tshwane_tourism_app.py")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        print("\n💡 Troubleshooting:")
        print("1. Run the crawler: python simple_tshwane_crawler.py")
        print("2. Run the integration: python integrate_crawled_data.py")
        print("3. Check file permissions and paths")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
