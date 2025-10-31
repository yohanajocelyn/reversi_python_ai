# Reversi AI - Setup and Installation Guide

This guide will walk you through setting up and running the Python-based Reversi (Othello) game on a new computer.

1. Install Python
   First, you need to install Python from the official source.

- Go to the official Python website: python.org
- Download the latest stable version for your operating system (e.g., Python 3.12).

2. Run the Python Installer
   Once the download is complete, run the installer file (e.g., python-3.12.x.exe on Windows or the .pkg file on macOS).

3. IMPORTANT: Add Python to PATH (Windows)
   This is the most critical step for the installer.
   On the very first screen of the Windows installer, look at the bottom.
   You MUST check the box that says "Add python.exe to PATH".
   If you miss this step, your computer won't know where to find Python in the terminal.
   After checking the box, click "Install Now" and follow the prompts to complete the installation.
   (For macOS and Linux, the installer typically handles this for you.)

4. Verify Python Installation
   After installation, open your terminal (Command Prompt on Windows, Terminal on macOS/Linux) and type:

```
python --version
```

or

```
python3 --version
```

You should see the installed Python version displayed.

5. Create virtual environment (optional but recommended)
   It's a good practice to create a virtual environment for your Python projects to manage dependencies.
   In your terminal, navigate to the directory where you want to set up the Reversi AI and run:

```
python -m venv reversi_env

```

    Activate the virtual environment:

- On Windows:

```
reversi_env\Scripts\activate

```

- On macOS/Linux:

```
source reversi_env/bin/activate

```

After activating the virtual environment, run the package installation command again to ensure all dependencies are installed within the virtual environment:

```
pip install -r requirements.txt
```

6. Run the Reversi AI
   Now you can run the Reversi AI. In your terminal, navigate to the directory where the Reversi AI code is located and run:

```
python reversi_ai.py
```

or

```
python3 reversi_ai.py
```

This will start the Reversi game with the AI.
Enjoy playing Reversi against the AI!

```

```
