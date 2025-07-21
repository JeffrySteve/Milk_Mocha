"""
Simple user activity detection for Milk Mocha Pet
"""
import time
import random
from datetime import datetime


class UserActivityDetector:
    """Simple user activity detector for determining when to show messages"""
    
    def __init__(self):
        self.last_check_time = time.time()
    
    def should_show_message(self, last_message_time, interval):
        """Determine if we should show a message based on timing"""
        current_time = time.time()
        
        # If no previous message, always allow
        if not last_message_time:
            return True
        
        # Check if enough time has passed
        time_passed = current_time - last_message_time
        return time_passed >= interval
    
    def get_time_context(self):
        """Get the current time context (morning, afternoon, evening, night)"""
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 12:
            return "morning"
        elif 12 <= current_hour < 18:
            return "afternoon"
        elif 18 <= current_hour < 22:
            return "evening"
        else:
            return "night"
    
    def get_contextual_activity(self):
        """Get a contextual activity description based on time"""
        time_context = self.get_time_context()
        
        contexts = {
            "morning": ["working", "productive", "fresh", "energetic"],
            "afternoon": ["focused", "busy", "productive", "active"],
            "evening": ["winding down", "relaxing", "social", "creative"],
            "night": ["late working", "relaxing", "quiet", "peaceful"]
        }
        
        # Return a random context for the current time
        return random.choice(contexts.get(time_context, ["general"]))
