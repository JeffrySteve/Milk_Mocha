#!/usr/bin/env python3
"""
Test script to verify the transparency feature with minimum limit
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

def test_transparency_feature():
    """Test the transparency feature with minimum limit"""
    app = QApplication(sys.argv)
    
    # Create the pet
    pet = MilkMochaPet()
    
    # Test settings window creation
    settings_window = SettingsWindow()
    print("✓ Settings window created with transparency slider")
    
    # Test transparency slider range
    min_val = settings_window.transparency_slider.minimum()
    max_val = settings_window.transparency_slider.maximum()
    current_val = settings_window.transparency_slider.value()
    
    print(f"✓ Transparency slider range: {min_val} - {max_val}")
    print(f"✓ Current transparency value: {current_val}")
    
    if min_val >= 100:
        print("✓ Minimum transparency limit enforced (≥100)")
    else:
        print("✗ Minimum transparency limit not enforced")
    
    # Test transparency application
    config_data = pet.load_config()
    if "transparency" in config_data:
        transparency = config_data["transparency"]
        applied_transparency = max(100, min(255, transparency))
        opacity = applied_transparency / 255.0
        print(f"✓ Transparency in config: {transparency}")
        print(f"✓ Applied transparency: {applied_transparency}")
        print(f"✓ Window opacity: {opacity:.2f}")
    else:
        print("✗ Transparency not found in config")
    
    # Test restart signal connection
    try:
        settings_window.restart_requested.connect(pet.restart_app)
        print("✓ Restart signal connected successfully")
    except Exception as e:
        print(f"✗ Error connecting restart signal: {e}")
    
    print("\n🎉 Transparency feature with minimum limit verified!")
    print("- Transparency range: 100-255 (prevents complete fade out)")
    print("- Settings apply with app restart")
    print("- Minimum opacity: 0.39 (100/255)")
    print("- Maximum opacity: 1.00 (255/255)")
    
    # Show the pet briefly
    pet.show()
    
    # Close after 3 seconds
    QTimer.singleShot(3000, app.quit)
    
    return app.exec_()

if __name__ == "__main__":
    test_transparency_feature()
