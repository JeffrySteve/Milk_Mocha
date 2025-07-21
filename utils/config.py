"""
Configuration management utilities for Milk Mocha Pet
"""
import os
import json


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path="config/settings.json"):
        self.config_path = config_path
        self.config_data = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Default config
        return {
            "spawn_interval": 10000,
            "transparency": 255,
            "last_position": [300, 300],
            "auto_spawn": True,
            "milk_mocha_speaking": True,
            "speaking_interval": 15
        }
    
    def save_config(self, new_position=None):
        """Save current configuration"""
        try:
            os.makedirs("config", exist_ok=True)
            if new_position:
                self.config_data["last_position"] = new_position
            with open(self.config_path, "w") as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config_data.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config_data[key] = value
    
    def update_position(self, x, y):
        """Update pet position in config"""
        self.config_data["last_position"] = [x, y]
        self.save_config()
