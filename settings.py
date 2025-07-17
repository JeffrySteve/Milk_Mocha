import tkinter as tk
from utils import load_config, save_config

class SettingsWindow(tk.Toplevel):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.title("Milk Mocha Settings")
        self.geometry("300x200")
        self.resizable(False, False)

        self.config_data = load_config()

        tk.Label(self, text="Milk Bottle Spawn Interval (sec):").pack(pady=5)
        self.interval_var = tk.IntVar(value=self.config_data["spawn_interval"] // 1000)
        tk.Entry(self, textvariable=self.interval_var).pack()

        tk.Label(self, text="Transparency (0-255):").pack(pady=5)
        self.transparency_var = tk.IntVar(value=self.config_data["transparency"])
        tk.Entry(self, textvariable=self.transparency_var).pack()

        self.auto_spawn_var = tk.BooleanVar(value=self.config_data.get("auto_spawn", True))
        tk.Checkbutton(self, text="Enable Auto Spawn", variable=self.auto_spawn_var).pack(pady=5)

        tk.Button(self, text="Save", command=self.save_settings).pack(pady=10)

    def save_settings(self):
        interval_ms = max(1000, self.interval_var.get() * 1000)
        transparency = min(max(0, self.transparency_var.get()), 255)

        self.config_data["spawn_interval"] = interval_ms
        self.config_data["transparency"] = transparency
        self.config_data["auto_spawn"] = self.auto_spawn_var.get()

        save_config(self.config_data)
        self.pet.apply_settings(self.config_data)
        self.destroy()
