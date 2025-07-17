#!/usr/bin/env python3
"""
Test script to demonstrate system tray integration
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_system_tray():
    """Test system tray integration"""
    app = QApplication(sys.argv)
    
    # Check if system tray is available
    from PyQt5.QtWidgets import QSystemTrayIcon
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("❌ System tray not available on this system")
        return
    
    from main import MilkMochaPet
    
    # Create the pet
    pet = MilkMochaPet()
    
    print("🔔 Testing System Tray Integration")
    print("=" * 50)
    
    print("\n✅ SYSTEM TRAY FEATURES:")
    print("• Pet icon appears in system tray")
    print("• Single-click: Shows notification")
    print("• Double-click: Hide/Show pet")
    print("• Right-click: Full context menu")
    print("• Window close: Minimize to tray (not exit)")
    
    print("\n🎮 SYSTEM TRAY MENU:")
    print("• Hide/Show Pet - Toggle visibility")
    print("• Quick Actions - Animation shortcuts")
    print("  - Dance, Laugh, Excited, Heart Throw")
    print("  - Playing Guitar, Greeting, Run Random, Sleep")
    print("• Settings - Open settings window")
    print("• About - Show information")
    print("• Exit - Completely quit application")
    
    print("\n⌨️  KEYBOARD SHORTCUTS:")
    print("• H: Hide/Show pet")
    print("• ESC: Quit application")
    print("• SPACE: Dance")
    print("• P: Play guitar")
    print("• Y: Says yes")
    print("• R: Run to random location")
    print("• S: Open settings")
    
    print("\n🧪 TESTING INSTRUCTIONS:")
    print("1. Look for pet icon in system tray")
    print("2. Single-click tray icon for notification")
    print("3. Double-click tray icon to hide/show pet")
    print("4. Right-click tray icon for menu")
    print("5. Try 'Hide Pet' from tray menu")
    print("6. Try 'Quick Actions' from tray menu")
    print("7. Close window (X) - should minimize to tray")
    print("8. Press H key to toggle visibility")
    print("9. Use 'Exit' from tray menu to quit")
    
    def demonstrate_tray_features():
        print("\n🎬 DEMONSTRATION:")
        print("⭐ Watch the system tray notifications!")
        
        # Show initial notification
        QTimer.singleShot(2000, lambda: [
            print("🔔 Showing welcome notification..."),
            pet.tray_icon.showMessage(
                "Milk Mocha Pet",
                "System tray integration active! Try the tray menu.",
                pet.tray_icon.Information,
                3000
            )
        ])
        
        # Hide pet after 5 seconds
        QTimer.singleShot(5000, lambda: [
            print("👻 Hiding pet to demonstrate tray functionality..."),
            pet.hide(),
            pet.show_hide_action.setText("Show Pet")
        ])
        
        # Show pet again after 8 seconds
        QTimer.singleShot(8000, lambda: [
            print("👋 Showing pet again..."),
            pet.show(),
            pet.show_hide_action.setText("Hide Pet")
        ])
        
        # Demo quick action from tray
        QTimer.singleShot(10000, lambda: [
            print("🎭 Triggering dance from tray..."),
            pet.show_dancing()
        ])
        
        print("✅ System tray integration ready!")
    
    demonstrate_tray_features()
    
    print("\n🎯 BENEFITS:")
    print("• Pet can be hidden but still accessible")
    print("• Quick access to all animations")
    print("• System integration feels native")
    print("• Closing window doesn't exit app")
    print("• Full control from tray menu")
    
    print("\n🏆 SYSTEM TRAY INTEGRATION COMPLETE!")
    print("Your pet now lives in the system tray!")
    
    # Run longer to test tray functionality
    return app.exec_()

if __name__ == "__main__":
    test_system_tray()
