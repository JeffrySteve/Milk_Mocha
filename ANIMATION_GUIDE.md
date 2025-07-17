# 🥛 Milk Mocha Pet - Animation System Guide

## 🎭 Animation Methods

### Core States
- `show_idle()` - Default idle state (loops)
- `show_sleeping()` - Sleep after 60s inactivity
- `show_crying()` - Cry after 5min inactivity

### Interaction Animations
- `show_greeting()` - Startup greeting (3s → idle)
- `show_excited()` - Happy reaction (3s → idle)
- `show_laugh()` - Laughing reaction (3s → idle)
- `show_heartthrow()` - Love reaction (3s → idle)
- `show_doubtful()` - Rejection reaction (3s → idle)
- `show_says_yes()` - Achievement reaction (2s → idle)

### Activity Animations
- `show_drinking()` - Milk bottle consumption (3s → idle)
- `show_playing()` - Guitar playing (4s → idle)
- `show_dancing()` - Dance mode (5s → idle, random dance1/dance2)

## 🎯 Trigger System

### Automatic Triggers
- **Startup**: `show_greeting()` after 1s
- **Inactivity (60s)**: `show_sleeping()`
- **Inactivity (5min)**: `show_crying()`
- **Milk bottle click**: `show_drinking()`

### User Interactions
- **Left click**: Random reaction (excited/laugh/heartthrow)
- **Right click**: `show_heartthrow()`
- **Double click**: `show_greeting()`
- **10+ clicks**: Angry reaction

### Keyboard Shortcuts
- **Space**: `show_dancing()`
- **P**: `show_playing()`
- **Y**: `show_says_yes()`
- **S**: Open settings

## 🎬 GIF Mapping

| State/Action | GIF File | Duration | Purpose |
|-------------|----------|----------|---------|
| Idle | idle.gif | Loop | Default state |
| Drinking | drinking.gif | 3s | Milk bottle interaction |
| Sleeping | tierd.gif | Loop | Inactivity (60s) |
| Playing | playing_guitar.gif | 4s | P key or random |
| Greeting | says_hi.gif | 3s | Startup/double-click |
| Excited | excited.gif | 3s | Click reaction |
| Dancing | dance1.gif/dance2.gif | 5s | Space key |
| Crying | crying.gif | 4s | Long inactivity (5min) |
| Laughing | laugh.gif | 3s | Click reaction |
| Heart Throw | heartThrow.gif | 3s | Right-click love |
| Sitting | Sitting.gif | - | Optional idle variation |
| Watching | watching_mobile.gif | - | Do not disturb mode |
| Running | running.gif | - | Movement animation |
| Says Yes | says_yes.gif | 2s | Achievement |
| Doubtful | looking_doubtfuly.gif | 3s | Rejection/empty bottle |
| Angry | Angry.gif | 3s | Spam clicking |
| Pleasing | pleaseing.gif | - | Request animation |

## 🔧 Technical Features

### Lightweight Design
- Uses `QTimer.singleShot()` for automatic return to idle
- No blocking animations
- Memory efficient GIF switching

### Settings Integration
- Transparency control (100-255) preserved
- Auto-spawn bottle logic separate
- Settings restart app functionality

### State Management
- Proper interaction time tracking
- Click counter for spam protection
- Inactivity monitoring

## 🎮 Usage Examples

```python
# Basic usage
pet.show_greeting()  # Shows greeting, auto-returns to idle after 3s

# Random reactions
reactions = [pet.show_excited, pet.show_laugh, pet.show_heartthrow]
random.choice(reactions)()

# Timed sequences
QTimer.singleShot(1000, pet.show_greeting)
QTimer.singleShot(4000, pet.show_idle)
```

## 🛠️ Customization

### Adding New Animations
1. Add GIF file to `assets/mocha_gifs/`
2. Add path to `self.gif_paths` dictionary
3. Create `show_newanimation()` method
4. Add trigger in appropriate event handler

### Modifying Durations
- Edit duration parameter in `switch_gif()` calls
- Adjust inactivity timers in `check_inactivity()`
- Modify keyboard/mouse event response times

### Custom Triggers
- Add new keyboard shortcuts in `keyPressEvent()`
- Create custom mouse gestures in mouse event handlers
- Add timer-based events with `QTimer.singleShot()`
