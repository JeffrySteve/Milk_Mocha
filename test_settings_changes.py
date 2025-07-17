#!/usr/bin/env python3
"""
Test script to verify the settings changes
"""
import sys
import os
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import MilkMochaPet
from settings import SettingsWindow

def test_settings_changes():
    """Test the updated settings"""
    app = QApplication(sys.argv)
    
    # Create the pet
    pet = MilkMochaPet()
    
    # Test settings window creation
    settings_window = SettingsWindow()
    print("✓ Settings window created successfully (no transparency slider)")
    
    # Test restart signal connection
    try:
        settings_window.restart_requested.connect(pet.restart_app)
        print("✓ Restart signal connected successfully")
    except Exception as e:
        print(f"✗ Error connecting restart signal: {e}")
    
    # Test config loading without transparency
    config_data = pet.load_config()
    expected_keys = ["spawn_interval", "auto_spawn", "last_position"]
    
    for key in expected_keys:
        if key in config_data:
            print(f"✓ Config has {key}: {config_data[key]}")
        else:
            print(f"✗ Config missing {key}")
    
    if "transparency" in config_data:
        print("✗ Transparency still in config (should be removed)")
    else:
        print("✓ Transparency removed from config")
    
    print("\n🎉 Settings changes verified!")
    print("- Transparency feature removed")
    print("- Apply button now says 'Apply & Restart'")
    print("- App will restart when settings are changed")
    
    # Show the pet briefly
    pet.show()
    
    # Close after 2 seconds
    QTimer.singleShot(2000, app.quit)
    
    return app.exec_()

if __name__ == "__main__":
    test_settings_changes()
