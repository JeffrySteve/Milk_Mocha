# System Tray Integration User Guide

## 🎯 Overview
Your Milk Mocha Pet now includes complete system tray integration, allowing you to control the pet's visibility and access features even when the main window is hidden!

## 🔧 System Tray Features

### 📍 Tray Icon
- **Location**: Look for the Milk Mocha Pet icon in your system tray (bottom-right corner of screen)
- **Icon**: Created from the pet's GIF frames for a dynamic appearance
- **Tooltip**: Shows "Milk Mocha Pet - Desktop Companion" when hovering

### 🖱️ Click Actions
- **Single Click**: Shows a notification with current status
- **Double Click**: Toggle pet visibility (hide/show)
- **Right Click**: Opens the full context menu

### 📋 Context Menu Options

#### 🔄 Hide/Show Pet
- Toggles the pet's visibility on your desktop
- Text changes dynamically based on current state
- Keyboard shortcut: **H key**

#### ⚡ Quick Actions Submenu
Access your favorite animations instantly:
- **Dance** - Make your pet dance
- **Laugh** - Trigger laughing animation
- **Excited** - Show excitement
- **Heart Throw** - Throw hearts
- **Playing Guitar** - Musical performance
- **Greeting** - Wave hello
- **Run Random** - Run to random location
- **Sleep** - Tired animation

#### ⚙️ Settings
- Opens the settings window
- Control transparency, spawn intervals, and more
- Keyboard shortcut: **S key**

#### ℹ️ About
- Shows information about the pet and its features
- Displays as a system notification

#### 🚪 Exit
- Completely closes the application
- Use this for proper shutdown
- Keyboard shortcut: **ESC key**

## 🎮 User Experience

### 🔒 Hide to Tray
- **Closing Window**: When you click the X button, the pet minimizes to the tray instead of quitting
- **Notification**: Shows "Milk Mocha Pet hidden to tray. Double-click tray icon to show."
- **Access**: Pet remains fully functional through the tray menu

### 📢 Notifications
- **Welcome**: Shows when system tray is initialized
- **Status Updates**: Informs you when pet is hidden/shown
- **Feature Info**: Displays information about pet capabilities

### ⌨️ Keyboard Shortcuts
All keyboard shortcuts work even when the pet is hidden:
- **H**: Hide/Show toggle
- **ESC**: Quit application
- **SPACE**: Dance
- **P**: Play guitar
- **Y**: Says yes
- **R**: Run to random location
- **S**: Open settings

## 🎨 Benefits

### 🏠 Desktop Management
- **Clean Desktop**: Hide pet when working, show when relaxing
- **No Interruption**: Pet accessible but not distracting
- **Persistent**: Pet stays in memory even when hidden

### 🚀 Quick Access
- **Instant Animations**: Trigger fun animations without opening window
- **Fast Settings**: Access configuration without hunting for window
- **One-Click Control**: Hide/show with simple double-click

### 🔧 System Integration
- **Native Feel**: Integrates seamlessly with Windows system tray
- **Professional**: Clean, organized menu structure
- **Informative**: Clear notifications and status updates

## 🛠️ Technical Details

### 🔍 System Requirements
- Windows system tray support (available on all modern Windows versions)
- PyQt5 framework with QSystemTrayIcon support
- Sufficient system resources for background processing

### 🎯 Implementation Features
- **Dynamic Icon**: Created from pet's GIF frames
- **Smart Hiding**: Window close minimizes to tray, doesn't exit
- **Proper Cleanup**: Exit from tray menu ensures complete shutdown
- **Status Tracking**: Menu items update based on current state

## 🎉 Usage Tips

1. **First Launch**: Look for the pet icon in your system tray
2. **Quick Hide**: Double-click tray icon for instant hide/show
3. **Entertainment**: Use Quick Actions for instant fun
4. **Productivity**: Hide pet during work, show during breaks
5. **Customization**: Access settings quickly from tray menu
6. **Proper Exit**: Always use "Exit" from tray menu to quit cleanly

## 🏆 Conclusion

The system tray integration transforms your Milk Mocha Pet into a true desktop companion that's always accessible but never intrusive. Enjoy the perfect balance of entertainment and productivity!

---
*Your pet is now fully integrated into your system - have fun exploring all the tray features!*
