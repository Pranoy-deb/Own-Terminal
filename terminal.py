import os
import socket
import sys
import subprocess
from colorama import Fore, Style
import platform
import psutil
import time
import shutil
import getpass


# Import pwd and grp only on Unix-like systems
if os.name != "nt":
    import pwd
    import grp

# Global variable to track if the user is in "root mode"
is_root_mode = False

def print_prompt():
    """Displays the custom terminal prompt."""
    hostname = socket.gethostname()
    cwd = os.getcwd()

    # Change the prompt if in root mode
    if is_root_mode:
        prompt = (
            f"{Fore.GREEN}┏━({Fore.RED}AN0NYM0U5{Fore.YELLOW}@{Fore.RED}{hostname}{Fore.GREEN})\n"
            f"┃ 📁 {Fore.GREEN}{cwd}\n"
            f"┗▶ $#$ {Style.RESET_ALL}"
        )
    else:
        prompt = (
            f"{Fore.GREEN}┏━({Fore.RED}AN0NYM0U5{Fore.YELLOW}@{Fore.RED}{hostname}{Fore.GREEN})\n"
            f"┃ 📁 {Fore.GREEN}{cwd}\n"
            f"┗▶ $ {Style.RESET_ALL}"
        )
    print(prompt, end="")

def clear_screen():
    """Clears the terminal screen without exiting."""
    os.system("cls" if os.name == "nt" else "clear")

def list_directory():
    """Lists all files and folders in the current directory (like ls or dir)."""
    for item in os.listdir():
        print(item)

def change_directory(command):
    """Changes the directory like the cd command."""
    stripped = command[3:].strip()  # Remove 'cd ' from beginning
    path = stripped.strip('"').strip("'")  # Remove surrounding quotes if any

    if not path:
        # Just 'cd' shows current directory
        print(os.getcwd())
        return
    
    if path == "..":
        os.chdir("..")
        return

    if path.lower().startswith("/d ") and os.name == "nt":
        drive_path = path[3:].strip()
        try:
            os.chdir(drive_path + "\\")
        except FileNotFoundError:
            print(f"Error: Drive '{drive_path}' not found.")
        return

    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"Error: Directory '{path}' not found.")
    except NotADirectoryError:
        print(f"Error: '{path}' is not a directory.")
    except OSError as e:
        print(f"OSError: {e}")

# 
def run_python_interactive():
    """Runs an interactive Python shell inside the custom terminal."""
    print(f"{Fore.YELLOW}Entering Python interactive mode. Type 'exit()' or 'Ctrl+D' to return.{Style.RESET_ALL}")
    try:
        subprocess.run([sys.executable], check=False)
    except KeyboardInterrupt:
        print("\nExiting Python interactive mode.")

def run_python_script(command):
    """Runs a Python script or handles Python-related commands.
    
    Supports:
    - python script.py [args]
    - python --version/-v
    - python -m module [args]
    """
    parts = command.split()
    
    # Handle version check requests
    if len(parts) > 1 and parts[1] in ["--version", "-v", "-version"]:
        run_python_version()
        return
    
    # Handle module execution (python -m module)
    if len(parts) > 2 and parts[1] == "-m":
        try:
            subprocess.run([sys.executable, "-m", parts[2]] + parts[3:])
        except Exception as e:
            print(f"Error executing module: {e}")
        return
    
    # Handle normal script execution
    if len(parts) < 2:
        print("Usage: python <script.py> [args] or python -m <module> [args]")
        return
    
    script_name = parts[1]
    
    if not os.path.exists(script_name):
        print(f"Error: File '{script_name}' not found.")
        return
    
    try:
        # Run the script with any additional arguments
        subprocess.run([sys.executable, script_name] + parts[2:], check=False)
    except Exception as e:
        print(f"Error executing script: {e}")


def run_python_version():
    """Show Python version using subprocess to get accurate version info."""
    try:
        subprocess.run([sys.executable, "--version"])
    except Exception as e:
        print(f"Error checking Python version: {e}")

def execute_network_command(command):
    """Executes network-related commands."""
    parts = command.split()

    if parts[0] == "ipconfig" and os.name == "nt":
        subprocess.run(["ipconfig"])
    elif parts[0] == "ifconfig" and os.name != "nt":
        subprocess.run(["ifconfig"])
    elif parts[0] == "ping" and len(parts) > 1:
        subprocess.run(["ping", parts[1]])
    elif parts[0] in ["tracert", "traceroute"]:
        subprocess.run(["tracert" if os.name == "nt" else "traceroute", parts[1]])
    elif parts[0] == "netstat":
        subprocess.run(["netstat"])
    elif parts[0] == "nslookup" and len(parts) > 1:
        subprocess.run(["nslookup", parts[1]])
    elif parts[0] == "hostname":
        subprocess.run(["hostname"])
    else:
        print("Unknown network command.")

def show_system_info():
    """Show system information (OS, kernel, architecture)."""
    print(f"System: {platform.system()}")
    print(f"Node Name: {platform.node()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

def show_current_user():
    """Show the current user."""
    print(f"Current User: {os.getlogin()}")

def show_uptime():
    """Show how long the system has been running."""
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_hours = uptime_seconds // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60
    print(f"Uptime: {int(uptime_hours)} hours, {int(uptime_minutes)} minutes")

def show_disk_usage():
    """Show disk space usage."""
    disk_usage = psutil.disk_usage('/')
    print(f"Total: {disk_usage.total // (1024 ** 3)} GB")
    print(f"Used: {disk_usage.used // (1024 ** 3)} GB")
    print(f"Free: {disk_usage.free // (1024 ** 3)} GB")
    print(f"Usage: {disk_usage.percent}%")

def show_memory_usage():
    """Show memory usage."""
    memory = psutil.virtual_memory()
    print(f"Total: {memory.total // (1024 ** 2)} MB")
    print(f"Available: {memory.available // (1024 ** 2)} MB")
    print(f"Used: {memory.used // (1024 ** 2)} MB")
    print(f"Usage: {memory.percent}%")

def show_running_processes():
    """Show running processes."""
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        print(proc.info)

def create_file(file_name):
    """Create an empty file."""
    try:
        with open(file_name, 'w'):
            pass
        print(f"File '{file_name}' created.")
    except Exception as e:
        print(f"Error creating file: {e}")

def create_directory(directory_name):
    """Create a new directory."""
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created.")
    except FileExistsError:
        print(f"Error: Directory '{directory_name}' already exists.")
    except Exception as e:
        print(f"Error creating directory: {e}")

def delete_file(file_name):
    """Delete a file."""
    try:
        os.remove(file_name)
        print(f"File '{file_name}' deleted.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"Error deleting file: {e}")

def delete_empty_directory(directory_name):
    """Delete an empty directory."""
    try:
        os.rmdir(directory_name)
        print(f"Directory '{directory_name}' deleted.")
    except FileNotFoundError:
        print(f"Error: Directory '{directory_name}' not found.")
    except OSError:
        print(f"Error: Directory '{directory_name}' is not empty.")
    except Exception as e:
        print(f"Error deleting directory: {e}")

def delete_directory_recursive(directory_name):
    """Delete a directory and its contents recursively."""
    try:
        shutil.rmtree(directory_name)
        print(f"Directory '{directory_name}' and its contents deleted.")
    except FileNotFoundError:
        print(f"Error: Directory '{directory_name}' not found.")
    except Exception as e:
        print(f"Error deleting directory: {e}")

def move_file_or_directory(source, destination):
    """Move or rename a file or directory."""
    try:
        shutil.move(source, destination)
        print(f"Moved '{source}' to '{destination}'.")
    except FileNotFoundError:
        print(f"Error: Source '{source}' not found.")
    except Exception as e:
        print(f"Error moving file/directory: {e}")

def copy_file_or_directory(source, destination):
    """Copy a file or directory."""
    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        print(f"Copied '{source}' to '{destination}'.")
    except FileNotFoundError:
        print(f"Error: Source '{source}' not found.")
    except Exception as e:
        print(f"Error copying file/directory: {e}")

def show_file_contents(file_name):
    """Show the contents of a file."""
    try:
        with open(file_name, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

def write_to_file(file_name, text):
    """Write text to a file."""
    try:
        with open(file_name, 'w') as file:
            file.write(text)
        print(f"Text written to '{file_name}'.")
    except Exception as e:
        print(f"Error writing to file: {e}")

def list_block_devices():
    """List all block devices (like lsblk)."""
    if os.name == "nt":
        print("'lsblk' is not supported on Windows. Use 'wmic logicaldisk get' instead.")
    else:
        try:
            subprocess.run(["lsblk"])
        except FileNotFoundError:
            print("'lsblk' command not found. Ensure it is installed on your system.")

def show_directory_size(path):
    """Show the size of a directory."""
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        print(f"Size of '{path}': {total_size // (1024 ** 2)} MB")
    except FileNotFoundError:
        print(f"Error: Path '{path}' not found.")
    except Exception as e:
        print(f"Error calculating directory size: {e}")

def show_mounted_filesystems():
    """Show mounted file systems."""
    if os.name == "nt":
        print("'mount' is not supported on Windows. Use 'wmic logicaldisk get' instead.")
    else:
        try:
            subprocess.run(["mount"])
        except FileNotFoundError:
            print("'mount' command not found. Ensure it is installed on your system.")

def unmount_device(device):
    """Unmount a drive (Linux/macOS only)."""
    if os.name == "nt":
        print("'umount' is not supported on Windows.")
    else:
        try:
            subprocess.run(["umount", device])
            print(f"Device '{device}' unmounted.")
        except FileNotFoundError:
            print("'umount' command not found. Ensure it is installed on your system.")
        except Exception as e:
            print(f"Error unmounting device: {e}")

def list_windows_drives():
    """List drives (Windows only)."""
    if os.name == "nt":
        try:
            subprocess.run(["wmic", "logicaldisk", "get"])
        except FileNotFoundError:
            print("'wmic' command not found. Ensure it is available on your system.")
    else:
        print("'wmic' is only supported on Windows.")

def check_disk_health(drive):
    """Check disk health (Windows only)."""
    if os.name == "nt":
        try:
            subprocess.run(["chkdsk", drive])
        except FileNotFoundError:
            print("'chkdsk' command not found. Ensure it is available on your system.")
    else:
        print("'chkdsk' is only supported on Windows.")

def show_user_and_group_ids():
    """Displays user and group IDs (Linux/macOS only)."""
    if os.name == "nt":
        print("'id' is not supported on Windows.")
    else:
        try:
            subprocess.run(["id"])
        except FileNotFoundError:
            print("'id' command not found. Ensure it is installed on your system.")

def show_user_groups():
    """Lists all groups the user belongs to (Linux/macOS only)."""
    if os.name == "nt":
        print("'groups' is not supported on Windows.")
    else:
        try:
            subprocess.run(["groups"])
        except FileNotFoundError:
            print("'groups' command not found. Ensure it is installed on your system.")

def change_file_permissions(permissions, file_name):
    """Changes file permissions (Linux/macOS only)."""
    if os.name == "nt":
        print("'chmod' is not supported on Windows.")
    else:
        try:
            os.chmod(file_name, int(permissions, 8))
            print(f"Permissions of '{file_name}' changed to {permissions}.")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except Exception as e:
            print(f"Error changing permissions: {e}")

def change_file_ownership(user_group, file_name):
    """Changes file ownership (Linux/macOS only)."""
    if os.name == "nt":
        print("'chown' is not supported on Windows.")
    else:
        try:
            user, group = user_group.split(":")
            uid = pwd.getpwnam(user).pw_uid
            gid = grp.getgrnam(group).gr_gid
            os.chown(file_name, uid, gid)
            print(f"Ownership of '{file_name}' changed to {user}:{group}.")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except KeyError:
            print(f"Error: User or group not found.")
        except Exception as e:
            print(f"Error changing ownership: {e}")

def change_user_password():
    """Allows user to change their password (Linux/macOS only)."""
    if os.name == "nt":
        print("'password' is not supported on Windows.")
    else:
        try:
            subprocess.run(["passwd"])
        except FileNotFoundError:
            print("'passwd' command not found. Ensure it is installed on your system.")
        except Exception as e:
            print(f"Error changing password: {e}")

def simulate_sudo(command):
    """Simulates running a command as an administrator (Linux/macOS only)."""
    if os.name == "nt":
        print("'sudo' is not supported on Windows.")
    else:
        try:
            subprocess.run(["sudo"] + command.split())
        except FileNotFoundError:
            print("'sudo' command not found. Ensure it is installed on your system.")
        except Exception as e:
            print(f"Error running command with sudo: {e}")

def list_windows_users():
    """Lists all user accounts (Windows only)."""
    if os.name == "nt":
        try:
            subprocess.run(["net", "user"])
        except FileNotFoundError:
            print("'net' command not found. Ensure it is available on your system.")
    else:
        print("'net user' is only supported on Windows.")

def list_windows_admin_users():
    """Lists admin users (Windows only)."""
    if os.name == "nt":
        try:
            subprocess.run(["net", "localgroup", "administrators"])
        except FileNotFoundError:
            print("'net' command not found. Ensure it is available on your system.")
    else:
        print("'net localgroup administrators' is only supported on Windows.")

def go_to_root():
    """Simulates 'sudo su' by toggling root mode."""
    global is_root_mode
    is_root_mode = not is_root_mode  # Toggle root mode
    if is_root_mode:
        print(f"{Fore.YELLOW}Entered root mode. Commands will not actually execute as root.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Exited root mode.{Style.RESET_ALL}")

# Execite All git Command 
def execute_git_command(command):
    """Executes Git commands."""
    parts = command.strip().split()

    if parts[0] != "git":
        print("Unknown command.")
        return

    if len(parts) == 1:
        print("Usage: git <command>")
        return

    git_command = parts[1]

    if git_command in ["--version", "-v"]:
        subprocess.run(["git", "--version"])
    elif git_command == "init":
        subprocess.run(["git", "init"])
    elif git_command == "clone" and len(parts) > 2:
        subprocess.run(["git", "clone", parts[2]])
    elif git_command == "status":
        subprocess.run(["git", "status"])
    elif git_command == "add" and len(parts) > 2:
        subprocess.run(["git", "add"] + parts[2:])
    elif git_command == "commit" and "-m" in parts:
        message_index = parts.index("-m") + 1
        message = " ".join(parts[message_index:])
        subprocess.run(["git", "commit", "-m", message])
    elif git_command == "log":
        subprocess.run(["git", "log"])
    elif git_command == "branch":
        subprocess.run(parts)
    elif git_command == "checkout" and len(parts) > 2:
        subprocess.run(["git", "checkout", parts[2]])
    elif git_command == "merge" and len(parts) > 2:
        subprocess.run(["git", "merge", parts[2]])
    elif git_command == "pull":
        subprocess.run(["git", "pull"])
    elif git_command == "push":
        subprocess.run(["git", "push"])
    elif git_command == "remote" and "-v" in parts:
        subprocess.run(["git", "remote", "-v"])
    elif git_command == "reset" and "--hard" in parts:
        subprocess.run(["git", "reset", "--hard", "HEAD"])
    elif git_command == "stash":
        subprocess.run(parts)
    else:
        print("Unknown Git command.")

def open_application(app_name):
    """Opens an application by its name."""
    try:
        if os.name == "nt":  # Windows
            subprocess.Popen([app_name], shell=True)
        else:  # Linux/macOS
            subprocess.Popen([app_name])
        print(f"Opened {app_name}.")
    except FileNotFoundError:
        print(f"Error: Application '{app_name}' not found.")
    except Exception as e:
        print(f"Error opening application: {e}")

def close_application(app_name):
    """Closes an application by its name."""
    try:
        if os.name == "nt":  # Windows
            os.system(f"taskkill /f /im {app_name}")
        else:  # Linux/macOS
            os.system(f"pkill {app_name}")
        print(f"Closed {app_name}.")
    except Exception as e:
        print(f"Error closing application: {e}")

def laravel_artisan_command(command):
    """Executes Laravel Artisan commands."""
    parts = command.split()

    if parts[0] == "artisan":
        if len(parts) == 1:
            print("Usage: artisan <command>")
            return

        artisan_command = parts[1]

        if artisan_command == "list":
            subprocess.run(["php", "artisan", "list"])
        elif artisan_command == "make:model" and len(parts) > 2:
            subprocess.run(["php", "artisan", "make:model", parts[2]])
        elif artisan_command == "make:controller" and len(parts) > 2:
            subprocess.run(["php", "artisan", "make:controller", parts[2]])
        elif artisan_command == "make:migration" and len(parts) > 2:
            subprocess.run(["php", "artisan", "make:migration", parts[2]])
        elif artisan_command == "migrate":
            subprocess.run(["php", "artisan", "migrate"])
        elif artisan_command == "serve":
            subprocess.run(["php", "artisan", "serve"])
        elif artisan_command == "tinker":
            subprocess.run(["php", "artisan", "tinker"])
        elif artisan_command == "cache:clear":
            subprocess.run(["php", "artisan", "cache:clear"])
        elif artisan_command == "config:cache":
            subprocess.run(["php", "artisan", "config:cache"])
        elif artisan_command == "queue:work":
            subprocess.run(["php", "artisan", "queue:work"])
        elif artisan_command == "db:seed":
            subprocess.run(["php", "artisan", "db:seed"])
        elif artisan_command == "route:list":
            subprocess.run(["php", "artisan", "route:list"])
        elif artisan_command == "schedule:run":
            subprocess.run(["php", "artisan", "schedule:run"])
        else:
            print("Unknown Artisan command.")
    else:
        print("Unknown command.")

def run_terminal():
    """Runs an interactive Python-based terminal emulator."""
    global is_root_mode
    while True:
        print_prompt()
        cmd = input().strip()  # Get user input
        cmd_lower = cmd.lower()

        if cmd.lower() == "exit":
            print("Exiting terminal...")
            sys.exit()  # Exit the program

        elif cmd in ["ls", "dir"]:
            list_directory()

        elif cmd.startswith("cd"):
            change_directory(cmd)

        elif cmd.lower() == "clear":
            clear_screen()  # Clear the screen

        elif cmd.lower() == "python":
            run_python_interactive()  # Start Python interactive mode

        elif cmd.startswith("python "):
            run_python_script(cmd)  # Run a Python script

        elif cmd_lower in ["python --version", "py --version", "python -v", "python -version", "python3 -v", "python3 -version"]:
            run_python_version()

        elif cmd.split()[0] in ["ipconfig", "ifconfig", "ping", "tracert", "traceroute", "netstat", "nslookup", "hostname"]:
            execute_network_command(cmd)  # Handle network commands

        elif cmd == "uname":
            show_system_info()  # Show system information

        elif cmd == "whoami":
            show_current_user()  # Show current user

        elif cmd == "uptime":
            show_uptime()  # Show system uptime

        elif cmd == "df -h":
            show_disk_usage()  # Show disk space usage

        elif cmd == "free -m":
            show_memory_usage()  # Show memory usage

        elif cmd == "ps aux":
            show_running_processes()  # Show running processes

        elif cmd.startswith("mf "):
            create_file(cmd.split()[1])  # Create an empty file

        elif cmd.startswith("mkdir "):
            create_directory(cmd.split()[1])  # Create a new directory

        elif cmd.startswith("rm "):
            if len(cmd.split()) == 2:
                delete_file(cmd.split()[1])  # Delete a file
            elif len(cmd.split()) == 3 and cmd.split()[1] == "-r":
                delete_directory_recursive(cmd.split()[2])  # Delete a directory recursively

        elif cmd.startswith("rmdir "):
            delete_empty_directory(cmd.split()[1])  # Delete an empty directory

        elif cmd.startswith("mv "):
            parts = cmd.split()
            if len(parts) == 3:
                move_file_or_directory(parts[1], parts[2])  # Move/rename a file or directory

        elif cmd.startswith("cp "):
            parts = cmd.split()
            if len(parts) == 3:
                copy_file_or_directory(parts[1], parts[2])  # Copy a file or directory

        elif cmd.startswith("cat "):
            show_file_contents(cmd.split()[1])  # Show file contents

        elif cmd.startswith("echo ") and ">" in cmd:
            parts = cmd.split(">")
            text = parts[0].replace("echo", "").strip().strip('"')
            file_name = parts[1].strip()
            write_to_file(file_name, text)  # Write text to a file

        elif cmd == "lsblk":
            list_block_devices()  # List block devices

        elif cmd.startswith("du -sh "):
            show_directory_size(cmd.split()[2])  # Show directory size

        elif cmd == "mount":
            show_mounted_filesystems()  # Show mounted file systems

        elif cmd.startswith("umount "):
            unmount_device(cmd.split()[1])  # Unmount a device

        elif cmd == "wmic logicaldisk get":
            list_windows_drives()  # List drives (Windows only)

        elif cmd.startswith("chkdsk "):
            check_disk_health(cmd.split()[1])  # Check disk health (Windows only)

        elif cmd == "id":
            show_user_and_group_ids()  # Show user and group IDs

        elif cmd == "groups":
            show_user_groups()  # Show user groups

        elif cmd.startswith("chmod "):
            parts = cmd.split()
            if len(parts) == 3:
                change_file_permissions(parts[1], parts[2])  # Change file permissions

        elif cmd.startswith("chown "):
            parts = cmd.split()
            if len(parts) == 3:
                change_file_ownership(parts[1], parts[2])  # Change file ownership

        elif cmd == "password":
            change_user_password()  # Change user password

        elif cmd.startswith("sudo "):
            simulate_sudo(cmd[5:])  # Simulate sudo

        elif cmd == "net user":
            list_windows_users()  # List Windows users

        elif cmd == "net localgroup administrators":
            list_windows_admin_users()  # List Windows admin users

        elif cmd == "sudo su" or cmd == "go to root":
            go_to_root()  # Toggle root mode

        elif cmd.lower().startswith("git "):
            execute_git_command(cmd) # Execute Git commands

        elif cmd.startswith("open "):
            open_application(cmd.split()[1])  # Open an application

        elif cmd.startswith("close "):
            close_application(cmd.split()[1])  # Close an application

        elif cmd.startswith("artisan "):
                laravel_artisan_command(cmd.split(" ", 1)[1])

        else:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                output = result.stdout.strip() or result.stderr.strip()
                print(output)
            except Exception as e:
                print(f"Error running command: {e}")
# Run the terminal
run_terminal()