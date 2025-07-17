import sys
import os
import json
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QSize

class MilkMochaPet(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up window properties for transparency
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Initialize variables
        self.current_gif = "assets/mocha_gifs/idle.gif"
        self.drag_start_position = None
        self.active_bottles = []
        
        # Load config
        self.config_data = self.load_config()
        
        # Create the main label for the pet
        self.pet_label = QLabel(self)
        self.pet_label.setAlignment(Qt.AlignCenter)
        
        # Load and set up the GIF
        self.setup_pet_animation()
        
        # Set position from config
        last_pos = self.config_data.get("last_position", [300, 300])
        self.move(last_pos[0], last_pos[1])
        
        # Set transparency
        transparency = self.config_data.get("transparency", 255)
        self.setWindowOpacity(transparency / 255.0)
        
        # Set up timers
        self.spawn_interval = self.config_data.get("spawn_interval", 10000)
        self.auto_spawn = self.config_data.get("auto_spawn", True)
        
        if self.auto_spawn:
            self.spawn_timer = QTimer()
            self.spawn_timer.timeout.connect(self.spawn_milk_bottle)
            self.spawn_timer.start(self.spawn_interval)
        
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
    
    def feed_pet(self):
        """Switch to drinking animation temporarily"""
        self.change_gif("assets/mocha_gifs/drinking.gif")
        QTimer.singleShot(5000, self.return_to_idle)
    
    def return_to_idle(self):
        """Return to idle animation"""
        self.change_gif("assets/mocha_gifs/idle.gif")
    
    def spawn_milk_bottle(self):
        """Spawn a milk bottle if none exists"""
        if not self.active_bottles:
            bottle = MilkBottle(self)
            self.active_bottles.append(bottle)
    
    def remove_bottle(self, bottle):
        """Remove bottle from active list"""
        if bottle in self.active_bottles:
            self.active_bottles.remove(bottle)
    
    def get_position_bbox(self):
        """Get bounding box for collision detection"""
        return (self.x(), self.y(), self.x() + self.width(), self.y() + self.height())
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_start_position:
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
        self.save_config()
        
        # Clean up bottles
        for bottle in self.active_bottles[:]:
            bottle.close()
        
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
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_start_position:
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
