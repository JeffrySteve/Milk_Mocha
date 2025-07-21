import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QPushButton, QSpinBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SettingsWindow(QWidget):
    settings_changed = pyqtSignal(dict)
    restart_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Milk Mocha Pet Settings")
        self.setFixedSize(400, 400)  # Increased height for new settings
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
        
        # Transparency setting with minimum limit
        transparency_layout = QVBoxLayout()
        transparency_label = QLabel("Transparency (100-255):")
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(100, 255)  # Minimum 100 to prevent complete fade out
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
        
        # Milk Mocha speaking setting
        self.speaking_checkbox = QCheckBox("Enable Milk Mocha Speaking (AI Messages)")
        self.speaking_checkbox.setChecked(self.settings.get("milk_mocha_speaking", True))
        layout.addWidget(self.speaking_checkbox)
        
        # Speaking interval setting
        speaking_interval_layout = QHBoxLayout()
        speaking_interval_label = QLabel("Speaking Interval (minutes):")
        self.speaking_interval_spinbox = QSpinBox()
        self.speaking_interval_spinbox.setRange(5, 60)
        self.speaking_interval_spinbox.setValue(self.settings.get("speaking_interval", 15))
        self.speaking_interval_spinbox.setEnabled(self.speaking_checkbox.isChecked())
        
        # Connect checkbox to enable/disable interval setting
        self.speaking_checkbox.toggled.connect(self.speaking_interval_spinbox.setEnabled)
        
        speaking_interval_layout.addWidget(speaking_interval_label)
        speaking_interval_layout.addWidget(self.speaking_interval_spinbox)
        layout.addLayout(speaking_interval_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply & Restart")
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
                "milk_mocha_speaking": True,
                "speaking_interval": 15,
                "last_position": [300, 300]
            }
    
    def apply_settings(self):
        """Apply current settings and restart app"""
        self.settings["spawn_interval"] = self.spawn_spinbox.value() * 1000
        self.settings["transparency"] = self.transparency_slider.value()
        self.settings["auto_spawn"] = self.auto_spawn_checkbox.isChecked()
        self.settings["milk_mocha_speaking"] = self.speaking_checkbox.isChecked()
        self.settings["speaking_interval"] = self.speaking_interval_spinbox.value()
        
        # Save settings
        self.save_settings()
        
        # Emit restart signal
        self.restart_requested.emit()
        
        # Close window
        self.close()
    
    def save_settings(self):
        """Save settings to file"""
        try:
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
