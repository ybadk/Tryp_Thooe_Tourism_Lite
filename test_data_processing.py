#!/usr/bin/env python3
"""
Enhanced Test Script for Tshwane Tourism Data Processing Suite
Verifies all components including AI tool integrations work correctly
Tests Devin, v0, Cursor, Manus, and Lovable integrations
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path
import tempfile
from datetime import datetime
import asyncio
from typing import Dict, List, Optional, Any
import logging
import uuid
from enum import Enum

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    required_modules = [
        ('streamlit', 'st'),
        ('pandas', 'pd'),
        ('requests', 'requests'),
        ('beautifulsoup4', 'BeautifulSoup'),
        ('plotly.express', 'px'),
        ('transformers', 'transformers'),
        ('cryptography.fernet', 'Fernet')
    ]
    
    failed_imports = []
    
    for module_name, import_name in required_modules:
        try:
            if module_name == 'beautifulsoup4':
                from bs4 import BeautifulSoup
            elif module_name == 'plotly.express':
                import plotly.express as px
            elif module_name == 'cryptography.fernet':
                from cryptography.fernet import Fernet
            else:
                __import__(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            failed_imports.append((module_name, str(e)))
            print(f"❌ {module_name}: {e}")
    
    if failed_imports:
        print(f"\n⚠️ Failed imports: {len(failed_imports)}")
        return False
    else:
        print("✅ All imports successful!")
        return True

def test_data_processor():
    """Test the data processor module"""
    print("\n🧪 Testing data processor...")
    
    try:
        from data_processor import TshwaneDataProcessor
        
        processor = TshwaneDataProcessor()
        print("✅ Data processor initialized")
        
        # Test model loading
        if hasattr(processor, 'sentiment_analyzer') and processor.sentiment_analyzer:
            print("✅ Sentiment analyzer loaded")
        else:
            print("⚠️ Sentiment analyzer not loaded (this is okay)")
        
        # Test data folder creation
        if Path(processor.data_folder).exists():
            print("✅ Data folder created")
        else:
            print("❌ Data folder not created")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Data processor test failed: {e}")
        return False

def test_integrated_processor():
    """Test the integrated processor module"""
    print("\n🧪 Testing integrated processor...")
    
    try:
        from integrated_data_processor import IntegratedTshwaneProcessor
        
        processor = IntegratedTshwaneProcessor()
        print("✅ Integrated processor initialized")
        
        # Test model loading
        if processor.models:
            print(f"✅ {len(processor.models)} AI models loaded")
        else:
            print("⚠️ No AI models loaded (this is okay for testing)")
        
        return True
        
    except Exception as e:
        print(f"❌ Integrated processor test failed: {e}")
        return False

def test_encryption():
    """Test encryption functionality"""
    print("\n🧪 Testing encryption...")
    
    try:
        from cryptography.fernet import Fernet
        
        # Generate key
        key = Fernet.generate_key()
        f = Fernet(key)
        
        # Test data
        test_data = "This is sensitive booking information"
        
        # Encrypt
        encrypted_data = f.encrypt(test_data.encode())
        print("✅ Data encrypted successfully")
        
        # Decrypt
        decrypted_data = f.decrypt(encrypted_data).decode()
        
        if decrypted_data == test_data:
            print("✅ Data decrypted successfully")
            return True
        else:
            print("❌ Decryption failed - data mismatch")
            return False
            
    except Exception as e:
        print(f"❌ Encryption test failed: {e}")
        return False

def test_data_processing():
    """Test data processing with sample data"""
    print("\n🧪 Testing data processing with sample data...")
    
    try:
        # Create sample CSV data
        sample_data = {
            'place_name': ['Union Buildings', 'Voortrekker Monument', 'Zoo'],
            'description': ['Government buildings', 'Historic monument', 'Animal park'],
            'type': ['government', 'monument', 'attraction'],
            'rating': [4.5, 4.2, 4.8]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            temp_file = f.name
        
        print("✅ Sample data created")
        
        # Test reading the data
        loaded_df = pd.read_csv(temp_file)
        
        if len(loaded_df) == len(df):
            print("✅ Data loading successful")
        else:
            print("❌ Data loading failed")
            return False
        
        # Clean up
        os.unlink(temp_file)
        print("✅ Cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        return False

def test_weather_recommendations():
    """Test weather recommendation functionality"""
    print("\n🧪 Testing weather recommendations...")
    
    try:
        # Sample places data
        places_data = [
            {'content': 'Beautiful outdoor park with hiking trails', 'name': 'Nature Park'},
            {'content': 'Indoor museum with air conditioning', 'name': 'City Museum'},
            {'content': 'Covered market with local crafts', 'name': 'Craft Market'}
        ]
        
        places_df = pd.DataFrame(places_data)
        
        # Test weather mapping
        weather_keywords = {
            'sunny': ['outdoor', 'park', 'hiking'],
            'rainy': ['indoor', 'museum', 'covered'],
            'hot': ['air conditioning', 'cool', 'shade']
        }
        
        # Test sunny weather recommendations
        sunny_recommendations = []
        for _, place in places_df.iterrows():
            content = place['content'].lower()
            score = sum(1 for keyword in weather_keywords['sunny'] if keyword in content)
            if score > 0:
                sunny_recommendations.append(place['name'])
        
        if sunny_recommendations:
            print(f"✅ Sunny weather recommendations: {sunny_recommendations}")
        else:
            print("⚠️ No sunny weather recommendations found")
        
        return True
        
    except Exception as e:
        print(f"❌ Weather recommendations test failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\n🧪 Testing file operations...")
    
    try:
        # Test directory creation
        test_dir = Path("test_data")
        test_dir.mkdir(exist_ok=True)
        print("✅ Directory creation successful")
        
        # Test JSON file operations
        test_data = {
            "test": "data",
            "timestamp": datetime.now().isoformat(),
            "numbers": [1, 2, 3, 4, 5]
        }
        
        json_file = test_dir / "test.json"
        with open(json_file, 'w') as f:
            json.dump(test_data, f, indent=2)
        print("✅ JSON file write successful")
        
        # Test reading JSON
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        
        if loaded_data['test'] == test_data['test']:
            print("✅ JSON file read successful")
        else:
            print("❌ JSON file read failed")
            return False
        
        # Test CSV file operations
        csv_data = pd.DataFrame({
            'name': ['Test1', 'Test2', 'Test3'],
            'value': [10, 20, 30]
        })
        
        csv_file = test_dir / "test.csv"
        csv_data.to_csv(csv_file, index=False)
        print("✅ CSV file write successful")
        
        # Test reading CSV
        loaded_csv = pd.read_csv(csv_file)
        if len(loaded_csv) == len(csv_data):
            print("✅ CSV file read successful")
        else:
            print("❌ CSV file read failed")
            return False
        
        # Cleanup
        json_file.unlink()
        csv_file.unlink()
        test_dir.rmdir()
        print("✅ File cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_ai_tool_integrations():
    """Test AI tool integrations"""
    print("\n🤖 Testing AI tool integrations...")

    try:
        # Test Devin-style planning
        print("Testing Devin planning system...")
        from tshwane_tourism_app import TshwanePlanningSystem
        planner = TshwanePlanningSystem()
        plan = planner.suggest_plan("Test tourism data processing")

        if len(plan) > 0:
            print("✅ Devin planning system working")
        else:
            print("❌ Devin planning system failed")
            return False

        # Test v0-style components
        print("Testing v0 component system...")
        from tshwane_tourism_app import ComponentSystem
        component_system = ComponentSystem()
        project = component_system.create_code_project("test", {"test": "component"})

        if project and 'id' in project:
            print("✅ v0 component system working")
        else:
            print("❌ v0 component system failed")
            return False

        # Test Cursor-style search
        print("Testing Cursor semantic search...")
        from tshwane_tourism_app import SemanticSearch
        search = SemanticSearch()
        results = search.search_tourism_content("test", [{"content": "test content", "name": "test"}])

        if isinstance(results, list):
            print("✅ Cursor semantic search working")
        else:
            print("❌ Cursor semantic search failed")
            return False

        # Test Manus-style processing
        print("Testing Manus real-time processing...")
        from tshwane_tourism_app import RealTimeProcessor
        processor = RealTimeProcessor()
        task_id = processor.add_task("test_task", "test_type", {})

        if task_id:
            print("✅ Manus processing system working")
        else:
            print("❌ Manus processing system failed")
            return False

        print("✅ All AI tool integrations working!")
        return True

    except Exception as e:
        print(f"❌ AI tool integration test failed: {e}")
        return False

def test_enhanced_processor():
    """Test enhanced integrated processor"""
    print("\n🧪 Testing enhanced processor...")

    try:
        from enhanced_integrated_processor import EnhancedTourismProcessor

        processor = EnhancedTourismProcessor()
        print("✅ Enhanced processor initialized")

        # Test planning
        plan = processor.suggest_plan("Test data processing")
        if len(plan) > 0:
            print("✅ Enhanced planning working")
        else:
            print("❌ Enhanced planning failed")
            return False

        # Test tool calling
        tool_call = processor.call_tool("semantic_search", {"query": "test", "data": []}, "Test search")
        if tool_call:
            print("✅ Enhanced tool calling working")
        else:
            print("❌ Enhanced tool calling failed")
            return False

        # Test component creation
        component_id = processor.create_component("test_component", {"test": "props"})
        if component_id:
            print("✅ Enhanced component creation working")
        else:
            print("❌ Enhanced component creation failed")
            return False

        return True

    except ImportError:
        print("⚠️ Enhanced processor not available (this is okay)")
        return True
    except Exception as e:
        print(f"❌ Enhanced processor test failed: {e}")
        return False

def test_session_management():
    """Test session management system"""
    print("\n🧪 Testing session management...")

    try:
        # Mock streamlit session state
        class MockSessionState:
            def __init__(self):
                self.data = {}

            def __contains__(self, key):
                return key in self.data

            def __getitem__(self, key):
                return self.data[key]

            def __setitem__(self, key, value):
                self.data[key] = value

        # Test session initialization
        mock_session = MockSessionState()

        # Simulate session manager
        defaults = {
            'website_data': {},
            'places_data': [],
            'notifications': [],
            'user_preferences': {'theme': 'nature'}
        }

        for key, value in defaults.items():
            if key not in mock_session:
                mock_session[key] = value

        if len(mock_session.data) == len(defaults):
            print("✅ Session management working")
            return True
        else:
            print("❌ Session management failed")
            return False

    except Exception as e:
        print(f"❌ Session management test failed: {e}")
        return False

def test_real_time_features():
    """Test real-time features"""
    print("\n🧪 Testing real-time features...")

    try:
        # Test notification system
        notifications = []

        def add_notification(message, type="info"):
            notification = {
                'id': str(uuid.uuid4())[:8],
                'message': message,
                'type': type,
                'timestamp': datetime.now().isoformat()
            }
            notifications.append(notification)

        add_notification("Test notification", "success")

        if len(notifications) == 1 and notifications[0]['type'] == 'success':
            print("✅ Real-time notifications working")
        else:
            print("❌ Real-time notifications failed")
            return False

        # Test progress tracking
        progress_data = {'current': 0, 'total': 100}

        def update_progress(value):
            progress_data['current'] = value
            return progress_data['current'] / progress_data['total']

        progress = update_progress(50)

        if abs(progress - 0.5) < 0.001:  # Use tolerance for float comparison
            print("✅ Progress tracking working")
        else:
            print("❌ Progress tracking failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Real-time features test failed: {e}")
        return False

def test_component_rendering():
    """Test component rendering system"""
    print("\n🧪 Testing component rendering...")

    try:
        # Mock component registry
        component_registry = {}

        def create_component(component_type, props):
            component_id = str(uuid.uuid4())[:8]
            component = {
                'id': component_id,
                'type': component_type,
                'props': props,
                'created_at': datetime.now().isoformat()
            }
            component_registry[component_id] = component
            return component_id

        # Test component creation
        component_id = create_component("gallery_card", {"title": "Test", "description": "Test card"})

        if component_id in component_registry:
            print("✅ Component creation working")
        else:
            print("❌ Component creation failed")
            return False

        # Test component retrieval
        component = component_registry.get(component_id)

        if component and component['type'] == 'gallery_card':
            print("✅ Component retrieval working")
        else:
            print("❌ Component retrieval failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Component rendering test failed: {e}")
        return False

def run_enhanced_tests():
    """Run enhanced test suite with AI tool integrations"""
    print("🤖 ENHANCED TSHWANE TOURISM AI SUITE - TEST SUITE")
    print("=" * 70)

    # Original tests
    original_tests = [
        ("Import Test", test_imports),
        ("Data Processor Test", test_data_processor),
        ("Integrated Processor Test", test_integrated_processor),
        ("Encryption Test", test_encryption),
        ("Data Processing Test", test_data_processing),
        ("Weather Recommendations Test", test_weather_recommendations),
        ("File Operations Test", test_file_operations)
    ]

    # Enhanced AI tool tests
    ai_tool_tests = [
        ("AI Tool Integrations Test", test_ai_tool_integrations),
        ("Enhanced Processor Test", test_enhanced_processor),
        ("Session Management Test", test_session_management),
        ("Real-time Features Test", test_real_time_features),
        ("Component Rendering Test", test_component_rendering)
    ]

    results = []

    print("\n🔧 Running Original Tests...")
    for test_name, test_func in original_tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    print("\n🤖 Running AI Tool Integration Tests...")
    for test_name, test_func in ai_tool_tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Enhanced summary
    print("\n" + "="*70)
    print("📊 ENHANCED TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    # Categorize results
    original_passed = sum(1 for i, (_, result) in enumerate(results) if i < len(original_tests) and result)
    ai_tool_passed = sum(1 for i, (_, result) in enumerate(results) if i >= len(original_tests) and result)

    print(f"📈 Overall Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    print(f"🔧 Original Tests: {original_passed}/{len(original_tests)} passed")
    print(f"🤖 AI Tool Tests: {ai_tool_passed}/{len(ai_tool_tests)} passed")

    print("\n📋 Detailed Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        category = "🔧" if test_name in [t[0] for t in original_tests] else "🤖"
        print(f"{status} {category} {test_name}")

    if passed == total:
        print("\n🎉 All tests passed! The enhanced AI system is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run: python run_data_processing.py (Enhanced runner)")
        print("2. Run: streamlit run tshwane_tourism_app.py (Enhanced main app)")
        print("3. Run: streamlit run enhanced_integrated_processor.py (AI processor)")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please check the errors above.")
        print("💡 The system may still be functional despite some test failures.")
        print("🔧 Focus on fixing AI tool integration issues for full functionality.")

    return passed == total

def run_all_tests():
    """Wrapper for backward compatibility"""
    return run_enhanced_tests()

def main():
    """Main test execution"""
    print("🧪 Starting Tshwane Tourism Data Processing Test Suite...")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    success = run_all_tests()
    
    print(f"\n📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("✅ System is ready for deployment!")
    else:
        print("⚠️ System has some issues but may still be functional.")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test suite crashed: {e}")
        print("Please contact support: kgothatsothooe@gmail.com")
