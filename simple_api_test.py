#!/usr/bin/env python3
"""
Simple Gemini API test
"""

import requests
import json

def test_gemini_simple():
    """Simple test of Gemini API"""
    
    # Load API key
    try:
        with open("config/api_keys.json", 'r') as f:
            config = json.load(f)
            api_key = config.get("gemini_api_key")
        print(f"✅ API key: {api_key[:10]}...")
    except Exception as e:
        print(f"❌ Error loading API key: {e}")
        return
    
    # Test endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Say hello"
                    }
                ]
            }
        ]
    }
    
    print(f"🧪 Testing URL: {url}")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📝 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API is working!")
            try:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"💬 Message: {text}")
            except:
                print("⚠️ Could not parse response")
        else:
            print(f"❌ API Error {response.status_code}")
            print("🔍 Possible causes:")
            if response.status_code == 400:
                print("- Invalid request format")
            elif response.status_code == 401:
                print("- Invalid API key")
            elif response.status_code == 403:
                print("- API not enabled or billing issue")
            elif response.status_code == 404:
                print("- Wrong endpoint URL or model name")
            elif response.status_code == 429:
                print("- Rate limit exceeded")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_gemini_simple()
