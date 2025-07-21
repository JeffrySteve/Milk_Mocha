#!/usr/bin/env python3
"""
Milk Mocha Speech Test - Debug version
"""

import sys
import os
import json
import time
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtCore import Qt, QTimer, QSize

# Import our modules
from modules.gemini_handler import GeminiService
from modules.user_activity import UserActivityDetector

class MochaSpeechTest(QWidget):
    def __init__(self):
        super().__init__()
        print("🤖 Initializing Milk Mocha Speech Test...")
        
        # Set up basic window
        self.setWindowTitle("Mocha Speech Test")
        self.setFixedSize(200, 200)
        
        # Load config
        self.load_config()
        
        # Initialize speech system
        self.gemini_service = GeminiService()
        self.user_activity = UserActivityDetector()
        self.last_message_time = None
        self.speech_bubble = None
        
        # Create pet display
        self.pet_label = QLabel(self)
        self.pet_label.setText("🥛 Mocha Pet")
        self.pet_label.setAlignment(Qt.AlignCenter)
        self.pet_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.pet_label.setGeometry(50, 80, 100, 40)
        
        # Position window
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - 250, screen.height() - 250)
        
        print(f"✅ Speaking enabled: {self.speaking_enabled}")
        print(f"✅ Speaking interval: {self.speaking_interval} seconds")
        
        # Start speech system
        if self.speaking_enabled:
            self.start_speech_test()
        
        self.show()
    
    def load_config(self):
        """Load configuration"""
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.speaking_enabled = config.get("milk_mocha_speaking", True)
                self.speaking_interval = config.get("speaking_interval", 2) * 60
        except:
            self.speaking_enabled = True
            self.speaking_interval = 120  # 2 minutes
    
    def start_speech_test(self):
        """Start speech testing"""
        print("🎯 Starting speech test...")
        
        # Send immediate test message
        QTimer.singleShot(3000, self.send_test_greeting)
        
        # Set up regular check
        self.speech_timer = QTimer()
        self.speech_timer.timeout.connect(self.check_speech)
        self.speech_timer.start(30000)  # Check every 30 seconds for testing
    
    def send_test_greeting(self):
        """Send test greeting"""
        print("🌟 Sending test greeting...")
        
        def get_greeting():
            try:
                message = self.gemini_service.get_message("greetings")
                print(f"✅ Got message from Gemini: {message}")
                QTimer.singleShot(0, lambda: self.show_speech_bubble(message))
                self.last_message_time = time.time()
            except Exception as e:
                print(f"❌ Error getting greeting: {e}")
                fallback = "Hello! I'm your Milk Mocha pet! 🥛✨"
                QTimer.singleShot(0, lambda: self.show_speech_bubble(fallback))
        
        thread = threading.Thread(target=get_greeting)
        thread.daemon = True
        thread.start()
    
    def check_speech(self):
        """Check if should speak"""
        print("🔍 Checking if should speak...")
        
        if not self.speaking_enabled:
            print("❌ Speaking disabled")
            return
        
        current_time = time.time()
        if self.last_message_time and (current_time - self.last_message_time) < 60:  # 1 minute for testing
            print(f"⏰ Too soon - last message was {current_time - self.last_message_time:.1f} seconds ago")
            return
        
        print("✅ Time to speak!")
        self.send_contextual_message()
    
    def send_contextual_message(self):
        """Send contextual message"""
        print("🎯 Getting contextual message...")
        
        def get_message():
            try:
                activity_context = self.user_activity.get_contextual_activity()
                print(f"📊 Activity context: {activity_context}")
                
                message = self.gemini_service.get_contextual_message(activity_context)
                print(f"✅ Got contextual message: {message}")
                
                QTimer.singleShot(0, lambda: [
                    self.show_speech_bubble(message),
                    setattr(self, 'last_message_time', time.time())
                ])
                
            except Exception as e:
                print(f"❌ Error getting contextual message: {e}")
                fallback = self.gemini_service.handler.get_fallback_message("random")
                print(f"💾 Using fallback: {fallback}")
                QTimer.singleShot(0, lambda: [
                    self.show_speech_bubble(fallback),
                    setattr(self, 'last_message_time', time.time())
                ])
        
        thread = threading.Thread(target=get_message)
        thread.daemon = True
        thread.start()
    
    def show_speech_bubble(self, message):
        """Show speech bubble"""
        print(f"💬 Showing speech bubble: {message}")
        
        # Hide existing bubble
        if self.speech_bubble:
            self.speech_bubble.hide()
            self.speech_bubble.deleteLater()
        
        # Create bubble
        from main import SpeechBubble
        self.speech_bubble = SpeechBubble(message, None)
        
        # Position above pet
        bubble_x = self.x() + 50
        bubble_y = self.y() - 100
        
        print(f"📍 Bubble position: ({bubble_x}, {bubble_y})")
        
        self.speech_bubble.move(bubble_x, bubble_y)
        self.speech_bubble.show()
        self.speech_bubble.raise_()
        
        # Auto-hide
        QTimer.singleShot(10000, self.hide_speech_bubble)
        
        print("✅ Speech bubble displayed!")
    
    def hide_speech_bubble(self):
        """Hide speech bubble"""
        if self.speech_bubble:
            print("💬 Hiding speech bubble")
            self.speech_bubble.hide()
            self.speech_bubble.deleteLater()
            self.speech_bubble = None
    
    def keyPressEvent(self, event):
        """Handle key press"""
        if event.key() == Qt.Key_T:
            print("🧪 Manual test triggered!")
            test_msg = f"Test message at {time.strftime('%H:%M:%S')} 🧪"
            self.show_speech_bubble(test_msg)
        elif event.key() == Qt.Key_G:
            print("🤖 Manual Gemini test triggered!")
            self.send_test_greeting()
        elif event.key() == Qt.Key_Escape:
            self.close()

def main():
    app = QApplication(sys.argv)
    
    print("🚀 Starting Milk Mocha Speech Test...")
    print("💡 Press T for test bubble, G for Gemini message, ESC to exit")
    
    test = MochaSpeechTest()
    
    return app.exec_()

if __name__ == "__main__":
    main()
