#!/usr/bin/env python3
"""
Tshwane Tourism Website Crawler and Cloner
Crawls and creates a local clone of http://www.visittshwane.co.za
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
from pathlib import Path
import time
import json
import csv
from datetime import datetime
import logging
import re
from typing import Set, Dict, List, Optional
import hashlib
import mimetypes
from urllib.robotparser import RobotFileParser

class TshwaneWebsiteCrawler:
    """Comprehensive website crawler and cloner"""
    
    def __init__(self, base_url: str = "http://www.visittshwane.co.za"):
        self.base_url = base_url.rstrip('/')
        self.domain = urllib.parse.urlparse(base_url).netloc
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.crawled_data: Dict[str, any] = {}
        self.assets: Dict[str, str] = {}
        
        # Setup directories
        self.clone_dir = Path("tshwane_website_clone")
        self.data_dir = Path("crawled_data")
        self.assets_dir = self.clone_dir / "assets"
        
        self.setup_directories()
        self.setup_logging()
        self.setup_session()
    
    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            self.clone_dir,
            self.data_dir,
            self.assets_dir,
            self.clone_dir / "css",
            self.clone_dir / "js",
            self.clone_dir / "images",
            self.clone_dir / "pages"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Created directories in: {self.clone_dir}")
    
    def setup_logging(self):
        """Setup logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.data_dir / 'crawler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_session(self):
        """Setup requests session with proper headers"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def check_robots_txt(self) -> bool:
        """Check robots.txt for crawling permissions"""
        try:
            robots_url = f"{self.base_url}/robots.txt"
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            can_crawl = rp.can_fetch('*', self.base_url)
            self.logger.info(f"Robots.txt check: {'Allowed' if can_crawl else 'Restricted'}")
            return can_crawl
        except Exception as e:
            self.logger.warning(f"Could not check robots.txt: {e}")
            return True  # Assume allowed if can't check
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid for crawling"""
        if not url:
            return False
        
        # Parse URL
        parsed = urllib.parse.urlparse(url)
        
        # Must be same domain
        if parsed.netloc and parsed.netloc != self.domain:
            return False
        
        # Skip certain file types
        skip_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar', '.exe'}
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False
        
        # Skip certain patterns
        skip_patterns = ['mailto:', 'tel:', 'javascript:', '#']
        if any(pattern in url.lower() for pattern in skip_patterns):
            return False
        
        return True
    
    def normalize_url(self, url: str, base_url: str) -> str:
        """Normalize and resolve relative URLs"""
        if not url:
            return ""
        
        # Remove fragments
        url = url.split('#')[0]
        
        # Resolve relative URLs
        resolved = urllib.parse.urljoin(base_url, url)
        
        # Normalize
        parsed = urllib.parse.urlparse(resolved)
        normalized = urllib.parse.urlunparse(parsed)
        
        return normalized
    
    def download_asset(self, asset_url: str, asset_type: str) -> Optional[str]:
        """Download and save asset (CSS, JS, images)"""
        try:
            response = self.session.get(asset_url, timeout=30)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            extension = mimetypes.guess_extension(content_type.split(';')[0])
            
            if not extension:
                if 'css' in asset_type.lower():
                    extension = '.css'
                elif 'javascript' in asset_type.lower():
                    extension = '.js'
                else:
                    extension = '.bin'
            
            # Generate filename
            url_hash = hashlib.md5(asset_url.encode()).hexdigest()[:8]
            filename = f"{asset_type}_{url_hash}{extension}"
            
            # Save to appropriate directory
            if asset_type == 'css':
                filepath = self.clone_dir / "css" / filename
            elif asset_type == 'js':
                filepath = self.clone_dir / "js" / filename
            elif asset_type == 'image':
                filepath = self.clone_dir / "images" / filename
            else:
                filepath = self.assets_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            self.logger.info(f"Downloaded {asset_type}: {filename}")
            return str(filepath.relative_to(self.clone_dir))
            
        except Exception as e:
            self.logger.error(f"Failed to download {asset_url}: {e}")
            return None
    
    def extract_assets(self, soup: BeautifulSoup, page_url: str) -> Dict[str, str]:
        """Extract and download all assets from a page"""
        assets = {}
        
        # CSS files
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                css_url = self.normalize_url(href, page_url)
                if css_url and self.is_valid_url(css_url):
                    local_path = self.download_asset(css_url, 'css')
                    if local_path:
                        assets[css_url] = local_path
                        link['href'] = local_path
        
        # JavaScript files
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                js_url = self.normalize_url(src, page_url)
                if js_url and self.is_valid_url(js_url):
                    local_path = self.download_asset(js_url, 'js')
                    if local_path:
                        assets[js_url] = local_path
                        script['src'] = local_path
        
        # Images
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                img_url = self.normalize_url(src, page_url)
                if img_url and self.is_valid_url(img_url):
                    local_path = self.download_asset(img_url, 'image')
                    if local_path:
                        assets[img_url] = local_path
                        img['src'] = local_path
        
        return assets
    
    def extract_page_data(self, soup: BeautifulSoup, url: str) -> Dict[str, any]:
        """Extract structured data from a page"""
        data = {
            'url': url,
            'title': '',
            'meta_description': '',
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': [],
            'contact_info': {},
            'social_links': [],
            'scraped_at': datetime.now().isoformat()
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            data['title'] = title_tag.get_text(strip=True)
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '')
        
        # Headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            data['headings'].append({
                'level': heading.name,
                'text': heading.get_text(strip=True)
            })
        
        # Paragraphs
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 10:
                data['paragraphs'].append(text)
        
        # Links
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            if href and text:
                data['links'].append({
                    'url': self.normalize_url(href, url),
                    'text': text
                })
        
        # Images
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            alt = img.get('alt', '')
            if src:
                data['images'].append({
                    'src': self.normalize_url(src, url),
                    'alt': alt
                })
        
        # Extract contact information
        page_text = soup.get_text()
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, page_text)
        data['contact_info']['emails'] = list(set(emails))
        
        # Phone numbers (South African format)
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
        
        return data
    
    def crawl_page(self, url: str) -> Optional[Dict[str, any]]:
        """Crawl a single page"""
        if url in self.visited_urls or url in self.failed_urls:
            return None
        
        try:
            self.logger.info(f"Crawling: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if it's HTML content
            content_type = response.headers.get('content-type', '')
            if 'text/html' not in content_type:
                self.logger.warning(f"Skipping non-HTML content: {url}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract structured data
            page_data = self.extract_page_data(soup, url)
            
            # Extract and download assets
            assets = self.extract_assets(soup, url)
            page_data['assets'] = assets
            
            # Save HTML file
            page_filename = self.get_page_filename(url)
            page_path = self.clone_dir / "pages" / page_filename
            
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            page_data['local_file'] = str(page_path.relative_to(self.clone_dir))
            
            self.visited_urls.add(url)
            self.crawled_data[url] = page_data
            
            self.logger.info(f"✅ Successfully crawled: {url}")
            return page_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to crawl {url}: {e}")
            self.failed_urls.add(url)
            return None
    
    def get_page_filename(self, url: str) -> str:
        """Generate a safe filename for a page"""
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.strip('/')
        
        if not path or path == '/':
            return 'index.html'
        
        # Replace invalid characters
        safe_path = re.sub(r'[<>:"/\\|?*]', '_', path)
        
        # Ensure .html extension
        if not safe_path.endswith('.html'):
            safe_path += '.html'
        
        return safe_path
    
    def discover_urls(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """Discover URLs from a page"""
        urls = set()
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href:
                normalized_url = self.normalize_url(href, base_url)
                if self.is_valid_url(normalized_url):
                    urls.add(normalized_url)
        
        return urls
    
    def crawl_website(self, max_pages: int = 50, delay: float = 1.0) -> Dict[str, any]:
        """Crawl the entire website"""
        print(f"🕷️ Starting crawl of {self.base_url}")
        print(f"📁 Clone directory: {self.clone_dir}")
        
        # Check robots.txt
        if not self.check_robots_txt():
            print("⚠️ Robots.txt restricts crawling, but continuing...")
        
        # Start with the base URL
        urls_to_crawl = {self.base_url}
        crawled_count = 0
        
        while urls_to_crawl and crawled_count < max_pages:
            current_url = urls_to_crawl.pop()
            
            if current_url in self.visited_urls or current_url in self.failed_urls:
                continue
            
            page_data = self.crawl_page(current_url)
            
            if page_data:
                crawled_count += 1
                
                # Discover new URLs from this page
                try:
                    response = self.session.get(current_url, timeout=30)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    new_urls = self.discover_urls(soup, current_url)
                    
                    # Add new URLs to crawl queue
                    for new_url in new_urls:
                        if new_url not in self.visited_urls and new_url not in self.failed_urls:
                            urls_to_crawl.add(new_url)
                
                except Exception as e:
                    self.logger.error(f"Error discovering URLs from {current_url}: {e}")
            
            # Respectful delay
            time.sleep(delay)
            
            print(f"📊 Progress: {crawled_count}/{max_pages} pages crawled")
        
        # Save crawl results
        self.save_crawl_results()
        
        print(f"✅ Crawling completed!")
        print(f"📊 Statistics:")
        print(f"   - Pages crawled: {len(self.visited_urls)}")
        print(f"   - Failed URLs: {len(self.failed_urls)}")
        print(f"   - Assets downloaded: {len(self.assets)}")
        
        return {
            'crawled_pages': len(self.visited_urls),
            'failed_pages': len(self.failed_urls),
            'total_assets': len(self.assets),
            'crawl_data': self.crawled_data
        }
    
    def save_crawl_results(self):
        """Save crawl results to files"""
        # Save JSON data
        with open(self.data_dir / 'crawl_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.crawled_data, f, indent=2, ensure_ascii=False)
        
        # Save CSV summary
        csv_data = []
        for url, data in self.crawled_data.items():
            csv_data.append({
                'url': url,
                'title': data.get('title', ''),
                'meta_description': data.get('meta_description', ''),
                'headings_count': len(data.get('headings', [])),
                'paragraphs_count': len(data.get('paragraphs', [])),
                'links_count': len(data.get('links', [])),
                'images_count': len(data.get('images', [])),
                'emails_found': len(data.get('contact_info', {}).get('emails', [])),
                'phones_found': len(data.get('contact_info', {}).get('phones', [])),
                'social_links_count': len(data.get('social_links', [])),
                'local_file': data.get('local_file', ''),
                'scraped_at': data.get('scraped_at', '')
            })
        
        with open(self.data_dir / 'crawl_summary.csv', 'w', newline='', encoding='utf-8') as f:
            if csv_data:
                writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                writer.writeheader()
                writer.writerows(csv_data)
        
        # Save failed URLs
        with open(self.data_dir / 'failed_urls.txt', 'w', encoding='utf-8') as f:
            for url in self.failed_urls:
                f.write(f"{url}\n")
        
        print(f"💾 Crawl results saved to: {self.data_dir}")

def main():
    """Main execution function"""
    print("🕷️ TSHWANE TOURISM WEBSITE CRAWLER & CLONER")
    print("=" * 50)
    
    # Initialize crawler
    crawler = TshwaneWebsiteCrawler()
    
    # Configuration
    max_pages = 25  # Limit to avoid overwhelming the server
    delay = 2.0     # 2 second delay between requests
    
    print(f"🎯 Target: {crawler.base_url}")
    print(f"📄 Max pages: {max_pages}")
    print(f"⏱️ Delay: {delay} seconds")
    print()
    
    try:
        # Start crawling
        results = crawler.crawl_website(max_pages=max_pages, delay=delay)
        
        print("\n" + "=" * 50)
        print("📊 CRAWL COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"✅ Pages crawled: {results['crawled_pages']}")
        print(f"❌ Failed pages: {results['failed_pages']}")
        print(f"📁 Clone location: {crawler.clone_dir}")
        print(f"📊 Data location: {crawler.data_dir}")
        
        # Show some sample data
        if crawler.crawled_data:
            print("\n📋 Sample crawled data:")
            sample_url = list(crawler.crawled_data.keys())[0]
            sample_data = crawler.crawled_data[sample_url]
            print(f"   Title: {sample_data.get('title', 'N/A')}")
            print(f"   Headings: {len(sample_data.get('headings', []))}")
            print(f"   Paragraphs: {len(sample_data.get('paragraphs', []))}")
            print(f"   Images: {len(sample_data.get('images', []))}")
            print(f"   Contact emails: {len(sample_data.get('contact_info', {}).get('emails', []))}")
        
        print("\n🎯 Next steps:")
        print("1. Check the cloned website in: tshwane_website_clone/")
        print("2. Review crawled data in: crawled_data/")
        print("3. Use the data in your tourism applications")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⏹️ Crawling stopped by user")
        return False
    except Exception as e:
        print(f"\n❌ Crawling failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
