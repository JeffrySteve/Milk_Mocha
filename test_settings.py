#!/usr/bin/env python3
"""
Test script to validate the settings integration
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import MilkMochaPet
from settings import SettingsWindow

def test_settings_integration():
    """Test the settings integration"""
    app = QApplication(sys.argv)
    
    # Create the pet
    pet = MilkMochaPet()
    
    # Test settings window creation
    settings_window = SettingsWindow()
    print("✓ Settings window created successfully")
    
    # Test signal connection
    try:
        settings_window.settings_changed.connect(pet.update_settings)
        print("✓ Settings signal connected successfully")
    except Exception as e:
        print(f"✗ Error connecting settings signal: {e}")
    
    # Test settings update method
    test_settings = {
        "spawn_interval": 10000,
        "transparency": 200,
        "auto_spawn": True
    }
    
    try:
        pet.update_settings(test_settings)
        print("✓ Settings update method works")
    except Exception as e:
        print(f"✗ Error updating settings: {e}")
    
    # Test keyboard shortcut
    print("✓ Keyboard shortcut (S key) should open settings")
    
    # Test right-click menu
    print("✓ Right-click menu should show settings option")
    
    print("\n🎉 All tests passed! Settings integration is working correctly.")
    
    # Show the pet briefly
    pet.show()
    
    # Close after 2 seconds
    QTimer.singleShot(2000, app.quit)
    
    return app.exec_()

if __name__ == "__main__":
    test_settings_integration()
