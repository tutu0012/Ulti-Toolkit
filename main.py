import sys
import asyncio
import ctypes
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox,
    QSlider, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from core.bloatassasin.killer import Pistol
from core.wordsafe.worder import Generator
from core.keyware.runner import KeySoundPlayer
from core.computerboost.rocket import Pilot
from core.computer_monitor.monitor import SystemDiagnostics
import pyperclip
import threading
import os
import json
from core.ultitoolkit_settuper.keypressattr_dir import make_keypressattr_dir, make_keypressattr_files_in_dir
from core.ultitoolkit_settuper.issettuped_dir import make_issettuped_dir, make_issettuped_files_in_dir
from core.auto_updater.seeker import check_and_update

class AppWindow(QWidget):
    data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'UltiToolKit', 'data')
    issetuppedbool_dir = os.path.join(data_dir, 'isSettuped_bool')
    issetuppedbool_file = os.path.join(issetuppedbool_dir, 'ISSETUPPED_BOOL.json')
    keypressattr_dir = os.path.join(data_dir, 'keypressattr')
    keypress_isactive_file = os.path.join(keypressattr_dir, 'ISACTIVE.json')

    def __init__(self):
        super().__init__()
        self.is_dark_theme = False
        self.theme_button = None
        self.setup_application_data()
        self.setWindowTitle("ULTITOOLKIT v3.0.0")
        self.setGeometry(100, 100, 360, 280)
        self.init_ui()
        
        QTimer.singleShot(1000, self.check_for_updates)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(12)

        self.buttons = {
            "Password Generator": self.open_password_generator,
            "Bloatware Killer": self.open_bloatware_killer,
            "Key Sound Player": self.open_key_sound_player,
            "Computer General Booster": self.open_computer_booster,
            "Computer Monitor": self.open_computer_monitor,
            "Run as Administrator": self.request_admin_privileges,
        }

        for label, func in self.buttons.items():
            btn = QPushButton(label)
            btn.setMinimumHeight(35)
            btn.clicked.connect(func)
            self.content_layout.addWidget(btn)

        main_layout.addLayout(self.content_layout)

        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()
        
        self.theme_button = QPushButton("🌙")
        self.theme_button.setFixedSize(30, 30)
        self.theme_button.setToolTip("Toggle Dark/Light Theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        bottom_bar.addWidget(self.theme_button)
        
        main_layout.addLayout(bottom_bar)
        
        self.setLayout(main_layout)
        self.key_player = None

        self.apply_theme()

    def setup_application_data(self):
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            if not os.path.exists(self.issetuppedbool_file) or not self._is_setup_complete():
                self._perform_setup()

            theme_file = os.path.join(self.data_dir, 'theme_preference.json')
            if os.path.exists(theme_file):
                try:
                    with open(theme_file, 'r') as f:
                        data = json.load(f)
                        self.is_dark_theme = data.get("dark_theme", False)
                except Exception as e:
                    print(f"Failed to load theme preference: {e}")
        except Exception as e:
            print(f"Setup error: {e}")
    
    def _is_setup_complete(self):
        try:
            with open(self.issetuppedbool_file, 'r') as f:
                data = json.load(f)
                return data.get("setupped", False)
        except:
            return False
    
    def _perform_setup(self):
        try:
            make_keypressattr_dir()
            make_keypressattr_files_in_dir()
            make_issettuped_dir()
            make_issettuped_files_in_dir()

            with open(self.issetuppedbool_file, 'w') as f:
                json.dump({"setupped": True}, f)
        except Exception as e:
            print(f"Setup process error: {e}")
            
    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2D2D30;
                    color: #FFFFFF;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #3E3E42;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #45454A;
                }
                QPushButton:pressed {
                    background-color: #555555;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QMessageBox {
                    background-color: #2D2D30;
                }
                QInputDialog {
                    background-color: #2D2D30;
                }
            """)
            if self.theme_button:
                self.theme_button.setText("☀️")
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #F0F0F0;
                    color: #000000;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #E1E1E1;
                    border: 1px solid #B9B9B9;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #D1D1D1;
                }
                QPushButton:pressed {
                    background-color: #C1C1C1;
                }
                QLabel {
                    color: #000000;
                }
            """)
            if self.theme_button:
                self.theme_button.setText("🌙")
            
    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        
        theme_file = os.path.join(self.data_dir, 'theme_preference.json')
        try:
            with open(theme_file, 'w') as f:
                json.dump({"dark_theme": self.is_dark_theme}, f)
        except Exception as e:
            print(f"Failed to save theme preference: {e}")

    def check_for_updates(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(check_and_update(self))
        loop.close()
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def request_admin_privileges(self):
        if self.is_admin():
            self.show_popup("Admin privileges", "The application is already running with administrator privileges.")
            return
        
        confirm = QMessageBox.question(
            self,
            "Administrator Privileges",
            "Some features require administrator privileges. Do you want to restart the application as administrator?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                python_exe = sys.executable

                script_path = os.path.abspath(sys.argv[0])

                args = [python_exe, script_path] + sys.argv[1:]

                if sys.platform.startswith('win'):
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", python_exe, " ".join([f'"{arg}"' for arg in args[1:]]), None, 1
                    )
                    sys.exit()
                else:
                    self.show_popup("Not Supported", "Admin elevation is only supported on Windows.")
            except Exception as e:
                self.show_popup("Error", f"Failed to restart with admin privileges: {str(e)}")
                
    def should_request_admin(self, feature_name):
        confirm = QMessageBox.question(
            self,
            "Administrator Privileges Required",
            f"The {feature_name} feature works best with administrator privileges.\n\n"
            "Do you want to restart the application as administrator?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.request_admin_privileges()
            return True
        elif confirm == QMessageBox.StandardButton.Cancel:
            return True
        
        return False

    def open_password_generator(self):
        level, ok1 = QInputDialog.getInt(self, "Security Level", "Enter security level (1-5):", 3, 1, 5)
        if not ok1: 
            return
            
        length, ok2 = QInputDialog.getInt(self, "Password Length", "Enter password length:", 12, 1, 128)
        if not ok2: 
            return
            
        use_symbols, ok3 = QInputDialog.getText(self, "Use Symbols?", "Use symbols? (y/n):")
        if not ok3:
            return
            
        use_symbols = use_symbols.lower() == 'y'
        symbols_count = 0
        
        if use_symbols:
            symbols_count, ok4 = QInputDialog.getInt(self, "Symbols Count", "How many symbols?", 4, 0, length)
            if not ok4: 
                return
        
        gen = Generator()
        password = gen.generate(level, length, use_symbols, symbols_count)
        pyperclip.copy(password)
        self.show_popup("Generated Password", "Password copied to clipboard!")

    def open_bloatware_killer(self):
        if not self.is_admin() and self.should_request_admin("Bloatware Killer"):
            return
            
        pistol = Pistol()
        self.show_popup("Search", "Looking for bloatware...")
        all_targets, msg = pistol.look_for_target()

        if not all_targets:
            self.show_popup("No Targets Found", "No targets found." + (f" {msg}" if msg else ""))
            return

        targets_list = "\n".join([f"{i+1}: {proc.name()} (PID {proc.pid})" for i, proc in enumerate(all_targets)])
        innocent_input, ok = QInputDialog.getText(
            self, "Innocents", f"Found targets:\n{targets_list}\n\nMark innocent (comma separated):")
        
        if not ok:
            self.show_popup("Cancelled", "Operation cancelled.")
            return

        innocent_indexes = []
        if innocent_input.strip():
            try:
                innocent_indexes = [int(i.strip()) - 1 for i in innocent_input.split(",")]
            except:
                self.show_popup("Invalid Input", "Invalid input. Skipping innocence filter.")
        
        filtered_targets = [p for i, p in enumerate(all_targets) if i not in innocent_indexes]

        if not filtered_targets:
            self.show_popup("No Valid Targets", "All suspects marked innocent.")
            return

        confirm, ok = QInputDialog.getText(self, "Confirm", f"{len(filtered_targets)} target(s) selected.\nEliminate? (y/n):")
        if ok and confirm.lower() == 'y':
            result = pistol.shoot_target(filtered_targets)
            self.show_popup("Elimination Result", result)
        else:
            self.show_popup("Cancelled", "Operation cancelled.")

    def open_key_sound_player(self):
        if not self.key_player:
            self.key_player = KeySoundPlayer()
            self.key_player.load_sound()
            if hasattr(self.key_player, 'default_sound') and self.key_player.default_sound:
                threading.Thread(target=self.key_player.run, daemon=True).start()
                self.show_popup("Key Sound Player", "Key sounds activated.\nESC + F12 to disable.\nESC + F11 to re-enable.")
                
                volume_window = QWidget()
                volume_window.setWindowTitle("Volume Control")
                layout = QVBoxLayout()
                
                def create_slider(label_text, volume_key):
                    label = QLabel(label_text)
                    slider = QSlider(Qt.Orientation.Horizontal)
                    slider.setMinimum(0)
                    slider.setMaximum(100)
                    current_value = self.key_player.volumes.get(volume_key, 1.0)
                    slider.setValue(int(current_value * 100))
                    def update_volume(value):
                        self.key_player.volumes[volume_key] = value / 100
                    slider.valueChanged.connect(update_volume)
                    layout.addWidget(label)
                    layout.addWidget(slider)

                create_slider("Geral", "default")
                create_slider("Enter", "enter")
                create_slider("Shift", "shift")
                
                additional_keys = {
                    "backspace": "Backspace",
                    "tab": "Tab", 
                    "capslock": "CapsLock"
                }
                
                for key, label in additional_keys.items():
                    if key not in self.key_player.volumes:
                        self.key_player.volumes[key] = 1.0
                    create_slider(label, key)
                
                volume_window.setLayout(layout)
                volume_window.show()
                self.volume_window = volume_window
            else:
                self.show_popup("No Sound", "No sound was loaded.")
        else:
            self.show_popup("Already Loaded", "KeySoundPlayer already initialized.\nUse ESC + F12 to disable, ESC + F11 to re-enable.")

    def open_computer_booster(self):
        if not self.is_admin() and self.should_request_admin("Computer Booster"):
            return
            
        options = [
            "Boost FPS (Power plan & Xbox Game Bar)",
            "Clean Temporary Files",
            "Full Optimization (Both options)"
        ]
        
        option, ok = QInputDialog.getItem(
            self,
            "Computer Optimization",
            "Select optimization action:",
            options,
            0,
            False
        )
        
        if not ok:
            self.show_popup("Cancelled", "Optimization cancelled.")
            return
            
        results = []
        
        if "Boost FPS" in option or "Full Optimization" in option:
            confirm, ok = QInputDialog.getText(
                self, 
                "Performance Boost Confirmation", 
                "This function will:\n- Set power plan to high performance\n- Disable Xbox Game Bar recording\n\nThis may require administrator permissions.\nProceed? (y/n):"
            )
            
            if ok and confirm.lower() == 'y':
                result = Pilot.boost_fps_safe()
                results.append(f"Performance Boost: {result}")
            else:
                results.append("Performance boost cancelled.")

        if "Clean Temporary Files" in option or "Full Optimization" in option:
            confirm, ok = QInputDialog.getText(
                self,
                "Temp Files Cleanup Confirmation",
                "This will clean temporary files from your system.\nProceed? (y/n):"
            )
            
            if ok and confirm.lower() == 'y':
                result = Pilot.clean_temp_files()
                results.append(f"Temp Files Cleanup: {result}")
            else:
                results.append("Temp files cleanup cancelled.")

        self.show_popup("Optimization Results", "\n\n".join(results))

    def open_computer_monitor(self):
        self.diag = SystemDiagnostics()
        self.diag.show()
        print("Initializing...")
        self.diag.start_auto_update()

    def show_popup(self, title, message):
        QMessageBox.information(self, title, message)

def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()