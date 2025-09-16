#!/usr/bin/env python3
"""
Simple Tshwane Tourism Website Crawler
Quick and reliable crawler for http://www.visittshwane.co.za
"""

import os
import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
from pathlib import Path
import time
import re
from urllib.parse import urljoin, urlparse

def create_directories():
    """Create necessary directories"""
    directories = [
        "tshwane_crawled_data",
        "tshwane_crawled_data/pages",
        "tshwane_crawled_data/assets",
        "tshwane_crawled_data/data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created directories")

def crawl_main_page(url="http://www.visittshwane.co.za"):
    """Crawl the main page and extract data"""
    print(f"🕷️ Crawling: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data
        data = {
            'url': url,
            'title': soup.find('title').text if soup.find('title') else '',
            'meta_description': '',
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': [],
            'contact_info': {'emails': [], 'phones': []},
            'social_links': [],
            'scraped_at': datetime.now().isoformat()
        }
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '')
        
        # Headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = heading.get_text(strip=True)
            if text:
                data['headings'].append({
                    'level': heading.name,
                    'text': text
                })
        
        # Paragraphs
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                data['paragraphs'].append(text)
        
        # Links
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            if href and text:
                full_url = urljoin(url, href)
                data['links'].append({
                    'url': full_url,
                    'text': text
                })
        
        # Images
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            alt = img.get('alt', '')
            if src:
                full_url = urljoin(url, src)
                data['images'].append({
                    'src': full_url,
                    'alt': alt
                })
        
        # Extract contact information
        page_text = soup.get_text()
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, page_text)
        data['contact_info']['emails'] = list(set(emails))
        
        # Phone numbers
        phone_pattern = r'(\+27|0)[0-9\s\-\(\)]{8,15}'
        phones = re.findall(phone_pattern, page_text)
        data['contact_info']['phones'] = list(set(phones))
        
        # Social media links
        social_patterns = {
            'facebook': r'facebook\.com',
            'twitter': r'twitter\.com',
            'instagram': r'instagram\.com',
            'linkedin': r'linkedin\.com',
            'youtube': r'youtube\.com'
        }
        
        for link in data['links']:
            for platform, pattern in social_patterns.items():
                if re.search(pattern, link['url'], re.IGNORECASE):
                    data['social_links'].append({
                        'platform': platform,
                        'url': link['url'],
                        'text': link['text']
                    })
        
        # Save HTML
        with open('tshwane_crawled_data/pages/main_page.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print("✅ Main page crawled successfully")
        return data
        
    except Exception as e:
        print(f"❌ Error crawling main page: {e}")
        return None

def crawl_additional_pages(main_data, max_pages=5):
    """Crawl additional pages found in main page"""
    print(f"🔍 Crawling additional pages (max: {max_pages})")
    
    additional_data = []
    crawled_count = 0
    
    if not main_data or 'links' not in main_data:
        return additional_data
    
    base_domain = "visittshwane.co.za"
    
    for link in main_data['links']:
        if crawled_count >= max_pages:
            break
        
        url = link['url']
        
        # Only crawl same domain links
        if base_domain not in url:
            continue
        
        # Skip certain file types
        if any(url.lower().endswith(ext) for ext in ['.pdf', '.doc', '.jpg', '.png', '.gif']):
            continue
        
        # Skip certain patterns
        if any(pattern in url.lower() for pattern in ['mailto:', 'tel:', 'javascript:']):
            continue
        
        try:
            print(f"  📄 Crawling: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            page_data = {
                'url': url,
                'title': soup.find('title').text if soup.find('title') else '',
                'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
                'paragraphs': [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 20],
                'scraped_at': datetime.now().isoformat()
            }
            
            additional_data.append(page_data)
            crawled_count += 1
            
            # Save page
            filename = f"page_{crawled_count}.html"
            with open(f'tshwane_crawled_data/pages/{filename}', 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"  ✅ Saved: {filename}")
            
            # Be respectful - delay between requests
            time.sleep(2)
            
        except Exception as e:
            print(f"  ❌ Error crawling {url}: {e}")
            continue
    
    print(f"✅ Crawled {crawled_count} additional pages")
    return additional_data

def extract_tourism_data(all_data):
    """Extract tourism-specific data"""
    print("🎯 Extracting tourism data...")
    
    tourism_data = {
        'places': [],
        'restaurants': [],
        'events': [],
        'accommodations': [],
        'contact_info': {},
        'social_links': [],
        'extracted_at': datetime.now().isoformat()
    }
    
    # Keywords for categorization
    place_keywords = ['museum', 'park', 'monument', 'gallery', 'center', 'square', 'garden', 'attraction']
    restaurant_keywords = ['restaurant', 'cafe', 'dining', 'food', 'cuisine', 'bar', 'grill']
    event_keywords = ['event', 'festival', 'concert', 'show', 'exhibition', 'conference']
    accommodation_keywords = ['hotel', 'lodge', 'guesthouse', 'accommodation', 'stay', 'resort']
    
    # Process all crawled data
    for data in all_data:
        if not data:
            continue
        
        # Combine all text content
        all_text = []

        # Handle headings - check if they're dictionaries or strings
        headings = data.get('headings', [])
        if headings:
            if isinstance(headings[0], dict):
                all_text.extend([h['text'] for h in headings])
            else:
                all_text.extend(headings)

        # Handle paragraphs
        paragraphs = data.get('paragraphs', [])
        if paragraphs:
            all_text.extend(paragraphs)
        
        for text in all_text:
            text_lower = text.lower()
            
            # Categorize content
            if any(keyword in text_lower for keyword in place_keywords):
                tourism_data['places'].append({
                    'name': text[:100],
                    'description': text,
                    'type': 'attraction',
                    'source_url': data.get('url', '')
                })
            
            elif any(keyword in text_lower for keyword in restaurant_keywords):
                tourism_data['restaurants'].append({
                    'name': text[:100],
                    'description': text,
                    'type': 'restaurant',
                    'source_url': data.get('url', '')
                })
            
            elif any(keyword in text_lower for keyword in event_keywords):
                tourism_data['events'].append({
                    'name': text[:100],
                    'description': text,
                    'type': 'event',
                    'source_url': data.get('url', '')
                })
            
            elif any(keyword in text_lower for keyword in accommodation_keywords):
                tourism_data['accommodations'].append({
                    'name': text[:100],
                    'description': text,
                    'type': 'accommodation',
                    'source_url': data.get('url', '')
                })
        
        # Collect contact info and social links
        if 'contact_info' in data:
            for email in data['contact_info'].get('emails', []):
                if email not in tourism_data['contact_info'].get('emails', []):
                    tourism_data['contact_info'].setdefault('emails', []).append(email)
            
            for phone in data['contact_info'].get('phones', []):
                if phone not in tourism_data['contact_info'].get('phones', []):
                    tourism_data['contact_info'].setdefault('phones', []).append(phone)
        
        if 'social_links' in data:
            tourism_data['social_links'].extend(data['social_links'])
    
    # Remove duplicates and limit results
    tourism_data['places'] = tourism_data['places'][:20]
    tourism_data['restaurants'] = tourism_data['restaurants'][:15]
    tourism_data['events'] = tourism_data['events'][:10]
    tourism_data['accommodations'] = tourism_data['accommodations'][:10]
    
    print(f"✅ Extracted {len(tourism_data['places'])} places")
    print(f"✅ Extracted {len(tourism_data['restaurants'])} restaurants")
    print(f"✅ Extracted {len(tourism_data['events'])} events")
    print(f"✅ Extracted {len(tourism_data['accommodations'])} accommodations")
    
    return tourism_data

def save_data(main_data, additional_data, tourism_data):
    """Save all crawled data"""
    print("💾 Saving crawled data...")
    
    # Save main data as JSON
    with open('tshwane_crawled_data/data/main_page_data.json', 'w', encoding='utf-8') as f:
        json.dump(main_data, f, indent=2, ensure_ascii=False)
    
    # Save additional pages data
    with open('tshwane_crawled_data/data/additional_pages_data.json', 'w', encoding='utf-8') as f:
        json.dump(additional_data, f, indent=2, ensure_ascii=False)
    
    # Save tourism data
    with open('tshwane_crawled_data/data/tourism_data.json', 'w', encoding='utf-8') as f:
        json.dump(tourism_data, f, indent=2, ensure_ascii=False)
    
    # Save tourism data as CSV files
    if tourism_data['places']:
        with open('tshwane_crawled_data/data/places.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'description', 'type', 'source_url'])
            writer.writeheader()
            writer.writerows(tourism_data['places'])
    
    if tourism_data['restaurants']:
        with open('tshwane_crawled_data/data/restaurants.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'description', 'type', 'source_url'])
            writer.writeheader()
            writer.writerows(tourism_data['restaurants'])
    
    # Save contact info
    if tourism_data['contact_info']:
        with open('tshwane_crawled_data/data/contact_info.json', 'w', encoding='utf-8') as f:
            json.dump(tourism_data['contact_info'], f, indent=2)
    
    # Save social links
    if tourism_data['social_links']:
        with open('tshwane_crawled_data/data/social_links.json', 'w', encoding='utf-8') as f:
            json.dump(tourism_data['social_links'], f, indent=2)
    
    print("✅ All data saved successfully")

def main():
    """Main execution function"""
    print("🕷️ SIMPLE TSHWANE TOURISM WEBSITE CRAWLER")
    print("=" * 50)
    print(f"🎯 Target: http://www.visittshwane.co.za")
    print(f"📁 Output: tshwane_crawled_data/")
    print()
    
    try:
        # Create directories
        create_directories()
        
        # Crawl main page
        main_data = crawl_main_page()
        if not main_data:
            print("❌ Failed to crawl main page")
            return False
        
        # Crawl additional pages
        additional_data = crawl_additional_pages(main_data, max_pages=5)
        
        # Extract tourism-specific data
        all_data = [main_data] + additional_data
        tourism_data = extract_tourism_data(all_data)
        
        # Save all data
        save_data(main_data, additional_data, tourism_data)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 CRAWLING COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"✅ Main page: Crawled")
        print(f"✅ Additional pages: {len(additional_data)}")
        print(f"✅ Places found: {len(tourism_data['places'])}")
        print(f"✅ Restaurants found: {len(tourism_data['restaurants'])}")
        print(f"✅ Contact emails: {len(tourism_data['contact_info'].get('emails', []))}")
        print(f"✅ Social links: {len(tourism_data['social_links'])}")
        print(f"📁 Data saved to: tshwane_crawled_data/")
        
        print("\n🎯 Files created:")
        print("  📄 tshwane_crawled_data/pages/ - HTML pages")
        print("  📊 tshwane_crawled_data/data/ - JSON and CSV data")
        print("  🏛️ places.csv - Tourist attractions")
        print("  🍽️ restaurants.csv - Dining options")
        print("  📞 contact_info.json - Contact details")
        print("  📱 social_links.json - Social media links")
        
        return True
        
    except Exception as e:
        print(f"❌ Crawling failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Ready to use the crawled data in your tourism applications!")
    else:
        print("\n💡 Check your internet connection and try again.")
