import tkinter as tk
import sys
from settings import SettingsWindow
from utils import load_config, save_config
from PIL import Image, ImageTk, ImageSequence
import os
import time

GIF_SIZE = (150, 150)
BOTTLE_SIZE = (50, 50)  # Smaller size for bottles

class MilkMochaPet(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.configure(bg='black')
        self.wm_attributes("-transparentcolor", "black")

        self.frames = []
        self.current_gif = "assets/mocha_gifs/idle.gif"
        self.load_gif_frames(self.current_gif)

        self.label = tk.Label(self, bd=0, bg='black')
        self.label.pack()

        self.frame_index = 0
        self.animate_gif()

        self.bind('<Button-1>', self.start_drag)
        self.bind('<B1-Motion>', self.do_drag)

        # Track active bottles to prevent multiple spawns
        self.active_bottles = []

        # Schedule the milk bottle spawn every 10 seconds for manual testing
        self.config_data = load_config()
        self.spawn_interval = self.config_data.get("spawn_interval", 10000)

        # Set position if saved
        last_pos = self.config_data.get("last_position", [300, 300])
        self.geometry(f"+{last_pos[0]}+{last_pos[1]}")

        # Transparency
        transparency = self.config_data.get("transparency", 255)
        self.attributes("-alpha", transparency / 255)

        # Auto spawn control
        self.auto_spawn = self.config_data.get("auto_spawn", True)
        if self.auto_spawn:
            self.after(self.spawn_interval, self.spawn_milk_bottle)


    def load_gif_frames(self, gif_path):
        self.frames.clear()
        try:
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                # Convert to RGBA for proper transparency handling
                frame = frame.convert('RGBA')
                # Resize the frame
                frame = frame.resize(GIF_SIZE, Image.Resampling.LANCZOS)
                frame_tk = ImageTk.PhotoImage(frame)
                self.frames.append(frame_tk)
        except Exception as e:
            print(f"Error loading GIF {gif_path}: {e}")
            # Create a default transparent frame if loading fails
            default_img = Image.new('RGBA', GIF_SIZE, (0, 0, 0, 0))
            default_tk = ImageTk.PhotoImage(default_img)
            self.frames.append(default_tk)

        # **Fix: reset frame index**
        self.frame_index = 0



    def animate_gif(self):
        if self.frames and len(self.frames) > 0:
            self.label.configure(image=self.frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(100, self.animate_gif)

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_drag(self, event):
        x = self.winfo_pointerx() - self._drag_start_x
        y = self.winfo_pointery() - self._drag_start_y
        self.geometry(f'+{x}+{y}')

    def get_position_bbox(self):
        x = self.winfo_x()
        y = self.winfo_y()
        return (x, y, x + GIF_SIZE[0], y + GIF_SIZE[1])

    def feed_pet(self):
        # Switch to drinking.gif for 5 sec, then revert
        self.current_gif = "assets/mocha_gifs/drinking.gif"
        self.load_gif_frames(self.current_gif)
        self.after(5000, self.return_to_idle)

    def return_to_idle(self):
        self.current_gif = "assets/mocha_gifs/idle.gif"
        self.load_gif_frames(self.current_gif)

    def spawn_milk_bottle(self):
        # Only spawn if no active bottles exist
        if not self.active_bottles:
            bottle = MilkBottle(self)
            self.active_bottles.append(bottle)
        # Schedule the next bottle spawn in 10 seconds for testing
        self.after(10000, self.spawn_milk_bottle)

    def remove_bottle(self, bottle):
        # Remove bottle from active list when it's destroyed
        if bottle in self.active_bottles:
            self.active_bottles.remove(bottle)

    def apply_settings(self, config):
        self.spawn_interval = config.get("spawn_interval", 10000)
        transparency = config.get("transparency", 255)
        self.attributes("-alpha", transparency / 255)
        self.auto_spawn = config.get("auto_spawn", True)

        # Restart spawn loop cleanly
        self.after_cancel(self.spawn_milk_bottle)
        if self.auto_spawn:
            self.after(self.spawn_interval, self.spawn_milk_bottle)

class MilkBottle(tk.Toplevel):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.configure(bg='black')
        self.wm_attributes("-transparentcolor", "black")

        self.frames = []
        gif_path = "assets/food_gifs/milk_bottle.gif"
        try:
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                # Convert to RGBA for proper transparency handling
                frame = frame.convert('RGBA')
                # Resize the frame
                frame = frame.resize(BOTTLE_SIZE, Image.Resampling.LANCZOS)
                frame_tk = ImageTk.PhotoImage(frame)
                self.frames.append(frame_tk)
        except Exception as e:
            print(f"Error loading GIF {gif_path}: {e}")
            # Use transparent fallback if gif fails
            default_img = Image.new('RGBA', BOTTLE_SIZE, (0, 0, 0, 0))
            default_tk = ImageTk.PhotoImage(default_img)
            self.frames.append(default_tk)

        # Create label with no padding or border and transparent background
        self.label = tk.Label(self, bd=0, bg='black')
        self.label.pack()

        self.frame_index = 0
        self.animate_gif()


        self.bind('<Button-1>', self.start_drag)
        self.bind('<B1-Motion>', self.do_drag)

        # Random or fixed initial position
        self.geometry(f"+300+300")

        # Start collision checking loop
        self.check_collision()

    def animate_gif(self):
        if self.frames:
            self.label.configure(image=self.frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(100, self.animate_gif)

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_drag(self, event):
        x = self.winfo_pointerx() - self._drag_start_x
        y = self.winfo_pointery() - self._drag_start_y
        self.geometry(f'+{x}+{y}')

    def get_position_bbox(self):
        x = self.winfo_x()
        y = self.winfo_y()
        return (x, y, x + BOTTLE_SIZE[0], y + BOTTLE_SIZE[1])

    def check_collision(self):
        bottle_box = self.get_position_bbox()
        pet_box = self.pet.get_position_bbox()

        if (bottle_box[0] < pet_box[2] and
            bottle_box[2] > pet_box[0] and
            bottle_box[1] < pet_box[3] and
            bottle_box[3] > pet_box[1]):
            # Collision detected
            self.pet.feed_pet()
            self.pet.remove_bottle(self)
            self.destroy()
        else:
            self.after(100, self.check_collision)


if __name__ == "__main__":
    pet = MilkMochaPet()
    pet.mainloop()
