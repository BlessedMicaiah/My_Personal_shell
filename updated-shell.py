import os
import subprocess
import sys
import shlex
import platform
import signal
import time
from datetime import datetime
from colorama import init, Fore, Back, Style
import pkg_resources
import requests
from tqdm import tqdm

# Loading Bar
def loading_bar(bard, bar_length=50, loading_time=8.0):
    """Display a loading bar in the console."""
    print(f"{Fore.CYAN}{bard}:{Style.RESET_ALL}")
    steps = bar_length * 1
    interval = loading_time / steps
    symbols = ['░', '▒', '▓', '█']

    for step in range(steps + 1):
        progress = step / steps
        completed = int(progress * bar_length)
        loading_bar = ""
        for i in range(bar_length):
            if i < completed - 1:
                loading_bar += f"{Fore.CYAN}{symbols[-1]}{Style.RESET_ALL}"
            elif i == completed - 1:
                loading_bar += f"{Fore.GREEN}{symbols[step % len(symbols)]}{Style.RESET_ALL}"
            else:
                loading_bar += f"{Fore.GREEN}░{Style.RESET_ALL}"
        
        percentage = progress * 100
        sys.stdout.write(f"\r{loading_bar}{Fore.RED}{percentage:5.1f}%{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(interval)
    
    final_bar = f"{Fore.GREEN}{symbols[-1] * bar_length}{Style.RESET_ALL}"
    sys.stdout.write(f"\r{final_bar}{Fore.GREEN} 100.0%{Style.RESET_ALL}\n")
    sys.stdout.flush()

# Initialize colorama for cross-platform color support
init(autoreset=True)

def signal_handler(sig, frame):
    print(f"\n{Fore.RED}Exiting shell...{Style.RESET_ALL}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print(datetime.now().isoformat())

def testo():
    loading_bar("Deploying Warzone Assets", bar_length=50, loading_time=8.0)
    print(f"{Fore.GREEN}Assets Deployed{Style.RESET_ALL}")    

def list_files(path="."):
    try:
        for entry in os.listdir(path):
            if os.path.isdir(os.path.join(path, entry)):
                print(f"{Fore.BLUE}{entry}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}{entry}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error listing files: {e}{Style.RESET_ALL}")

def print_help():
    print(f"{Fore.YELLOW}Shell commands:{Style.RESET_ALL}")
    help_commands = [
        ("cd <path>", "Change directory"),
        ("cd ..", "Go back to the previous directory"),
        ("ls", "List files in the current directory"),
        ("pwd", "Print current working directory"),
        ("mkdir <dir>", "Create a new directory"),
        ("rmdir <dir>", "Remove an empty directory"),
        ("find <name>", "Search for files or directories"),
        ("cls/clear", "Clear the terminal screen"),
        ("help", "Display this help message"),
        ("exit/quit", "Exit the shell"),
        ("sysinfo", "Display system information"),
        ("timestamp", "Print current timestamp"),
        ("history", "Show command history"),
        ("install <pkg>", "Install a package using the system's package manager"),
        ("sudo <command>", "Execute a command with sudo privileges"),
        ("cat <file>", "Display content of a file"),
        ("touch <file>", "Create an empty file"),
        ("rm <file>", "Remove a file"),
        ("vim <file>", "Edit a file with vim"),
        ("devtool <tool>", "Install development tools (vim/mysql/vscode/git)")
    ]
    for cmd, desc in help_commands:
        print(f"  {Fore.CYAN}{cmd}{Style.RESET_ALL:<20} - {desc}")

def system_info():
    print(f"{Fore.MAGENTA}System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Processor: {platform.processor()}")
    print(f"Python Version: {platform.python_version()}{Style.RESET_ALL}")

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
        print(f"{Fore.RED}No supported package manager found.{Style.RESET_ALL}")
        return

    try:
        print(f"{Fore.YELLOW}Using {package_manager} to install {package}...{Style.RESET_ALL}")
        if package_manager in ["apt-get", "yum", "dnf"]:
            subprocess.run(["sudo", package_manager, "update"], check=True)
            subprocess.run(["sudo", package_manager, "install", "-y", package], check=True)
        elif package_manager == "pacman":
            subprocess.run(["sudo", package_manager, "-Sy", package], check=True)
        elif package_manager == "brew":
            subprocess.run(["brew", "install", package], check=True)
        else:
            print(f"{Fore.RED}Unsupported package manager: {package_manager}{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}Successfully installed {package}.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Failed to install {package}: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

def execute_command(command, use_sudo=False):
    try:
        args = shlex.split(command)
        if use_sudo:
            args = ["sudo"] + args
        result = subprocess.run(args, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout:
            print(f"{Fore.GREEN}{result.stdout}{Style.RESET_ALL}", end="")
        if result.stderr:
            print(f"{Fore.RED}{result.stderr}{Style.RESET_ALL}", end="")
    except FileNotFoundError:
        print(f"{Fore.RED}Command not found: {command}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error executing command: {e}{Style.RESET_ALL}")

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
        print(f"{Fore.RED}Error during search: {e}{Style.RESET_ALL}")
    return results

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if platform.system() != 'Windows' else 'cls')

def echo(args):
    print(' '.join(args))

def cat_file(file_name):
    try:
        with open(file_name, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"{Fore.RED}File not found: {file_name}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")

def touch_file(file_name):
    try:
        with open(file_name, 'a'):
            os.utime(file_name, None)
        print(f"{Fore.GREEN}File {file_name} created or updated.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error creating file: {e}{Style.RESET_ALL}")

def remove_file(file_name):
    try:
        os.remove(file_name)
        print(f"{Fore.GREEN}File {file_name} removed.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}File not found: {file_name}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error removing file: {e}{Style.RESET_ALL}")

def edit_file(file_name):
    try:
        subprocess.call(['vim', file_name])
    except FileNotFoundError:
        print(f"{Fore.RED}Vim not found. Please install vim.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error editing file: {e}{Style.RESET_ALL}")

def download_file(url, filename):
    """Download a file from URL with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

def install_development_tool(tool_name):
    """Install common development tools."""
    system = platform.system().lower()
    
    tool_installers = {
        'vim': {
            'linux': lambda: execute_command('sudo apt-get install -y vim'),
            'darwin': lambda: execute_command('brew install vim'),
            'windows': lambda: print(f"{Fore.YELLOW}Please download Vim from: https://www.vim.org/download.php{Style.RESET_ALL}")
        },
        'mysql': {
            'linux': lambda: execute_command('sudo apt-get install -y mysql-server'),
            'darwin': lambda: execute_command('brew install mysql'),
            'windows': lambda: print(f"{Fore.YELLOW}Please download MySQL from: https://dev.mysql.com/downloads/{Style.RESET_ALL}")
        },
        'vscode': {
            'linux': lambda: execute_command('sudo snap install code --classic'),
            'darwin': lambda: execute_command('brew install --cask visual-studio-code'),
            'windows': lambda: print(f"{Fore.YELLOW}Please download VS Code from: https://code.visualstudio.com/download{Style.RESET_ALL}")
        },
        'git': {
            'linux': lambda: execute_command('sudo apt-get install -y git'),
            'darwin': lambda: execute_command('brew install git'),
            'windows': lambda: print(f"{Fore.YELLOW}Please download Git from: https://git-scm.com/download/win{Style.RESET_ALL}")
        }
    }

    if tool_name not in tool_installers:
        print(f"{Fore.RED}Tool '{tool_name}' is not supported. Available tools: {', '.join(tool_installers.keys())}{Style.RESET_ALL}")
        return

    try:
        if system in tool_installers[tool_name]:
            print(f"{Fore.CYAN}Installing {tool_name}...{Style.RESET_ALL}")
            tool_installers[tool_name][system]()
            print(f"{Fore.GREEN}{tool_name} installation completed!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Installation of {tool_name} is not supported on {system}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error installing {tool_name}: {e}{Style.RESET_ALL}")

def main():
    history = []

    while True:
        current_dir = os.getcwd()
        try:
            command = input(f"{Fore.CYAN}{current_dir} $ {Style.RESET_ALL}")
        except EOFError:
            print(f"\n{Fore.RED}Exiting shell...{Style.RESET_ALL}")
            break

        history.append(command)
        args = shlex.split(command)

        if command.lower() in ["exit", "quit"]:
            print(f"{Fore.YELLOW}Exiting shell...{Style.RESET_ALL}")
            break

        if not args:
            continue

        if args[0].lower() in ["exit", "quit"]:
            print(f"{Fore.YELLOW}Exiting shell...{Style.RESET_ALL}")
            break

        if args[0] == "echo":
            echo(args[1:])
            continue

        if command == "clear":
            clear_screen()
            continue

        if command == "cls":
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
                print(f"{Fore.RED}cd: missing argument{Style.RESET_ALL}")
            except FileNotFoundError:
                print(f"{Fore.RED}cd: no such file or directory: {path}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error changing directory: {e}{Style.RESET_ALL}")
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
                print(f"{Fore.GREEN}Directory '{dir_name}' created.{Style.RESET_ALL}")
            except IndexError:
                print(f"{Fore.RED}mkdir: missing directory name{Style.RESET_ALL}")
            except FileExistsError:
                print(f"{Fore.RED}mkdir: cannot create directory '{dir_name}': File exists{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error creating directory: {e}{Style.RESET_ALL}")
            continue

        if command.startswith("rmdir"):
            try:
                dir_name = shlex.split(command)[1]
                os.rmdir(dir_name)
                print(f"{Fore.GREEN}Directory '{dir_name}' removed.{Style.RESET_ALL}")
            except IndexError:
                print(f"{Fore.RED}rmdir: missing directory name{Style.RESET_ALL}")
            except OSError as e:
                print(f"{Fore.RED}rmdir: failed to remove '{dir_name}': {e}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error removing directory: {e}{Style.RESET_ALL}")
            continue

        if command.startswith("find"):
            try:
                name = shlex.split(command)[1]
                results = find_files(name)
                if results:
                    print(f"{Fore.YELLOW}Found the following matches:{Style.RESET_ALL}")
                    for result in results:
                        print(f"{Fore.BLUE}{result}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}No matches found for '{name}'{Style.RESET_ALL}")
            except IndexError:
                print(f"{Fore.RED}find: missing search term{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error during find operation: {e}{Style.RESET_ALL}")
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
            loading_bar("Installing", bar_length=50, loading_time=5.0)
            try:
                package = shlex.split(command)[1]
                install_package(package)
            except IndexError:
                print(f"{Fore.RED}install: missing package name{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error during installation: {e}{Style.RESET_ALL}")
            continue

        if command.startswith("sudo"):
            sudo_command = command[5:].strip()
            execute_command(sudo_command, use_sudo=True)
            continue

        if command.startswith("cat"):
            try:
                cat_file(shlex.split(command)[1])
            except IndexError:
                print(f"{Fore.RED}cat: missing file name{Style.RESET_ALL}")
            continue

        if command.startswith("touch"):
            try:
                touch_file(shlex.split(command)[1])
            except IndexError:
                print(f"{Fore.RED}touch: missing file name{Style.RESET_ALL}")
            continue

        if command.startswith("rm"):
            try:
                remove_file(shlex.split(command)[1])
            except IndexError:
                print(f"{Fore.RED}rm: missing file name{Style.RESET_ALL}")
            continue

        if command.startswith("vim"):
            try:
                edit_file(shlex.split(command)[1])
            except IndexError:
                print(f"{Fore.RED}vim: missing file name{Style.RESET_ALL}")
            continue

        if command.startswith("testo"):
            testo()
            continue

        if command.startswith("devtool"):
            try:
                tool = shlex.split(command)[1]
                install_development_tool(tool)
            except IndexError:
                print(f"{Fore.RED}devtool: missing tool name{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Available tools: vim, mysql, vscode, git{Style.RESET_ALL}")
            continue

        execute_command(command)

if __name__ == "__main__":
    main()