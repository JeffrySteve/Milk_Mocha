#!/usr/bin/env python3
"""
Debug Gemini API issues
"""
import sys
import os
import asyncio
import aiohttp
import json

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

async def test_gemini_api():
    """Test the Gemini API directly"""
    
    # Load API key
    api_key = None
    try:
        with open("config/api_keys.json", 'r') as f:
            config = json.load(f)
            api_key = config.get("gemini_api_key")
    except Exception as e:
        print(f"❌ Error loading API key: {e}")
        return
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"🔑 API key loaded: {api_key[:10]}...")
    
    # Test multiple model endpoints
    model_endpoints = [
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent"
    ]
    
    # Prepare test payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Say hello in under 10 words with an emoji"
                    }
                ]
            }
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        for model_url in model_endpoints:
            model_name = model_url.split('/')[-1].split(':')[0]
            url = f"{model_url}?key={api_key}"
            
            print(f"\n🧪 Testing model: {model_name}")
            print(f"📡 URL: {model_url}")
            
            try:
                async with session.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    
                    print(f"📊 Status Code: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ Success! Response: {json.dumps(result, indent=2)}")
                        
                        # Extract the text
                        try:
                            text = result["candidates"][0]["content"]["parts"][0]["text"]
                            print(f"💬 Extracted message: '{text.strip()}'")
                        except (KeyError, IndexError) as e:
                            print(f"❌ Error extracting text: {e}")
                        
                        break  # Success, no need to try other models
                        
                    else:
                        error_text = await response.text()
                        print(f"❌ HTTP {response.status} Error:")
                        print(f"📄 Response: {error_text}")
                        
            except Exception as e:
                print(f"❌ Exception: {e}")
                import traceback
                traceback.print_exc()
    
    print("\n🎯 API test complete!")

if __name__ == "__main__":
    print("🧪 Testing Gemini API directly...")
    asyncio.run(test_gemini_api())
