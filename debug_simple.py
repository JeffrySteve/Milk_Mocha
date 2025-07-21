#!/usr/bin/env python3
"""
Simple test to debug Gemini messages
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Testing Gemini functionality...")

# Test 1: Basic imports
try:
    from modules.gemini_handler import GeminiService
    from modules.user_activity import UserActivityDetector
    print("✅ Imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: Create services
try:
    gemini_service = GeminiService()
    user_activity = UserActivityDetector()
    print("✅ Services created")
except Exception as e:
    print(f"❌ Service creation failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: Check API key and settings
print(f"🔑 API key available: {gemini_service.handler.api_key is not None}")

# Test 4: Try getting a simple message
print("📝 Testing simple message...")
try:
    message = gemini_service.get_message("random")
    print(f"✅ Got message: '{message}'")
except Exception as e:
    print(f"❌ Simple message failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Try getting contextual activity
print("📊 Testing activity context...")
try:
    activity = user_activity.get_contextual_activity()
    print(f"✅ Got activity: '{activity}'")
except Exception as e:
    print(f"❌ Activity detection failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Try getting contextual message
print("🎯 Testing contextual message...")
try:
    activity = user_activity.get_contextual_activity()
    contextual_message = gemini_service.get_contextual_message(activity)
    print(f"✅ Got contextual message: '{contextual_message}'")
except Exception as e:
    print(f"❌ Contextual message failed: {e}")
    import traceback
    traceback.print_exc()

print("🎯 Test complete!")
