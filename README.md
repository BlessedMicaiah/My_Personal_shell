Welcome to My_Personal_shell! This repository contains a custom Python-based shell I’ve built to enhance my command-line experience. It’s a lightweight, cross-platform shell with colorful output, useful commands, and automation features. Whether you’re here to explore, adapt, or contribute, I hope you find it valuable!
Overview
My_Personal_shell is a Python script that implements a custom command-line interface. It supports common shell commands (e.g., cd, ls, mkdir), system utilities, package management, and even a fancy loading bar for visual feedback. Built with cross-platform compatibility in mind, it runs on Linux, macOS, and Windows, leveraging libraries like colorama for colored output and tqdm for progress bars.
Features
Colorful Interface: Uses colorama for cross-platform colored terminal output (e.g., blue directories, green files).

Loading Bar: A customizable loading bar for tasks like package installation or custom commands (e.g., testo).

File Management: Commands like ls (list files), mkdir, rmdir, touch, rm, cat, and vim for editing.

System Commands: Execute shell commands directly, with optional sudo support.

System Info: Display system details with sysinfo (OS, architecture, Python version, etc.).

Package Management: Install packages via install <pkg> using detected package managers (e.g., apt-get, brew).

Development Tools: Install tools like vim, mysql, vscode, or git with devtool <tool>.

Search Functionality: Find files or directories with find <name>.

Command History: View past commands with history.

Custom Commands: Includes a demo testo command to deploy "Warzone Assets" with a loading bar.

Installation
To set up and run this shell on your system, follow these steps:
Clone the Repository:
bash

git clone https://github.com/BlessedMicaiah/My_Personal_shell.git
cd My_Personal_shell

Install Python:
Ensure you have Python 3.6+ installed. Check with:
bash

python3 --version

Install Dependencies:
Install required Python packages using pip:
bash

pip3 install -r requirements.txt

The required packages are:
colorama: For colored terminal output.

tqdm: For progress bars.

requests: For file downloads (if extended).
Create a requirements.txt file with:

colorama>=0.4.6
tqdm>=4.66.1
requests>=2.31.0

Run the Shell:
Start the shell by running the main script:
bash

python3 updated_shell.py  

Usage
Once the shell starts, you’ll see a prompt with the current directory (e.g., /home/user $). Type commands and press Enter. Examples:
List Files:

ls

Output: Files in green, directories in blue.

Change Directory:

cd /path/to/dir
cd ..

Install a Package:

install htop

Displays a loading bar and installs using the system’s package manager.

System Info:

sysinfo

Shows OS, release, architecture, etc.

Custom Command:

testo

Deploys "Warzone Assets" with an 8-second loading bar.

Development Tools:

devtool git

Installs Git based on your OS.

Help:

help

Lists all available commands.

Run help to see the full command list, including mkdir, rm, cat, touch, find, and more.
Configuration
Customize Commands: Edit shell.py (or your script name) to add new commands or modify existing ones in the main() loop.

Loading Bar: Adjust loading_bar() parameters (e.g., bar_length, loading_time) for different effects.

Colors: Modify Fore.<COLOR> calls (e.g., Fore.CYAN) using colorama options.

Contributing
I’d love your input! To contribute:
Fork this repository.

Create a branch (git checkout -b feature/your-idea).

Make changes and commit (git commit -m "Add cool feature").

Push to your fork (git push origin feature/your-idea).

Open a pull request with a description of your changes.

Report bugs or suggest features via issues!
License
This project is licensed under the MIT License (LICENSE). Feel free to use, modify, and distribute it.
Acknowledgments
Built with Python and libraries like colorama, tqdm, and requests.

Inspired by classic shells (Bash, Zsh) and modern CLI tools.

