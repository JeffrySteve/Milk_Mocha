import sys
import os
import json
import random
import time
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QSize
from settings import SettingsWindow

class MilkMochaPet(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up window properties for transparency
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Make widget focusable for keyboard events
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Initialize variables
        self.current_gif = "assets/mocha_gifs/idle.gif"
        self.drag_start_position = None
        self.active_bottles = []
        
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
        
        # Load config
        self.config_data = self.load_config()
        
        # 2️⃣ Apply loaded settings
        self.spawn_interval = self.config_data["spawn_interval"]
        self.auto_spawn = self.config_data["auto_spawn"]
        
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
        
        # 3️⃣ Startup greeting sequence
        QTimer.singleShot(1000, self.show_greeting)
        
        # 2️⃣ Right-click menu for settings
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        self.show()
    
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
        gif_path = self.gif_paths.get(gif_key, self.gif_paths["idle"])
        self.change_gif(gif_path)
        if duration:
            QTimer.singleShot(duration, lambda: self.switch_gif(revert_to))
    
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
        self.switch_gif("playing", duration=4000)
    
    def show_greeting(self):
        """Show greeting animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("greeting", duration=3000)
    
    def show_excited(self):
        """Show excited animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("excited", duration=3000)
    
    def show_laugh(self):
        """Show laughing animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("laugh", duration=3000)
    
    def show_heartthrow(self):
        """Show heart throw animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("heartthrow", duration=3000)
    
    def show_dancing(self):
        """Show dancing animation and return to idle"""
        self.last_interaction_time = time.time()
        dance_gif = random.choice(["dancing", "dancing2"])
        self.switch_gif(dance_gif, duration=5000)
    
    def show_crying(self):
        """Show crying animation"""
        self.switch_gif("crying", duration=4000)
    
    def show_doubtful(self):
        """Show doubtful animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("doubtful", duration=3000)
    
    def show_says_yes(self):
        """Show says yes animation and return to idle"""
        self.last_interaction_time = time.time()
        self.switch_gif("says_yes", duration=2000)
    
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
            self.switch_gif("angry", duration=3000)
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
        
        settings_action = context_menu.addAction("Settings")
        settings_action.triggered.connect(self.open_settings)
        
        quit_action = context_menu.addAction("Quit")
        quit_action.triggered.connect(self.close)
        
        context_menu.exec_(self.mapToGlobal(position))
    
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
        # Save window position
        self.config_data["last_position"] = [self.x(), self.y()]
        self.save_config()
        
        # Clean up bottles
        for bottle in self.active_bottles[:]:
            bottle.close()
        
        # Stop timers
        if hasattr(self, 'running_timer'):
            self.running_timer.stop()
        if hasattr(self, 'spawn_timer'):
            self.spawn_timer.stop()
        
        # Stop animations
        if hasattr(self, 'animation') and self.animation:
            try:
                self.animation.finished.disconnect()
                self.animation.stop()
            except:
                pass  # Ignore if already disconnected
        
        # Stop movie
        if hasattr(self, 'movie'):
            self.movie.stop()
        
        super().closeEvent(event)


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
