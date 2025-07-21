"""
Improved Gemini service with timeout protection
"""
import asyncio
import threading
import time
from utils.gemini_service import GeminiService as OriginalGeminiService

class SafeGeminiService:
    """Gemini service wrapper with timeout protection to prevent crashes"""
    
    def __init__(self):
        self.original_service = OriginalGeminiService()
        self.timeout_seconds = 5  # 5 second timeout
    
    def get_message_with_timeout(self, context: str = "random", custom_prompt: str = None) -> str:
        """Get message with timeout protection"""
        try:
            result = [None]
            exception = [None]
            
            def get_message_thread():
                try:
                    result[0] = self.original_service.get_message(context, custom_prompt)
                except Exception as e:
                    exception[0] = e
            
            # Start thread
            thread = threading.Thread(target=get_message_thread)
            thread.daemon = True
            thread.start()
            
            # Wait with timeout
            thread.join(self.timeout_seconds)
            
            if thread.is_alive():
                print(f"⏰ Gemini API timeout after {self.timeout_seconds}s, using fallback")
                return self.original_service.handler.get_fallback_message(context)
            
            if exception[0]:
                print(f"❌ Gemini API error: {exception[0]}")
                return self.original_service.handler.get_fallback_message(context)
            
            if result[0]:
                return result[0]
            else:
                print("🤔 Gemini returned empty result, using fallback")
                return self.original_service.handler.get_fallback_message(context)
                
        except Exception as e:
            print(f"❌ SafeGeminiService error: {e}")
            return "🤖 Milk Mocha's AI is taking a nap! 😴"
    
    def get_contextual_message(self, user_activity: str = "working") -> str:
        """Get contextual message with timeout protection"""
        context_mapping = {
            "working": "motivational",
            "break": "wellness", 
            "morning": "greetings",
            "afternoon": "random",
            "evening": "wellness",
            "idle": "humorous"
        }
        
        context = context_mapping.get(user_activity, "random")
        return self.get_message_with_timeout(context)
    
    # Delegate other methods to original service
    @property
    def handler(self):
        return self.original_service.handler
