import subprocess
import os
import shutil

class Pilot:
    @staticmethod
    def boost_fps_safe():
        result_messages = []
        try:
            subprocess.run(["powercfg", "-setactive", "SCHEME_MIN"], check=True)
            result_messages.append("[✓] High performance power plan activated.")

            subprocess.run([
                "reg", "add",
                r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR",
                "/v", "AppCaptureEnabled",
                "/t", "REG_DWORD",
                "/d", "0",
                "/f"
            ], check=True)
            result_messages.append("[✓] GameDVR disabled.")
            
        except subprocess.CalledProcessError as e:
            return f"[x] Error applying FPS boost: {e}"
        except Exception as e:
            return f"[x] Unexpected error: {e}"
            
        return "\n".join(result_messages)
    
    @staticmethod
    def clean_temp_files():
        temp_files_folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp')
        files_removed = 0
        files_failed = 0
        
        try:
            if not os.path.exists(temp_files_folder):
                return "[!] Temp folder not found"
                
            for item in os.listdir(temp_files_folder):
                item_path = os.path.join(temp_files_folder, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                        files_removed += 1
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path, ignore_errors=True)
                        files_removed += 1
                except (PermissionError, OSError):
                    files_failed += 1
                    
            return f"[+] Temp files cleaned: {files_removed} removed, {files_failed} failed (likely in use)"
        except Exception as e:
            return f"[x] Error cleaning temp files: {e}"