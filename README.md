# 🚀 UltiToolkit v3.0.0 – **REMAKED**
### completely remastered — better organization, better code, better everything

---

## 📦 what is UltiToolkit?
UltiToolkit is an all-in-one toolkit focused on customization, performance, and simplicity.

with it, you can:
- 🖥️ monitor your PC's status;
- 🔐 generate secure passwords;
- 🧹 eliminate bloatware;
- 🎵 customize keyboard sounds;
- ⚡ boost system performance.

---

## 🤔 why use it?
if your PC is slow or overloaded, UltiToolkit can help fix a big part of that quickly.

plus:
- 🔧 perfect for customization lovers;
- 🧠 easy to use, even your grandma could do it;
- 💻 lightweight and straight to the point.

---

## ⚙️ how to use?

### 🔐 Password Generator
1. choose the security level;
2. set the length;
3. include symbols? how many?;
4. boom, password generated.

### 🧹 Bloatware Killer
1. scans for useless programs;
2. mark the ones you **don’t** want to remove;
3. enjoy the speed boost!

### 🎵 Key Sound Player
1. choose the default, Enter and Shift key sounds;
2. adjust volume live;
3. toggle on/off with `ESC + F11` / `ESC + F12`.

### ⚡ System Booster
1. choose to disable GameDVR, clean temp files, or both;
2. confirm — magic happens.

### 🖥️ System Monitor
- just run it and see live info: CPU, RAM, disk usage, and more.

---

## 🔁 what changed in the remaked version?
- 🔄 fully rewritten code;
- 📁 clean, organized structure;
- 🎯 faster and more efficient features;
- 📦 cleaner repo, user-focused.

---

## 🧩 used libraries

### built-in:
`subprocess`, `shutil`, `os`, `json`, `platform`, `socket`, `time`, `tkinter`, `sys`, `math`, `threading`, `string`, `random`, `tempfile`, `zipfile`

### external:
`PyQt6`, `psutil`, `ctypes`, `asyncio`, `pyperclip`, `packaging`, `httpx`, `pynput`, `simpleaudio`, `pydub`, `wmi`, `pywin32`, `ffmpeg`

### installers:
- [Chocolatey](https://chocolatey.org/)
- [pip](https://pypi.org/project/pip/) (comes with Python)

### system dependencies:
- [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

---

## 🛠️ how to install?

### 1. Python libraries:
open the terminal (Win + R → `cmd`) and run:

```bash
pip install PyQt6 zipfile psutil ctypes asyncio pyperclip packaging httpx pynput simpleaudio pydub wmi pywin32
```

### 2. Chocolatey:
- open **PowerShell as admin** and run:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = `
[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
### 3. system dependencies:
- open **PowerShell as admin** and run:

```powershell
choco install ffmpeg visualstudio2022buildtools --package-parameters \"--allWorkloads --includeRecommended --includeOptional --passive -- locale en-US\" -y
```

---

## ✋ credits

- [OpenHardwareMonitor] (https://openhardwaremonitor.org/): used for temperature monitoring, license is on the file License.html

---

## 🛣 roadmap:

- 3.0.2: instead of using OpenHardwareMonitor, using c# compiled LibreHardwareMonitor (or hand-made hardware monitor) to support modern components

- 3.5.0: more tools, better performance, better interface

---

## 💬 final message:
> thanks for using UltiToolkit!  
> built with coffee, code and ♥ by tutu0012  
> contributions are always welcome – [open an issue](https://github.com/tutu0012/Ulti-Toolkit/issues) or send a PR!

---
