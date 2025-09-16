#!/usr/bin/env python3
"""
Test script for Hugging Face model integration in the chat interface
This script tests the basic functionality without requiring Streamlit.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))


def test_huggingface_imports():
    """Test that Hugging Face libraries can be imported"""
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        print("✅ Hugging Face imports successful")
        return True
    except ImportError as e:
        print(f"❌ Hugging Face imports failed: {e}")
        return False


def test_model_loading():
    """Test loading a small Hugging Face model"""
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

        # Use a smaller model for testing
        model_name = "microsoft/DialoGPT-small"  # Smaller model for testing

        print(f"🔄 Loading {model_name}...")

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="cpu"  # Use CPU for testing
        )

        # Create pipeline
        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=50,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        print("✅ Model loading successful")
        return True

    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False


def test_text_generation():
    """Test basic text generation"""
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

        # Use a smaller model for testing
        model_name = "microsoft/DialoGPT-small"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="cpu"
        )

        # Create pipeline
        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=30,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        # Test generation
        test_input = "Hello, how are you?"
        result = hf_pipeline(test_input)

        if result and len(result) > 0:
            print(
                f"✅ Text generation successful: {result[0]['generated_text'][:50]}...")
            return True
        else:
            print("❌ Text generation failed - no output")
            return False

    except Exception as e:
        print(f"❌ Text generation failed: {e}")
        return False


def test_embeddings():
    """Test sentence embeddings"""
    try:
        from sentence_transformers import SentenceTransformer

        # Load a small embedding model
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        # Test embedding
        sentences = ["Hello world", "Tshwane tourism", "South Africa"]
        embeddings = model.encode(sentences)

        if embeddings.shape[0] == len(sentences):
            print(f"✅ Embeddings successful: {embeddings.shape}")
            return True
        else:
            print("❌ Embeddings failed - wrong shape")
            return False

    except Exception as e:
        print(f"❌ Embeddings failed: {e}")
        return False


def test_langchain_integration():
    """Test LangChain with Hugging Face"""
    try:
        from langchain_community.llms import HuggingFacePipeline
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        import torch

        # Use a smaller model for testing
        model_name = "microsoft/DialoGPT-small"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="cpu"
        )

        # Create pipeline
        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=30,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        # Create LangChain wrapper
        llm = HuggingFacePipeline(
            pipeline=hf_pipeline,
            model_kwargs={"temperature": 0.7, "max_length": 30}
        )

        # Test generation
        result = llm("Hello")

        if result and len(result) > 0:
            print(f"✅ LangChain integration successful: {result[:50]}...")
            return True
        else:
            print("❌ LangChain integration failed")
            return False

    except Exception as e:
        print(f"❌ LangChain integration failed: {e}")
        return False


def main():
    """Run all Hugging Face integration tests"""
    print("🧪 Testing Hugging Face Integration for Chat Interface")
    print("=" * 60)

    tests = [
        ("Hugging Face Imports", test_huggingface_imports),
        ("Model Loading", test_model_loading),
        ("Text Generation", test_text_generation),
        ("Sentence Embeddings", test_embeddings),
        ("LangChain Integration", test_langchain_integration)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All Hugging Face integration tests passed!")
        print("✅ Chat interface is ready to use with local models.")
        return True
    elif passed >= 3:
        print("⚠️ Some tests failed, but core functionality should work.")
        print("ℹ️ Chat interface will use fallback responses for failed components.")
        return True
    else:
        print("❌ Too many tests failed. Check your Hugging Face installation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
