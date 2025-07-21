"""
Complete test for T key story functionality
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.pet import MilkMochaPet

def test_t_key_story():
    print("🧪 Testing T key story functionality...")
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    try:
        # Create pet instance
        pet = MilkMochaPet()
        print("✅ Pet instance created successfully")
        
        # Check if gemini service is available
        print(f"🤖 Gemini service available: {hasattr(pet, 'gemini_service')}")
        if hasattr(pet, 'gemini_service'):
            print(f"   - Model available: {pet.gemini_service.model is not None}")
            print(f"   - API key set: {pet.gemini_service.api_key is not None}")
        
        # Test the tell_funny_story method directly
        print("\n📚 Testing tell_funny_story method...")
        if hasattr(pet, 'behavior') and hasattr(pet.behavior, 'tell_funny_story'):
            print("✅ tell_funny_story method found")
            
            # Call the method directly
            pet.behavior.tell_funny_story()
            print("✅ tell_funny_story method called successfully")
            
            # Wait a bit to see if the story appears
            QTimer.singleShot(3000, app.quit)  # Quit after 3 seconds
            
        else:
            print("❌ tell_funny_story method not found")
            
        # Show the pet
        pet.show()
        print("✅ Pet shown on screen")
        
        # Start the app for a few seconds to test
        app.exec_()
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🧪 Test completed")

if __name__ == "__main__":
    test_t_key_story()
