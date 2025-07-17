import json
import random
import asyncio
import aiohttp
import os
from typing import Optional, List

class GeminiClient:
    """Lightweight Gemini API client for getting motivational messages"""
    
    def __init__(self):
        self.api_key = self.load_api_key()
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.fallback_quotes = self.load_fallback_quotes()
        
        # 3️⃣ Prompts list
        self.prompts = [
            "Tell me a cute motivational quote under 20 words.",
            "Give me a short clean joke under 20 words.",
            "Tell me a cozy one-sentence story for relaxation.",
            "Say something cheerful to make me smile.",
            "Give me a fun fact under 20 words.",
            "Share a wholesome thought under 20 words.",
            "Tell me something positive about taking breaks.",
            "Give me a gentle reminder to stay hydrated.",
            "Share a cute animal fact under 20 words.",
            "Tell me why rest is important in under 20 words."
        ]
    
    def load_api_key(self) -> Optional[str]:
        """Load Gemini API key from config file"""
        try:
            config_path = "config/api_keys.json"
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    api_key = config.get("gemini_api_key")
                    if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
                        return api_key
        except Exception as e:
            print(f"Error loading API key: {e}")
        return None
    
    def load_fallback_quotes(self) -> List[str]:
        """4️⃣ Load offline fallback quotes"""
        try:
            fallback_path = "config/fallback_quotes.json"
            if os.path.exists(fallback_path):
                with open(fallback_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading fallback quotes: {e}")
        
        # Default fallbacks if file doesn't exist
        return [
            "You are doing great! Keep going! 🌟",
            "Why did the cat sit on the computer? To keep an eye on the mouse! 🐱",
            "You deserve a small break and a big smile. 😊",
            "Believe in yourself, Milk Mocha does! 🥛",
            "Every small step counts towards your goals! 👣",
            "Remember to drink water and take breaks! 💧",
            "You're more amazing than you realize! ✨",
            "A good laugh is sunshine in the house! ☀️",
            "Rest is not a waste of time, it's essential! 💤",
            "You've got this! One step at a time! 🚀"
        ]
    
    def get_random_prompt(self) -> str:
        """Get a random prompt from the list"""
        return random.choice(self.prompts)
    
    def get_fallback_message(self) -> str:
        """Get a random fallback message when API fails"""
        return random.choice(self.fallback_quotes)
    
    async def get_gemini_message(self) -> str:
        """
        Get a message from Gemini API with error handling
        Returns fallback message if API call fails
        """
        if not self.api_key:
            print("No Gemini API key found, using fallback")
            return self.get_fallback_message()
        
        try:
            prompt = self.get_random_prompt()
            
            # Prepare the request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt + " Be friendly and encouraging. Keep it under 20 words."
                            }
                        ]
                    }
                ]
            }
            
            # Make API call
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}?key={self.api_key}"
                
                async with session.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Extract text from response
                        try:
                            text = result["candidates"][0]["content"]["parts"][0]["text"]
                            # Clean up the text
                            text = text.strip().replace('\n', ' ')
                            if text:
                                print(f"✅ Gemini response: {text}")
                                return text
                        except (KeyError, IndexError):
                            print("Error parsing Gemini response")
                    else:
                        print(f"Gemini API error: {response.status}")
                        
        except asyncio.TimeoutError:
            print("Gemini API timeout")
        except Exception as e:
            print(f"Gemini API error: {e}")
        
        # Return fallback on any error
        fallback = self.get_fallback_message()
        print(f"🔄 Using fallback: {fallback}")
        return fallback

# Synchronous wrapper for use in Qt application
class GeminiSync:
    """Synchronous wrapper for Gemini client"""
    
    def __init__(self):
        self.client = GeminiClient()
    
    def get_message(self) -> str:
        """Get message synchronously"""
        try:
            # Run async function in new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            message = loop.run_until_complete(self.client.get_gemini_message())
            loop.close()
            return message
        except Exception as e:
            print(f"Error getting Gemini message: {e}")
            return self.client.get_fallback_message()
