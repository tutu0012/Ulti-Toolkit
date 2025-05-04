import httpx
import os
import tempfile
import zipfile
import shutil
from packaging import version
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal

class UpdaterSignals(QObject):
    update_available = pyqtSignal(str, str)
    update_progress = pyqtSignal(int)
    update_completed = pyqtSignal(bool, str)
    update_error = pyqtSignal(str)

class AutoUpdater:
    GITHUB_API_URL = "https://api.github.com/tutu0012/Ulti-Toolkit/releases/latest"
    CURRENT_VERSION = "3.0.0"
    
    def __init__(self):
        self.signals = UpdaterSignals()
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def check_for_updates(self):
        try:
            response = await self.client.get(self.GITHUB_API_URL)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data.get("tag_name", "").lstrip("v")
            
            if not latest_version:
                self.signals.update_error.emit("Could not determine latest version")
                return False, None
            
            if version.parse(latest_version) > version.parse(self.CURRENT_VERSION):
                self.signals.update_available.emit(self.CURRENT_VERSION, latest_version)
                return True, release_data
            else:
                return False, None
                
        except httpx.HTTPError as e:
            self.signals.update_error.emit(f"HTTP error occurred: {str(e)}")
            return False, None
        except Exception as e:
            self.signals.update_error.emit(f"Error checking for updates: {str(e)}")
            return False, None
    
    async def download_update(self, release_data):
        try:
            assets = release_data.get("assets", [])
            download_url = None
            
            for asset in assets:
                if asset.get("name", "").endswith(".zip"):
                    download_url = asset.get("browser_download_url")
                    break
            
            if not download_url:
                self.signals.update_error.emit("No downloadable update found")
                return False, None

            async with self.client.stream("GET", download_url) as response:
                response.raise_for_status()

                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0

                with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_file:
                    temp_path = temp_file.name
                    
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        temp_file.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self.signals.update_progress.emit(progress)
            
            return True, temp_path
            
        except Exception as e:
            self.signals.update_error.emit(f"Error downloading update: {str(e)}")
            return False, None
    
    async def install_update(self, zip_path):
        try:
            extract_dir = tempfile.mkdtemp()

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

            extracted_root = None
            for item in os.listdir(extract_dir):
                item_path = os.path.join(extract_dir, item)
                if os.path.isdir(item_path):
                    extracted_root = item_path
                    break
            
            if not extracted_root:
                extracted_root = extract_dir

            self._copy_files(extracted_root, app_dir)

            os.unlink(zip_path)
            shutil.rmtree(extract_dir)

            self.signals.update_completed.emit(True, "Update completed successfully!")
            return True
            
        except Exception as e:
            self.signals.update_error.emit(f"Error installing update: {str(e)}")
            self.signals.update_completed.emit(False, f"Update failed: {str(e)}")
            return False
    
    def _copy_files(self, src_dir, dst_dir):
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join(dst_dir, item)
            
            if os.path.isdir(src_path):
                os.makedirs(dst_path, exist_ok=True)
                self._copy_files(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
    
    async def update_process(self):
        update_available, release_data = await self.check_for_updates()
        
        if not update_available:
            return False
            
        download_success, zip_path = await self.download_update(release_data)
        
        if not download_success:
            return False
            
        install_success = await self.install_update(zip_path)
        return install_success
    
    async def close(self):
        await self.client.aclose()


class UpdaterUI:
    
    @staticmethod
    def show_update_dialog(parent, current_version, latest_version):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Update Available")
        msg_box.setText(f"A new version of Ulti-Toolkit is available!\n\n"
                        f"Current version: {current_version}\n"
                        f"Latest version: {latest_version}\n\n"
                        f"Would you like to update now?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)
        return msg_box.exec() == QMessageBox.StandardButton.Yes
    
    @staticmethod
    def show_progress_dialog(parent, progress):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Updating")
        msg_box.setText(f"Downloading update: {progress}%")
        msg_box.setStandardButtons(QMessageBox.StandardButton.NoButton)
        return msg_box
    
    @staticmethod
    def show_completion_dialog(parent, success, message):
        """Show update completion message."""
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Update Complete" if success else "Update Failed")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msg_box.exec()


async def check_and_update(parent_window=None):
    updater = AutoUpdater()
    
    try:
        update_available, release_data = await updater.check_for_updates()
        
        if not update_available:
            return False
        
        if not parent_window:
            return False

        if not UpdaterUI.show_update_dialog(parent_window, updater.CURRENT_VERSION, 
                                           release_data.get("tag_name", "").lstrip("v")):
            return False

        download_success, zip_path = await updater.download_update(release_data)
        
        if not download_success:
            return False
        
        install_success = await updater.install_update(zip_path)
        
        if install_success:
            UpdaterUI.show_completion_dialog(
                parent_window, True, 
                "Update completed successfully! Please restart the application."
            )
            return True
        else:
            return False
            
    finally:
        await updater.close()