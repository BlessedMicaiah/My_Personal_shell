import os
import subprocess
import sys
import shlex
import platform
import signal
from datetime import datetime

def signal_handler(sig, frame):
    print("\nExiting shell...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def list_files(path="."):
    try:
        for entry in os.listdir(path):
            print(entry)
    except Exception as e:
        print(f"Error listing files: {e}")

def print_help():
    print("Shell commands:")
    print("  cd <path>        - Change directory")
    print("  cd ..            - Go back to the previous directory")
    print("  ls               - List files in the current directory")
    print("  pwd              - Print current working directory")
    print("  mkdir <dir>      - Create a new directory")
    print("  rmdir <dir>      - Remove an empty directory")
    print("  find <name>      - Search for files or directories")
    print("  clear            - Clear the terminal screen")
    print("  help             - Display this help message")
    print("  exit/quit        - Exit the shell")
    print("  sysinfo          - Display system information")
    print("  timestamp        - Print current timestamp")
    print("  history          - Show command history")
    print("  install <pkg>    - Install a package using the system's package manager")
    print("  sudo <command>   - Execute a command with sudo privileges")

def system_info():
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Processor: {platform.processor()}")
    print(f"Python Version: {platform.python_version()}")

def detect_package_manager():
    if platform.system() == "Linux":
        for manager in ["apt-get", "yum", "dnf", "pacman"]:
            if subprocess.run(["which", manager], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                return manager
    elif platform.system() == "Darwin":
        if subprocess.run(["which", "brew"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            return "brew"
    return None

def install_package(package):
    package_manager = detect_package_manager()
    if not package_manager:
        print("No supported package manager found.")
        return

    try:
        print(f"Using {package_manager} to install {package}...")
        if package_manager in ["apt-get", "yum", "dnf"]:
            subprocess.run(["sudo", package_manager, "update"], check=True)
            subprocess.run(["sudo", package_manager, "install", "-y", package], check=True)
        elif package_manager == "pacman":
            subprocess.run(["sudo", package_manager, "-Sy", package], check=True)
        elif package_manager == "brew":
            subprocess.run(["brew", "install", package], check=True)
        else:
            print(f"Unsupported package manager: {package_manager}")
            return
        print(f"Successfully installed {package}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def execute_command(command, use_sudo=False):
    try:
        args = shlex.split(command)
        if use_sudo:
            args = ["sudo"] + args
        result = subprocess.run(args, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")
    except FileNotFoundError:
        print(f"Command not found: {command}")
    except Exception as e:
        print(f"Error executing command: {e}")

def find_files(name, path="."):
    results = []
    try:
        for root, dirs, files in os.walk(path):
            if name in dirs:
                results.append(os.path.join(root, name))
            for file in files:
                if name in file:
                    results.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error during search: {e}")
    return results

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if platform.system() != 'Windows' else 'cls')

def echo(args):
    print(' '.join(args))

def main():
    history = []

    while True:
        current_dir = os.getcwd()
        try:
            command = input(f"{current_dir} $ ")
        except EOFError:
            print("\nExiting shell...")
            break

        history.append(command)
        args = shlex.split(command)

        if command.lower() in ["exit", "quit"]:
            print("Exiting shell...")
            break

        if not args:
            continue

        if args[0].lower() in ["exit", "quit"]:
            print("Exiting shell...")
            break

        if args[0] == "echo":
            echo(args[1:])
            continue

        if command == "clear":
            clear_screen()
            continue

        if command.startswith("cd"):
            try:
                path = shlex.split(command)[1]
                if path == "..":
                    os.chdir(os.path.dirname(current_dir))
                else:
                    os.chdir(path)
            except IndexError:
                print("cd: missing argument")
            except FileNotFoundError:
                print(f"cd: no such file or directory: {path}")
            except Exception as e:
                print(f"Error changing directory: {e}")
            continue

        if command == "ls":
            list_files()
            continue

        if command == "pwd":
            print(current_dir)
            continue

        if command.startswith("mkdir"):
            try:
                dir_name = shlex.split(command)[1]
                os.mkdir(dir_name)
                print(f"Directory '{dir_name}' created.")
            except IndexError:
                print("mkdir: missing directory name")
            except FileExistsError:
                print(f"mkdir: cannot create directory '{dir_name}': File exists")
            except Exception as e:
                print(f"Error creating directory: {e}")
            continue

        if command.startswith("rmdir"):
            try:
                dir_name = shlex.split(command)[1]
                os.rmdir(dir_name)
                print(f"Directory '{dir_name}' removed.")
            except IndexError:
                print("rmdir: missing directory name")
            except OSError as e:
                print(f"rmdir: failed to remove '{dir_name}': {e}")
            except Exception as e:
                print(f"Error removing directory: {e}")
            continue

        if command.startswith("find"):
            try:
                name = shlex.split(command)[1]
                results = find_files(name)
                if results:
                    print("Found the following matches:")
                    for result in results:
                        print(result)
                else:
                    print(f"No matches found for '{name}'")
            except IndexError:
                print("find: missing search term")
            except Exception as e:
                print(f"Error during find operation: {e}")
            continue

        if command == "help":
            print_help()
            continue

        if command == "sysinfo":
            system_info()
            continue

        if command == "timestamp":
            print(datetime.now().isoformat())
            continue

        if command == "history":
            for i, cmd in enumerate(history):
                print(f"{i + 1}: {cmd}")
            continue

        if command.startswith("install"):
            try:
                package = shlex.split(command)[1]
                install_package(package)
            except IndexError:
                print("install: missing package name")
            except Exception as e:
                print(f"Error during installation: {e}")
            continue

        if command.startswith("sudo"):
            sudo_command = command[5:].strip()
            execute_command(sudo_command, use_sudo=True)
            continue

        execute_command(command)

if __name__ == "__main__":
    main()
