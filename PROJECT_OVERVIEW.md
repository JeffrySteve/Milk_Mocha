# 🥛 Milk Mocha Pet - Clean Production Version

## Project Overview
Milk Mocha Pet is a delightful desktop companion featuring an adorable animated character that interacts with users through AI-powered conversations, cute animations, and responsive behaviors.

## ✨ Features

### 🎭 **Animations & Interactions**
- **Interactive Animations**: Click to trigger random reactions (excited, laughing, heart throw)
- **Automatic Behaviors**: Periodic dancing, running to random locations, and spontaneous actions
- **Emotional Responses**: Different animations for various moods and interactions
- **Smooth Movement**: Fluid animation transitions and position changes

### 🤖 **AI Integration**
- **Gemini AI Messages**: Context-aware conversations based on time of day and user activity
- **Fallback System**: Built-in cute messages when AI is unavailable
- **Thread-Safe**: Crash-resistant AI calls with timeout protection
- **Smart Timing**: Intelligent message scheduling based on user activity

### 🎮 **User Controls**
- **Keyboard Shortcuts**: 
  - `G` - Request AI message
  - `Space` - Dance animation
  - `S` - Open settings
  - `P` - Play guitar
  - `Y` - Say yes
  - `R` - Run to random location
  - `H` - Hide/Show pet
  - `ESC` - Exit application
- **Mouse Interactions**: Click for reactions, right-click for heart throw, double-click for greeting
- **System Tray**: Background operation with tray icon

### ⚙️ **Configuration**
- **Settings Window**: Easy configuration of AI speaking intervals and behaviors
- **Persistent Config**: Settings saved between sessions
- **Position Memory**: Remembers pet location on screen

## 🏗️ **Architecture**

### **Modular Design**
```
Milk_Mocha/
├── main.py                 # Application entry point
├── core/                   # Core functionality
│   ├── pet.py             # Main pet widget and coordination
│   └── pet_behavior.py    # Behavior logic and interactions
├── ui/                     # User interface components
│   ├── speech_bubble.py   # AI message display
│   ├── milk_bottle.py     # Interactive milk bottle
│   ├── system_tray.py     # System tray management
│   └── settings_window.py # Configuration dialog
├── animation/              # Animation management
│   └── gif_manager.py     # GIF loading and switching
├── utils/                  # Utilities and services
│   ├── config.py          # Configuration management
│   ├── user_activity.py   # Activity detection
│   ├── gemini_service.py  # AI service implementation
│   └── safe_gemini.py     # Thread-safe AI wrapper
├── assets/                 # Media resources
│   ├── mocha_gifs/        # Pet animation GIFs
│   ├── food_gifs/         # Food-related GIFs
│   └── sounds/            # Audio files
└── config/                # Configuration files
    └── settings.json      # User preferences
```

### **Key Components**

#### **Core System**
- **MilkMochaPet**: Main widget coordinating all components
- **PetBehavior**: Handles interactions, timing, and AI communication
- **ConfigManager**: Persistent settings management

#### **AI System**
- **SafeGeminiService**: Thread-safe AI wrapper with timeout protection
- **GeminiService**: Core AI communication with fallback messages
- **UserActivityDetector**: Context-aware message timing

#### **Animation System**
- **GifManager**: Efficient GIF loading and animation switching
- **SpeechBubble**: Thread-safe message display with smooth animations

## 🚀 **Getting Started**

### **Requirements**
```
PyQt5>=5.15.0
google-generativeai  # Optional, for AI features
```

### **Installation**
1. Clone or download the project
2. Install dependencies: `pip install -r requirements.txt`
3. (Optional) Set up Gemini API key for AI features
4. Run: `python main.py`

### **API Setup (Optional)**
- Get a Gemini API key from Google AI Studio
- Set environment variable: `GEMINI_API_KEY=your_key_here`
- Without API key, the pet uses built-in cute messages

## 🎯 **Usage**
- **Desktop Companion**: Runs as a desktop widget that stays on top
- **Always Available**: Minimizes to system tray, never truly closes
- **Interactive**: Responds to clicks, keyboard shortcuts, and time-based events
- **Configurable**: Adjust AI frequency and behaviors through settings

## 🔧 **Technical Features**
- **Thread Safety**: All AI operations use proper signal-slot communication
- **Error Resilience**: Comprehensive error handling prevents crashes
- **Resource Efficient**: Optimized GIF loading and memory management
- **Cross-Platform**: Works on Windows, macOS, and Linux (with Qt5)

## 🎨 **Customization**
- **Easy GIF Replacement**: Add new animations by placing GIFs in assets/mocha_gifs/
- **Message Customization**: Modify fallback messages in utils/gemini_service.py
- **Behavior Tuning**: Adjust timing and frequencies in core/pet_behavior.py

---

**Milk Mocha Pet** - Your adorable, AI-powered desktop companion! 🥛✨
