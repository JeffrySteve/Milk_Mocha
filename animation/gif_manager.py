"""
GIF and animation management for Milk Mocha Pet
"""
import os
import random
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QSize, QTimer


class GifManager:
    """Manages GIF animations and transitions"""
    
    def __init__(self, pet_widget):
        self.pet_widget = pet_widget
        self.current_gif = "assets/mocha_gifs/idle.gif"
        self.animation_timer = None
        
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
    
    def setup_pet_animation(self, pet_label):
        """Set up the pet GIF animation"""
        if os.path.exists(self.current_gif):
            self.movie = QMovie(self.current_gif)
            
            # Scale the movie to desired size
            gif_size = QSize(150, 150)
            self.movie.setScaledSize(gif_size)
            
            # Set up the label
            pet_label.setMovie(self.movie)
            pet_label.setFixedSize(gif_size)
            self.pet_widget.setFixedSize(gif_size)
            
            # Start the animation
            self.movie.start()
        else:
            print(f"GIF file not found: {self.current_gif}")
    
    def change_gif(self, gif_path, pet_label):
        """Change the current GIF animation"""
        if os.path.exists(gif_path):
            self.current_gif = gif_path
            self.movie.stop()
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(QSize(150, 150))
            pet_label.setMovie(self.movie)
            self.movie.start()
    
    def switch_gif(self, gif_key, pet_label, duration=None, revert_to="idle"):
        """Switch to a specific GIF animation with optional duration and revert"""
        # Cancel any existing animation timer
        if self.animation_timer:
            self.animation_timer.stop()
            self.animation_timer = None
        
        gif_path = self.gif_paths.get(gif_key, self.gif_paths["idle"])
        self.change_gif(gif_path, pet_label)
        
        if duration:
            # Create new animation timer
            self.animation_timer = QTimer()
            self.animation_timer.setSingleShot(True)
            self.animation_timer.timeout.connect(lambda: self.switch_gif(revert_to, pet_label))
            self.animation_timer.start(duration)
    
    def get_random_action(self):
        """Get a random action animation name"""
        actions = [
            "dancing", "laugh", "excited", "heartthrow", 
            "playing", "greeting", "says_yes", "doubtful"
        ]
        return random.choice(actions)
    
    def stop_timers(self):
        """Stop all animation timers"""
        if self.animation_timer:
            self.animation_timer.stop()
            self.animation_timer = None
        
        if hasattr(self, 'movie'):
            self.movie.stop()
