"""
Test script for debugging Gemini 'G' key crash issue
"""
import sys
import time
from PyQt5.QtWidgets import QApplication
from core.pet import MilkMochaPet

def test_gemini_g_key():
    """Test the G key functionality in isolation"""
    print("🧪 Testing Gemini G key functionality...")
    
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Create pet
        print("Creating pet...")
        pet = MilkMochaPet()
        
        # Test the request_contextual_message method directly
        print("Testing request_contextual_message...")
        pet.request_contextual_message()
        
        # Wait a bit for the thread to complete
        print("Waiting 10 seconds for message...")
        
        # Use QTimer to quit after delay
        from PyQt5.QtCore import QTimer
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(app.quit)
        timer.start(10000)  # 10 seconds
        
        # Run event loop
        app.exec_()
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_g_key()
