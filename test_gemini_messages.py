#!/usr/bin/env python3
"""
Test what happens when main.py tries to show Gemini messages
"""
import sys
import os
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Import the classes we need
try:
    from modules.gemini_handler import GeminiService
    from modules.user_activity import UserActivityDetector
    from main import SpeechBubble
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class GeminiTestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Initialize services like main.py does
        self.gemini_service = GeminiService()
        self.user_activity = UserActivityDetector()
        self.speech_bubble = None
        self.last_message_time = None
        
    def initUI(self):
        self.setWindowTitle('Gemini Message Test')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.status_label = QLabel('Click buttons to test Gemini integration')
        layout.addWidget(self.status_label)
        
        # Test buttons
        test_basic = QPushButton('Test Basic Gemini Message')
        test_basic.clicked.connect(self.test_basic_message)
        layout.addWidget(test_basic)
        
        test_contextual = QPushButton('Test Contextual Gemini Message')
        test_contextual.clicked.connect(self.test_contextual_message)
        layout.addWidget(test_contextual)
        
        test_manual = QPushButton('Test Manual Context Message')
        test_manual.clicked.connect(self.test_manual_context)
        layout.addWidget(test_manual)
        
        self.setLayout(layout)
        
    def show_speech_bubble(self, message):
        """Simplified speech bubble display"""
        print(f"💬 Displaying speech bubble: {message}")
        
        # Hide existing bubble
        if self.speech_bubble:
            try:
                self.speech_bubble.hide()
                self.speech_bubble.deleteLater()
            except:
                pass
            self.speech_bubble = None
        
        # Create new bubble
        self.speech_bubble = SpeechBubble(message, self)
        self.speech_bubble.move(200, 200)  # Simple positioning
        self.speech_bubble.show()
        self.speech_bubble.raise_()
        
        # Auto-hide after 10 seconds
        QTimer.singleShot(10000, self.hide_speech_bubble)
        
        self.status_label.setText(f"Bubble shown: {message[:50]}...")
        
    def hide_speech_bubble(self):
        """Hide speech bubble"""
        if self.speech_bubble:
            try:
                self.speech_bubble.hide()
                self.speech_bubble.deleteLater()
                self.speech_bubble = None
                print("💬 Speech bubble hidden")
            except:
                pass
    
    def test_basic_message(self):
        """Test basic Gemini message like main.py does"""
        self.status_label.setText("Testing basic Gemini message...")
        print("🧪 Testing basic Gemini message...")
        
        def get_message():
            try:
                message = self.gemini_service.get_message("random")
                print(f"📨 Received message: {message}")
                QTimer.singleShot(0, lambda: self.show_speech_bubble(message))
                self.last_message_time = time.time()
            except Exception as e:
                print(f"❌ Error getting basic message: {e}")
                QTimer.singleShot(0, lambda: self.status_label.setText(f"Error: {e}"))
        
        thread = threading.Thread(target=get_message)
        thread.daemon = True
        thread.start()
    
    def test_contextual_message(self):
        """Test contextual message like main.py does"""
        self.status_label.setText("Testing contextual Gemini message...")
        print("🧪 Testing contextual Gemini message...")
        
        def get_contextual_message():
            try:
                # Get user activity context
                activity_context = self.user_activity.get_contextual_activity()
                print(f"🎯 Activity context: {activity_context}")
                
                # Get appropriate message
                message = self.gemini_service.get_contextual_message(activity_context)
                print(f"📨 Received contextual message: {message}")
                
                # Show message in UI thread
                QTimer.singleShot(0, lambda: self.show_speech_bubble(message))
                self.last_message_time = time.time()
                
            except Exception as e:
                print(f"❌ Error getting contextual message: {e}")
                # Fallback to simple message
                try:
                    fallback = self.gemini_service.handler.get_fallback_message("random")
                    print(f"🔄 Using fallback: {fallback}")
                    QTimer.singleShot(0, lambda: self.show_speech_bubble(fallback))
                    self.last_message_time = time.time()
                except Exception as e2:
                    print(f"❌ Even fallback failed: {e2}")
                    QTimer.singleShot(0, lambda: self.status_label.setText(f"All failed: {e2}"))
        
        thread = threading.Thread(target=get_contextual_message)
        thread.daemon = True
        thread.start()
    
    def test_manual_context(self):
        """Test with manual context"""
        self.status_label.setText("Testing manual context message...")
        print("🧪 Testing manual context message...")
        
        def get_manual_message():
            try:
                message = self.gemini_service.get_message("motivational", "Give me a short encouraging message")
                print(f"📨 Received manual message: {message}")
                QTimer.singleShot(0, lambda: self.show_speech_bubble(message))
                self.last_message_time = time.time()
            except Exception as e:
                print(f"❌ Error getting manual message: {e}")
                QTimer.singleShot(0, lambda: self.status_label.setText(f"Error: {e}"))
        
        thread = threading.Thread(target=get_manual_message)
        thread.daemon = True
        thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Show test window
    test_window = GeminiTestWindow()
    test_window.show()
    
    print("🧪 Gemini Message Test Window Started!")
    print("✅ Click the buttons to test different message types")
    print("📋 Watch the console for detailed debug output")
    
    sys.exit(app.exec_())
