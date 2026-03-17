"""
Integrated Data Processor that works with existing AI agents
Uses Hugging Face models to avoid API dependencies
"""

import streamlit as st
import pandas as pd
import json
import os
import sys
from pathlib import Path
import importlib.util
from transformers import pipeline
import torch
import warnings
from services.weather_service import WeatherService
warnings.filterwarnings('ignore')

# Add existing agent directories to path
current_dir = Path(__file__).parent
agent_dirs = [
    'ai_data_analysis_agent',
    'ai_data_visualisation_agent',
    'ai_travel_agent',
    'customer_support_voice_agent',
    'opeani_research_agent'
]

for agent_dir in agent_dirs:
    agent_path = current_dir / agent_dir
    if agent_path.exists():
        sys.path.append(str(agent_path))


class IntegratedTshwaneProcessor:
    """Integrated processor using existing AI agents and Hugging Face models"""
    
    def __init__(self):
        self.data_folder = "processed_data"
        self.ensure_data_folder()
        self.models = {}
        self.weather_service = WeatherService()
        self.load_huggingface_models()
    
    def ensure_data_folder(self):
        """Create data folder if it doesn't exist"""
        Path(self.data_folder).mkdir(exist_ok=True)
    
    def load_huggingface_models(self):
        """Load Hugging Face models for various tasks"""
        try:
            st.info("🤖 Loading Hugging Face models...")
            
            # Text classification for content categorization
            self.models['classifier'] = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Sentiment analysis
            self.models['sentiment'] = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Named Entity Recognition
            self.models['ner'] = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Text summarization
            self.models['summarizer'] = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=0 if torch.cuda.is_available() else -1
            )
            
            st.success("✅ All Hugging Face models loaded successfully!")
            
        except Exception as e:
            st.warning(f"⚠️ Some models failed to load: {e}")
            # Fallback to CPU-only models
            self.load_fallback_models()
    
    def load_fallback_models(self):
        """Load lighter models as fallback"""
        try:
            self.models['sentiment'] = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            
            self.models['classifier'] = pipeline(
                "text-classification",
                model="distilbert-base-uncased"
            )
            
            st.info("✅ Fallback models loaded")
            
        except Exception as e:
            st.error(f"❌ Failed to load fallback models: {e}")
    
    def process_with_data_analysis_agent(self, csv_file):
        """Use the existing data analysis agent"""
        try:
            # Import the data analysis functions
            spec = importlib.util.spec_from_file_location(
                "data_analyst",
                "ai_data_analysis_agent/ai_data_analyst.py"
            )
            data_analyst = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(data_analyst)
            
            # Process the CSV file
            if os.path.exists(csv_file):
                df = pd.read_csv(csv_file)
                
                # Use the preprocessing function from the agent
                temp_path, columns, processed_df = data_analyst.preprocess_and_save(csv_file)
                
                return {
                    'processed_data': processed_df,
                    'columns': columns,
                    'temp_path': temp_path,
                    'summary': {
                        'rows': len(processed_df),
                        'columns': len(columns),
                        'data_types': processed_df.dtypes.to_dict()
                    }
                }
            
        except Exception as e:
            st.error(f"❌ Error with data analysis agent: {e}")
            return None
    
    def process_with_visualization_agent(self, data, query):
        """Use the existing visualization agent concepts"""
        try:
            # Create visualizations using the patterns from the viz agent
            import plotly.express as px
            import plotly.graph_objects as go
            
            if isinstance(data, pd.DataFrame):
                # Generate automatic visualizations
                visualizations = []
                
                # Categorical data visualization
                categorical_cols = data.select_dtypes(include=['object']).columns
                for col in categorical_cols[:3]:  # Limit to 3 columns
                    if data[col].nunique() < 20:  # Only if not too many categories
                        fig = px.bar(
                            data[col].value_counts().reset_index(),
                            x='index', y=col,
                            title=f'Distribution of {col}'
                        )
                        visualizations.append(fig)
                
                # Numerical data visualization
                numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
                for col in numerical_cols[:3]:  # Limit to 3 columns
                    fig = px.histogram(data, x=col, title=f'Distribution of {col}')
                    visualizations.append(fig)
                
                return visualizations
            
        except Exception as e:
            st.error(f"❌ Error with visualization: {e}")
            return []
    
    def analyze_tourism_content(self, content_list):
        """Analyze tourism content using Hugging Face models"""
        results = {
            'categorized_content': {},
            'sentiment_analysis': {},
            'entities': {},
            'summaries': {}
        }
        
        # Categories for tourism content
        tourism_categories = [
            "tourist attractions and places",
            "restaurants and dining",
            "accommodation and hotels",
            "events and activities",
            "transportation and travel",
            "general information"
        ]
        
        for i, content in enumerate(content_list[:50]):  # Limit processing
            if len(content.strip()) < 20:  # Skip very short content
                continue
            
            try:
                # Categorize content
                if 'classifier' in self.models:
                    classification = self.models['classifier'](content, tourism_categories)
                    category = classification['labels'][0]
                    
                    if category not in results['categorized_content']:
                        results['categorized_content'][category] = []
                    results['categorized_content'][category].append(content)
                
                # Analyze sentiment
                if 'sentiment' in self.models:
                    sentiment = self.models['sentiment'](content[:512])  # Limit length
                    results['sentiment_analysis'][i] = sentiment[0]
                
                # Extract entities
                if 'ner' in self.models:
                    entities = self.models['ner'](content[:512])
                    results['entities'][i] = entities
                
                # Generate summary for longer content
                if len(content) > 200 and 'summarizer' in self.models:
                    try:
                        summary = self.models['summarizer'](
                            content[:1024],
                            max_length=100,
                            min_length=30
                        )
                        results['summaries'][i] = summary[0]['summary_text']
                    except:
                        pass  # Skip if summarization fails
                
            except Exception as e:
                st.warning(f"⚠️ Error processing content {i}: {e}")
                continue
        
        return results
    
    def create_tourism_dataframes(self, analyzed_content):
        """Create structured dataframes from analyzed content"""
        dataframes = {}
        
        # Create dataframe for each category
        for category, content_list in analyzed_content['categorized_content'].items():
            df_data = []
            for content in content_list:
                df_data.append({
                    'content': content,
                    'category': category,
                    'length': len(content),
                    'word_count': len(content.split()),
                    'processed_at': pd.Timestamp.now()
                })
            
            if df_data:
                dataframes[category] = pd.DataFrame(df_data)
        
        # Create sentiment dataframe
        sentiment_data = []
        for idx, sentiment in analyzed_content['sentiment_analysis'].items():
            sentiment_data.append({
                'content_index': idx,
                'label': sentiment['label'],
                'score': sentiment['score'],
                'processed_at': pd.Timestamp.now()
            })
        
        if sentiment_data:
            dataframes['sentiment_analysis'] = pd.DataFrame(sentiment_data)
        
        # Create entities dataframe
        entity_data = []
        for idx, entities in analyzed_content['entities'].items():
            for entity in entities:
                entity_data.append({
                    'content_index': idx,
                    'entity_text': entity['word'],
                    'entity_label': entity['entity_group'],
                    'confidence': entity['score'],
                    'processed_at': pd.Timestamp.now()
                })
        
        if entity_data:
            dataframes['entities'] = pd.DataFrame(entity_data)
        
        return dataframes
    
    def generate_weather_recommendations(self, places_df, weather_condition=None):
        """Generate weather-based recommendations using AI"""
        if places_df is None or places_df.empty:
            return pd.DataFrame()

        resolved_condition = weather_condition or "auto"
        snapshot = None
        if str(resolved_condition).lower() in {"auto", "current", "live"}:
            snapshot = self.weather_service.fetch_current_weather()
            resolved_condition = snapshot.condition if snapshot else "mild"

        scored_places = self.weather_service.score_places_for_weather(
            places_df.to_dict('records'),
            resolved_condition,
            limit=10,
        )

        recommendations = []
        for place in scored_places:
            recommendations.append({
                'place': place.get('name') or str(place.get('content', ''))[:100],
                'weather_suitability_score': place.get('weather_suitability_score', 0),
                'weather_condition': resolved_condition,
                'recommended_for': place.get('reason', 'Matched by live weather scoring'),
                'live_weather_summary': self.weather_service.format_summary(snapshot) if snapshot else ''
            })

        return pd.DataFrame(recommendations)
    
    def save_all_processed_data(self, dataframes, analyzed_content):
        """Save all processed data to files"""
        try:
            # Save dataframes as CSV
            for name, df in dataframes.items():
                filename = f"{self.data_folder}/tshwane_{name.replace(' ', '_')}.csv"
                df.to_csv(filename, index=False)
                st.success(f"✅ Saved {filename}")
            
            # Save analyzed content as JSON
            with open(f"{self.data_folder}/analyzed_content.json", 'w', encoding='utf-8') as f:
                json.dump(analyzed_content, f, indent=2, ensure_ascii=False, default=str)
            
            # Create summary report
            summary = {
                'processing_date': pd.Timestamp.now().isoformat(),
                'total_categories': len(analyzed_content['categorized_content']),
                'total_content_pieces': sum(len(content_list) for content_list in analyzed_content['categorized_content'].values()),
                'sentiment_distribution': self.calculate_sentiment_distribution(analyzed_content),
                'top_entities': self.get_top_entities(analyzed_content),
                'dataframes_created': list(dataframes.keys())
            }
            
            with open(f"{self.data_folder}/processing_summary.json", 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            
            st.success(f"✅ All data saved to {self.data_folder}/")
            return summary
            
        except Exception as e:
            st.error(f"❌ Error saving data: {e}")
            return None
    
    def calculate_sentiment_distribution(self, analyzed_content):
        """Calculate sentiment distribution"""
        sentiments = {}
        for sentiment_data in analyzed_content['sentiment_analysis'].values():
            label = sentiment_data['label']
            sentiments[label] = sentiments.get(label, 0) + 1
        return sentiments
    
    def get_top_entities(self, analyzed_content):
        """Get top entities by frequency"""
        entity_counts = {}
        for entities in analyzed_content['entities'].values():
            for entity in entities:
                entity_text = entity['word']
                entity_counts[entity_text] = entity_counts.get(entity_text, 0) + 1
        
        # Return top 10 entities
        sorted_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_entities[:10])


def main():
    """Main function for Streamlit app"""
    st.title("🤖 Integrated Tshwane Tourism Data Processor")
    st.markdown("*Using Hugging Face models and existing AI agents*")
    
    processor = IntegratedTshwaneProcessor()
    
    # File upload section
    st.header("📁 Upload Tourism Data")
    uploaded_file = st.file_uploader(
        "Upload CSV file with tourism content",
        type=['csv']
    )
    
    if uploaded_file:
        # Save uploaded file
        with open("temp_upload.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process with data analysis agent
        st.header("📊 Data Analysis")
        analysis_result = processor.process_with_data_analysis_agent("temp_upload.csv")
        
        if analysis_result:
            st.success("✅ Data analysis completed!")
            st.json(analysis_result['summary'])
            
            # Show data preview
            st.subheader("Data Preview")
            st.dataframe(analysis_result['processed_data'].head())
            
            # Process content with AI models
            st.header("🤖 AI Content Analysis")
            if st.button("Analyze Content with AI"):
                with st.spinner("Processing with Hugging Face models..."):
                    # Extract content for analysis
                    content_list = []
                    for col in analysis_result['processed_data'].columns:
                        if analysis_result['processed_data'][col].dtype == 'object':
                            content_list.extend(
                                analysis_result['processed_data'][col].dropna().astype(str).tolist()
                            )
                    
                    # Analyze content
                    analyzed_content = processor.analyze_tourism_content(content_list)
                    
                    # Create dataframes
                    dataframes = processor.create_tourism_dataframes(analyzed_content)
                    
                    # Save all data
                    summary = processor.save_all_processed_data(dataframes, analyzed_content)
                    
                    if summary:
                        st.success("✅ AI analysis completed!")
                        st.json(summary)
                        
                        # Display results
                        st.subheader("📈 Analysis Results")
                        
                        # Show categorized content
                        if 'categorized_content' in analyzed_content:
                            st.write("**Content Categories:**")
                            for category, content_list in analyzed_content['categorized_content'].items():
                                st.write(f"- {category}: {len(content_list)} items")
                        
                        # Show sentiment distribution
                        if 'sentiment_analysis' in analyzed_content:
                            sentiment_dist = processor.calculate_sentiment_distribution(analyzed_content)
                            st.write("**Sentiment Distribution:**")
                            st.bar_chart(sentiment_dist)
                        
                        # Weather recommendations
                        st.subheader("🌤️ Weather-Based Recommendations")
                        weather_condition = st.selectbox(
                            "Select weather condition:",
                            ["sunny", "rainy", "cloudy", "hot", "cold"]
                        )
                        
                        if st.button("Get Weather Recommendations"):
                            places_df = dataframes.get('tourist attractions and places')
                            if places_df is not None:
                                recommendations = processor.generate_weather_recommendations(
                                    places_df, weather_condition
                                )
                                if not recommendations.empty:
                                    st.dataframe(recommendations)
                                else:
                                    st.info("No specific recommendations for this weather condition.")
                            else:
                                st.info("No places data available for recommendations.")
            
            # Visualization section
            st.header("📊 Data Visualization")
            if st.button("Generate Visualizations"):
                visualizations = processor.process_with_visualization_agent(
                    analysis_result['processed_data'],
                    "Show me the data distribution"
                )
                
                for viz in visualizations:
                    st.plotly_chart(viz, use_container_width=True)
    
    else:
        st.info("Please upload a CSV file to begin processing.")
        
        # Show example of what the processor can do
        st.header("🎯 What This Processor Can Do")
        st.markdown("""
        - **🤖 AI-Powered Content Analysis**: Uses Hugging Face models for sentiment analysis, entity recognition, and content categorization
        - **📊 Data Processing**: Integrates with existing data analysis agents
        - **📈 Visualization**: Creates automatic visualizations of tourism data
        - **🌤️ Smart Recommendations**: Generates weather-based place recommendations
        - **💾 Data Export**: Saves processed data in multiple formats (CSV, JSON)
        - **🔒 No API Keys Required**: Uses open-source Hugging Face models
        """)


if __name__ == "__main__":
    main()
