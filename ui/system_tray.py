"""
System tray management for Milk Mocha Pet
"""
import os
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QMovie, QIcon, QPixmap
from PyQt5.QtCore import Qt


class SystemTrayManager:
    """Manages system tray icon and menu"""
    
    def __init__(self, pet_instance):
        self.pet = pet_instance
        self.tray_icon = None
        self.show_hide_action = None
        
        # Initialize system tray
        self.init_system_tray()
    
    def init_system_tray(self):
        """Initialize system tray icon and menu"""
        # Check if system tray is available
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("System tray not available")
            return
        
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self.pet)
        
        # Set tray icon (use a simple icon or create one from existing GIF)
        try:
            # Try to use the idle GIF as icon
            if os.path.exists("assets/mocha_gifs/idle.gif"):
                movie = QMovie("assets/mocha_gifs/idle.gif")
                movie.jumpToFrame(0)  # Get first frame
                pixmap = movie.currentPixmap().scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.tray_icon.setIcon(QIcon(pixmap))
            else:
                # Fallback: create a simple icon
                pixmap = QPixmap(32, 32)
                pixmap.fill(Qt.transparent)
                self.tray_icon.setIcon(QIcon(pixmap))
        except:
            # If all else fails, use default icon
            self.tray_icon.setIcon(self.pet.style().standardIcon(self.pet.style().SP_ComputerIcon))
        
        # Set tooltip
        self.tray_icon.setToolTip("Milk Mocha Pet")
        
        # Create tray menu
        self.create_tray_menu()
        
        # Connect double-click to show/hide
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Show the tray icon
        self.tray_icon.show()
    
    def create_tray_menu(self):
        """Create the system tray context menu"""
        tray_menu = QMenu()
        
        # Show/Hide Pet
        self.show_hide_action = QAction("Hide Pet", self.pet)
        self.show_hide_action.triggered.connect(self.toggle_visibility)
        tray_menu.addAction(self.show_hide_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Quick Actions submenu
        quick_actions_menu = tray_menu.addMenu("Quick Actions")
        
        quick_actions = [
            ("Dance", self.pet.show_dancing),
            ("Laugh", self.pet.show_laugh),
            ("Excited", self.pet.show_excited),
            ("Heart Throw", self.pet.show_heartthrow),
            ("Playing Guitar", self.pet.show_playing),
            ("Greeting", self.pet.show_greeting),
            ("Run Random", self.pet.run_to_random_location),
            ("Sleep", self.pet.show_sleeping)
        ]
        
        for name, action in quick_actions:
            quick_action = QAction(name, self.pet)
            quick_action.triggered.connect(action)
            quick_actions_menu.addAction(quick_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Settings
        settings_action = QAction("Settings", self.pet)
        settings_action.triggered.connect(self.pet.open_settings)
        tray_menu.addAction(settings_action)
        
        # About
        about_action = QAction("About", self.pet)
        about_action.triggered.connect(self.show_about)
        tray_menu.addAction(about_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Exit
        exit_action = QAction("Exit", self.pet)
        exit_action.triggered.connect(self.pet.quit_application)
        tray_menu.addAction(exit_action)
        
        # Set the menu
        self.tray_icon.setContextMenu(tray_menu)
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_visibility()
        elif reason == QSystemTrayIcon.Trigger:
            # Single click - show a notification
            self.tray_icon.showMessage(
                "Milk Mocha Pet",
                "Pet is active! Double-click to show/hide.",
                QSystemTrayIcon.Information,
                2000
            )
    
    def toggle_visibility(self):
        """Toggle pet visibility"""
        if self.pet.isVisible():
            self.pet.hide()
            self.show_hide_action.setText("Show Pet")
            self.tray_icon.showMessage(
                "Milk Mocha Pet",
                "Pet hidden. Access from system tray.",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            self.pet.show()
            self.show_hide_action.setText("Hide Pet")
            self.tray_icon.showMessage(
                "Milk Mocha Pet",
                "Pet is now visible!",
                QSystemTrayIcon.Information,
                2000
            )
    
    def show_about(self):
        """Show about information"""
        self.tray_icon.showMessage(
            "About Milk Mocha Pet",
            "A cute desktop companion with animations and interactions!\n\nFeatures:\n• Draggable pet\n• Random animations\n• Feeding system\n• Settings control\n• System tray integration",
            QSystemTrayIcon.Information,
            5000
        )
    
    def hide(self):
        """Hide the system tray icon"""
        if self.tray_icon:
            self.tray_icon.hide()
