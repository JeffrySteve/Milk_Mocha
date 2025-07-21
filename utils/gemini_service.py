"""
Gemini AI Service for generating cute pet messages
"""
import os
import random

# Optional import for Google Generative AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False
    print("ℹ️ google-generativeai not installed. Using fallback messages only.")


class GeminiHandler:
    """Handles Gemini AI message generation"""
    
    def __init__(self):
        self.fallback_messages = {
            "random": [
                "🥛 Hello there! I'm Milk Mocha, your adorable desktop companion! ✨",
                "💕 Hope you're having a wonderful day! Keep being awesome! 🌟",
                "🎉 Time for a little break! You deserve it! 💖",
                "🌈 Sending you positive vibes and virtual hugs! 🤗",
                "✨ Remember to stay hydrated and take care of yourself! 💧",
                "🎮 Ready for some fun? Let's make today amazing! 🚀",
                "🍀 You're doing great! Keep up the fantastic work! 💪",
                "🌸 Spreading some joy your way! Smile! 😊",
                "🎯 Focus mode activated! You've got this! 💯",
                "🥰 Just wanted to say you're pretty awesome! 💫"
            ],
            "greetings": [
                "🌅 Good morning! Ready to conquer the day? ☀️",
                "👋 Hello there! Great to see you! 😊",
                "🎊 Welcome back! Missed you! 💕",
                "✨ Hey wonderful human! How are you today? 🌟",
                "🥛 Milk Mocha reporting for duty! What's the plan? 📋"
            ],
            "working": [
                "💼 Keep up the great work! You're crushing it! 🚀",
                "⚡ Productivity mode: ON! You're amazing! 💻",
                "🎯 Focused and fabulous! That's you! ✨",
                "💪 Work hard, dream big! You've got this! 🌟",
                "📈 Progress is progress! Every step counts! 🎉"
            ]
        }
    
    def get_fallback_message(self, context: str = "random") -> str:
        """Get a fallback message when AI is unavailable"""
        messages = self.fallback_messages.get(context, self.fallback_messages["random"])
        return random.choice(messages)


class GeminiService:
    """Main Gemini service for generating AI messages"""
    
    def __init__(self):
        self.handler = GeminiHandler()
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        
        if GENAI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini API configured successfully")
            except Exception as e:
                print(f"⚠️ Gemini API setup failed: {e}")
                self.model = None
        elif not GENAI_AVAILABLE:
            print("ℹ️ Google Generative AI not available. Install with: pip install google-generativeai")
        else:
            print("ℹ️ No Gemini API key found. Set GEMINI_API_KEY environment variable for AI features.")
    
    def get_message(self, context: str = "random", custom_prompt: str = None) -> str:
        """Get a message from Gemini AI or fallback"""
        
        if not self.model:
            return self.handler.get_fallback_message(context)
        
        try:
            # Create appropriate prompt based on context
            if custom_prompt:
                prompt = custom_prompt
            else:
                prompts = {
                    "random": "Generate a cute, short, encouraging message from Milk Mocha, an adorable desktop pet. Include emojis and keep it under 50 words. Be cheerful and supportive!",
                    "greetings": "Generate a cute greeting message from Milk Mocha, an adorable desktop pet. Make it warm and welcoming with emojis. Keep it under 40 words.",
                    "working": "Generate an encouraging work-related message from Milk Mocha, an adorable desktop pet. Be supportive and motivating with emojis. Keep it under 45 words.",
                    "break": "Generate a message encouraging the user to take a break, from Milk Mocha, an adorable desktop pet. Be caring and remind them to rest with emojis. Keep it under 40 words."
                }
                prompt = prompts.get(context, prompts["random"])
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return self.handler.get_fallback_message(context)
                
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return self.handler.get_fallback_message(context)
