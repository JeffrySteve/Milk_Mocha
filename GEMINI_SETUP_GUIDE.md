# Gemini API Setup Guide

## 🤖 Overview
Your Milk Mocha Pet now includes AI-powered motivational messages using Google's Gemini API! The pet will randomly show speech bubbles with personalized messages, jokes, and motivational quotes.

## 🔧 Setup Instructions

### 1️⃣ Get Your Gemini API Key

1. **Visit Google AI Studio**: Go to [https://aistudio.google.com/](https://aistudio.google.com/)
2. **Sign in**: Use your Google account
3. **Create API Key**: 
   - Click on "Get API Key" in the top right
   - Click "Create API Key"
   - Copy the generated key (starts with "AIza...")

### 2️⃣ Configure Your Pet

1. **Open Configuration File**: `config/api_keys.json`
2. **Add Your Key**: Replace `"YOUR_GEMINI_API_KEY_HERE"` with your actual API key:
   ```json
   {
     "gemini_api_key": "AIzaSyC_your_actual_key_here"
   }
   ```
3. **Save the File**

### 3️⃣ Install Dependencies

Run this command in your project directory:
```bash
pip install aiohttp
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Features

### 🗨️ Speech Bubbles
- **Random Timing**: Appears every 30-60 minutes
- **Smart Positioning**: Shows above your pet's head
- **Auto-Hide**: Disappears after 15 seconds
- **Click to Dismiss**: Click bubble to hide it instantly

### 🤖 Gemini Messages
- **Motivational Quotes**: Encouraging messages under 20 words
- **Clean Jokes**: Family-friendly humor
- **Fun Facts**: Interesting tidbits to brighten your day
- **Wellness Reminders**: Gentle nudges to take breaks and stay healthy

### 🔄 Offline Fallbacks
- **No Internet?**: Uses local motivational quotes
- **API Issues?**: Automatically switches to backup messages
- **Always Available**: Never leaves you without encouragement

## 🎨 Message Types

The pet will randomly choose from these prompt categories:

### 💪 Motivational
- "You are doing great! Keep going! 🌟"
- "Every small step counts towards your goals! 👣"
- "You've got this! One step at a time! 🚀"

### 😄 Humorous
- "Why did the cat sit on the computer? To keep an eye on the mouse! 🐱"
- "A good laugh is sunshine in the house! ☀️"

### 🌱 Wellness
- "Remember to drink water and take breaks! 💧"
- "Rest is not a waste of time, it's essential! 💤"
- "Breathe deeply, you're exactly where you need to be! 🌸"

### 🧠 Fun Facts
- Educational and entertaining facts under 20 words
- Cute animal facts and interesting trivia

## ⚙️ Configuration

### 📁 Files Created
- `modules/gemini_client.py` - API client and message handling
- `config/api_keys.json` - Your API key storage
- `config/fallback_quotes.json` - Offline backup messages

### 🔧 Customization Options

#### Change Message Frequency
Edit the timer intervals in `main.py`:
```python
# Current: 30-60 minutes
min_interval = 30 * 60 * 1000  # 30 minutes
max_interval = 60 * 60 * 1000  # 60 minutes
```

#### Add Custom Prompts
Edit the prompts list in `modules/gemini_client.py`:
```python
self.prompts = [
    "Tell me a cute motivational quote under 20 words.",
    "Your custom prompt here...",
    # Add more prompts
]
```

#### Add Custom Fallbacks
Edit `config/fallback_quotes.json`:
```json
[
  "Your custom fallback message here! 🌟",
  "Another encouraging message! 💪"
]
```

## 🛠️ Troubleshooting

### 🔑 API Key Issues
- **Invalid Key**: Double-check your API key in `config/api_keys.json`
- **Quota Exceeded**: Check your Google AI Studio usage limits
- **Network Issues**: Pet will use fallback messages automatically

### 💬 Speech Bubble Issues
- **Not Showing**: Check console for error messages
- **Wrong Position**: Pet automatically adjusts for screen bounds
- **Won't Hide**: Click the bubble or wait 15 seconds

### 🐛 Common Errors
- **Import Error**: Make sure `aiohttp` is installed
- **File Not Found**: Ensure all config files exist
- **API Timeout**: Increased to 10 seconds, should handle most cases

## 🎉 Usage Tips

1. **First Launch**: Messages start appearing after 30-60 minutes
2. **No Key Required**: Works with fallback messages if no API key
3. **Privacy**: Your API key stays local in your config file
4. **Customizable**: Edit prompts and fallbacks to match your style
5. **Reliable**: Always has backup messages when API is unavailable

## 🚀 Advanced Features

### 🔄 Smart Fallbacks
- Automatically detects API failures
- Seamlessly switches to local messages
- No interruption to user experience

### 🎯 Contextual Messages
- Prompts designed for desktop companion use
- Encouraging and positive messaging
- Appropriate length for speech bubbles

### 🎨 Visual Design
- Styled speech bubbles with rounded corners
- Fade-in animations for smooth appearance
- Proper positioning relative to pet

## 🏆 Benefits

- **🧠 AI-Powered**: Fresh, personalized messages from Gemini
- **🔄 Reliable**: Always works with offline fallbacks
- **🎯 Contextual**: Messages perfect for work break encouragement
- **🎨 Beautiful**: Polished speech bubble design
- **⚡ Lightweight**: Minimal impact on system resources
- **🔒 Private**: Your API key stays on your computer

---

**Your Milk Mocha Pet is now AI-powered! Enjoy personalized encouragement throughout your day! 🎉**
