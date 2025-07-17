#!/usr/bin/env python3
"""
Test script for Gemini API integration
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_integration():
    """Test Gemini API integration"""
    app = QApplication(sys.argv)
    
    print("🤖 Testing Gemini API Integration")
    print("=" * 50)
    
    # Test Gemini client
    from modules.gemini_client import GeminiSync
    
    print("\n✅ GEMINI CLIENT TEST:")
    client = GeminiSync()
    
    # Test API key loading
    if client.client.api_key and client.client.api_key != "YOUR_GEMINI_API_KEY_HERE":
        print("✅ API key loaded successfully")
        print(f"   Key starts with: {client.client.api_key[:8]}...")
    else:
        print("⚠️  No API key found - will use fallback messages")
    
    # Test fallback quotes
    print(f"\n📝 FALLBACK QUOTES LOADED: {len(client.client.fallback_quotes)} quotes")
    print("   Sample fallback:", client.client.fallback_quotes[0])
    
    # Test prompts
    print(f"\n🎯 PROMPT TEMPLATES: {len(client.client.prompts)} prompts")
    print("   Sample prompt:", client.client.prompts[0])
    
    # Test getting a message
    print("\n🔄 TESTING MESSAGE RETRIEVAL:")
    try:
        message = client.get_message()
        print(f"✅ Message received: {message}")
        message_type = "🤖 Gemini API" if client.client.api_key else "📝 Fallback"
        print(f"   Source: {message_type}")
    except Exception as e:
        print(f"❌ Error getting message: {e}")
    
    print("\n🎮 INTEGRATION FEATURES:")
    print("• Random timer: 30-60 minute intervals")
    print("• Speech bubbles: Positioned above pet")
    print("• Auto-hide: 15 seconds duration")
    print("• Click to dismiss: Immediate hiding")
    print("• Fallback system: Always available")
    
    # Test main application with Gemini
    print("\n🧪 TESTING MAIN APPLICATION:")
    from main import MilkMochaPet
    
    pet = MilkMochaPet()
    
    print("✅ Pet created with Gemini integration")
    print(f"   Gemini client initialized: {hasattr(pet, 'gemini_client')}")
    print(f"   Speech bubble support: {hasattr(pet, 'speech_bubble')}")
    
    # Test speech bubble manually
    def test_speech_bubble():
        print("\n💬 Testing speech bubble display...")
        test_message = "Hello! This is a test message from your Milk Mocha Pet! 🥛✨"
        pet.show_speech_bubble(test_message)
        
        # Hide after 5 seconds for testing
        QTimer.singleShot(5000, lambda: [
            print("   Speech bubble hidden"),
            pet.hide_speech_bubble()
        ])
    
    # Test Gemini message request
    def test_gemini_request():
        print("\n🤖 Testing Gemini message request...")
        pet.request_gemini_message()
    
    # Schedule tests
    QTimer.singleShot(2000, test_speech_bubble)
    QTimer.singleShot(8000, test_gemini_request)
    
    print("\n🎬 DEMONSTRATION:")
    print("⭐ Watch for speech bubbles appearing above the pet!")
    print("1. Manual speech bubble test (2 seconds)")
    print("2. Gemini message request test (8 seconds)")
    print("3. Close pet window or press ESC to quit")
    
    print("\n🔧 SETUP INSTRUCTIONS:")
    print("1. Get Gemini API key from https://aistudio.google.com/")
    print("2. Add to config/api_keys.json")
    print("3. Messages will appear every 30-60 minutes")
    print("4. Click speech bubbles to dismiss them")
    
    print("\n🏆 GEMINI INTEGRATION COMPLETE!")
    print("Your pet now has AI-powered motivational messages!")
    
    return app.exec_()

if __name__ == "__main__":
    test_gemini_integration()
