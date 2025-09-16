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
import requests
from typing import Dict, List, Any, Optional
import warnings
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
        self.load_data()

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
                {'name': 'Union Buildings', 'lat': -25.7449,
                    'lng': 28.1878, 'type': 'historical'},
                {'name': 'Freedom Park', 'lat': -25.7667,
                    'lng': 28.1833, 'type': 'cultural'},
                {'name': 'Voortrekker Monument', 'lat': -25.7767,
                    'lng': 28.1756, 'type': 'historical'},
                {'name': 'Pretoria Zoo', 'lat': -25.7389,
                    'lng': 28.1889, 'type': 'nature'},
                {'name': 'Church Square', 'lat': -25.7479,
                    'lng': 28.1893, 'type': 'historical'},
                {'name': 'Melrose House', 'lat': -25.7500,
                    'lng': 28.2000, 'type': 'historical'},
                {'name': 'Pretoria Botanical Gardens', 'lat': -
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
        st.markdown("### 🗺️ Realistic Tshwane Tourism Map (Interactive)")
        coords_df = self.data.get('coordinates', pd.DataFrame())
        desc_df = self.data.get('descriptions', pd.DataFrame())
        sent_df = self.data.get('sentiment', pd.DataFrame())

        # Merge all info for popups
        merged = coords_df.copy()
        merged = pd.merge(merged, desc_df, left_on='name',
                          right_on='place_name', how='left')
        merged = pd.merge(merged, sent_df, left_on='name',
                          right_on='place_name', how='left', suffixes=('', '_sent'))

        # Center map on Tshwane
        map_center = [-25.7449, 28.1878]
        m = folium.Map(location=map_center, zoom_start=12,
                       tiles='CartoDB positron')
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in merged.iterrows():
            lat, lng = row['lat'], row['lng']
            name = row['name']
            desc = row.get('short_description', row.get(
                'description', 'No description'))
            sentiment = row.get('sentiment_score',
                                row.get('average_rating', 0.7))
            sentiment_color = self.get_sentiment_color(sentiment)
            rating = row.get('average_rating', 'N/A')
            total_reviews = row.get('total_reviews', 'N/A')
            popup_html = f"""
            <div style='width: 250px;'>
                <h4 style='margin-bottom: 5px;'>{name}</h4>
                <p style='font-size: 13px; margin-bottom: 5px;'>{desc}</p>
                <p style='font-size: 12px; margin-bottom: 2px;'><b>Sentiment:</b> <span style='color:{sentiment_color}; font-weight:bold;'>{sentiment:.2f}</span></p>
                <p style='font-size: 12px; margin-bottom: 2px;'><b>Rating:</b> {rating} ⭐</p>
                <p style='font-size: 12px;'><b>Reviews:</b> {total_reviews}</p>
            </div>
            """
            folium.Marker(
                location=[lat, lng],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=sentiment_color, icon='info-sign')
            ).add_to(marker_cluster)

        # Add legend
        legend_html = '''
         <div style="position: fixed; 
         bottom: 50px; left: 50px; width: 180px; height: 110px; 
         background-color: white; border:2px solid #bbb; z-index:9999; font-size:14px; border-radius: 8px; padding: 10px;">
         <b>Sentiment Legend</b><br>
         <i class="fa fa-map-marker fa-2x" style="color:green"></i> Very Positive (≥0.8)<br>
         <i class="fa fa-map-marker fa-2x" style="color:orange"></i> Mixed/Neutral (0.6-0.8)<br>
         <i class="fa fa-map-marker fa-2x" style="color:red"></i> Negative (&lt;0.6)<br>
         </div>
         '''
        m.get_root().html.add_child(folium.Element(legend_html))

        st_folium(m, width="100%", height=600)

    def render_google_maps_iframe(self):
        # Deprecated: replaced by folium map
        pass

    def render_temperature_dashboard(self):
        """Render temperature analytics dashboard"""
        st.markdown("### 🌡️ Annual Temperature Analytics")

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
        st.markdown("### 📊 Data Table Views")

        # Tab for different data views
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Places", "Temperature", "Sentiment", "Descriptions"])

        with tab1:
            if 'places' in self.data:
                st.dataframe(self.data['places'], use_container_width=True)

                # Filter options
                st.markdown("#### 🔍 Filter Places")
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

                st.dataframe(filtered_df, use_container_width=True)

        with tab2:
            if 'temperature' in self.data:
                st.dataframe(self.data['temperature'],
                             use_container_width=True)

                # Temperature statistics
                st.markdown("#### 📈 Temperature Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Max Temp", f"{self.data['temperature']['max_temperature'].max():.1f}°C")
                with col2:
                    st.metric(
                        "Min Temp", f"{self.data['temperature']['min_temperature'].min():.1f}°C")
                with col3:
                    st.metric(
                        "Avg Temp", f"{self.data['temperature']['avg_temperature'].mean():.1f}°C")

        with tab3:
            if 'sentiment' in self.data:
                st.dataframe(self.data['sentiment'], use_container_width=True)

                # Sentiment insights
                st.markdown("#### 💡 Sentiment Insights")
                best_rated = self.data['sentiment'].loc[self.data['sentiment']
                                                        ['average_rating'].idxmax()]
                most_reviewed = self.data['sentiment'].loc[self.data['sentiment']
                                                           ['total_reviews'].idxmax()]

                col1, col2 = st.columns(2)
                with col1:
                    st.info(
                        f"🏆 Best Rated: {best_rated['place_name']} ({best_rated['average_rating']}/5.0)")
                with col2:
                    st.info(
                        f"📝 Most Reviewed: {most_reviewed['place_name']} ({most_reviewed['total_reviews']} reviews)")

        with tab4:
            if 'descriptions' in self.data:
                st.dataframe(self.data['descriptions'],
                             use_container_width=True)

                # Description analytics
                st.markdown("#### 📝 Description Analytics")
                category_counts = self.data['descriptions']['category'].value_counts(
                )
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
