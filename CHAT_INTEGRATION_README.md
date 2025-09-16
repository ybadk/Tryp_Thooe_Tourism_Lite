# 🌿 Tshwane Tourism Chat Interface Integration

## Overview

This document describes the integration of an AI-powered chat interface into the Tshwane Tourism Interactive Portal. The chat interface provides intelligent assistance for tourism-related queries using Retrieval-Augmented Generation (RAG) technology.

## Features

### 🤖 AI Chat Assistant
- **RAG-Powered Responses**: Uses LangChain to provide intelligent responses based on tourism data
- **Multi-Mode Support**: Different chat modes for various use cases
- **Real-time Interaction**: Instant responses to user queries
- **Context Awareness**: Maintains conversation history for better responses

### 🎯 Chat Modes
1. **Tourism Assistant**: General tourism information and recommendations
2. **Website Chat**: Chat with specific tourism websites
3. **Booking Help**: Assistance with booking queries
4. **Planning Guide**: Help with trip planning

### ⚡ Quick Actions
- Pre-defined buttons for common queries
- Instant access to popular topics
- Streamlined user experience

### 📊 Analytics
- Chat message analytics
- User interaction tracking
- Response time monitoring

## Installation

### Prerequisites
- Python 3.8+
- Streamlit
- Hugging Face models (local, no API key required)

### Setup Steps

1. **Install Dependencies**
   ```bash
   pip install -r chat_requirements.txt
   ```

2. **Environment Variables** (Optional)
   Create a `.env` file in the project root for additional configuration:
   ```env
   # Optional: Set device for model loading
   DEVICE=cpu  # or cuda for GPU
   ```

3. **Run the Application**
   ```bash
   streamlit run tshwane_tourism_app.py
   ```

## Usage

### Accessing the Chat Interface

1. **From the Main App**: Click "AI Chat Assistant" in the sidebar navigation
2. **Direct Access**: Navigate to the chat section in the main interface

### Using the Chat

1. **Select Chat Mode**: Choose from available modes in the dropdown
2. **Ask Questions**: Type your tourism-related questions
3. **Use Quick Actions**: Click pre-defined buttons for common queries
4. **View Analytics**: Monitor chat performance and insights

### Example Queries

```
User: "What museums are worth visiting in Tshwane?"
Assistant: "🏛️ Tshwane has several excellent museums! I recommend the Ditsong National Museum of Cultural History, the Pretoria Art Museum, and the Voortrekker Monument..."

User: "Where should I stay in Tshwane?"
Assistant: "🏨 Tshwane has accommodation for every budget! From luxury hotels in the city center to cozy guesthouses in the suburbs..."

User: "Help me plan my Tshwane trip"
Assistant: "🗺️ Let me help you plan your Tshwane visit! I can suggest itineraries based on your interests, time available, and budget..."
```

## Technical Architecture

### Core Components

1. **TourismChatInterface Class**
   - Main chat interface controller
   - Manages chat history and state
   - Handles AI response generation

2. **RAG Integration**
   - Vector store creation from tourism websites
   - Context-aware retrieval
   - Conversational chain management

3. **Fallback System**
   - Rule-based responses when AI is unavailable
   - Tourism-specific knowledge base
   - Graceful degradation

### Data Sources

- **CSV Files**: Tourism data from local CSV files
- **Websites**: Real-time data from tourism websites
- **Session State**: User preferences and chat history

### AI Models

- **Primary**: Microsoft Phi-4-mini-flash-reasoning (local Hugging Face model)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Fallback**: Rule-based response system
- **Vector Store**: ChromaDB for document retrieval

## Code Structure

```
chat_interface.py
├── TourismChatInterface Class
│   ├── load_tourism_data()
│   ├── get_vectorstore_from_url()
│   ├── get_context_retriever_chain()
│   ├── get_conversational_rag_chain()
│   ├── get_ai_response()
│   ├── get_fallback_response()
│   ├── add_message()
│   ├── display_chat_interface()
│   ├── display_quick_actions()
│   └── display_chat_analytics()
└── display_chat_interface_main()
```

## Integration Points

### Main Application Integration
- **Sidebar Navigation**: Added "AI Chat Assistant" option
- **Main Content**: Chat interface displays in main content area
- **Session State**: Shared state management with main app

### Data Integration
- **Tourism Data**: Uses existing tourism data from CSV files
- **Website Data**: Integrates with scraped website data
- **User Preferences**: Maintains user settings across sessions

## Best Practices Implemented

### From System Prompts Analysis

1. **Modular Design**
   - Separate chat interface module
   - Clean separation of concerns
   - Reusable components

2. **Error Handling**
   - Graceful fallbacks when AI is unavailable
   - Comprehensive exception handling
   - User-friendly error messages

3. **Performance Optimization**
   - Caching for vector stores
   - Efficient data loading
   - Minimal API calls

4. **User Experience**
   - Intuitive interface design
   - Quick action buttons
   - Real-time feedback

5. **Accessibility**
   - Clear visual hierarchy
   - Descriptive button labels
   - Screen reader friendly

## Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### Chat Settings
- **Max History**: 10 messages (configurable)
- **Response Timeout**: 30 seconds
- **Vector Store**: ChromaDB with OpenAI embeddings

## Troubleshooting

### Common Issues

1. **LangChain Import Error**
   ```bash
   pip install langchain langchain-openai
   ```

2. **OpenAI API Key Missing**
   - Create `.env` file with your API key
   - Restart the application

3. **Vector Store Creation Fails**
   - Check internet connection
   - Verify website URLs are accessible
   - Check API key validity

### Debug Mode
Enable debug mode by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Planned Features
- **Multi-language Support**: Afrikaans, Zulu, and other local languages
- **Voice Integration**: Speech-to-text and text-to-speech
- **Advanced Analytics**: Detailed chat insights and metrics
- **Personalization**: User preference learning
- **Integration APIs**: Connect with booking systems

### Technical Improvements
- **Caching**: Redis integration for better performance
- **Scalability**: Microservices architecture
- **Security**: Enhanced data encryption
- **Monitoring**: Real-time performance monitoring

## Contributing

### Development Guidelines
1. Follow the existing code structure
2. Add comprehensive error handling
3. Include unit tests for new features
4. Update documentation for changes
5. Follow the established naming conventions

### Testing
```bash
# Run chat interface tests
python -m pytest tests/test_chat_interface.py

# Run integration tests
python -m pytest tests/test_integration.py
```

## License

This chat interface integration is part of the Tshwane Tourism Interactive Portal project and follows the same licensing terms.

## Support

For technical support or questions about the chat interface:
- Check the troubleshooting section above
- Review the code comments and documentation
- Contact the development team

---

**Note**: This chat interface enhances the Tshwane Tourism Portal by providing intelligent, context-aware assistance to users seeking tourism information and planning help. 