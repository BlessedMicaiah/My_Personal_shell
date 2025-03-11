# Stylish Shell README

## Overview

Welcome to My\_Personal\_shell! This repository contains a custom Python-based shell I’ve built to enhance my command-line experience. It’s a lightweight, cross-platform shell with colorful output, useful commands, and automation features. Whether you’re here to explore, adapt, or contribute, I hope you find it valuable! Overview My\_Personal\_shell is a Python script that implements a custom command-line interface. It supports common shell commands (e.g., cd, ls, mkdir), system utilities, package management, and even a fancy loading bar for visual feedback. Built with cross-platform compatibility in mind, it runs on Linux, macOS, and Windows, leveraging libraries like colorama for colored output and tqdm for progress bars. Features Colorful Interface: Uses colorama for cross-platform colored terminal output (e.g., blue directories, green files).

## Features

- 🎨 **Colorful Terminal Output**: Enhanced readability with color-coded text.
- 🖥️ **Interactive Shell**: Supports commands like `cd`, `ls`, `pwd`, and more.
- 🏗️ **System Information**: Displays OS details, architecture, and Python version.
- 📂 **File Management**: Create, remove, and edit files with commands like `touch`, `rm`, and `vim`.
- 📦 **Package Management**: Installs packages using the system's package manager.
- 🚀 **Development Tools**: Quickly install tools like Vim, MySQL, VS Code, and Git.
- ⏳ **Loading Bar**: Provides visual feedback during installations.

## Installation

Ensure you have Python installed. Then, install the required dependencies using:

```sh
pip install colorama tqdm requests
```

## Usage

Run the script to start an interactive shell:

```sh
python script.py
```

## Available Commands

| Command          | Description                              |
| ---------------- | ---------------------------------------- |
| `cd <path>`      | 🔄 Change directory                      |
| `ls`             | 📋 List files in the current directory   |
| `pwd`            | 📍 Print working directory               |
| `mkdir <dir>`    | 📂 Create a new directory                |
| `rmdir <dir>`    | 🗑️ Remove an empty directory            |
| `find <name>`    | 🔎 Search for files or directories       |
| `clear`          | 🧹 Clear the terminal screen             |
| `sysinfo`        | 🏗️ Display system information           |
| `timestamp`      | ⏰ Print current timestamp                |
| `history`        | 📜 Show command history                  |
| `install <pkg>`  | 📦 Install a package                     |
| `sudo <command>` | ⚡ Execute a command with sudo privileges |
| `cat <file>`     | 📄 Display file contents                 |
| `touch <file>`   | 📝 Create an empty file                  |
| `rm <file>`      | 🗑️ Remove a file                        |
| `vim <file>`     | ✏️ Edit a file with Vim                  |
| `devtool <tool>` | 🛠️ Install development tools            |

## Example Usage

```sh
$ ls
📂 Documents  📂 Downloads  📄 script.py

$ sysinfo
🏗️ System: Linux
🏷️ Release: Ubuntu 20.04
🖥️ Processor: x86_64
🐍 Python Version: 3.8
```

## Contributions

Feel free to submit issues or pull requests to enhance functionality.

## License

This project is licensed under the MIT License.

