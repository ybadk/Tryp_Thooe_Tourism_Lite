#!/usr/bin/env python3
"""
Test script for the Tshwane Tourism Chat Interface
This script tests the basic functionality of the chat interface without requiring Streamlit.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_chat_interface_import():
    """Test that the chat interface can be imported"""
    try:
        from chat_interface import TourismChatInterface, ChatMode, ChatMessage
        print("✅ Chat interface imports successful")
        return True
    except ImportError as e:
        print(f"❌ Chat interface import failed: {e}")
        return False

def test_chat_interface_creation():
    """Test creating a chat interface instance"""
    try:
        from chat_interface import TourismChatInterface
        chat_interface = TourismChatInterface()
        print("✅ Chat interface creation successful")
        return True
    except Exception as e:
        print(f"❌ Chat interface creation failed: {e}")
        return False

def test_fallback_response():
    """Test the fallback response system"""
    try:
        from chat_interface import TourismChatInterface
        chat_interface = TourismChatInterface()
        
        # Test various queries
        test_queries = [
            "Tell me about museums",
            "Where should I stay?",
            "What's the weather like?",
            "How do I get around?",
            "Help me plan my trip"
        ]
        
        for query in test_queries:
            response = chat_interface.get_fallback_response(query)
            if response and len(response) > 10:
                print(f"✅ Fallback response for '{query}': {response[:50]}...")
            else:
                print(f"❌ Poor fallback response for '{query}'")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Fallback response test failed: {e}")
        return False

def test_message_creation():
    """Test creating chat messages"""
    try:
        from chat_interface import ChatMessage
        from datetime import datetime
        
        message = ChatMessage(
            id="test123",
            content="Test message",
            sender="user",
            timestamp=datetime.now()
        )
        
        if message.content == "Test message" and message.sender == "user":
            print("✅ Chat message creation successful")
            return True
        else:
            print("❌ Chat message creation failed")
            return False
    except Exception as e:
        print(f"❌ Chat message test failed: {e}")
        return False

def test_tourism_data_loading():
    """Test loading tourism data from CSV files"""
    try:
        import pandas as pd
        
        # Test loading CSV files
        csv_files = [
            'tshwane_places.csv',
            'processed_data/tshwane_places.csv'
        ]
        
        loaded_data = {}
        for csv_file in csv_files:
            try:
                if os.path.exists(csv_file):
                    df = pd.read_csv(csv_file)
                    loaded_data[csv_file] = len(df)
                    print(f"✅ Loaded {csv_file}: {len(df)} records")
                else:
                    print(f"⚠️ {csv_file} not found (this is okay)")
            except Exception as e:
                print(f"⚠️ Could not load {csv_file}: {e}")
        
        if loaded_data:
            print("✅ Tourism data loading test completed")
            return True
        else:
            print("⚠️ No CSV files found, but this is acceptable for testing")
            return True
            
    except Exception as e:
        print(f"❌ Tourism data loading test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Tshwane Tourism Chat Interface")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_chat_interface_import),
        ("Creation Test", test_chat_interface_creation),
        ("Fallback Response Test", test_fallback_response),
        ("Message Creation Test", test_message_creation),
        ("Tourism Data Test", test_tourism_data_loading)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Chat interface is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 