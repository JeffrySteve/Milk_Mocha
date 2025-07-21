# Milk Mocha Pet - Modular Architecture 🥛

## Project Structure

The project has been refactored into a clean, modular architecture for better maintainability:

```
Milk_Mocha/
├── main_modular.py          # New main entry point
├── main.py                  # Original monolithic version (backup)
├── core/                    # Core pet functionality
│   ├── __init__.py
│   ├── pet.py              # Main pet widget class
│   └── pet_behavior.py     # Behavior and interaction logic
├── ui/                     # User interface components
│   ├── __init__.py
│   ├── speech_bubble.py    # Speech bubble widget
│   ├── milk_bottle.py      # Milk bottle widget
│   └── system_tray.py      # System tray management
├── animation/              # Animation management
│   ├── __init__.py
│   └── gif_manager.py      # GIF and animation handling
├── utils/                  # Utilities and helpers
│   ├── __init__.py
│   └── config.py           # Configuration management
├── modules/                # Existing modules (unchanged)
│   ├── gemini_handler.py
│   ├── user_activity.py
│   ├── mood_tracker.py
│   └── ...
└── assets/                 # Assets (unchanged)
    ├── mocha_gifs/
    ├── food_gifs/
    └── sounds/
```

## Module Responsibilities

### 🎯 Core Module (`core/`)
- **`pet.py`**: Main `MilkMochaPet` widget class, coordinates all components
- **`pet_behavior.py`**: Handles pet behaviors, AI interactions, and timers

### 🎨 UI Module (`ui/`)
- **`speech_bubble.py`**: Speech bubble widget for displaying messages
- **`milk_bottle.py`**: Interactive milk bottle for feeding
- **`system_tray.py`**: System tray icon and menu management

### 🎬 Animation Module (`animation/`)
- **`gif_manager.py`**: Manages GIF animations and transitions

### 🔧 Utils Module (`utils/`)
- **`config.py`**: Configuration file management and persistence

## Key Improvements

### ✅ Separation of Concerns
- Each module has a single, clear responsibility
- UI components are isolated from business logic
- Configuration management is centralized

### ✅ Better Maintainability
- Code is organized into logical modules
- Easier to find and modify specific functionality
- Reduced file size (from 1000+ lines to ~200-300 lines per file)

### ✅ Enhanced Modularity
- Components can be developed and tested independently
- Easy to add new features without affecting existing code
- Clear interfaces between modules

### ✅ Improved Debugging
- Issues can be isolated to specific modules
- Cleaner error handling and logging
- Better separation of concerns for troubleshooting

## Usage

### Running the Application
```bash
# New modular version
python main_modular.py

# Original version (backup)
python main.py
```

### Keyboard Shortcuts
- **T**: Test speech bubble
- **G**: Gemini contextual message
- **B**: Basic Gemini message  
- **F**: Fallback message test
- **D**: Debug Gemini API
- **Space**: Dance animation
- **S**: Open settings
- **P**: Play guitar animation
- **Y**: Say yes animation
- **R**: Run to random location
- **H**: Hide/Show pet
- **ESC**: Exit application

## Development Notes

### Adding New Animations
1. Add GIF file to `assets/mocha_gifs/`
2. Update `gif_paths` in `animation/gif_manager.py`
3. Create method in `core/pet.py` that calls `gif_manager.switch_gif()`

### Adding New UI Components
1. Create new file in `ui/` directory
2. Import and initialize in `core/pet.py`
3. Add any necessary methods to pet class

### Adding New Behaviors
1. Add methods to `core/pet_behavior.py`
2. Set up timers or triggers as needed
3. Call from `core/pet.py` keyboard/mouse events

### Configuration Changes
1. Modify default values in `utils/config.py`
2. Update settings window if needed
3. Test configuration persistence

## Future Enhancements

- [ ] Plugin system for custom behaviors
- [ ] Theme system for different pet appearances
- [ ] Multi-pet support
- [ ] Enhanced AI conversation features
- [ ] Mobile companion app integration

## Migration from Original

The original `main.py` has been preserved as a backup. All functionality has been maintained in the modular version with the following benefits:

- **Easier maintenance**: Find specific functionality quickly
- **Better testing**: Test individual components in isolation
- **Cleaner code**: Each file has a focused purpose
- **Faster development**: Add features without touching unrelated code

To use the new modular version, simply run `main_modular.py` instead of `main.py`.
