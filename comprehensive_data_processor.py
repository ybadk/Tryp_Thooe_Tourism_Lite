#!/usr/bin/env python3
"""
Comprehensive Data Processor for Tshwane Tourism
================================================

This script loads all CSV files, matches relevant data, crawls the web for additional information,
and creates individual CSV files for each place with comprehensive data.

Features:
- Loads all CSV files from multiple directories
- Matches places across different datasets
- Web crawling for additional information
- Data enrichment and validation
- Creates individual CSV files for each place
- Stores data in organized folder structure

Author: Thapelo Kgothatso Thooe
Enterprise: Profit Projects Online Virtual Assistance
Registration: K2025200646
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class PlaceData:
    """Data class to hold comprehensive place information"""
    name: str
    description: str = ""
    type: str = ""
    category: str = ""
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: str = ""
    phone: str = ""
    website: str = ""
    email: str = ""
    rating: Optional[float] = None
    visitor_count: Optional[int] = None
    opening_hours: str = ""
    entrance_fee: str = ""
    accessibility: str = ""
    best_time: str = ""
    visit_duration: str = ""
    highlights: str = ""
    facilities: str = ""
    special_features: str = ""
    seasonal_info: str = ""
    photography_allowed: str = ""
    social_media: str = ""
    last_updated: str = ""
    data_sources: List[str] = None
    web_scraped_data: Dict[str, Any] = None

    def __post_init__(self):
        if self.data_sources is None:
            self.data_sources = []
        if self.web_scraped_data is None:
            self.web_scraped_data = {}


class ComprehensiveDataProcessor:
    """Main class for processing and enriching tourism data"""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "processed_places_data"
        self.output_dir.mkdir(exist_ok=True)

        # Data storage
        self.places_data: Dict[str, PlaceData] = {}
        self.csv_files: List[Path] = []
        self.web_cache: Dict[str, Dict[str, Any]] = {}

        # Web scraping settings
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        logger.info("Comprehensive Data Processor initialized")

    def discover_csv_files(self) -> List[Path]:
        """Discover all CSV files in the project directory"""
        csv_files = []

        # Search in main directory and subdirectories
        search_paths = [
            self.base_dir,
            self.base_dir / "processed_data",
            self.base_dir / "scraps",
            self.base_dir / "Tryp_Thooe_Tourism",
            self.base_dir / "cleaned_csvs"
        ]

        for search_path in search_paths:
            if search_path.exists():
                for csv_file in search_path.rglob("*.csv"):
                    csv_files.append(csv_file)
                    logger.info(f"Found CSV file: {csv_file}")

        logger.info(f"Total CSV files discovered: {len(csv_files)}")
        return csv_files

    def load_csv_file(self, file_path: Path) -> Optional[pd.DataFrame]:
        """Load a CSV file with error handling"""
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            logger.info(
                f"Successfully loaded {file_path.name} with {len(df)} rows")
            return df
        except Exception as e:
            logger.warning(f"Failed to load {file_path.name}: {e}")
            return None

    def normalize_place_name(self, name: str) -> str:
        """Normalize place name for matching"""
        if pd.isna(name):
            return ""

        # Remove common prefixes and suffixes
        name = str(name).strip()
        name = re.sub(r'^the\s+', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+', ' ', name)
        name = name.lower()

        return name

    def match_places_across_datasets(self, dataframes: List[Tuple[str, pd.DataFrame]]) -> Dict[str, PlaceData]:
        """Match places across different datasets and create comprehensive records"""
        places_dict = {}

        for source_name, df in dataframes:
            logger.info(f"Processing dataset: {source_name}")

            for _, row in df.iterrows():
                # Try different column names for place name
                name_cols = ['name', 'place_name', 'display_name', 'title']
                place_name = None

                for col in name_cols:
                    if col in df.columns and not pd.isna(row[col]):
                        place_name = self.normalize_place_name(row[col])
                        break

                if not place_name:
                    continue

                # Create or update place data
                if place_name not in places_dict:
                    places_dict[place_name] = PlaceData(name=place_name)

                place_data = places_dict[place_name]
                place_data.data_sources.append(source_name)

                # Map data based on column names
                self._map_row_data_to_place(place_data, row, source_name)

        logger.info(
            f"Matched {len(places_dict)} unique places across datasets")
        return places_dict

    def _map_row_data_to_place(self, place_data: PlaceData, row: pd.Series, source_name: str):
        """Map row data to place data object"""
        # Basic information
        if 'description' in row and not pd.isna(row['description']):
            if not place_data.description:
                place_data.description = str(row['description'])

        if 'type' in row and not pd.isna(row['type']):
            if not place_data.type:
                place_data.type = str(row['type'])

        if 'category' in row and not pd.isna(row['category']):
            if not place_data.category:
                place_data.category = str(row['category'])

        # Location data
        if 'lat' in row and not pd.isna(row['lat']):
            place_data.lat = float(row['lat'])

        if 'lng' in row and not pd.isna(row['lng']):
            place_data.lng = float(row['lng'])

        # Contact information
        if 'phone' in row and not pd.isna(row['phone']):
            place_data.phone = str(row['phone'])

        if 'website' in row and not pd.isna(row['website']):
            place_data.website = str(row['website'])

        if 'contact_email' in row and not pd.isna(row['contact_email']):
            place_data.email = str(row['contact_email'])

        # Detailed information
        if 'short_description' in row and not pd.isna(row['short_description']):
            if not place_data.description:
                place_data.description = str(row['short_description'])

        if 'long_description' in row and not pd.isna(row['long_description']):
            place_data.description = str(row['long_description'])

        if 'address' in row and not pd.isna(row['address']):
            place_data.address = str(row['address'])

        if 'rating' in row and not pd.isna(row['rating']):
            place_data.rating = float(row['rating'])

        if 'visitor_count' in row and not pd.isna(row['visitor_count']):
            place_data.visitor_count = int(row['visitor_count'])

        # Additional fields
        for field in ['opening_hours', 'entrance_fee', 'accessibility', 'best_time',
                      'visit_duration', 'highlights', 'facilities', 'special_features',
                      'seasonal_info', 'photography_allowed', 'social_media']:
            if field in row and not pd.isna(row[field]):
                setattr(place_data, field, str(row[field]))

    def crawl_web_for_place_info(self, place_name: str, website: str = "") -> Dict[str, Any]:
        """Crawl web for additional place information"""
        scraped_data = {}

        try:
            # Try to find website if not provided
            if not website:
                website = self._search_for_website(place_name)

            if website:
                scraped_data = self._scrape_website_data(website, place_name)

            # Add delay to be respectful
            time.sleep(1)

        except Exception as e:
            logger.warning(f"Failed to crawl web for {place_name}: {e}")

        return scraped_data

    def _search_for_website(self, place_name: str) -> str:
        """Search for place website using Google"""
        try:
            search_query = f"{place_name} Tshwane Pretoria South Africa official website"
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"

            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract first result
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/url?q='):
                    url = href.split('/url?q=')[1].split('&')[0]
                    if any(domain in url.lower() for domain in ['.co.za', '.com', '.org']):
                        return url

        except Exception as e:
            logger.warning(
                f"Failed to search for website for {place_name}: {e}")

        return ""

    def _scrape_website_data(self, website: str, place_name: str) -> Dict[str, Any]:
        """Scrape data from place website"""
        scraped_data = {}

        try:
            response = self.session.get(website, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract contact information
            scraped_data['phone'] = self._extract_phone(soup)
            scraped_data['email'] = self._extract_email(soup)
            scraped_data['address'] = self._extract_address(soup)

            # Extract description
            scraped_data['description'] = self._extract_description(soup)

            # Extract opening hours
            scraped_data['opening_hours'] = self._extract_opening_hours(soup)

            # Extract social media
            scraped_data['social_media'] = self._extract_social_media(soup)

            logger.info(f"Successfully scraped data for {place_name}")

        except Exception as e:
            logger.warning(f"Failed to scrape {website}: {e}")

        return scraped_data

    def _extract_phone(self, soup: BeautifulSoup) -> str:
        """Extract phone number from website"""
        phone_pattern = r'(\+27|0)[0-9\s\-\(\)]{8,15}'

        for text in soup.stripped_strings:
            match = re.search(phone_pattern, text)
            if match:
                return match.group(0)

        return ""

    def _extract_email(self, soup: BeautifulSoup) -> str:
        """Extract email from website"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        for text in soup.stripped_strings:
            match = re.search(email_pattern, text)
            if match:
                return match.group(0)

        return ""

    def _extract_address(self, soup: BeautifulSoup) -> str:
        """Extract address from website"""
        address_keywords = ['address', 'location', 'street', 'avenue', 'road']

        for element in soup.find_all(['p', 'div', 'span']):
            text = element.get_text().lower()
            if any(keyword in text for keyword in address_keywords):
                return element.get_text().strip()

        return ""

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract description from website"""
        # Look for meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']

        # Look for first paragraph
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if len(text) > 50:
                return text

        return ""

    def _extract_opening_hours(self, soup: BeautifulSoup) -> str:
        """Extract opening hours from website"""
        hours_keywords = ['hours', 'opening', 'time', 'schedule']

        for element in soup.find_all(['p', 'div', 'span']):
            text = element.get_text().lower()
            if any(keyword in text for keyword in hours_keywords):
                return element.get_text().strip()

        return ""

    def _extract_social_media(self, soup: BeautifulSoup) -> str:
        """Extract social media links from website"""
        social_platforms = ['facebook', 'twitter',
                            'instagram', 'linkedin', 'youtube']
        social_links = []

        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            for platform in social_platforms:
                if platform in href:
                    social_links.append(platform)

        return ', '.join(set(social_links))

    def enrich_place_data(self, places_dict: Dict[str, PlaceData]) -> Dict[str, PlaceData]:
        """Enrich place data with web crawling and additional processing"""
        logger.info("Starting data enrichment process...")

        # Use ThreadPoolExecutor for parallel web crawling
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_place = {}

            for place_name, place_data in places_dict.items():
                # Only crawl if we have a website or if place has significant data
                if place_data.website or len(place_data.data_sources) > 1:
                    future = executor.submit(
                        self.crawl_web_for_place_info,
                        place_name,
                        place_data.website
                    )
                    future_to_place[future] = place_name

            # Process completed web crawling results
            for future in as_completed(future_to_place):
                place_name = future_to_place[future]
                try:
                    scraped_data = future.result()
                    places_dict[place_name].web_scraped_data = scraped_data

                    # Update place data with scraped information
                    if scraped_data.get('phone') and not places_dict[place_name].phone:
                        places_dict[place_name].phone = scraped_data['phone']

                    if scraped_data.get('email') and not places_dict[place_name].email:
                        places_dict[place_name].email = scraped_data['email']

                    if scraped_data.get('address') and not places_dict[place_name].address:
                        places_dict[place_name].address = scraped_data['address']

                    if scraped_data.get('description') and not places_dict[place_name].description:
                        places_dict[place_name].description = scraped_data['description']

                    if scraped_data.get('opening_hours') and not places_dict[place_name].opening_hours:
                        places_dict[place_name].opening_hours = scraped_data['opening_hours']

                    if scraped_data.get('social_media') and not places_dict[place_name].social_media:
                        places_dict[place_name].social_media = scraped_data['social_media']

                except Exception as e:
                    logger.warning(
                        f"Failed to enrich data for {place_name}: {e}")

        logger.info("Data enrichment completed")
        return places_dict

    def create_individual_csv_files(self, places_dict: Dict[str, PlaceData]):
        """Create individual CSV files for each place"""
        logger.info("Creating individual CSV files for each place...")

        # Create subdirectories by type
        type_dirs = {}

        for place_name, place_data in places_dict.items():
            # Create safe filename with length limit
            safe_name = re.sub(r'[^\w\s-]', '', place_name)
            safe_name = re.sub(r'[-\s]+', '_', safe_name)

            # Limit filename length to 50 characters to avoid Windows path issues
            if len(safe_name) > 50:
                safe_name = safe_name[:50]

            # Add hash to ensure uniqueness for truncated names
            if len(place_name) > 50:
                name_hash = hashlib.md5(place_name.encode()).hexdigest()[:8]
                safe_name = f"{safe_name}_{name_hash}"

            filename = f"{safe_name}.csv"

            # Determine directory based on type
            place_type = place_data.type or place_data.category or "other"
            if place_type not in type_dirs:
                type_dir = self.output_dir / place_type
                type_dir.mkdir(exist_ok=True)
                type_dirs[place_type] = type_dir

            file_path = type_dirs[place_type] / filename

            # Convert place data to DataFrame
            place_dict = {
                'name': place_data.name,
                'description': place_data.description,
                'type': place_data.type,
                'category': place_data.category,
                'lat': place_data.lat,
                'lng': place_data.lng,
                'address': place_data.address,
                'phone': place_data.phone,
                'website': place_data.website,
                'email': place_data.email,
                'rating': place_data.rating,
                'visitor_count': place_data.visitor_count,
                'opening_hours': place_data.opening_hours,
                'entrance_fee': place_data.entrance_fee,
                'accessibility': place_data.accessibility,
                'best_time': place_data.best_time,
                'visit_duration': place_data.visit_duration,
                'highlights': place_data.highlights,
                'facilities': place_data.facilities,
                'special_features': place_data.special_features,
                'seasonal_info': place_data.seasonal_info,
                'photography_allowed': place_data.photography_allowed,
                'social_media': place_data.social_media,
                'last_updated': datetime.now().isoformat(),
                'data_sources': ','.join(place_data.data_sources),
                'web_scraped_data': json.dumps(place_data.web_scraped_data)
            }

            df = pd.DataFrame([place_dict])
            df.to_csv(file_path, index=False, encoding='utf-8')

            logger.info(f"Created CSV file: {file_path}")

        logger.info(f"Created {len(places_dict)} individual CSV files")

    def create_summary_report(self, places_dict: Dict[str, PlaceData]):
        """Create a summary report of the data processing"""
        report_path = self.output_dir / "processing_summary.json"

        # Calculate statistics
        total_places = len(places_dict)
        places_with_coordinates = sum(
            1 for p in places_dict.values() if p.lat and p.lng)
        places_with_websites = sum(
            1 for p in places_dict.values() if p.website)
        places_with_phone = sum(1 for p in places_dict.values() if p.phone)
        places_with_email = sum(1 for p in places_dict.values() if p.email)

        # Type distribution
        type_counts = {}
        for place_data in places_dict.values():
            place_type = place_data.type or place_data.category or "unknown"
            type_counts[place_type] = type_counts.get(place_type, 0) + 1

        # Data source distribution
        source_counts = {}
        for place_data in places_dict.values():
            for source in place_data.data_sources:
                source_counts[source] = source_counts.get(source, 0) + 1

        summary = {
            'processing_date': datetime.now().isoformat(),
            'total_places': total_places,
            'places_with_coordinates': places_with_coordinates,
            'places_with_websites': places_with_websites,
            'places_with_phone': places_with_phone,
            'places_with_email': places_with_email,
            'type_distribution': type_counts,
            'source_distribution': source_counts,
            'output_directory': str(self.output_dir)
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        logger.info(f"Created summary report: {report_path}")
        return summary

    def process_all_data(self):
        """Main method to process all data"""
        logger.info("Starting comprehensive data processing...")

        # Step 1: Discover CSV files
        csv_files = self.discover_csv_files()

        # Step 2: Load all CSV files
        dataframes = []
        for csv_file in csv_files:
            df = self.load_csv_file(csv_file)
            if df is not None:
                dataframes.append((csv_file.stem, df))

        # Step 3: Match places across datasets
        places_dict = self.match_places_across_datasets(dataframes)

        # Step 4: Enrich data with web crawling
        places_dict = self.enrich_place_data(places_dict)

        # Step 5: Create individual CSV files
        self.create_individual_csv_files(places_dict)

        # Step 6: Create summary report
        summary = self.create_summary_report(places_dict)

        logger.info("Comprehensive data processing completed!")
        return places_dict, summary


def main():
    """Main function to run the data processor"""
    print("🌿 Tshwane Tourism Comprehensive Data Processor")
    print("=" * 50)
    print("Enterprise: Profit Projects Online Virtual Assistance")
    print("Registration: K2025200646")
    print("Contact: kgothatsothooe@gmail.com")
    print("=" * 50)

    # Initialize processor
    processor = ComprehensiveDataProcessor()

    try:
        # Process all data
        places_dict, summary = processor.process_all_data()

        # Print summary
        print("\n📊 Processing Summary:")
        print(f"Total places processed: {summary['total_places']}")
        print(f"Places with coordinates: {summary['places_with_coordinates']}")
        print(f"Places with websites: {summary['places_with_websites']}")
        print(f"Places with phone: {summary['places_with_phone']}")
        print(f"Places with email: {summary['places_with_email']}")

        print(f"\n📁 Output directory: {summary['output_directory']}")
        print("\n✅ Data processing completed successfully!")

    except Exception as e:
        logger.error(f"Data processing failed: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
