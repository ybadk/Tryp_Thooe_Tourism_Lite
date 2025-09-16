#!/usr/bin/env python3
"""
CSV Data Loader for Tshwane Tourism
====================================

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
import re
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time
import hashlib
from urllib.parse import urljoin, urlparse
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PlaceData:
    """Data structure for place information"""
    name: str
    description: str = ""
    type: str = ""
    category: str = ""
    address: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: str = ""
    email: str = ""
    website: str = ""
    image: str = ""
    rating: Optional[float] = None
    price_range: str = ""
    opening_hours: str = ""
    facilities: str = ""
    special_features: str = ""
    weather_suitability: str = ""
    ai_sentiment: str = "neutral"
    verified_source: bool = False
    data_source: str = ""
    last_updated: str = ""
    web_data: Dict[str, Any] = None

class CSVDataLoader:
    """Main class for loading and processing CSV data"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "individual_places_data"
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories by type
        self.type_dirs = {}
        self.places_dict = {}
        
    def discover_csv_files(self) -> List[Path]:
        """Discover all CSV files in the project"""
        csv_files = []
        
        # Search in multiple directories
        search_dirs = [
            self.base_dir,
            self.base_dir / "processed_data",
            self.base_dir / "scraps",
            self.base_dir / "cleaned_csvs",
            self.base_dir / "Tryp_Thooe_Tourism",
            self.base_dir / "Tryp_Thooe_Tourism" / "processed_data",
            self.base_dir / "Tryp_Thooe_Tourism" / "scraps",
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for csv_file in search_dir.rglob("*.csv"):
                    csv_files.append(csv_file)
                    
        logger.info(f"Discovered {len(csv_files)} CSV files")
        return csv_files
    
    def load_csv_data(self, csv_files: List[Path]) -> Dict[str, pd.DataFrame]:
        """Load all CSV files into DataFrames"""
        dataframes = {}
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                key = f"{csv_file.parent.name}_{csv_file.stem}"
                dataframes[key] = df
                logger.info(f"Loaded {csv_file} with {len(df)} rows")
            except Exception as e:
                logger.warning(f"Could not load {csv_file}: {e}")
                
        return dataframes
    
    def normalize_place_name(self, name: str) -> str:
        """Normalize place name for matching"""
        if pd.isna(name):
            return ""
        
        # Convert to string and normalize
        name = str(name).strip()
        
        # Remove common prefixes/suffixes
        name = re.sub(r'^(the|a|an)\s+', '', name.lower())
        name = re.sub(r'\s+(restaurant|cafe|hotel|lodge|museum|park|gallery)$', '', name)
        
        # Remove special characters but keep spaces
        name = re.sub(r'[^\w\s]', '', name)
        
        # Normalize whitespace
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def match_places_across_datasets(self, dataframes: Dict[str, pd.DataFrame]) -> Dict[str, PlaceData]:
        """Match places across different datasets"""
        places_dict = {}
        
        # Create a mapping of normalized names to original data
        name_mapping = {}
        
        for source, df in dataframes.items():
            logger.info(f"Processing {source} with {len(df)} rows")
            
            # Determine column names (handle different naming conventions)
            name_col = None
            desc_col = None
            type_col = None
            lat_col = None
            lng_col = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'name' in col_lower or 'title' in col_lower:
                    name_col = col
                elif 'desc' in col_lower or 'description' in col_lower:
                    desc_col = col
                elif 'type' in col_lower or 'category' in col_lower:
                    type_col = col
                elif 'lat' in col_lower or 'latitude' in col_lower:
                    lat_col = col
                elif 'lng' in col_lower or 'longitude' in col_lower or 'lon' in col_lower:
                    lng_col = col
            
            for idx, row in df.iterrows():
                try:
                    # Get place name
                    if name_col and pd.notna(row[name_col]):
                        original_name = str(row[name_col]).strip()
                        normalized_name = self.normalize_place_name(original_name)
                        
                        if normalized_name and len(normalized_name) > 2:
                            # Create or update place data
                            if normalized_name not in places_dict:
                                places_dict[normalized_name] = PlaceData(
                                    name=original_name,
                                    data_source=source
                                )
                            
                            place_data = places_dict[normalized_name]
                            
                            # Update with available information
                            if desc_col and pd.notna(row[desc_col]):
                                if not place_data.description:
                                    place_data.description = str(row[desc_col])
                            
                            if type_col and pd.notna(row[type_col]):
                                if not place_data.type:
                                    place_data.type = str(row[type_col])
                            
                            if lat_col and pd.notna(row[lat_col]):
                                try:
                                    lat = float(row[lat_col])
                                    if -90 <= lat <= 90:
                                        place_data.latitude = lat
                                except (ValueError, TypeError):
                                    pass
                            
                            if lng_col and pd.notna(row[lng_col]):
                                try:
                                    lng = float(row[lng_col])
                                    if -180 <= lng <= 180:
                                        place_data.longitude = lng
                                except (ValueError, TypeError):
                                    pass
                            
                            # Add additional columns if they exist
                            for col in df.columns:
                                col_lower = col.lower()
                                if 'phone' in col_lower and pd.notna(row[col]):
                                    place_data.phone = str(row[col])
                                elif 'email' in col_lower and pd.notna(row[col]):
                                    place_data.email = str(row[col])
                                elif 'website' in col_lower and pd.notna(row[col]):
                                    place_data.website = str(row[col])
                                elif 'image' in col_lower and pd.notna(row[col]):
                                    place_data.image = str(row[col])
                                elif 'rating' in col_lower and pd.notna(row[col]):
                                    try:
                                        place_data.rating = float(row[col])
                                    except (ValueError, TypeError):
                                        pass
                                elif 'address' in col_lower and pd.notna(row[col]):
                                    place_data.address = str(row[col])
                                    
                except Exception as e:
                    logger.warning(f"Error processing row {idx} in {source}: {e}")
                    continue
        
        logger.info(f"Matched {len(places_dict)} unique places across datasets")
        return places_dict
    
    def crawl_web_for_additional_info(self, places_dict: Dict[str, PlaceData]) -> Dict[str, PlaceData]:
        """Crawl the web for additional information about places"""
        logger.info("Starting web crawling for additional information...")
        
        # Focus on major attractions and places with websites
        places_to_crawl = []
        for name, place_data in places_dict.items():
            if (place_data.website or 
                any(keyword in name.lower() for keyword in ['union buildings', 'museum', 'park', 'monument', 'gallery'])):
                places_to_crawl.append((name, place_data))
        
        logger.info(f"Crawling {len(places_to_crawl)} places for additional information")
        
        for name, place_data in places_to_crawl[:20]:  # Limit to 20 for demo
            try:
                # Try to get additional info from website if available
                if place_data.website:
                    web_data = self.scrape_website(place_data.website)
                    if web_data:
                        place_data.web_data = web_data
                        place_data.verified_source = True
                        place_data.last_updated = time.strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Extract additional information
                        if 'description' in web_data and not place_data.description:
                            place_data.description = web_data['description']
                        if 'phone' in web_data and not place_data.phone:
                            place_data.phone = web_data['phone']
                        if 'email' in web_data and not place_data.email:
                            place_data.email = web_data['email']
                        if 'opening_hours' in web_data:
                            place_data.opening_hours = web_data['opening_hours']
                        if 'facilities' in web_data:
                            place_data.facilities = web_data['facilities']
                            
            except Exception as e:
                logger.warning(f"Error crawling {name}: {e}")
                continue
                
            # Add small delay to be respectful
            time.sleep(0.5)
        
        logger.info("Web crawling completed")
        return places_dict
    
    def scrape_website(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape a website for additional information"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract information
            data = {
                'title': soup.find('title').text if soup.find('title') else '',
                'description': '',
                'phone': '',
                'email': '',
                'opening_hours': '',
                'facilities': ''
            }
            
            # Extract description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                data['description'] = meta_desc.get('content', '')
            
            # Extract contact information
            text = soup.get_text()
            
            # Phone pattern
            phone_pattern = r'(\+27|0)[0-9\s\-\(\)]{8,15}'
            phones = re.findall(phone_pattern, text)
            if phones:
                data['phone'] = phones[0]
            
            # Email pattern
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            if emails:
                data['email'] = emails[0]
            
            return data
            
        except Exception as e:
            logger.warning(f"Error scraping {url}: {e}")
            return None
    
    def enrich_data(self, places_dict: Dict[str, PlaceData]) -> Dict[str, PlaceData]:
        """Enrich data with additional information"""
        logger.info("Enriching data with additional information...")
        
        for name, place_data in places_dict.items():
            # Generate weather suitability based on type and description
            if place_data.type:
                if 'museum' in place_data.type.lower() or 'gallery' in place_data.type.lower():
                    place_data.weather_suitability = "indoor"
                elif 'park' in place_data.type.lower() or 'garden' in place_data.type.lower():
                    place_data.weather_suitability = "outdoor"
                else:
                    place_data.weather_suitability = "all_weather"
            
            # Generate AI sentiment (simplified)
            description = place_data.description.lower()
            positive_words = ['beautiful', 'amazing', 'wonderful', 'great', 'excellent', 'stunning']
            negative_words = ['poor', 'bad', 'terrible', 'awful', 'disappointing']
            
            positive_count = sum(1 for word in positive_words if word in description)
            negative_count = sum(1 for word in negative_words if word in description)
            
            if positive_count > negative_count:
                place_data.ai_sentiment = "positive"
            elif negative_count > positive_count:
                place_data.ai_sentiment = "negative"
            else:
                place_data.ai_sentiment = "neutral"
            
            # Generate price range based on type
            if place_data.type:
                if 'hotel' in place_data.type.lower() or 'lodge' in place_data.type.lower():
                    place_data.price_range = "$$$"
                elif 'restaurant' in place_data.type.lower():
                    place_data.price_range = "$$"
                else:
                    place_data.price_range = "$"
            
            # Generate unique ID
            place_data.last_updated = time.strftime("%Y-%m-%d %H:%M:%S")
        
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
            
            # Determine type directory
            place_type = place_data.type.lower() if place_data.type else 'other'
            
            # Map types to directories
            type_mapping = {
                'hotel': 'accommodation',
                'lodge': 'accommodation',
                'guesthouse': 'accommodation',
                'restaurant': 'restaurant',
                'cafe': 'restaurant',
                'museum': 'museum',
                'gallery': 'museum',
                'park': 'nature',
                'garden': 'nature',
                'monument': 'historical',
                'attraction': 'attraction',
                'venue': 'venue',
                'shopping': 'shopping',
                'spa': 'spa',
                'service': 'service'
            }
            
            directory = type_mapping.get(place_type, 'other')
            
            if directory not in type_dirs:
                type_dir = self.output_dir / directory
                type_dir.mkdir(exist_ok=True)
                type_dirs[directory] = type_dir
            
            # Create CSV data
            csv_data = {
                'name': place_data.name,
                'description': place_data.description,
                'type': place_data.type,
                'category': place_data.category,
                'address': place_data.address,
                'latitude': place_data.latitude,
                'longitude': place_data.longitude,
                'phone': place_data.phone,
                'email': place_data.email,
                'website': place_data.website,
                'image': place_data.image,
                'rating': place_data.rating,
                'price_range': place_data.price_range,
                'opening_hours': place_data.opening_hours,
                'facilities': place_data.facilities,
                'special_features': place_data.special_features,
                'weather_suitability': place_data.weather_suitability,
                'ai_sentiment': place_data.ai_sentiment,
                'verified_source': place_data.verified_source,
                'data_source': place_data.data_source,
                'last_updated': place_data.last_updated
            }
            
            # Add web data if available
            if place_data.web_data:
                csv_data['web_title'] = place_data.web_data.get('title', '')
                csv_data['web_description'] = place_data.web_data.get('description', '')
                csv_data['web_phone'] = place_data.web_data.get('phone', '')
                csv_data['web_email'] = place_data.web_data.get('email', '')
                csv_data['web_opening_hours'] = place_data.web_data.get('opening_hours', '')
                csv_data['web_facilities'] = place_data.web_data.get('facilities', '')
            
            # Create DataFrame and save
            df = pd.DataFrame([csv_data])
            file_path = type_dirs[directory] / f"{safe_name}.csv"
            df.to_csv(file_path, index=False)
            
            logger.info(f"Created {file_path}")
        
        # Create summary report
        self.create_summary_report(places_dict, type_dirs)
        
        logger.info(f"Created {len(places_dict)} individual CSV files")
    
    def create_summary_report(self, places_dict: Dict[str, PlaceData], type_dirs: Dict[str, Path]):
        """Create a summary report of the processing"""
        summary = {
            'total_places': len(places_dict),
            'places_by_type': {},
            'places_with_coordinates': 0,
            'places_with_websites': 0,
            'verified_places': 0,
            'sentiment_distribution': {},
            'weather_distribution': {},
            'processing_timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'directories_created': list(type_dirs.keys())
        }
        
        for place_data in places_dict.values():
            # Count by type
            place_type = place_data.type.lower() if place_data.type else 'unknown'
            summary['places_by_type'][place_type] = summary['places_by_type'].get(place_type, 0) + 1
            
            # Count places with coordinates
            if place_data.latitude and place_data.longitude:
                summary['places_with_coordinates'] += 1
            
            # Count places with websites
            if place_data.website:
                summary['places_with_websites'] += 1
            
            # Count verified places
            if place_data.verified_source:
                summary['verified_places'] += 1
            
            # Count sentiment distribution
            sentiment = place_data.ai_sentiment
            summary['sentiment_distribution'][sentiment] = summary['sentiment_distribution'].get(sentiment, 0) + 1
            
            # Count weather distribution
            weather = place_data.weather_suitability
            summary['weather_distribution'][weather] = summary['weather_distribution'].get(weather, 0) + 1
        
        # Save summary report
        summary_file = self.output_dir / "processing_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Created summary report: {summary_file}")
    
    def run(self):
        """Run the complete data processing pipeline"""
        logger.info("Starting CSV data processing pipeline...")
        
        # Step 1: Discover CSV files
        csv_files = self.discover_csv_files()
        
        # Step 2: Load CSV data
        dataframes = self.load_csv_data(csv_files)
        
        # Step 3: Match places across datasets
        places_dict = self.match_places_across_datasets(dataframes)
        
        # Step 4: Crawl web for additional information
        places_dict = self.crawl_web_for_additional_info(places_dict)
        
        # Step 5: Enrich data
        places_dict = self.enrich_data(places_dict)
        
        # Step 6: Create individual CSV files
        self.create_individual_csv_files(places_dict)
        
        logger.info("CSV data processing pipeline completed successfully!")
        return places_dict

def main():
    """Main function to run the CSV data loader"""
    loader = CSVDataLoader()
    places_dict = loader.run()
    
    print(f"\n✅ Processing completed!")
    print(f"📊 Total places processed: {len(places_dict)}")
    print(f"📁 Output directory: {loader.output_dir}")
    print(f"📋 Summary report: {loader.output_dir}/processing_summary.json")
    
    # Show some statistics
    types_count = {}
    for place_data in places_dict.values():
        place_type = place_data.type.lower() if place_data.type else 'unknown'
        types_count[place_type] = types_count.get(place_type, 0) + 1
    
    print(f"\n📈 Places by type:")
    for place_type, count in sorted(types_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   {place_type.title()}: {count}")

if __name__ == "__main__":
    main() 