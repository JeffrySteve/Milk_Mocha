#!/usr/bin/env python3
"""
Quick test to verify the Google AI import fix works
"""
print("🧪 Testing Milk Mocha Pet imports...")

try:
    print("📦 Testing utils.gemini_service...")
    from utils.gemini_service import GeminiService
    print("✅ GeminiService imported successfully")
    
    print("🔧 Testing service creation...")
    service = GeminiService()
    print("✅ GeminiService created successfully")
    
    print("💬 Testing fallback message...")
    message = service.get_message("random")
    print(f"✅ Got message: {message}")
    
    print("🛡️ Testing safe_gemini...")
    from utils.safe_gemini import SafeGeminiService
    safe_service = SafeGeminiService()
    print("✅ SafeGeminiService created successfully")
    
    print("🎉 All imports working! The app should now start successfully.")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🚀 Ready to test: python main.py")
