"""
Quick verification that Gemini is working
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.gemini_service import GeminiService

print("🔍 Verifying Gemini setup...")
service = GeminiService()

print(f"✅ API Key found: {service.api_key is not None}")
print(f"✅ Model configured: {service.model is not None}")

if service.model:
    print("🤖 Gemini AI is ready for story generation!")
    print("📱 You can now press T in the app for AI-generated stories!")
else:
    print("⚠️ Gemini AI not available, will use fallback stories")
