#!/usr/bin/env python3
"""
Simple speech bubble test - minimal version
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class TestSpeechBubble(QWidget):
    """Simple speech bubble test"""
    
    def __init__(self, message):
        super().__init__()
        self.message = message
        
        # Set up window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create label for text
        self.label = QLabel(self)
        self.label.setText(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Simple styling
        self.label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid #4CAF50;
                border-radius: 15px;
                padding: 10px;
                font-family: Arial;
                font-size: 12px;
                color: black;
                font-weight: bold;
            }
        """)
        
        # Set size
        self.setFixedSize(250, 80)
        self.label.setFixedSize(250, 80)
        
        # Position in center of screen
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 250) // 2
        y = (screen.height() - 80) // 2
        self.move(x, y)
        
        # Auto-close after 5 seconds
        QTimer.singleShot(5000, self.close)

def test_speech_bubble():
    """Test speech bubble display"""
    app = QApplication(sys.argv)
    
    print("🧪 Testing speech bubble display...")
    
    # Test message
    test_message = "🎯 Test speech bubble! If you can see this, the system works! 💬"
    
    # Create and show bubble
    bubble = TestSpeechBubble(test_message)
    bubble.show()
    
    print("✅ Speech bubble should be visible on screen for 5 seconds")
    print("💡 If you don't see it, there might be a display issue")
    
    # Run for 6 seconds then exit
    QTimer.singleShot(6000, app.quit)
    
    return app.exec_()

if __name__ == "__main__":
    test_speech_bubble()
