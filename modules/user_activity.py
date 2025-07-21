import ctypes
import time
from ctypes import wintypes
from typing import Tuple, Optional

class UserActivityDetector:
    """Detect user activity on Windows using Win32 API"""
    
    def __init__(self):
        # Windows API setup
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Define Windows structures
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [
                ('cbSize', wintypes.UINT),
                ('dwTime', wintypes.DWORD),
            ]
        
        self.LASTINPUTINFO = LASTINPUTINFO
    
    def get_idle_time(self) -> float:
        """
        Get the time in seconds since last user input
        
        Returns:
            Idle time in seconds
        """
        try:
            lastInputInfo = self.LASTINPUTINFO()
            lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
            
            if self.user32.GetLastInputInfo(ctypes.byref(lastInputInfo)):
                current_time = self.kernel32.GetTickCount()
                idle_time_ms = current_time - lastInputInfo.dwTime
                return idle_time_ms / 1000.0  # Convert to seconds
            else:
                print("Failed to get last input info")
                return 0.0
        except Exception as e:
            print(f"Error getting idle time: {e}")
            return 0.0
    
    def is_user_active(self, idle_threshold: float = 300.0) -> bool:
        """
        Check if user is considered active
        
        Args:
            idle_threshold: Time in seconds after which user is considered idle (default: 5 minutes)
        
        Returns:
            True if user is active, False if idle
        """
        idle_time = self.get_idle_time()
        return idle_time < idle_threshold
    
    def get_activity_status(self) -> Tuple[str, float]:
        """
        Get detailed activity status
        
        Returns:
            Tuple of (status_description, idle_time_seconds)
        """
        idle_time = self.get_idle_time()
        
        if idle_time < 30:  # Less than 30 seconds
            status = "active"
        elif idle_time < 300:  # Less than 5 minutes
            status = "recently_active"
        elif idle_time < 1800:  # Less than 30 minutes
            status = "idle"
        else:  # More than 30 minutes
            status = "away"
        
        return status, idle_time
    
    def get_time_context(self) -> str:
        """Get time-based context for messaging"""
        current_hour = time.localtime().tm_hour
        
        if 5 <= current_hour < 12:
            return "morning"
        elif 12 <= current_hour < 17:
            return "afternoon"
        elif 17 <= current_hour < 21:
            return "evening"
        else:
            return "night"
    
    def should_show_message(self, last_message_time: Optional[float] = None, 
                          min_interval: float = 900.0) -> bool:
        """
        Determine if it's appropriate to show a message
        
        Args:
            last_message_time: Timestamp of last message (None if no previous message)
            min_interval: Minimum time between messages in seconds (default: 15 minutes)
        
        Returns:
            True if message should be shown
        """
        # Check if user is active
        if not self.is_user_active():
            return False
        
        # Check time interval
        current_time = time.time()
        if last_message_time and (current_time - last_message_time) < min_interval:
            return False
        
        return True
    
    def get_contextual_activity(self) -> str:
        """
        Get contextual activity for message selection
        
        Returns:
            Activity context string for Gemini handler
        """
        status, idle_time = self.get_activity_status()
        time_context = self.get_time_context()
        
        # Combine activity and time context
        if status == "active":
            if time_context == "morning":
                return "morning"
            elif idle_time < 5:  # Very recent activity
                return "working"
            else:
                return "break"
        elif status == "recently_active":
            return "break"
        elif status == "idle":
            return "idle"
        else:  # away
            return "idle"
