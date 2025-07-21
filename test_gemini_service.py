#!/usr/bin/env python3
"""
Test GeminiService directly to find issues
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Testing GeminiService...")

try:
    from modules.gemini_handler import GeminiService
    print("✅ Successfully imported GeminiService")
except ImportError as e:
    print(f"❌ Failed to import GeminiService: {e}")
    sys.exit(1)

# Create service
print("🔧 Creating GeminiService...")
try:
    gemini_service = GeminiService()
    print("✅ GeminiService created successfully")
except Exception as e:
    print(f"❌ Failed to create GeminiService: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check API key
print("🔑 Checking API key...")
api_key = gemini_service.handler.api_key
if api_key:
    print(f"✅ API key found: {api_key[:10]}...")
else:
    print("❌ No API key found")

# Test basic message
print("\n📝 Testing basic message...")
try:
    message = gemini_service.get_message("random")
    print(f"✅ Got message: '{message}'")
except Exception as e:
    print(f"❌ Error getting message: {e}")
    import traceback
    traceback.print_exc()

# Test fallback message
print("\n🔄 Testing fallback message...")
try:
    fallback = gemini_service.handler.get_fallback_message("random")
    print(f"✅ Got fallback: '{fallback}'")
except Exception as e:
    print(f"❌ Error getting fallback: {e}")
    import traceback
    traceback.print_exc()

print("\n🎯 Test complete!")
