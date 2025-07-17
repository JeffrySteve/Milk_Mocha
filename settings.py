import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QPushButton, QSpinBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SettingsWindow(QWidget):
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Milk Mocha Pet Settings")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # Load current settings
        self.load_settings()
        
        # Create UI
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Milk Mocha Pet Settings")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Spawn interval setting
        spawn_layout = QHBoxLayout()
        spawn_label = QLabel("Bottle Spawn Interval (seconds):")
        self.spawn_spinbox = QSpinBox()
        self.spawn_spinbox.setRange(5, 300)
        self.spawn_spinbox.setValue(self.settings.get("spawn_interval", 10000) // 1000)
        spawn_layout.addWidget(spawn_label)
        spawn_layout.addWidget(self.spawn_spinbox)
        layout.addLayout(spawn_layout)
        
        # Transparency setting
        transparency_layout = QVBoxLayout()
        transparency_label = QLabel("Transparency:")
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(50, 255)
        self.transparency_slider.setValue(self.settings.get("transparency", 255))
        self.transparency_value_label = QLabel(f"{self.transparency_slider.value()}")
        self.transparency_slider.valueChanged.connect(lambda v: self.transparency_value_label.setText(str(v)))
        
        transparency_layout.addWidget(transparency_label)
        transparency_layout.addWidget(self.transparency_slider)
        transparency_layout.addWidget(self.transparency_value_label)
        layout.addLayout(transparency_layout)
        
        # Auto spawn setting
        self.auto_spawn_checkbox = QCheckBox("Auto Spawn Bottles")
        self.auto_spawn_checkbox.setChecked(self.settings.get("auto_spawn", True))
        layout.addWidget(self.auto_spawn_checkbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.close_button = QPushButton("Close")
        
        self.apply_button.clicked.connect(self.apply_settings)
        self.close_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """Load settings from file"""
        try:
            with open("config/settings.json", "r") as f:
                self.settings = json.load(f)
        except:
            self.settings = {
                "spawn_interval": 10000,
                "transparency": 255,
                "auto_spawn": True,
                "last_position": [300, 300]
            }
    
    def apply_settings(self):
        """Apply current settings"""
        self.settings["spawn_interval"] = self.spawn_spinbox.value() * 1000
        self.settings["transparency"] = self.transparency_slider.value()
        self.settings["auto_spawn"] = self.auto_spawn_checkbox.isChecked()
        
        # Save settings
        self.save_settings()
        
        # Emit signal to parent
        self.settings_changed.emit(self.settings)
        
        # Close window
        self.close()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            import os
            os.makedirs("config", exist_ok=True)
            with open("config/settings.json", "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings = SettingsWindow()
    settings.show()
    sys.exit(app.exec_())
