import psutil
import platform
import socket
import time
import wmi
import win32con
import win32process
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import QTimer

class SystemDiagnostics(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('System Diagnostics')
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU: ")
        self.temp_label = QLabel("Temperatures: ")
        layout.addWidget(self.temp_label)

        self.memory_label = QLabel("Memory: ")
        self.disk_label = QLabel("Disk: ")
        self.network_label = QLabel("Network: ")
        self.system_label = QLabel("System: ")
        self.time_label = QLabel("Time: ")

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.network_label)
        layout.addWidget(self.system_label)
        layout.addWidget(self.time_label)

        self.start_btn = QPushButton('Start Auto Update')
        self.start_btn.clicked.connect(self.start_auto_update)
        
        self.stop_btn = QPushButton('Stop Auto Update')
        self.stop_btn.clicked.connect(self.stop_auto_update)
        self.stop_btn.setEnabled(False)

        self.ohm_proc = None
        
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_diagnostics)
        
    def start_auto_update(self):
        self.timer.start(500)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.update_diagnostics()
        
    def stop_auto_update(self):
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def get_temps(self):
        try:
            def is_provider_running():
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] == 'OpenHardwareMonitor.exe':
                        return True
                return False
            
            if not is_provider_running():
                base_path = os.path.dirname(os.path.abspath(__file__))
                exe_path = os.path.join(base_path, 'OpenHardwareMonitor', 'OpenHardwareMonitor.exe')
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = win32con.SW_HIDE

                self.ohm_proc = subprocess.Popen(
                    [exe_path],
                    startupinfo=startupinfo,
                    creationflags=win32process.CREATE_NEW_PROCESS_GROUP
                )
                time.sleep(2.5)

            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            temps = w.Sensor()
            cpu_temp = None
            gpu_temp = None
            for sensor in temps:
                if sensor.SensorType == 'Temperature':
                    if 'CPU Package' in sensor.Name:
                        cpu_temp = sensor.Value
                    elif 'GPU Core' in sensor.Name:
                        gpu_temp = sensor.Value
            return cpu_temp, gpu_temp
        except Exception as e:
            return None, None

    def update_diagnostics(self):
        try:
            cpu_temp, gpu_temp = self.get_temps()

            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else "N/A"
            cpu_cores = psutil.cpu_count(logical=True)
            self.cpu_label.setText(f"CPU: {cpu_percent}% | Frequency: {cpu_freq} MHz | Cores: {cpu_cores}")

            self.temp_label.setText(f"Temperatures:\nCPU: {cpu_temp}°C\nGPU: {gpu_temp}°C")

            mem = psutil.virtual_memory()
            mem_total = round(mem.total / (1024.0 ** 3), 2)
            mem_used = round(mem.used / (1024.0 ** 3), 2)
            mem_percent = mem.percent
            self.memory_label.setText(f"Memory: {mem_used}GB / {mem_total}GB ({mem_percent}%)")

            disk = psutil.disk_usage('/')
            disk_total = round(disk.total / (1024.0 ** 3), 2)
            disk_used = round(disk.used / (1024.0 ** 3), 2)
            disk_percent = disk.percent
            self.disk_label.setText(f"Disk: {disk_used}GB / {disk_total}GB ({disk_percent}%)")

            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            self.network_label.setText(f"Network: Host: {hostname} | IP: {ip_address}")
            
            system = f"{platform.system()} {platform.version()}"
            python_version = platform.python_version()
            self.system_label.setText(f"System: {system} | Python: {python_version}")
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.setText(f"Last update: {current_time}")
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')
            self.stop_auto_update()

    def closeEvent(self, event):
        self.stop_auto_update()

        if self.ohm_proc is not None:
            try:
                self.ohm_proc.terminate()
            except Exception as e:
                print(f"Error closing OpenHardwareMonitor: {e}")

        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = SystemDiagnostics()
    window.show()
    app.exec()