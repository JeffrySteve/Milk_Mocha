"""
Main Milk Mocha Pet class - refactored and modular
"""
import sys
import time
import threading
from PyQt5.QtWidgets import QWidget, QLabel, QMenu, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve

# Import our modular components
from utils.config import ConfigManager
from animation.gif_manager import GifManager
from ui.speech_bubble import SpeechBubble
from ui.milk_bottle import MilkBottle
from ui.system_tray import SystemTrayManager
from core.pet_behavior import PetBehavior

# Import existing modules
from settings import SettingsWindow
from modules.gemini_handler import GeminiService
from modules.user_activity import UserActivityDetector


class MilkMochaPet(QWidget):
    """Main Milk Mocha Pet widget - now modular and organized"""
    
    def __init__(self):
        super().__init__()
        
        # Set up window properties for transparency
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Make widget focusable for keyboard events
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Initialize core systems
        self.config = ConfigManager()
        self.gif_manager = GifManager(self)
        
        # Initialize variables
        self.drag_start_position = None
        self.active_bottles = []
        self.animation = None  # Track current position animation
        self.speech_bubble = None  # Track speech bubble
        self.bubble_timer = None  # Track bubble auto-hide timer
        self.bubble_follow_timer = None  # Track bubble following timer
        
        # Initialize services
        self.gemini_service = GeminiService()
        self.user_activity = UserActivityDetector()
        self.last_message_time = None
        
        # Initialize settings window reference
        self.settings_window = None
        
        # Create the main label for the pet
        self.pet_label = QLabel(self)
        self.pet_label.setAlignment(Qt.AlignCenter)
        
        # Set up the pet animation using gif manager
        self.gif_manager.setup_pet_animation(self.pet_label)
        
        # Apply settings from config
        self.apply_config_settings()
        
        # Initialize UI components
        self.system_tray = SystemTrayManager(self)
        
        # Initialize behavior system
        self.behavior = PetBehavior(self)
        
        # Set up context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Start bottle spawning if enabled
        if self.config.get("auto_spawn", True):
            self.spawn_timer = QTimer()
            self.spawn_timer.timeout.connect(self.spawn_milk_bottle)
            self.spawn_timer.start(self.config.get("spawn_interval", 10000))
        
        # 3️⃣ Startup greeting sequence
        QTimer.singleShot(1000, self.show_greeting)
        
        self.show()
    
    def apply_config_settings(self):
        """Apply settings from configuration"""
        # Set position from config
        last_pos = self.config.get("last_position", [300, 300])
        self.move(last_pos[0], last_pos[1])
        
        # Set transparency (with minimum limit)
        transparency = self.config.get("transparency", 255)
        transparency = max(100, min(255, transparency))  # Ensure range 100-255
        self.setWindowOpacity(transparency / 255.0)
    
    def debug_gemini_api(self):
        """Debug function for testing Gemini API"""
        print("🔍 Running detailed Gemini debug...")
        
        def debug_api():
            try:
                # Test basic connection
                print("Testing basic Gemini connection...")
                test_message = self.gemini_service.get_message("random", "Say 'Debug test successful!'")
                print(f"✅ Debug test result: {test_message}")
                
                # Show result
                self.show_speech_bubble(f"🔍 Debug: {test_message}")
                
            except Exception as e:
                print(f"❌ Debug test failed: {e}")
                import traceback
                traceback.print_exc()
                self.show_speech_bubble(f"🔍 Debug failed: {str(e)}")
        
        thread = threading.Thread(target=debug_api)
        thread.daemon = True
        thread.start()
    
    # Animation methods that delegate to gif_manager
    def show_idle(self):
        """Show idle animation (default state)"""
        self.gif_manager.switch_gif("idle", self.pet_label)
    
    def show_drinking(self):
        """Show drinking animation for 10 seconds and return to idle"""
        self._update_interaction_time()
        print("🥛 Pet is drinking for 10 seconds!")
        self.gif_manager.switch_gif("drinking", self.pet_label, duration=10000)
    
    def show_sleeping(self):
        """Show sleeping animation"""
        self.gif_manager.switch_gif("sleeping", self.pet_label)
    
    def show_playing(self):
        """Show playing guitar animation and return to idle"""
        self._update_interaction_time()
        self.gif_manager.switch_gif("playing", self.pet_label, duration=6000)
    
    def show_greeting(self):
        """Show greeting animation and return to idle"""
        self._update_interaction_time()
        self.gif_manager.switch_gif("greeting", self.pet_label, duration=5000)
    
    def show_excited(self):
        """Show excited animation and return to idle"""
        self._update_interaction_time()
        self.gif_manager.switch_gif("excited", self.pet_label, duration=5000)
    
    def show_laugh(self):
        """Show laughing animation and return to idle"""
        self._update_interaction_time()
        self.gif_manager.switch_gif("laugh", self.pet_label, duration=5000)
    
    def show_heartthrow(self):
        """Show heart throw animation and return to idle"""
        self._update_interaction_time()
        self.gif_manager.switch_gif("heartthrow", self.pet_label, duration=5000)
    
    def show_dancing(self):
        """Show dancing animation and return to idle"""
        self._update_interaction_time()
        import random
        dance_gif = random.choice(["dancing", "dancing2"])
        self.gif_manager.switch_gif(dance_gif, self.pet_label, duration=8000)
    
    def show_crying(self):
        """Show crying animation"""
        self.gif_manager.switch_gif("crying", self.pet_label, duration=6000)
    
    def show_doubtful(self):
        """Show doubtful animation and return to idle"""
        self._update_interaction_time()
        self.gif_manager.switch_gif("doubtful", self.pet_label, duration=5000)
    
    def show_says_yes(self):
        """Show says yes animation and return to idle"""
        self._update_interaction_time()
        self.gif_manager.switch_gif("says_yes", self.pet_label, duration=4000)
    
    def show_angry(self):
        """Show angry animation and return to idle"""
        self._update_interaction_time()
        self.gif_manager.switch_gif("angry", self.pet_label, duration=5000)
    
    # Delegate behavior methods to behavior manager
    def run_to_random_location(self):
        """Run to a random location on screen"""
        self.behavior.run_to_random_location()
    
    def request_contextual_message(self):
        """Request a contextual message based on user activity"""
        self.behavior.request_contextual_message()
    
    def request_custom_message(self, custom_prompt: str, context: str = "random"):
        """Request a custom message with specific prompt"""
        self.behavior.request_custom_message(custom_prompt, context)
    
    def show_speech_bubble(self, message):
        """Display speech bubble with message above Milk Mocha"""
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
    
    def _update_interaction_time(self):
        """Safely update interaction time"""
        if hasattr(self, 'behavior') and self.behavior:
            self.behavior.update_interaction_time()
    
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
    
    def feed_pet(self):
        """Switch to drinking animation, then return to idle"""
        self.show_drinking()
    
    def spawn_milk_bottle(self):
        """Spawn a milk bottle if none exists"""
        if not self.active_bottles:
            print("🍼 Spawning milk bottle!")  # Debug message
            bottle = MilkBottle(self)
            self.active_bottles.append(bottle)
    
    def remove_bottle(self, bottle):
        """Remove bottle from active list"""
        if bottle in self.active_bottles:
            self.active_bottles.remove(bottle)
    
    def get_position_bbox(self):
        """Get bounding box for collision detection"""
        return (self.x(), self.y(), self.x() + self.width(), self.y() + self.height())
    
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key_Space:
            self.show_dancing()
        elif event.key() == Qt.Key_S:
            self.open_settings()
        elif event.key() == Qt.Key_P:
            self.show_playing()
        elif event.key() == Qt.Key_Y:
            self.show_says_yes()
        elif event.key() == Qt.Key_R:
            self.run_to_random_location()
        elif event.key() == Qt.Key_H:
            self.system_tray.toggle_visibility()
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
            self.debug_gemini_api()
        elif event.key() == Qt.Key_Escape:
            self.quit_application()
        super().keyPressEvent(event)
    
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
    
    def open_settings(self):
        """Open settings window"""
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsWindow()
            self.settings_window.restart_requested.connect(self.restart_app)
            self.settings_window.show()
        else:
            self.settings_window.raise_()
            self.settings_window.activateWindow()
    
    def restart_app(self):
        """Restart the application"""
        import subprocess
        subprocess.Popen([sys.executable] + sys.argv)
        QApplication.quit()
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging and interactions"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            self.behavior.handle_click(event)
        elif event.button() == Qt.RightButton:
            self.behavior.pet_pet(event)
    
    def mouseDoubleClickEvent(self, event):
        """Handle double-click for greeting"""
        if event.button() == Qt.LeftButton:
            self.show_greeting()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_start_position:
            self._update_interaction_time()
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
            self.config.update_position(self.x(), self.y())
    
    def closeEvent(self, event):
        """Handle window close event"""
        # If system tray is available, minimize to tray instead of closing
        if hasattr(self, 'system_tray') and self.system_tray.tray_icon and self.system_tray.tray_icon.isVisible():
            event.ignore()
            self.hide()
            self.system_tray.show_hide_action.setText("Show Pet")
            self.system_tray.tray_icon.showMessage(
                "Milk Mocha Pet",
                "Pet minimized to system tray. Double-click tray icon to restore.",
                self.system_tray.tray_icon.Information,
                3000
            )
        else:
            # If no tray, quit normally
            self.quit_application()
            super().closeEvent(event)
    
    def quit_application(self):
        """Completely quit the application"""
        print("🚪 Exiting Milk Mocha Pet...")
        
        # Hide system tray icon
        if hasattr(self, 'system_tray'):
            self.system_tray.hide()
        
        # Save current state before quitting
        self.config.update_position(self.x(), self.y())
        
        # Close all active bottles
        for bottle in self.active_bottles[:]:
            bottle.close()
        
        # Stop all timers and cleanup
        if hasattr(self, 'behavior'):
            self.behavior.stop_timers()
        
        if hasattr(self, 'gif_manager'):
            self.gif_manager.stop_timers()
        
        if hasattr(self, 'spawn_timer'):
            self.spawn_timer.stop()
        
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
