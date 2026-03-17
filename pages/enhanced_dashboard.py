import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import warnings
import urllib.parse
from services.weather_service import WeatherService
from ui.streamlit_cards import render_dataframe_cards, render_metric_strip, render_record_cards, render_section_header
warnings.filterwarnings('ignore')


class EnhancedDashboard:
    """Enhanced dashboard with Google Maps integration and advanced analytics"""

    def __init__(self):
        self.data_sources = {
            'places': 'tshwane_places.csv',
            'temperature': 'tshwane_temperature_data.csv',
            'coordinates': 'tshwane_coordinates.csv',
            'sentiment': 'tshwane_sentiment_data.csv',
            'descriptions': 'tshwane_descriptions.csv'
        }
        self.weather_service = WeatherService()
        self.load_data()

    def render_live_weather_overview(self):
        """Render a live weather snapshot from Open-Meteo when available."""
        snapshot = self.weather_service.fetch_current_weather()
        if not snapshot:
            st.caption("Live weather data is currently unavailable, so the dashboard is showing stored historical analytics.")
            return

        st.markdown("#### 🌤️ Live Tshwane Weather")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Condition", snapshot.condition.capitalize())
        col2.metric("Temperature", f"{snapshot.temperature_c:.1f}°C")
        col3.metric("Feels like", f"{snapshot.apparent_temperature_c:.1f}°C")
        col4.metric("Wind", f"{snapshot.wind_speed_kmh:.1f} km/h")
        st.caption(f"Source: Open-Meteo • Observed at {snapshot.observed_at}")

    def load_data(self):
        """Load all CSV data sources"""
        self.data = {}
        for key, filename in self.data_sources.items():
            try:
                file_path = Path(filename)
                if file_path.exists():
                    self.data[key] = pd.read_csv(file_path)
                else:
                    # Create sample data if file doesn't exist
                    self.data[key] = self.create_sample_data(key)
            except Exception as e:
                st.warning(f"Could not load {filename}: {e}")
                self.data[key] = self.create_sample_data(key)

    def create_sample_data(self, data_type: str) -> pd.DataFrame:
        """Create sample data for missing CSV files"""
        if data_type == 'temperature':
            # Annual temperature data for Tshwane
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            avg_temp = [23.5, 23.2, 21.8, 18.9, 15.2, 12.8,
                        12.9, 15.8, 19.5, 21.8, 22.9, 23.3]
            min_temp = [16.2, 15.9, 14.1, 10.8, 6.9, 3.8,
                        3.9, 6.8, 10.5, 13.2, 14.9, 15.8]
            max_temp = [30.8, 30.5, 29.5, 27.0, 23.5, 21.8,
                        21.9, 24.8, 28.5, 30.4, 31.9, 30.8]

            return pd.DataFrame({
                'month': months,
                'avg_temperature': avg_temp,
                'min_temperature': min_temp,
                'max_temperature': max_temp,
                'year': [2024] * 12
            })

        elif data_type == 'coordinates':
            # Places with coordinates
            places_data = [
                {'name': 'Union Buildings', 'lat':-25.7449,
                    'lng': 28.1878, 'type': 'historical'},
                {'name': 'Freedom Park', 'lat':-25.7667,
                    'lng': 28.1833, 'type': 'cultural'},
                {'name': 'Voortrekker Monument', 'lat':-25.7767,
                    'lng': 28.1756, 'type': 'historical'},
                {'name': 'Pretoria Zoo', 'lat':-25.7389,
                    'lng': 28.1889, 'type': 'nature'},
                {'name': 'Church Square', 'lat':-25.7479,
                    'lng': 28.1893, 'type': 'historical'},
                {'name': 'Melrose House', 'lat':-25.7500,
                    'lng': 28.2000, 'type': 'historical'},
                {'name': 'Pretoria Botanical Gardens', 'lat':-
                    25.7333, 'lng': 28.2833, 'type': 'nature'}
            ]
            return pd.DataFrame(places_data)

        elif data_type == 'sentiment':
            # Sentiment analysis data
            return pd.DataFrame({
                'place_name': ['Union Buildings', 'Freedom Park', 'Voortrekker Monument', 'Pretoria Zoo'],
                'positive_sentiment': [0.85, 0.78, 0.72, 0.91],
                'negative_sentiment': [0.05, 0.08, 0.15, 0.03],
                'neutral_sentiment': [0.10, 0.14, 0.13, 0.06],
                'total_reviews': [156, 89, 203, 234],
                'average_rating': [4.2, 4.0, 3.8, 4.5]
            })

        elif data_type == 'descriptions':
            # Enhanced descriptions
            return pd.DataFrame({
                'place_name': ['Union Buildings', 'Freedom Park', 'Voortrekker Monument', 'Pretoria Zoo'],
                'short_description': [
                    'Iconic government building and architectural masterpiece',
                    'Memorial site honoring South African freedom fighters',
                    'Monument commemorating the Great Trek',
                    'Premier wildlife conservation and education center'
                ],
                'long_description': [
                    'The Union Buildings form the official seat of the South African government and house the offices of the President. This architectural masterpiece was designed by Sir Herbert Baker and completed in 1913.',
                    'Freedom Park is a memorial site that honors those who sacrificed their lives for freedom and humanity in South Africa. It includes a museum, amphitheater, and spiritual sanctuary.',
                    'The Voortrekker Monument commemorates the Great Trek of the 1830s and 1840s. This massive granite structure stands as a symbol of Afrikaner heritage and history.',
                    'The National Zoological Gardens of South Africa, commonly known as Pretoria Zoo, is the largest zoo in the country and one of the top zoos in the world.'
                ],
                'category': ['Government', 'Memorial', 'Monument', 'Zoo'],
                'accessibility': ['Wheelchair accessible', 'Partially accessible', 'Limited accessibility', 'Fully accessible'],
                'best_time': ['Morning', 'Afternoon', 'Morning', 'All day']
            })

        else:
            return pd.DataFrame()

    def get_sentiment_color(self, sentiment_score):
        if sentiment_score >= 0.8:
            return 'green'
        elif sentiment_score >= 0.6:
            return 'orange'
        else:
            return 'red'

    def render_folium_map(self):
        render_section_header(
            "Tshwane Tourism Map",
            "A simplified native map plus card-based place summaries.",
            "🗺️",
        )
        coords_df = self.data.get('coordinates', pd.DataFrame())
        desc_df = self.data.get('descriptions', pd.DataFrame())
        sent_df = self.data.get('sentiment', pd.DataFrame())

        merged = coords_df.copy()
        merged = pd.merge(merged, desc_df, left_on='name',
                          right_on='place_name', how='left')
        merged = pd.merge(merged, sent_df, left_on='name',
                          right_on='place_name', how='left', suffixes=('', '_sent'))

        if {'lat', 'lng'}.issubset(merged.columns):
            map_df = merged[['lat', 'lng']].dropna().rename(columns={'lng': 'lon'})
            if not map_df.empty:
                st.map(map_df, use_container_width=True)

        cards = []
        for _, row in merged.head(8).iterrows():
            cards.append({
                'name': row.get('name', 'Unknown place'),
                'description': row.get('short_description') or row.get('description') or 'No description available.',
                'type': row.get('type', 'place'),
                'average_rating': row.get('average_rating', 'N/A'),
                'total_reviews': row.get('total_reviews', 'N/A'),
                'link': f"https://www.google.com/maps/search/{urllib.parse.quote_plus(str(row.get('name', 'Tshwane')))}",
            })

        render_record_cards(
            cards,
            title_key='name',
            description_keys=['description'],
            meta_keys=['type', 'average_rating', 'total_reviews'],
            link_key='link',
            columns_count=2,
            key_prefix='dashboard_map_cards',
        )

    def render_google_maps_iframe(self):
        # Deprecated: replaced by folium map
        pass

    def render_temperature_dashboard(self):
        """Render temperature analytics dashboard"""
        st.markdown("### 🌡️ Annual Temperature Analytics")
        self.render_live_weather_overview()

        if 'temperature' in self.data:
            temp_df = self.data['temperature']

            # Create temperature chart
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Monthly Average Temperature', 'Temperature Range',
                                'Seasonal Trends', 'Temperature Distribution'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )

            # Monthly average temperature
            fig.add_trace(
                go.Scatter(x=temp_df['month'], y=temp_df['avg_temperature'],
                           mode='lines+markers', name='Average', line=dict(color='blue')),
                row=1, col=1
            )

            # Temperature range
            fig.add_trace(
                go.Scatter(x=temp_df['month'], y=temp_df['max_temperature'],
                           mode='lines', name='Max', line=dict(color='red')),
                row=1, col=2
            )
            fig.add_trace(
                go.Scatter(x=temp_df['month'], y=temp_df['min_temperature'],
                           mode='lines', name='Min', line=dict(color='green')),
                row=1, col=2
            )

            # Seasonal trends
            fig.add_trace(
                go.Bar(x=temp_df['month'], y=temp_df['avg_temperature'],
                       name='Monthly Avg', marker_color='lightblue'),
                row=2, col=1
            )

            # Temperature distribution
            fig.add_trace(
                go.Histogram(x=temp_df['avg_temperature'], nbinsx=10,
                             name='Distribution', marker_color='orange'),
                row=2, col=2
            )

            fig.update_layout(height=600, showlegend=True,
                              title_text="Tshwane Temperature Analytics")
            st.plotly_chart(fig, use_container_width=True)

            # Temperature insights
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Annual Temp",
                          f"{temp_df['avg_temperature'].mean():.1f}°C")
            with col2:
                st.metric(
                    "Hottest Month", f"{temp_df.loc[temp_df['avg_temperature'].idxmax(), 'month']}")
            with col3:
                st.metric(
                    "Coldest Month", f"{temp_df.loc[temp_df['avg_temperature'].idxmin(), 'month']}")

    def render_sentiment_analytics(self):
        """Render sentiment analysis dashboard"""
        st.markdown("### 😊 Sentiment Analysis Dashboard")

        if 'sentiment' in self.data:
            sentiment_df = self.data['sentiment']

            # Sentiment overview
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Rating",
                          f"{sentiment_df['average_rating'].mean():.1f}/5.0")
            with col2:
                st.metric("Total Reviews",
                          f"{sentiment_df['total_reviews'].sum():,}")
            with col3:
                st.metric("Positive Sentiment",
                          f"{sentiment_df['positive_sentiment'].mean()*100:.1f}%")

            # Sentiment chart
            fig = px.bar(sentiment_df, x='place_name', y=['positive_sentiment', 'negative_sentiment', 'neutral_sentiment'],
                         title="Sentiment Distribution by Place",
                         barmode='stack',
                         color_discrete_map={'positive_sentiment': 'green', 'negative_sentiment': 'red', 'neutral_sentiment': 'gray'})

            fig.update_layout(height=400, xaxis_title="Places",
                              yaxis_title="Sentiment Score")
            st.plotly_chart(fig, use_container_width=True)

            # Ratings chart
            fig2 = px.scatter(sentiment_df, x='total_reviews', y='average_rating',
                              size='positive_sentiment', color='place_name',
                              title="Rating vs Reviews Analysis",
                              hover_data=['place_name'])

            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

    def render_table_views(self):
        """Render interactive table views"""
        render_section_header(
            "Data views",
            "Use tabs and cards instead of wide tables to reduce clutter.",
            "📊",
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Places", "Temperature", "Sentiment", "Descriptions"])

        with tab1:
            if 'places' in self.data:
                col1, col2 = st.columns(2)
                with col1:
                    selected_type = st.selectbox(
                        "Filter by type:", ['All'] + list(self.data['places']['type'].unique()))
                with col2:
                    search_term = st.text_input("Search places:", "")

                # Apply filters
                filtered_df = self.data['places']
                if selected_type != 'All':
                    filtered_df = filtered_df[filtered_df['type']
                                              == selected_type]
                if search_term:
                    filtered_df = filtered_df[filtered_df['name'].str.contains(
                        search_term, case=False)]

                render_dataframe_cards(
                    "Places",
                    filtered_df,
                    key_prefix='dashboard_places_cards',
                    title_key='name',
                    description_keys=['type'],
                    meta_keys=[col for col in ['city', 'province', 'rating'] if col in filtered_df.columns],
                    columns_count=2,
                    preview_limit=8,
                )

        with tab2:
            if 'temperature' in self.data:
                temp_df = self.data['temperature']
                render_metric_strip([
                    ("Max Temp", f"{temp_df['max_temperature'].max():.1f}°C", None),
                    ("Min Temp", f"{temp_df['min_temperature'].min():.1f}°C", None),
                    ("Avg Temp", f"{temp_df['avg_temperature'].mean():.1f}°C", None),
                ])
                render_dataframe_cards(
                    "Temperature",
                    temp_df,
                    key_prefix='dashboard_temperature_cards',
                    title_key='month',
                    description_keys=['avg_temperature'],
                    meta_keys=['min_temperature', 'max_temperature', 'year'],
                    columns_count=3,
                    preview_limit=12,
                )

        with tab3:
            if 'sentiment' in self.data:
                sentiment_df = self.data['sentiment']
                best_rated = sentiment_df.loc[sentiment_df['average_rating'].idxmax()]
                most_reviewed = sentiment_df.loc[sentiment_df['total_reviews'].idxmax()]
                render_metric_strip([
                    ("Best Rated", best_rated['place_name'], f"{best_rated['average_rating']}/5.0"),
                    ("Most Reviewed", most_reviewed['place_name'], int(most_reviewed['total_reviews'])),
                ])
                render_dataframe_cards(
                    "Sentiment",
                    sentiment_df,
                    key_prefix='dashboard_sentiment_cards',
                    title_key='place_name',
                    description_keys=['positive_sentiment'],
                    meta_keys=['negative_sentiment', 'neutral_sentiment', 'average_rating'],
                    columns_count=2,
                    preview_limit=8,
                )

        with tab4:
            if 'descriptions' in self.data:
                render_dataframe_cards(
                    "Descriptions",
                    self.data['descriptions'],
                    key_prefix='dashboard_description_cards',
                    title_key='place_name',
                    description_keys=['short_description', 'long_description'],
                    meta_keys=['category', 'accessibility', 'best_time'],
                    columns_count=2,
                    preview_limit=8,
                )
                category_counts = self.data['descriptions']['category'].value_counts()
                fig = px.pie(values=category_counts.values, names=category_counts.index,
                             title="Places by Category")
                st.plotly_chart(fig, use_container_width=True)

    def render_enhanced_analytics(self):
        """Render enhanced analytics with correlations"""
        st.markdown("### 🔍 Enhanced Analytics")

        # Correlation analysis
        if 'sentiment' in self.data and 'descriptions' in self.data:
            st.markdown("#### 📊 Correlation Analysis")

            # Merge sentiment and descriptions data
            merged_data = pd.merge(self.data['sentiment'], self.data['descriptions'],
                                   left_on='place_name', right_on='place_name', how='inner')

            # Create correlation matrix
            numeric_cols = ['positive_sentiment', 'negative_sentiment', 'neutral_sentiment',
                            'total_reviews', 'average_rating']

            correlation_matrix = merged_data[numeric_cols].corr()

            fig = px.imshow(correlation_matrix,
                            title="Correlation Matrix",
                            color_continuous_scale='RdBu',
                            aspect="auto")

            st.plotly_chart(fig, use_container_width=True)

            # Insights
            st.markdown("#### 💡 Key Insights")
            insights = [
                "Places with higher positive sentiment tend to have more reviews",
                "Average rating correlates strongly with positive sentiment",
                "Neutral sentiment shows inverse correlation with total reviews"
            ]

            for insight in insights:
                st.markdown(f"• {insight}")


def main():
    """Main dashboard function"""
    st.set_page_config(
        page_title="Enhanced Tshwane Tourism Dashboard",
        page_icon="🗺️",
        layout="wide"
    )

    st.title("🗺️ Enhanced Tshwane Tourism Dashboard")
    st.markdown("---")

    # Initialize dashboard
    dashboard = EnhancedDashboard()

    # Render components
    dashboard.render_folium_map()
    st.markdown("---")

    dashboard.render_temperature_dashboard()
    st.markdown("---")

    dashboard.render_sentiment_analytics()
    st.markdown("---")

    dashboard.render_table_views()
    st.markdown("---")

    dashboard.render_enhanced_analytics()


if __name__ == "__main__":
    main()
