"""
Milk bottle UI component for feeding the pet
"""
import os
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QSize, QTimer


class MilkBottle(QWidget):
    """Interactive milk bottle widget"""
    
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
