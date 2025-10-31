# Library Used

## 1. Pygame

Pygame is a third-party Python library. It's used in this project to help create all of the game's UI (board, disk pieces, texts and instructions)

## 2. Copy:

Copy is Python's library that we use for its .deepcopy() function which copies the game state for the competitive algorithm (MiniMax with Alpha-Beta Pruning) to simulate the game as it is exploring the possible actions and finding the heuristic score

## 3. Math:

Math is Python's library that we use for its math.inf value for the alpha (-inf) and beta (+inf) in our algorithm

# IDE Used

## Visual Studio Code

# Reversi AI - Setup and Installation Guide

This guide will walk you through setting up and running the Python-based Reversi (Othello) game on a new computer.

## 1. Install Python

First, you need to install Python from the official source.

- Go to the official Python website: [python.org](https://python.org)
- Download the latest stable version for your operating system (e.g., Python 3.12).
- **NOTE:** Make sure to download Python 3.x, as Python 2.x is no longer supported.
- **NOTE:** Python 3.14+ won't work with this codebase; please use Python 3.13 or earlier.

## 2. Run the Python Installer

Once the download is complete, run the installer file (e.g., `python-3.12.x.exe` on Windows or the `.pkg` file on macOS).

## 3. IMPORTANT: Add Python to PATH (Windows)

This is the most critical step for the installer.
On the very first screen of the Windows installer, look at the bottom.
You **MUST** check the box that says "Add python.exe to PATH".
If you miss this step, your computer won't know where to find Python in the terminal.
After checking the box, click "Install Now" and follow the prompts to complete the installation.
(For macOS and Linux, the installer typically handles this for you.)

## 4. Verify Python Installation

After installation, open your terminal (Command Prompt on Windows, Terminal on macOS/Linux) and type:

```bash
python --version
```

or

```bash
python3 --version
```

You should see the installed Python version displayed.

## 5. Create Virtual Environment (Optional but Recommended)

**Note:** If you prefer not to create a virtual environment, you can proceed directly to Step 6.

It's a good practice to create a virtual environment for your Python projects to manage dependencies.
In your terminal, navigate to the directory where you want to set up the Reversi AI and run:

```bash
python -m venv reversi_env
```

Activate the virtual environment:

- **On Windows:**

```bash
reversi_env\Scripts\activate
```

- **On macOS/Linux:**

```bash
source reversi_env/bin/activate
```

## 6. Install Dependencies

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

## 7. Run the Reversi AI

Now you can run the Reversi AI. In your terminal, navigate to the directory where the Reversi AI code is located and run:

```bash
python reversi_ai.py
```

or

```bash
python3 reversi_ai.py
```

This will start the Reversi game with the AI.

Enjoy playing Reversi against the AI!
