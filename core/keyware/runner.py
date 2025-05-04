from tkinter import Tk, filedialog
from pydub import AudioSegment, effects
import math
import simpleaudio as sa
from pynput import keyboard
import threading
import os
import json

def volume_to_db(volume):
    if volume <= 0:
        return -120
    return 20 * math.log10(volume)

class KeySoundPlayer:
    def __init__(self):
        self.default_sound = None
        self.sounds = {}
        self.key_down = set()
        self.esc_pressed = False
        self.listener = None
        self.volumes = {
            "default": 1.0,
            "enter": 1.0,
            "shift": 1.0,
            "backspace": 1.0,
            "tab": 1.0,
            "capslock": 1.0
        }
        self.path_state = os.path.join(
            os.path.expanduser('~'),
            'AppData', 'Local', 'UltiToolKit', 'data', 'keypressattr', 'ISACTIVE.json'
        )
        self.active = self._load_state()

    def _load_state(self):
        if not os.path.exists(self.path_state):
            return True
            
        try:
            with open(self.path_state, 'r') as f:
                data = json.load(f)
                return data.get("active", True)
        except:
            return True

    def _save_state(self):
        try:
            os.makedirs(os.path.dirname(self.path_state), exist_ok=True)
            with open(self.path_state, 'w') as f:
                json.dump({"active": self.active}, f)
        except Exception as e:
            print(f"[KeySoundPlayer] Failed to save state: {e}")

    def load_sound(self):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select default sound",
            filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.flac")]
        )
        root.destroy()
        
        if not file_path:
            return
            
        try:
            sound = self._load_and_trim(file_path)
            if isinstance(sound, tuple):
                print(sound[0])
                return
                
            self.default_sound = sound
            
            special_keys = {"enter": "ENTER", "shift": "SHIFT"}
            root = Tk()
            root.withdraw()
            
            for key, label in special_keys.items():
                another = filedialog.askopenfilename(
                    title=f"Optional sound for {label}",
                    filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.flac")]
                )
                if another:
                    sound = self._load_and_trim(another)
                    if not isinstance(sound, tuple):
                        self.sounds[key] = sound
                        
            root.destroy()
        except Exception as e:
            print(f"[KeySoundPlayer] Error loading sounds: {e}")
            self.default_sound = None

    def _load_and_trim(self, path):
        try:
            audio = AudioSegment.from_file(path)
            return effects.strip_silence(audio, silence_len=50, silence_thresh=-40, padding=0)
        except Exception as e:
            return f"[KeySoundPlayer] Error loading {path}: {e}", None

    def play_sound_once(self, sound, volume=1.0):
        if sound is None:
            return
            
        try:
            sound = sound + (volume_to_db(volume))
            wav_data = sound.set_frame_rate(44100).set_channels(2).set_sample_width(2).raw_data
            play_obj = sa.play_buffer(
                wav_data,
                num_channels=2,
                bytes_per_sample=2,
                sample_rate=44100
            )
        except Exception as e:
            print(f"[KeySoundPlayer] Error playing sound: {e}")

    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.esc_pressed = True
            return

        if key == keyboard.Key.f12 and self.esc_pressed:
            self.active = False
            self._save_state()
            return

        if key == keyboard.Key.f11 and self.esc_pressed:
            self.active = True
            self._save_state()
            return

        if self.active and key not in self.key_down:
            self.key_down.add(key)
            name = self._get_key_name(key)
            sound = self.sounds.get(name, self.default_sound)
            if sound:
                volume_key = name
                if name == "shift_r":
                    volume_key = "shift"
                elif name == "caps_lock":
                    volume_key = "capslock"

                if volume_key not in self.volumes:
                    volume_key = "default"
                    
                volume = self.volumes.get(volume_key, 1.0)
                threading.Thread(target=self.play_sound_once, args=(sound, volume), daemon=True).start()

    def _get_key_name(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                return key.char.lower()
            else:
                return key.name.lower()
        except:
            return ""

    def on_release(self, key):
        if key in self.key_down:
            self.key_down.remove(key)
        if key == keyboard.Key.esc:
            self.esc_pressed = False

    def run(self):
        if self.default_sound is None:
            return
            
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()