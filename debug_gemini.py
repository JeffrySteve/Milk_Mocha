#!/usr/bin/env python3
"""
Gemini API Debug Tool
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.gemini_handler import GeminiService

def test_gemini_debug():
    """Test Gemini API with detailed debugging"""
    
    print("🔍 Gemini API Debug Test")
    print("=" * 50)
    
    # Initialize service
    print("1️⃣ Initializing Gemini service...")
    gemini_service = GeminiService()
    
    # Check API key
    if gemini_service.handler.api_key:
        print(f"✅ API key loaded: {gemini_service.handler.api_key[:10]}...")
    else:
        print("❌ No API key found!")
        print("🔧 To fix:")
        print("   1. Check config/api_keys.json exists")
        print("   2. Ensure gemini_api_key is set")
        print("   3. Get API key from https://makersuite.google.com/app/apikey")
        return
    
    # Test message
    print("\n2️⃣ Testing message generation...")
    try:
        message = gemini_service.get_message("greetings")
        print(f"✅ Success! Message: {message}")
        
        # Test different contexts
        contexts = ["motivational", "humorous", "wellness"]
        for context in contexts:
            print(f"\n3️⃣ Testing {context} context...")
            msg = gemini_service.get_message(context)
            print(f"   📝 {context}: {msg}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎯 Debug complete!")

if __name__ == "__main__":
    test_gemini_debug()
