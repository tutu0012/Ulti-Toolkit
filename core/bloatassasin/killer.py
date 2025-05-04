import subprocess
import psutil

class Pistol:
    def __init__(self):
        self.suspects = [
            "OneDrive.exe",
            "MicrosoftEdgeUpdate.exe",
            "YourPhone.exe",
            "PhoneExperienceHost.exe",
            "Widgets.exe",
            "SkypeApp.exe",
            "msedge.exe",
            "CalculatorApp.exe",
            "Taskmgr.exe"
        ]
    
    def look_for_target(self, innocents=None):
        error_msg = ""
        innocents = innocents or []
        targets = []
        
        try:
            for suspect in psutil.process_iter(['pid', 'name']):
                try:
                    name = suspect.info['name']
                    if name in self.suspects and name not in innocents:
                        targets.append(suspect)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            error_msg = f"Error during process scan: {e}"
            
        return targets, error_msg
    
    def shoot_target(self, targets):
        results = []
        
        for suspect in targets:
            try:
                subprocess.run(["taskkill", "/f", "/pid", str(suspect.pid)], check=True)
                results.append(f"[x] Suspect {suspect.name()} with PID {suspect.pid} killed with success.")
            except subprocess.CalledProcessError as error:
                results.append(f"[!] Oops! The suspect {suspect.name()} escaped: {error}")
            except Exception as error:
                results.append(f"[?] Oops! The suspect {suspect.name()} wasn't there: {error}")
        
        return "\n".join(results) if results else "No suspects were identified."