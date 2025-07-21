import json
import random
import asyncio
import aiohttp
import os
import time
from typing import Optional, List, Dict

class GeminiHandler:
    """Enhanced Gemini handler for Milk Mocha Pet speaking"""
    
    def __init__(self):
        self.api_key = self.load_api_key()
        # Try multiple model endpoints in order of preference
        self.model_endpoints = [
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent"
        ]
        self.base_url = self.model_endpoints[0]  # Start with first
        self.fallback_quotes = self.load_fallback_quotes()
        
        # Enhanced prompt categories for different contexts
        self.prompt_categories = {
            "motivational": [
                "Say a short motivational quote under 15 words that Milk Mocha would say.",
                "Give me an encouraging message under 15 words for someone working hard.",
                "Say something inspiring about taking breaks, under 15 words.",
                "Share a positive thought about productivity in under 15 words.",
                "Give a wholesome reminder about self-worth in under 15 words."
            ],
            "humorous": [
                "Tell me a short, funny joke like Milk Mocha would say, under 15 words.",
                "Say something cute and funny about coffee or milk, under 15 words.",
                "Make a playful comment about desktop pets, under 15 words.",
                "Say a light-hearted joke about working from home, under 15 words.",
                "Give a funny observation about computers or screens, under 15 words."
            ],
            "wellness": [
                "Say a wholesome one-line reminder for self-care, under 15 words.",
                "Give a gentle reminder about staying hydrated, under 15 words.",
                "Say something caring about taking breaks, under 15 words.",
                "Share a mindful thought about rest, under 15 words.",
                "Give a loving reminder about work-life balance, under 15 words."
            ],
            "greetings": [
                "Say a cheerful morning greeting like Milk Mocha would, under 15 words.",
                "Give a friendly afternoon check-in message, under 15 words.",
                "Say an encouraging evening message, under 15 words.",
                "Share a warm hello for someone at their computer, under 15 words.",
                "Give a cute greeting that includes milk or mocha, under 15 words."
            ],
            "random": [
                "Say something cute and random that Milk Mocha would say, under 15 words.",
                "Share a fun fact about animals in under 15 words.",
                "Give a random compliment to brighten someone's day, under 15 words.",
                "Say something playful about technology, under 15 words.",
                "Share a whimsical thought about desktop companions, under 15 words."
            ]
        }
        
        # Context-aware prompting
        self.last_category = None
        self.message_history = []
    
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
    
    def load_fallback_quotes(self) -> Dict[str, List[str]]:
        """Load categorized fallback quotes"""
        try:
            fallback_path = "config/fallback_quotes.json"
            if os.path.exists(fallback_path):
                with open(fallback_path, 'r') as f:
                    quotes = json.load(f)
                    # Categorize existing quotes
                    return self.categorize_fallback_quotes(quotes)
        except Exception as e:
            print(f"Error loading fallback quotes: {e}")
        
        # Default categorized fallbacks
        return {
            "motivational": [
                "You are doing great! Keep going! 🌟",
                "Every small step counts towards your goals! 👣",
                "You've got this! One step at a time! 🚀",
                "Believe in yourself, Milk Mocha does! 🥛",
                "Your potential is endless! 🌈"
            ],
            "humorous": [
                "Why did the cat sit on the computer? To keep an eye on the mouse! 🐱",
                "A good laugh is sunshine in the house! ☀️",
                "I'm like coffee - better when shared with friends! ☕",
                "Desktop pets: because real pets don't fit in taskbars! 💻",
                "I may be virtual, but my love for you is real! 💖"
            ],
            "wellness": [
                "Remember to drink water and take breaks! 💧",
                "Rest is not a waste of time, it's essential! 💤",
                "Breathe deeply, you're exactly where you need to be! 🌸",
                "Be kind to yourself, you're doing your best! 💖",
                "Your health is more important than any deadline! 🫂"
            ],
            "greetings": [
                "Hello there! Ready for a productive day? 👋",
                "Good morning! Let's make today amazing! 🌅",
                "Afternoon check-in: You're doing wonderfully! ☀️",
                "Evening vibes: Time to wind down soon! 🌙",
                "Hey friend! Milk Mocha here to brighten your day! 🥛"
            ],
            "random": [
                "Small progress is still progress! 🐾",
                "Your creativity and ideas are valuable! 🎨",
                "Did you know cats spend 70% of their lives sleeping? 😴",
                "You bring joy to those around you! 😄",
                "Technology is amazing, but you're even more amazing! ✨"
            ]
        }
    
    def categorize_fallback_quotes(self, quotes: List[str]) -> Dict[str, List[str]]:
        """Categorize existing fallback quotes by content"""
        categorized = {
            "motivational": [],
            "humorous": [],
            "wellness": [],
            "greetings": [],
            "random": []
        }
        
        # Simple keyword-based categorization
        for quote in quotes:
            lower_quote = quote.lower()
            if any(word in lower_quote for word in ["great", "keep going", "believe", "potential", "goal"]):
                categorized["motivational"].append(quote)
            elif any(word in lower_quote for word in ["why", "joke", "laugh", "funny", "cat", "mouse"]):
                categorized["humorous"].append(quote)
            elif any(word in lower_quote for word in ["rest", "sleep", "water", "break", "health", "breathe"]):
                categorized["wellness"].append(quote)
            elif any(word in lower_quote for word in ["hello", "morning", "afternoon", "evening", "hi"]):
                categorized["greetings"].append(quote)
            else:
                categorized["random"].append(quote)
        
        return categorized
    
    def get_contextual_prompt(self, context: str = "random") -> str:
        """Get a contextual prompt based on situation"""
        # Avoid repeating the same category
        available_categories = list(self.prompt_categories.keys())
        if self.last_category and len(available_categories) > 1:
            available_categories.remove(self.last_category)
        
        # Choose category based on context or randomly
        if context in self.prompt_categories:
            category = context
        else:
            category = random.choice(available_categories)
        
        self.last_category = category
        return random.choice(self.prompt_categories[category])
    
    def get_fallback_message(self, context: str = "random") -> str:
        """Get a contextual fallback message"""
        if context in self.fallback_quotes and self.fallback_quotes[context]:
            return random.choice(self.fallback_quotes[context])
        else:
            # If specific context not available, get from any category
            all_quotes = []
            for quotes_list in self.fallback_quotes.values():
                all_quotes.extend(quotes_list)
            return random.choice(all_quotes) if all_quotes else "Keep being awesome! 🌟"
    
    async def get_gemini_message(self, context: str = "random", custom_prompt: str = None) -> str:
        """
        Get a contextual message from Gemini API
        
        Args:
            context: Category of message (motivational, humorous, wellness, greetings, random)
            custom_prompt: Override with custom prompt
        
        Returns:
            Generated message or fallback
        """
        if not self.api_key:
            print("No Gemini API key found, using fallback")
            return self.get_fallback_message(context)
        
        # Check if we should use fallback only
        try:
            import json
            import os
            if os.path.exists("config/settings.json"):
                with open("config/settings.json", "r") as f:
                    settings = json.load(f)
                    if settings.get("use_fallback_only", False):
                        print("🔄 Using fallback messages only (API disabled)")
                        return self.get_fallback_message(context)
        except:
            pass
        
        try:
            # Get prompt
            if custom_prompt:
                prompt = custom_prompt + " Keep it under 15 words and friendly."
            else:
                prompt = self.get_contextual_prompt(context)
            
            # Add personality context
            personality_context = (
                "You are Milk Mocha, a cute desktop pet companion. "
                "Respond in a warm, friendly, encouraging tone. "
                "Keep responses very short (under 15 words) and include an emoji. "
            )
            
            # Prepare the request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": personality_context + prompt
                            }
                        ]
                    }
                ]
            }
            
            # Make API call with fallback models
            async with aiohttp.ClientSession() as session:
                for model_url in self.model_endpoints:
                    url = f"{model_url}?key={self.api_key}"
                    print(f"🔄 Trying model: {model_url.split('/')[-1].split(':')[0]}")
                    
                    try:
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
                                    
                                    # Store in message history
                                    if len(self.message_history) >= 10:
                                        self.message_history.pop(0)
                                    self.message_history.append(text)
                                    
                                    if text:
                                        print(f"✅ Gemini response ({context}): {text}")
                                        # Update successful URL for future use
                                        self.base_url = model_url
                                        return text
                                except (KeyError, IndexError):
                                    print("Error parsing Gemini response")
                            else:
                                error_text = await response.text()
                                print(f"❌ Model {model_url.split('/')[-1]} error {response.status}: {error_text}")
                                # Continue to try next model
                                continue
                                
                    except Exception as e:
                        print(f"❌ Exception with model {model_url.split('/')[-1]}: {e}")
                        continue
                        
        except asyncio.TimeoutError:
            print("Gemini API timeout")
        except Exception as e:
            print(f"Gemini API error: {e}")
        
        # Return fallback on any error
        fallback = self.get_fallback_message(context)
        print(f"🔄 Using fallback ({context}): {fallback}")
        return fallback

# Synchronous wrapper for PyQt integration
class GeminiService:
    """Synchronous service wrapper for Gemini handler"""
    
    def __init__(self):
        self.handler = GeminiHandler()
    
    def get_message(self, context: str = "random", custom_prompt: str = None) -> str:
        """Get message synchronously"""
        try:
            # Run async function in new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            message = loop.run_until_complete(
                self.handler.get_gemini_message(context, custom_prompt)
            )
            loop.close()
            return message
        except Exception as e:
            print(f"Error getting Gemini message: {e}")
            return self.handler.get_fallback_message(context)
    
    def get_contextual_message(self, user_activity: str = "working") -> str:
        """Get message based on user activity context"""
        context_mapping = {
            "working": "motivational",
            "break": "wellness", 
            "morning": "greetings",
            "afternoon": "random",
            "evening": "wellness",
            "idle": "humorous"
        }
        
        context = context_mapping.get(user_activity, "random")
        return self.get_message(context)
