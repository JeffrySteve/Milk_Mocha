#!/usr/bin/env python3
"""
Test Gemini API connectivity
"""

import asyncio
import aiohttp
import json
import os

async def test_gemini_api():
    """Test the Gemini API with current configuration"""
    
    # Load API key
    try:
        with open("config/api_keys.json", 'r') as f:
            config = json.load(f)
            api_key = config.get("gemini_api_key")
            if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
                print("❌ No valid API key found")
                return
        print(f"✅ API key loaded: {api_key[:10]}...")
    except Exception as e:
        print(f"❌ Error loading API key: {e}")
        return
    
    # Test different API endpoints
    endpoints_to_test = [
        "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    ]
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Say hello in under 10 words with an emoji."
                    }
                ]
            }
        ]
    }
    
    for endpoint in endpoints_to_test:
        print(f"\n🧪 Testing endpoint: {endpoint}")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{endpoint}?key={api_key}"
                print(f"🔗 Full URL: {url}")
                
                async with session.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    
                    print(f"📊 Response status: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ Success! Response: {json.dumps(result, indent=2)}")
                        
                        # Try to extract text
                        try:
                            text = result["candidates"][0]["content"]["parts"][0]["text"]
                            print(f"💬 Extracted text: {text}")
                        except (KeyError, IndexError) as e:
                            print(f"⚠️ Could not extract text: {e}")
                        
                        return  # Success, stop testing
                    else:
                        error_text = await response.text()
                        print(f"❌ Error {response.status}: {error_text}")
                        
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n🔍 All endpoints failed. Possible issues:")
    print("1. API key might be invalid or expired")
    print("2. Billing might not be enabled for Gemini API")
    print("3. API might not be enabled in Google Cloud Console")
    print("4. Rate limits might be exceeded")

if __name__ == "__main__":
    asyncio.run(test_gemini_api())
