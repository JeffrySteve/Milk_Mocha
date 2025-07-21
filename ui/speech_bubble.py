"""
Speech bubble UI component for Milk Mocha Pet
"""
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve


class SpeechBubble(QWidget):
    """Speech bubble widget for displaying Gemini messages"""
    
    def __init__(self, message, pet_parent=None):
        super().__init__(None)  # No Qt parent for independent window
        self.message = message
        self.pet_parent = pet_parent  # Reference to MilkMochaPet for communication
        
        # Set up window properties for better visibility
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Create label for text
        self.label = QLabel(self)
        self.label.setText(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Enhanced styling for better visibility
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 250);
                border: 3px solid #4CAF50;
                border-radius: 20px;
                padding: 15px;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #000;
                font-weight: bold;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 100);
            }
        """)
        
        # Calculate size based on text with better sizing
        font_metrics = self.label.fontMetrics()
        text_width = font_metrics.boundingRect(message).width()
        
        # Set bubble size (increased for better visibility)
        bubble_width = min(max(text_width + 60, 200), 300)
        bubble_height = 80
        
        # Calculate required height for wrapped text
        text_rect = font_metrics.boundingRect(0, 0, bubble_width - 40, 1000, Qt.TextWordWrap, message)
        required_height = max(text_rect.height() + 50, bubble_height)
        
        self.setFixedSize(bubble_width, required_height)
        self.label.setFixedSize(bubble_width, required_height)
        
        # Make widget focusable and ensure it's visible
        self.setFocusPolicy(Qt.NoFocus)
        self.setWindowOpacity(1.0)
        
        # Add fade-in animation
        self.fade_in()
    
    def fade_in(self):
        """Animate fade-in effect"""
        self.setWindowOpacity(0.0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(800)  # Slower for better visibility
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.fade_animation.start()
    
    def mousePressEvent(self, event):
        """Hide bubble when clicked - notify parent to handle safely"""
        if event.button() == Qt.LeftButton:
            print("💬 Speech bubble clicked - requesting hide...")
            # Let the parent handle the hiding to avoid conflicts
            if self.pet_parent:
                self.pet_parent.hide_speech_bubble()
            else:
                # Fallback if no parent
                try:
                    self.hide()
                    self.deleteLater()
                except RuntimeError:
                    pass
