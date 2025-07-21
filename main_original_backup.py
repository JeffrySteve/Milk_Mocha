import sys
import os
import json
import random
import time
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu, QSystemTrayIcon, QAction
from PyQt5.QtGui import QMovie, QPixmap, QIcon, QPainter, QPen, QBrush, QFont
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QSize, pyqtSignal
from settings import SettingsWindow
from modules.gemini_handler import GeminiService
from modules.user_activity import UserActivityDetector

class MilkMochaPet(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up window properties for transparencygg
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Make widget focusable for keyboard events
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Initialize variables
        self.current_gif = "assets/mocha_gifs/idle.gif"
        self.drag_start_position = None
        self.active_bottles = []
        self.animation_timer = None  # Track current animation timer
        self.speech_bubble = None  # Track speech bubble
        self.bubble_timer = None  # Track bubble auto-hide timer
        self.bubble_follow_timer = None  # Track bubble following timer
        
        # Initialize Gemini service and user activity detector
        self.gemini_service = GeminiService()
        self.user_activity = UserActivityDetector()
        self.last_message_time = None
        
        # 1️⃣ Organize GIF file paths with exact names and clear mapping
        self.gif_paths = {
            "idle": "assets/mocha_gifs/idle.gif",
            "drinking": "assets/mocha_gifs/drinking.gif",
            "sleeping": "assets/mocha_gifs/tierd.gif",
            "playing": "assets/mocha_gifs/playing_guitar.gif",
            "greeting": "assets/mocha_gifs/says_hi.gif",
            "excited": "assets/mocha_gifs/excited.gif",
            "dancing": "assets/mocha_gifs/dance1.gif",
            "dancing2": "assets/mocha_gifs/dance2.gif",
            "crying": "assets/mocha_gifs/crying.gif",
            "laugh": "assets/mocha_gifs/laugh.gif",
            "heartthrow": "assets/mocha_gifs/heartThrow.gif",
            "sitting": "assets/mocha_gifs/Sitting.gif",
            "watching": "assets/mocha_gifs/watching_mobile.gif",
            "running": "assets/mocha_gifs/running.gif",
            "says_yes": "assets/mocha_gifs/says_yes.gif",
            "doubtful": "assets/mocha_gifs/looking_doubtfuly.gif",
            "angry": "assets/mocha_gifs/Angry.gif",
            "pleasing": "assets/mocha_gifs/pleaseing.gif"
        }
        
        # 5️⃣ Inactivity tracking
        self.last_interaction_time = time.time()
        
        # 7️⃣ Click counter for anger trigger
        self.click_count = 0
        
        # Initialize settings window reference
        self.settings_window = None
        
        # Initialize system tray
        self.init_system_tray()
        
        # Load config
        self.config_data = self.load_config()
        
        # 2️⃣ Apply loaded settings
        self.spawn_interval = self.config_data["spawn_interval"]
        self.auto_spawn = self.config_data["auto_spawn"]
        self.speaking_enabled = self.config_data.get("milk_mocha_speaking", True)
        self.speaking_interval = self.config_data.get("speaking_interval", 15) * 60  # Convert to seconds
        
        # Create the main label for the pet
        self.pet_label = QLabel(self)
        self.pet_label.setAlignment(Qt.AlignCenter)
        
        # Load and set up the GIF
        self.setup_pet_animation()
        
        # Set position from config
        last_pos = self.config_data.get("last_position", [300, 300])
        self.move(last_pos[0], last_pos[1])
        
        # Set transparency (with minimum limit)
        transparency = self.config_data.get("transparency", 255)
        transparency = max(100, min(255, transparency))  # Ensure range 100-255
        self.setWindowOpacity(transparency / 255.0)
        
        if self.auto_spawn:
            self.spawn_timer = QTimer()
            self.spawn_timer.timeout.connect(self.spawn_milk_bottle)
            self.spawn_timer.start(self.spawn_interval)
        
        # 5️⃣ Start inactivity checking
        self.check_inactivity()
        
        # 🏃 Start random running timer (every 30 seconds)
        self.start_random_running()
        
        # 🎭 Start random action timer (every 45 seconds)
        self.start_random_actions()
        
        # 🤖 Start enhanced Gemini speaking system
        if self.speaking_enabled:
            self.start_smart_speaking_system()
        
        # 3️⃣ Startup greeting sequence
        QTimer.singleShot(1000, self.show_greeting)
        
        # 2️⃣ Right-click menu for settings
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        self.show()
    
    def init_system_tray(self):
        """Initialize system tray icon and menu"""
        # Check if system tray is available
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("System tray not available")
            return
        
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set tray icon (use a simple icon or create one from existing GIF)
        try:
            # Try to use the idle GIF as icon
            if os.path.exists("assets/mocha_gifs/idle.gif"):
                movie = QMovie("assets/mocha_gifs/idle.gif")
                movie.jumpToFrame(0)  # Get first frame
                pixmap = movie.currentPixmap().scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.tray_icon.setIcon(QIcon(pixmap))
            else:
                # Fallback: create a simple icon
                pixmap = QPixmap(32, 32)
                pixmap.fill(Qt.transparent)
                self.tray_icon.setIcon(QIcon(pixmap))
        except:
            # If all else fails, use default icon
            self.tray_icon.setIcon(self.style().standardIcon(self.style().SP_ComputerIcon))
        
        # Set tooltip
        self.tray_icon.setToolTip("Milk Mocha Pet")
        
        # Create tray menu
        self.create_tray_menu()
        
        # Connect double-click to show/hide
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Show the tray icon
        self.tray_icon.show()
    
    def create_tray_menu(self):
        """Create the system tray context menu"""
        tray_menu = QMenu()
        
        # Show/Hide Pet
        self.show_hide_action = QAction("Hide Pet", self)
        self.show_hide_action.triggered.connect(self.toggle_visibility)
        tray_menu.addAction(self.show_hide_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Quick Actions submenu
        quick_actions_menu = tray_menu.addMenu("Quick Actions")
        
        quick_actions = [
            ("Dance", self.show_dancing),
            ("Laugh", self.show_laugh),
            ("Excited", self.show_excited),
            ("Heart Throw", self.show_heartthrow),
            ("Playing Guitar", self.show_playing),
            ("Greeting", self.show_greeting),
            ("Run Random", self.run_to_random_location),
            ("Sleep", self.show_sleeping)
        ]
        
        for name, action in quick_actions:
            quick_action = QAction(name, self)
            quick_action.triggered.connect(action)
            quick_actions_menu.addAction(quick_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Settings
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        tray_menu.addAction(settings_action)
        
        # About
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        tray_menu.addAction(about_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Exit
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(exit_action)
        
        # Set the menu
        self.tray_icon.setContextMenu(tray_menu)
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_visibility()
        elif reason == QSystemTrayIcon.Trigger:
            # Single click - show a notification
            self.tray_icon.showMessage(
                "Milk Mocha Pet",
                "Pet is active! Double-click to show/hide.",
                QSystemTrayIcon.Information,
                2000
            )
    
    def toggle_visibility(self):
        """Toggle pet visibility"""
        if self.isVisible():
            self.hide()
            self.show_hide_action.setText("Show Pet")
            self.tray_icon.showMessage(
                "Milk Mocha Pet",
                "Pet hidden. Access from system tray.",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            self.show()
            self.show_hide_action.setText("Hide Pet")
            self.tray_icon.showMessage(
                "Milk Mocha Pet",
                "Pet is now visible!",
                QSystemTrayIcon.Information,
                2000
            )
    
    def show_about(self):
        """Show about information"""
        self.tray_icon.showMessage(
            "About Milk Mocha Pet",
            "A cute desktop companion with animations and interactions!\n\nFeatures:\n• Draggable pet\n• Random animations\n• Feeding system\n• Settings control\n• System tray integration",
            QSystemTrayIcon.Information,
            5000
        )
    
    def setup_pet_animation(self):
        """Set up the pet GIF animation"""
        if os.path.exists(self.current_gif):
            self.movie = QMovie(self.current_gif)
            
            # Scale the movie to desired size
            gif_size = QSize(150, 150)
            self.movie.setScaledSize(gif_size)
            
            # Set up the label
            self.pet_label.setMovie(self.movie)
            self.pet_label.setFixedSize(gif_size)
            self.setFixedSize(gif_size)
            
            # Start the animation
            self.movie.start()
        else:
            print(f"GIF file not found: {self.current_gif}")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists("config/settings.json"):
                with open("config/settings.json", "r") as f:
                    return json.load(f)
        except:
            pass
        
        # Default config
        return {
            "spawn_interval": 10000,
            "transparency": 255,
            "last_position": [300, 300],
            "auto_spawn": True
        }
    
    def save_config(self):
        """Save current configuration"""
        try:
            os.makedirs("config", exist_ok=True)
            self.config_data["last_position"] = [self.x(), self.y()]
            with open("config/settings.json", "w") as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def change_gif(self, gif_path):
        """Change the current GIF animation"""
        if os.path.exists(gif_path):
            self.current_gif = gif_path
            self.movie.stop()
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(QSize(150, 150))
            self.pet_label.setMovie(self.movie)
            self.movie.start()
    
    # 2️⃣ Create a method to switch GIFs cleanly
    def switch_gif(self, gif_key, duration=None, revert_to="idle"):
        """Switch to a specific GIF animation with optional duration and revert"""
        # Cancel any existing animation timer
        if self.animation_timer:
            self.animation_timer.stop()
            self.animation_timer = None
        
        gif_path = self.gif_paths.get(gif_key, self.gif_paths["idle"])
        self.change_gif(gif_path)
        
        if duration:
            # Create new animation timer
            self.animation_timer = QTimer()
            self.animation_timer.setSingleShot(True)
            self.animation_timer.timeout.connect(lambda: self.switch_gif(revert_to))
            self.animation_timer.start(duration)
    
    def play_gif_loop(self, gif_key, loop_count=1):
        """Play a GIF for its natural duration with specified loop count"""
        gif_path = self.gif_paths.get(gif_key, self.gif_paths["idle"])
        self.change_gif(gif_path)
        # Let the GIF play naturally without forced timeout
        # Will need to manually call return_to_idle() or another animation
    
    # 🪄 Organized animation methods
    def show_idle(self):
        """Show idle animation (default state)"""
        self.switch_gif("idle")
    
    def show_drinking(self):
        """Show drinking animation for 10 seconds and return to idle"""
        self.last_interaction_time = time.time()
        print("🥛 Pet is drinking for 10 seconds!")
        
        # Play drinking animation continuously for 10 seconds
        self.switch_gif("drinking", duration=10000)  # 10 seconds of drinking
    
    def show_sleeping(self):
        """Show sleeping animation"""
        self.switch_gif("sleeping")
    
    def show_playing(self):
        """Show playing guitar animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("playing", duration=6000)  # Extended to 6 seconds
    
    def show_greeting(self):
        """Show greeting animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("greeting", duration=5000)  # Extended to 5 seconds
    
    def show_excited(self):
        """Show excited animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("excited", duration=5000)  # Extended to 5 seconds
    
    def show_laugh(self):
        """Show laughing animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("laugh", duration=5000)  # Extended to 5 seconds
    
    def show_heartthrow(self):
        """Show heart throw animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("heartthrow", duration=5000)  # Extended to 5 seconds
    
    def show_dancing(self):
        """Show dancing animation and return to idle"""
        self.last_interaction_time = time.time()
        dance_gif = random.choice(["dancing", "dancing2"])
        self.switch_gif(dance_gif, duration=8000)  # Extended to 8 seconds
    
    def show_crying(self):
        """Show crying animation"""
        self.switch_gif("crying", duration=6000)  # Extended to 6 seconds
    
    def show_doubtful(self):
        """Show doubtful animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("doubtful", duration=5000)  # Extended to 5 seconds
    
    def show_says_yes(self):
        """Show says yes animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("says_yes", duration=4000)  # Extended to 4 seconds
    
    # 🏃 Random running feature
    def start_random_running(self):
        """Start the random running timer"""
        self.running_timer = QTimer()
        self.running_timer.timeout.connect(self.run_to_random_location)
        self.running_timer.start(30000)  # Run every 30 seconds
    
    def run_to_random_location(self):
        """Run to a random location on screen"""
        # Get screen dimensions
        screen = QApplication.primaryScreen().availableGeometry()
        
        # Calculate random position (keeping pet within screen bounds)
        random_x = random.randint(0, screen.width() - self.width())
        random_y = random.randint(0, screen.height() - self.height())
        
        # Show running animation
        self.show_running(random_x, random_y)
    
    def show_running(self, target_x=None, target_y=None):
        """Show running animation and smoothly move to target location"""
        self.last_interaction_time = time.time()
        
        # Show running GIF (will loop until we stop it)
        self.switch_gif("running")
        
        # If target coordinates provided, animate smoothly to target
        if target_x is not None and target_y is not None:
            # Stop and cleanup any existing animation
            if hasattr(self, 'animation') and self.animation:
                try:
                    self.animation.finished.disconnect()
                    self.animation.stop()
                except:
                    pass  # Ignore if already disconnected
            
            # Create smooth animation to target position
            self.animation = QPropertyAnimation(self, b"pos")
            self.animation.setDuration(2000)  # 2 seconds for smooth movement
            self.animation.setStartValue(QPoint(self.x(), self.y()))
            self.animation.setEndValue(QPoint(target_x, target_y))
            self.animation.setEasingCurve(QEasingCurve.OutQuad)  # Smooth deceleration
            
            # When animation finishes, stop running and return to idle
            self.animation.finished.connect(self.finish_running)
            
            # Start the smooth animation
            self.animation.start()
            print(f"🏃 Pet running smoothly to ({target_x}, {target_y})")
        else:
            # If no target, just show running for a short time
            QTimer.singleShot(3000, self.finish_running)
    
    def finish_running(self):
        """Finish running animation and return to idle"""
        # Stop running animation and return to idle
        self.switch_gif("idle")
        
        # Save new position to config
        self.save_config()
        
        print("🏃 Pet finished running and returned to idle")
    
    # 🤖 Enhanced Gemini speaking system
    def start_smart_speaking_system(self):
        """Start the enhanced speaking system with user activity detection"""
        print(f"🤖 Starting smart speaking system (interval: {self.speaking_interval//60} minutes)")
        
        # Check for speaking opportunities every 2 minutes
        self.speaking_check_timer = QTimer()
        self.speaking_check_timer.timeout.connect(self.check_speaking_opportunity)
        self.speaking_check_timer.start(120000)  # Check every 2 minutes
        
        # Also schedule a greeting message for startup (shorter delay for testing)
        QTimer.singleShot(5000, self.send_startup_greeting)  # 5 seconds after startup
        
        # For testing - show a test bubble immediately
        QTimer.singleShot(2000, lambda: self.show_speech_bubble("🎯 Milk Mocha is ready! Press G for Gemini messages, T for test bubbles, B for basic Gemini, F for fallback! 💬"))
    
    def check_speaking_opportunity(self):
        """Check if it's a good time to speak based on user activity"""
        if not self.speaking_enabled:
            print("🔇 Speaking disabled")
            return
        
        # Check if enough time has passed since last message
        current_time = time.time()
        if self.last_message_time and (current_time - self.last_message_time) < self.speaking_interval:
            print(f"⏰ Too soon - last message was {current_time - self.last_message_time:.1f} seconds ago")
            return
        
        print("✅ Time for a message!")
        # Check if user should receive a message
        if self.user_activity.should_show_message(self.last_message_time, self.speaking_interval):
            self.request_contextual_message()
        else:
            print("🚫 User activity detector says not a good time")
    
    def send_startup_greeting(self):
        """Send a contextual greeting message on startup"""
        print("🚀 send_startup_greeting called")
        if not self.speaking_enabled:
            print("🔇 Speaking disabled, skipping startup greeting")
            return
        
        time_context = self.user_activity.get_time_context()
        context = "greetings" if time_context == "morning" else "random"
        print(f"🌅 Time context: {time_context}, using context: {context}")
        
        def get_greeting():
            print("🔄 Getting startup greeting in thread...")
            try:
                message = self.gemini_service.get_message(context)
                print(f"✅ Got startup greeting: {message}")
                self.show_speech_bubble(message)
                self.last_message_time = time.time()
                print("✅ Startup greeting displayed immediately")
            except Exception as e:
                print(f"❌ Error getting startup greeting: {e}")
                import traceback
                traceback.print_exc()
        
        thread = threading.Thread(target=get_greeting)
        thread.daemon = True
        thread.start()
        print("🧵 Startup greeting thread started")
    
    def request_contextual_message(self):
        """Request a contextual message based on user activity"""
        print("🎯 request_contextual_message called")
        
        def get_contextual_message():
            print("🔄 Getting contextual message in thread...")
            try:
                # Get user activity context
                activity_context = self.user_activity.get_contextual_activity()
                print(f"🎯 Requesting message for context: {activity_context}")
                
                # Get appropriate message
                message = self.gemini_service.get_contextual_message(activity_context)
                print(f"✅ Got contextual message: {message}")
                
                # Show message immediately
                self.show_speech_bubble(message)
                self.last_message_time = time.time()
                print("✅ Contextual message displayed immediately")
                
            except Exception as e:
                print(f"❌ Error getting contextual message: {e}")
                import traceback
                traceback.print_exc()
                # Fallback to simple message
                try:
                    fallback = self.gemini_service.handler.get_fallback_message("random")
                    print(f"🔄 Using fallback: {fallback}")
                    self.show_speech_bubble(fallback)
                    self.last_message_time = time.time()
                    print("✅ Fallback message displayed immediately")
                except Exception as e2:
                    print(f"❌ Even fallback failed: {e2}")
                    traceback.print_exc()
        
        thread = threading.Thread(target=get_contextual_message)
        thread.daemon = True
        thread.start()
        print("🧵 Contextual message thread started")
    
    def request_custom_message(self, custom_prompt: str, context: str = "random"):
        """Request a custom message with specific prompt"""
        print(f"🎨 request_custom_message called with prompt: {custom_prompt}")
        
        def get_custom_message():
            print("🔄 Getting custom message in thread...")
            try:
                message = self.gemini_service.get_message(context, custom_prompt)
                print(f"✅ Got custom message: {message}")
                self.show_speech_bubble(message)
                self.last_message_time = time.time()
                print("✅ Custom message displayed immediately")
            except Exception as e:
                print(f"❌ Error getting custom message: {e}")
                import traceback
                traceback.print_exc()
                try:
                    fallback = self.gemini_service.handler.get_fallback_message(context)
                    print(f"🔄 Using fallback for custom: {fallback}")
                    self.show_speech_bubble(fallback)
                    print("✅ Custom fallback displayed immediately")
                except Exception as e2:
                    print(f"❌ Custom fallback failed: {e2}")
        
        thread = threading.Thread(target=get_custom_message)
        thread.daemon = True
        thread.start()
        print("🧵 Custom message thread started")
    
    def show_speech_bubble(self, message):
        """6️⃣ Display speech bubble with message above Milk Mocha"""
        print(f"💬 show_speech_bubble called with: {message}")
        print(f"💬 Creating speech bubble: {message}")
        
        # Hide existing speech bubble if any
        if self.speech_bubble:
            try:
                print("   Hiding existing speech bubble...")
                # Stop any existing bubble timer
                if hasattr(self, 'bubble_timer') and self.bubble_timer:
                    self.bubble_timer.stop()
                    self.bubble_timer = None
                # Stop bubble following timer
                if hasattr(self, 'bubble_follow_timer') and self.bubble_follow_timer:
                    self.bubble_follow_timer.stop()
                    self.bubble_follow_timer = None
                self.speech_bubble.hide()
                self.speech_bubble.deleteLater()
            except RuntimeError:
                # Object already deleted
                print("   Previous speech bubble already deleted")
            finally:
                self.speech_bubble = None
        
        # Create new speech bubble with this pet as parent for communication
        self.speech_bubble = SpeechBubble(message, self)
        print(f"   Speech bubble created successfully")
        
        # Position the bubble initially
        self.position_speech_bubble()
        print(f"   Speech bubble positioned")
        
        self.speech_bubble.show()
        self.speech_bubble.raise_()  # Bring to front
        print(f"   Speech bubble shown and raised")
        
        # Start bubble following timer (update position every 50ms for smooth following)
        self.bubble_follow_timer = QTimer()
        self.bubble_follow_timer.timeout.connect(self.position_speech_bubble)
        self.bubble_follow_timer.start(50)  # 20 FPS for smooth following
        print(f"   Following timer started")
        
        # Auto-hide after 15 seconds
        self.bubble_timer = QTimer()
        self.bubble_timer.setSingleShot(True)
        self.bubble_timer.timeout.connect(self.hide_speech_bubble)
        self.bubble_timer.start(15000)
        print(f"   Auto-hide timer started")
        
        print("✅ Speech bubble displayed and following enabled!")
    
    def position_speech_bubble(self):
        """Position the speech bubble relative to the pet"""
        if not self.speech_bubble or self.speech_bubble.isHidden():
            return
        
        try:
            # Get screen dimensions
            screen = QApplication.primaryScreen().availableGeometry()
            
            # Calculate bubble position - above and centered on pet
            pet_center_x = self.x() + self.width() // 2
            pet_top_y = self.y()
            
            bubble_x = pet_center_x - self.speech_bubble.width() // 2
            bubble_y = pet_top_y - self.speech_bubble.height() - 20  # 20px gap above pet
            
            # Keep bubble within screen bounds with safe margins
            bubble_x = max(10, min(bubble_x, screen.width() - self.speech_bubble.width() - 10))
            bubble_y = max(10, min(bubble_y, screen.height() - self.speech_bubble.height() - 10))
            
            # If bubble would be above screen, put it below pet instead
            if bubble_y < 10:
                bubble_y = self.y() + self.height() + 20
            
            # Move bubble to new position
            self.speech_bubble.move(bubble_x, bubble_y)
            
        except RuntimeError:
            # Bubble was deleted, stop following
            if hasattr(self, 'bubble_follow_timer') and self.bubble_follow_timer:
                self.bubble_follow_timer.stop()
                self.bubble_follow_timer = None
            self.speech_bubble = None
    
    def hide_speech_bubble(self):
        """Hide the speech bubble safely"""
        if self.speech_bubble and not self.speech_bubble.isHidden():
            try:
                print("💬 Auto-hiding speech bubble after 15 seconds")
                # Stop timers first
                if hasattr(self, 'bubble_timer') and self.bubble_timer:
                    self.bubble_timer.stop()
                    self.bubble_timer = None
                if hasattr(self, 'bubble_follow_timer') and self.bubble_follow_timer:
                    self.bubble_follow_timer.stop()
                    self.bubble_follow_timer = None
                # Hide and delete
                self.speech_bubble.hide()
                self.speech_bubble.deleteLater()
                self.speech_bubble = None
            except RuntimeError:
                # Object already deleted
                print("💬 Speech bubble already deleted")
                self.speech_bubble = None
        else:
            print("💬 No speech bubble to hide or already hidden")
    
    # 🎭 Random action feature
    def start_random_actions(self):
        """Start the random action timer"""
        if self.auto_spawn:  # Only if auto_spawn is enabled
            self.action_timer = QTimer()
            self.action_timer.timeout.connect(self.perform_random_action)
            self.action_timer.start(45000)  # Random action every 45 seconds
    
    def perform_random_action(self):
        """Perform a random action animation"""
        # Only perform random actions if currently idle
        if self.current_gif == self.gif_paths["idle"]:
            random_actions = [
                self.show_dancing,
                self.show_laugh,
                self.show_excited,
                self.show_heartthrow,
                self.show_playing,
                self.show_greeting,
                self.show_says_yes,
                self.show_doubtful
            ]
            
            # Pick a random action
            action = random.choice(random_actions)
            action()
            print(f"🎭 Pet performed random action: {action.__name__}")
    
    # 4️⃣ Updated feeding method
    def feed_pet(self):
        """Switch to drinking animation, then return to idle"""
        self.show_drinking()
    
    def return_to_idle(self):
        """Return to idle animation"""
        self.show_idle()
    
    # 5️⃣ Inactivity auto sleep
    def check_inactivity(self):
        """Check for inactivity and switch to sleeping if idle too long"""
        idle_time = time.time() - self.last_interaction_time
        if idle_time > 60:  # 1 minute of inactivity
            self.show_sleeping()
        elif idle_time > 300:  # 5 minutes - show crying
            self.show_crying()
        QTimer.singleShot(5000, self.check_inactivity)  # Check every 5 seconds
    
    # 6️⃣ & 7️⃣ Click handlers with random reactions
    def handle_click(self, event):
        """Handle left clicks with random reactions and spam protection"""
        self.click_count += 1
        self.last_interaction_time = time.time()
        
        if self.click_count >= 10:
            self.switch_gif("angry", duration=5000)  # Extended to 5 seconds
            self.click_count = 0
        else:
            # Random reaction on click
            reactions = [self.show_excited, self.show_laugh, self.show_heartthrow]
            random.choice(reactions)()
    
    def pet_pet(self, event):
        """Handle right clicks to pet with heart throw"""
        self.last_interaction_time = time.time()
        self.show_heartthrow()
    
    # 2️⃣ Context menu for settings
    def show_context_menu(self, position):
        """Show right-click context menu"""
        context_menu = QMenu(self)
        
        # Settings option
        settings_action = context_menu.addAction("Settings")
        settings_action.triggered.connect(self.open_settings)
        
        # Force Animation submenu
        force_menu = context_menu.addMenu("Force Animation")
        
        # Add animation options
        animations = [
            ("Dance", self.show_dancing),
            ("Laugh", self.show_laugh),
            ("Excited", self.show_excited),
            ("Heart Throw", self.show_heartthrow),
            ("Playing Guitar", self.show_playing),
            ("Greeting", self.show_greeting),
            ("Says Yes", self.show_says_yes),
            ("Crying", self.show_crying),
            ("Doubtful", self.show_doubtful),
            ("Run Random", self.run_to_random_location),
            ("Sleep", self.show_sleeping)
        ]
        
        for name, action in animations:
            anim_action = force_menu.addAction(name)
            anim_action.triggered.connect(action)
        
        # Separator
        context_menu.addSeparator()
        
        # Exit option
        quit_action = context_menu.addAction("Exit")
        quit_action.triggered.connect(self.quit_application)
        
        context_menu.exec_(self.mapToGlobal(position))
    
    def quit_application(self):
        """Completely quit the application"""
        print("🚪 Exiting Milk Mocha Pet...")
        
        # Hide system tray icon
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        
        # Save current state before quitting
        self.save_config()
        
        # Close all active bottles
        for bottle in self.active_bottles[:]:
            bottle.close()
        
        # Stop all timers
        if hasattr(self, 'running_timer'):
            self.running_timer.stop()
        if hasattr(self, 'spawn_timer'):
            self.spawn_timer.stop()
        if hasattr(self, 'action_timer'):
            self.action_timer.stop()
        if hasattr(self, 'speaking_check_timer'):
            self.speaking_check_timer.stop()
        if hasattr(self, 'animation_timer') and self.animation_timer:
            self.animation_timer.stop()
        if hasattr(self, 'bubble_timer') and self.bubble_timer:
            self.bubble_timer.stop()
        if hasattr(self, 'bubble_follow_timer') and self.bubble_follow_timer:
            self.bubble_follow_timer.stop()
        
        # Stop animations
        if hasattr(self, 'animation') and self.animation:
            try:
                self.animation.finished.disconnect()
                self.animation.stop()
            except:
                pass
        
        # Stop movie
        if hasattr(self, 'movie'):
            self.movie.stop()
        
        # Close settings window if open
        if self.settings_window and self.settings_window.isVisible():
            self.settings_window.close()
        
        # Hide speech bubble if showing
        if self.speech_bubble:
            try:
                self.speech_bubble.hide()
                self.speech_bubble.deleteLater()
            except RuntimeError:
                # Already deleted
                pass
            finally:
                self.speech_bubble = None
        
        # Force application to quit completely
        QApplication.quit()
        import sys
        sys.exit(0)
    
    # 8️⃣ Keyboard event handler for dance mode
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key_Space:
            self.show_dancing()
        elif event.key() == Qt.Key_S:
            self.open_settings()  # 3️⃣ Open settings with S key
        elif event.key() == Qt.Key_P:
            self.show_playing()  # P key for playing guitar
        elif event.key() == Qt.Key_Y:
            self.show_says_yes()  # Y key for yes reaction
        elif event.key() == Qt.Key_R:
            self.run_to_random_location()  # R key for manual running
        elif event.key() == Qt.Key_H:
            self.toggle_visibility()  # H key to hide/show
        elif event.key() == Qt.Key_T:
            # T key for testing speech bubble
            test_message = f"🧪 Test bubble at {time.strftime('%H:%M:%S')}! Press T again for more tests! 💬"
            self.show_speech_bubble(test_message)
        elif event.key() == Qt.Key_G:
            # G key for Gemini message test
            print("🤖 Manually requesting contextual message...")
            self.request_contextual_message()
        elif event.key() == Qt.Key_B:
            # B key for basic Gemini message test
            print("🤖 Manually requesting basic Gemini message...")
            self.request_custom_message("Say hello in a cute way", "greetings")
        elif event.key() == Qt.Key_F:
            # F key for fallback message test
            print("🔄 Testing fallback message...")
            fallback = self.gemini_service.handler.get_fallback_message("random")
            self.show_speech_bubble(fallback)
        elif event.key() == Qt.Key_D:
            # D key for detailed Gemini debug
            print("🔍 Running detailed Gemini debug...")
            self.debug_gemini_api()
        elif event.key() == Qt.Key_Escape:
            self.quit_application()  # ESC key to quit
        super().keyPressEvent(event)
    
    # 1️⃣ Settings management methods
    def restart_app(self):
        """Restart the application"""
        import subprocess
        subprocess.Popen([sys.executable] + sys.argv)
        QApplication.quit()
    
    def open_settings(self):
        """3️⃣ Open settings window"""
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsWindow()
            self.settings_window.restart_requested.connect(self.restart_app)
            self.settings_window.show()
        else:
            self.settings_window.raise_()
            self.settings_window.activateWindow()
    
    def spawn_milk_bottle(self):
        """Spawn a milk bottle if none exists"""
        if not self.active_bottles:
            print("🍼 Spawning milk bottle!")  # Debug message
            bottle = MilkBottle(self)
            self.active_bottles.append(bottle)
        
        # Note: Timer automatically restarts because it's a repeating timer
        # No need to manually restart it here
    
    def remove_bottle(self, bottle):
        """Remove bottle from active list"""
        if bottle in self.active_bottles:
            self.active_bottles.remove(bottle)
    
    def get_position_bbox(self):
        """Get bounding box for collision detection"""
        return (self.x(), self.y(), self.x() + self.width(), self.y() + self.height())
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging and interactions"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            self.handle_click(event)  # 7️⃣ Handle click counting
        elif event.button() == Qt.RightButton:
            self.pet_pet(event)  # 6️⃣ Right-click to pet
    
    def mouseDoubleClickEvent(self, event):
        """Handle double-click for greeting"""
        if event.button() == Qt.LeftButton:
            self.show_greeting()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_start_position:
            self.last_interaction_time = time.time()  # 5️⃣ Reset inactivity timer
            new_pos = event.globalPos() - self.drag_start_position
            
            # Keep within screen bounds
            screen = QApplication.primaryScreen().availableGeometry()
            new_x = max(0, min(new_pos.x(), screen.width() - self.width()))
            new_y = max(0, min(new_pos.y(), screen.height() - self.height()))
            
            self.move(new_x, new_y)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = None
            self.save_config()
    
    def closeEvent(self, event):
        """Handle window close event"""
        # If system tray is available, minimize to tray instead of closing
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            event.ignore()
            self.hide()
            self.show_hide_action.setText("Show Pet")
            self.tray_icon.showMessage(
                "Milk Mocha Pet",
                "Pet minimized to system tray. Double-click tray icon to restore.",
                QSystemTrayIcon.Information,
                3000
            )
        else:
            # If no tray, quit normally
            self.quit_application()
            super().closeEvent(event)


class SpeechBubble(QWidget):
    """6️⃣ Speech bubble widget for displaying Gemini messages"""
    
    def __init__(self, message, pet_parent=None):
        super().__init__(None)  # No Qt parent for independent window
        self.message = message
        self.pet_parent = pet_parent  # Reference to MilkMochaPet for communication
        
        # Set up window properties for better visibility
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Create label for text
        self.label = QLabel(self)
        self.label.setText(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Enhanced styling for better visibility
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 250);
                border: 3px solid #4CAF50;
                border-radius: 20px;
                padding: 15px;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #000;
                font-weight: bold;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 100);
            }
        """)
        
        # Calculate size based on text with better sizing
        font_metrics = self.label.fontMetrics()
        text_width = font_metrics.boundingRect(message).width()
        
        # Set bubble size (increased for better visibility)
        bubble_width = min(max(text_width + 60, 200), 300)
        bubble_height = 80
        
        # Calculate required height for wrapped text
        text_rect = font_metrics.boundingRect(0, 0, bubble_width - 40, 1000, Qt.TextWordWrap, message)
        required_height = max(text_rect.height() + 50, bubble_height)
        
        self.setFixedSize(bubble_width, required_height)
        self.label.setFixedSize(bubble_width, required_height)
        
        # Make widget focusable and ensure it's visible
        self.setFocusPolicy(Qt.NoFocus)
        self.setWindowOpacity(1.0)
        
        # Add fade-in animation
        self.fade_in()
    
    def fade_in(self):
        """Animate fade-in effect"""
        self.setWindowOpacity(0.0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(800)  # Slower for better visibility
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.fade_animation.start()
    
    def mousePressEvent(self, event):
        """Hide bubble when clicked - notify parent to handle safely"""
        if event.button() == Qt.LeftButton:
            print("💬 Speech bubble clicked - requesting hide...")
            # Let the parent handle the hiding to avoid conflicts
            if self.pet_parent:
                self.pet_parent.hide_speech_bubble()
            else:
                # Fallback if no parent
                try:
                    self.hide()
                    self.deleteLater()
                except RuntimeError:
                    pass


class MilkBottle(QWidget):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        
        # Set up window properties for transparency
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Initialize variables
        self.drag_start_position = None
        
        # Create the bottle label
        self.bottle_label = QLabel(self)
        self.bottle_label.setAlignment(Qt.AlignCenter)
        
        # Set up the bottle animation
        self.setup_bottle_animation()
        
        # Set initial position
        self.move(300, 300)
        
        # Start collision checking
        self.collision_timer = QTimer()
        self.collision_timer.timeout.connect(self.check_collision)
        self.collision_timer.start(100)  # Check every 100ms
        
        self.show()
    
    def setup_bottle_animation(self):
        """Set up the bottle GIF animation"""
        gif_path = "assets/food_gifs/milk_bottle.gif"
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            
            # Scale the movie to desired size
            bottle_size = QSize(50, 50)
            self.movie.setScaledSize(bottle_size)
            
            # Set up the label
            self.bottle_label.setMovie(self.movie)
            self.bottle_label.setFixedSize(bottle_size)
            self.setFixedSize(bottle_size)
            
            # Start the animation
            self.movie.start()
        else:
            print(f"Bottle GIF not found: {gif_path}")
    
    def get_position_bbox(self):
        """Get bounding box for collision detection"""
        return (self.x(), self.y(), self.x() + self.width(), self.y() + self.height())
    
    def check_collision(self):
        """Check for collision with pet"""
        bottle_box = self.get_position_bbox()
        pet_box = self.pet.get_position_bbox()
        
        if (bottle_box[0] < pet_box[2] and
            bottle_box[2] > pet_box[0] and
            bottle_box[1] < pet_box[3] and
            bottle_box[3] > pet_box[1]):
            # Collision detected
            self.pet.feed_pet()
            self.pet.remove_bottle(self)
            self.close()
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            # Trigger excited animation when bottle is clicked
            self.pet.show_excited()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_start_position:
            new_pos = event.globalPos() - self.drag_start_position
            
            # Keep within screen bounds
            screen = QApplication.primaryScreen().availableGeometry()
            new_x = max(0, min(new_pos.x(), screen.width() - self.width()))
            new_y = max(0, min(new_pos.y(), screen.height() - self.height()))
            
            self.move(new_x, new_y)
            
            # Trigger excited animation when bottle is being dragged
            if not hasattr(self, '_drag_excited_triggered'):
                self.pet.show_excited()
                self._drag_excited_triggered = True
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = None
            # Reset drag excited trigger
            if hasattr(self, '_drag_excited_triggered'):
                delattr(self, '_drag_excited_triggered')
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop collision timer
        if hasattr(self, 'collision_timer'):
            self.collision_timer.stop()
        
        # Stop movie
        if hasattr(self, 'movie'):
            self.movie.stop()
        
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show the pet
    pet = MilkMochaPet()
    
    # Run the application
    sys.exit(app.exec_())
