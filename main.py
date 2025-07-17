import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os

GIF_SIZE = (200, 200)

class MilkMochaPet(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.configure(bg='black')
        self.wm_attributes("-transparentcolor", "black")

        self.frames = []
        gif_path = "assets/mocha_gifs/idle.gif"
        self.load_gif_frames(gif_path)

        self.label = tk.Label(self, bd=0, bg='black')
        self.label.pack()

        self.frame_index = 0
        self.animate_gif()

        self.bind('<Button-1>', self.start_drag)
        self.bind('<B1-Motion>', self.do_drag)

    def load_gif_frames(self, gif_path):
        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            # Convert to RGBA to handle transparency properly
            frame = frame.convert('RGBA')
            frame = frame.resize(GIF_SIZE, Image.Resampling.LANCZOS)
            frame_tk = ImageTk.PhotoImage(frame)
            self.frames.append(frame_tk)

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

if __name__ == "__main__":
    pet = MilkMochaPet()
    pet.mainloop()
