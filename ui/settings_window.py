"""
Simple settings window for Milk Mocha Pet
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QCheckBox, QSpinBox, QPushButton, QGroupBox)
from PyQt5.QtCore import Qt


class SettingsWindow(QDialog):
    """Settings dialog for configuring Milk Mocha Pet"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Milk Mocha Pet Settings")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # Store reference to config (we'll get it from the pet)
        self.config = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Speaking settings group
        speaking_group = QGroupBox("AI Speaking Settings")
        speaking_layout = QVBoxLayout()
        
        # Enable/disable speaking
        self.speaking_enabled = QCheckBox("Enable Milk Mocha AI speaking")
        self.speaking_enabled.setChecked(True)
        speaking_layout.addWidget(self.speaking_enabled)
        
        # Speaking interval
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Speaking interval (minutes):"))
        self.speaking_interval = QSpinBox()
        self.speaking_interval.setRange(1, 60)
        self.speaking_interval.setValue(15)
        interval_layout.addWidget(self.speaking_interval)
        speaking_layout.addLayout(interval_layout)
        
        speaking_group.setLayout(speaking_layout)
        layout.addWidget(speaking_group)
        
        # Behavior settings group
        behavior_group = QGroupBox("Behavior Settings")
        behavior_layout = QVBoxLayout()
        
        # Auto spawn animations
        self.auto_spawn = QCheckBox("Enable automatic animations")
        self.auto_spawn.setChecked(True)
        behavior_layout.addWidget(self.auto_spawn)
        
        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_settings(self, config):
        """Load settings from config"""
        self.config = config
        
        # Load values from config
        self.speaking_enabled.setChecked(config.get("milk_mocha_speaking", True))
        self.speaking_interval.setValue(config.get("speaking_interval", 15))
        self.auto_spawn.setChecked(config.get("auto_spawn", True))
    
    def save_settings(self):
        """Save settings to config"""
        if self.config:
            # Save values to config
            self.config.set("milk_mocha_speaking", self.speaking_enabled.isChecked())
            self.config.set("speaking_interval", self.speaking_interval.value())
            self.config.set("auto_spawn", self.auto_spawn.isChecked())
            self.config.save()
        
        self.close()
    
    def show_with_config(self, config):
        """Show the settings window with current config"""
        self.load_settings(config)
        self.show()
        self.raise_()
        self.activateWindow()
