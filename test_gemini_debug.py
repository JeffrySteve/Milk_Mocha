#!/usr/bin/env python3
"""
Test Gemini integration to see what's going wrong
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Test imports
print("🧪 Testing Gemini integration...")

try:
    from modules.gemini_handler import GeminiService
    print("✅ Successfully imported GeminiService")
except ImportError as e:
    print(f"❌ Failed to import GeminiService: {e}")
    sys.exit(1)

try:
    from modules.user_activity import UserActivityDetector
    print("✅ Successfully imported UserActivityDetector")
except ImportError as e:
    print(f"❌ Failed to import UserActivityDetector: {e}")
    sys.exit(1)

# Test Gemini service
print("\n🤖 Testing Gemini service...")
gemini_service = GeminiService()

# Test basic message
print("📝 Testing basic message...")
try:
    message = gemini_service.get_message("random")
    print(f"✅ Got message: {message}")
except Exception as e:
    print(f"❌ Error getting message: {e}")

# Test contextual message
print("\n📝 Testing contextual message...")
try:
    user_activity = UserActivityDetector()
    activity_context = user_activity.get_contextual_activity()
    print(f"📊 Activity context: {activity_context}")
    
    contextual_message = gemini_service.get_contextual_message(activity_context)
    print(f"✅ Got contextual message: {contextual_message}")
except Exception as e:
    print(f"❌ Error getting contextual message: {e}")

# Check API key
print("\n🔑 Checking API key...")
api_key = gemini_service.handler.api_key
if api_key:
    print(f"✅ API key found: {api_key[:10]}...")
else:
    print("❌ No API key found - using fallback messages only")

# Check settings
print("\n⚙️ Checking settings...")
try:
    import json
    if os.path.exists("config/settings.json"):
        with open("config/settings.json", "r") as f:
            settings = json.load(f)
            print(f"✅ Settings loaded: {settings}")
            if settings.get("use_fallback_only", False):
                print("🔄 Fallback mode is enabled")
            else:
                print("🌐 API mode is enabled")
    else:
        print("❌ No settings.json found")
except Exception as e:
    print(f"❌ Error reading settings: {e}")

print("\n🎯 Test complete!")
