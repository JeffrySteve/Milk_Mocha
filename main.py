"""
Milk Mocha Pet - Main Entry Point
A cute desktop companion with animations, interactions, and AI conversations!

This is the refactored version with modular architecture:
- core/pet.py - Main pet widget
- core/pet_behavior.py - Behavior and interaction logic
- animation/gif_manager.py - Animation management
- ui/speech_bubble.py - Speech bubble UI
- ui/milk_bottle.py - Milk bottle UI
- ui/system_tray.py - System tray management
- utils/config.py - Configuration management
"""
import sys
from PyQt5.QtWidgets import QApplication

# Import the main pet class
from core.pet import MilkMochaPet


def main():
    """Main entry point for the Milk Mocha Pet application"""
    print("🥛 Starting Milk Mocha Pet - Modular Edition!")
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Milk Mocha Pet")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Milk Mocha Studios")
    
    # Create and show the pet
    pet = MilkMochaPet()
    
    print("✅ Milk Mocha Pet started successfully!")
    print("🎮 Keyboard shortcuts:")
    print("   • G - Ask Gemini for a message")
    print("   • Space - Dance")
    print("   • S - Settings")
    print("   • P - Play guitar")
    print("   • Y - Say yes")
    print("   • R - Run to random location")
    print("   • H - Hide/Show")
    print("   • ESC - Exit")
    
    # Run the application
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
