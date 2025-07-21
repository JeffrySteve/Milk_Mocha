#!/usr/bin/env python3
"""
Test script for speech bubble following and click handling
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(__file__))

# Import our classes
from main import MilkMochaPet, SpeechBubble

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Speech Bubble Test')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        # Create pet instance
        self.pet = MilkMochaPet()
        
        # Test buttons
        test_btn = QPushButton('Test Speech Bubble')
        test_btn.clicked.connect(self.test_speech_bubble)
        layout.addWidget(test_btn)
        
        move_btn = QPushButton('Move Pet (Test Following)')
        move_btn.clicked.connect(self.move_pet)
        layout.addWidget(move_btn)
        
        click_test_btn = QPushButton('Test Click Safety')
        click_test_btn.clicked.connect(self.test_click_safety)
        layout.addWidget(click_test_btn)
        
        self.status_label = QLabel('Ready to test!')
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def test_speech_bubble(self):
        """Test basic speech bubble functionality"""
        self.status_label.setText('Testing speech bubble...')
        message = "🧪 Test bubble! Try clicking me - I should not crash! 💬"
        self.pet.show_speech_bubble(message)
        
    def move_pet(self):
        """Move pet to test bubble following"""
        self.status_label.setText('Moving pet - bubble should follow!')
        # Move pet to a new position
        import random
        new_x = random.randint(100, 800)
        new_y = random.randint(100, 500)
        self.pet.move(new_x, new_y)
        
    def test_click_safety(self):
        """Test clicking speech bubbles multiple times"""
        self.status_label.setText('Testing click safety - try clicking bubbles quickly!')
        for i in range(3):
            QTimer.singleShot(i * 1000, lambda i=i: self.pet.show_speech_bubble(f"🔄 Bubble {i+1} - Click me safely!"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Show test window
    test_window = TestWindow()
    test_window.show()
    
    print("🧪 Speech Bubble Test Started!")
    print("✅ Features to test:")
    print("   1. Click 'Test Speech Bubble' to create a bubble")
    print("   2. Click 'Move Pet' to test bubble following")
    print("   3. Click 'Test Click Safety' for crash testing")
    print("   4. Click on speech bubbles - they should not crash!")
    print("   5. Move the pet around - bubble should follow smoothly")
    
    sys.exit(app.exec_())
