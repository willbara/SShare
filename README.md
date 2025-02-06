# Secure Share

Secure Share is a command-line tool for encrypting and securely sharing files over the internet. It uses AES encryption to protect your files and provides simple file transfer over networks.

## Features

- Encryption (AES-256) with password protection.
- Send and Receive Files securely over the network.
- Timeout Handling: Automatically stops listening if no connection is made within 10 seconds.
- Error Handling: Notifies you if connections fail or time out.
- Standalone Executable: Build and run as a .exe file without Python.

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/secure-share.git
cd secure-share
```

### Set Up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # For Windows
pip install -r requirements.txt
```

### Building the Standalone Executable

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Build the Executable:

```bash
pyinstaller --onefile secure_share/cli.py --name secure-share
```

3. The executable will be located in the dist/ folder:

```bash
dist/secure-share.exe
```

## Documentation Used

- [Cryptography Library](https://cryptography.io/en/latest/) 
- [Socket Library](https://docs.python.org/3/library/socket.html) 
- [PyInstaller](https://pyinstaller.org/en/stable/) 
```
```