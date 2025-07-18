# 🥛 Milk Mocha Pet - AI Desktop Companion

A delightful desktop pet with AI-powered motivational messages, animations, and interactive features!

## ✨ Features

- **🤖 AI Integration**: Gemini-powered speech bubbles every 2 minutes
- **🎭 18 Animations**: Dance, laugh, play guitar, and more
- **🍼 Interactive Feeding**: Drag milk bottles to feed your pet
- **🏃 Smart Movement**: Random running with smooth animations
- **🎛️ System Tray**: Hide/show and quick access to features
- **⚙️ Settings**: Transparency, intervals, and customization
- **💬 Speech Bubbles**: Motivational quotes, jokes, and reminders

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Gemini API** (Optional):
   - Get API key from [Google AI Studio](https://aistudio.google.com/)
   - Edit `config/api_keys.json` with your key
   - Works offline with fallback messages if no key provided

3. **Run Your Pet**:
   ```bash
   python main.py
   ```

## 🎮 Controls

### Keyboard Shortcuts
- **SPACE**: Dance animation
- **T**: Test speech bubble
- **G**: Request Gemini message
- **H**: Hide/Show pet
- **P**: Play guitar
- **Y**: Say yes
- **R**: Run to random location
- **S**: Open settings
- **ESC**: Exit application

### Mouse Interactions
- **Left Click**: Random reactions
- **Right Click**: Heart throw
- **Double Click**: Greeting
- **Drag**: Move pet around screen

### System Tray
- **Single Click**: Show notification
- **Double Click**: Hide/Show pet
- **Right Click**: Quick actions menu

## 📁 Project Structure

```
Milk_Mocha/
├── main.py                    # Main application
├── settings.py                # Settings window
├── requirements.txt           # Dependencies
├── assets/                    # GIF animations and sounds
├── config/                    # Configuration files
├── modules/                   # AI integration
└── README.md                  # This file
```

## 🛠️ Setup Guides

- **[Gemini Setup Guide](GEMINI_SETUP_GUIDE.md)**: Complete AI integration setup
- **[System Tray Guide](SYSTEM_TRAY_GUIDE.md)**: System tray features and usage

## 🎯 What Makes It Special

- **AI-Powered**: Fresh motivational messages from Google Gemini
- **Always Available**: Works offline with 25+ backup quotes
- **Non-Intrusive**: Lives in system tray when hidden
- **Highly Interactive**: Responds to clicks, keyboard, and movement
- **Customizable**: Adjust timing, transparency, and behavior
- **Professional**: Clean code with comprehensive error handling

## 🏆 Perfect For

- **Developers**: Motivational companion during coding sessions
- **Students**: Encouraging breaks and reminders
- **Remote Workers**: Friendly presence during long work days
- **Anyone**: Who wants a cute, interactive desktop companion!

---

*Enjoy your new AI-powered desktop companion! 🎉*