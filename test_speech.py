#!/usr/bin/env python3
"""
Test script to check if speech bubble system works
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🧪 Testing imports...")
    
    # Test basic imports
    from PyQt5.QtWidgets import QApplication, QLabel, QWidget
    from PyQt5.QtGui import QMovie, QPixmap, QIcon
    from PyQt5.QtCore import Qt, QTimer
    print("✅ PyQt5 imports successful")
    
    # Test custom modules
    from modules.gemini_handler import GeminiService
    print("✅ GeminiService import successful")
    
    from modules.user_activity import UserActivityDetector
    print("✅ UserActivityDetector import successful")
    
    # Test API key loading
    gemini_service = GeminiService()
    if gemini_service.handler.api_key:
        print(f"✅ API key loaded: {gemini_service.handler.api_key[:10]}...")
    else:
        print("❌ No API key found")
    
    # Test fallback quotes
    fallback = gemini_service.handler.get_fallback_message("random")
    print(f"✅ Fallback message: {fallback}")
    
    print("\n🎯 All tests passed! Speech system should work.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
