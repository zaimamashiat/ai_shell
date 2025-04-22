import os
import webbrowser
import subprocess
import shutil
import platform
import getpass
import time

# To track the current and previous directories
previous_directory = None

def execute_command(command: str):
    global previous_directory

    command = command.lower().strip()

    # Get the current directory
    current_directory = os.getcwd()

    if "open" in command and "google" in command:
        print("Opening Google...")
        webbrowser.open('https://www.google.com')
    elif 'nlp_cli.py' in sys.argv[0]:
        print("The script is already running. Exiting to prevent infinite terminal openings.")
        sys.exit()

    elif "list all files" in command or "list files" in command:
        print("Listing files in the current directory...")
        files = os.listdir('.')
        for file in files:
            print(file)

    elif "go to" in command:
        folder = command.split("go to")[-1].strip()
        suggested_dirs = auto_suggest_directories(folder)
        if suggested_dirs:
            print("Suggested directories:", ", ".join(suggested_dirs))
            print("You can select one or continue typing.")
        else:
            go_to_folder(folder)

    elif "go back" in command:
        if previous_directory:
            os.chdir(previous_directory)
            print(f"Changed directory back to {previous_directory}")
            previous_directory = os.getcwd()
        else:
            print("No previous directory to go back to.")

    elif "current folder" in command or "where am i" in command:
        print(f"You are currently in: {current_directory}")

    elif "create file" in command:
        print("Please provide the file name:")
        file_name = input("Enter file name: ").strip()
        try:
            with open(file_name, 'w') as file:
                print(f"File '{file_name}' created successfully.")
        except Exception as e:
            print(f"Error creating file: {e}")

    elif "flush dns" in command:
        flush_dns()

    elif "run script" in command:
        print("Please provide the script path:")
        script_path = input("Enter script path: ").strip()
        run_script(script_path)

    elif "help" in command:
        show_help()

    elif "rename file" in command:
        print("Please provide the current file name:")
        current_file_name = input("Enter current file name: ").strip()
        print("Please provide the new file name:")
        new_file_name = input("Enter new file name: ").strip()
        rename_file(current_file_name, new_file_name)

    elif "delete file" in command:
        print("Please provide the file name to delete:")
        file_name = input("Enter file name: ").strip()
        delete_file(file_name)

    elif "create directory" in command:
        print("Please provide the directory name:")
        dir_name = input("Enter directory name: ").strip()
        create_directory(dir_name)

    elif "search file" in command:
        print("Please provide the file name to search for:")
        file_name = input("Enter file name: ").strip()
        search_file(file_name)

    elif "system info" in command:
        display_system_info()

    elif "change permissions" in command:
        print("Please provide the file name:")
        file_name = input("Enter file name: ").strip()
        print("Please provide the new permissions (e.g., '755'):")
        permissions = input("Enter permissions: ").strip()
        change_permissions(file_name, permissions)

    elif "disk usage" in command:
        show_disk_usage()

    elif "backup file" in command:
        print("Please provide the file name to back up:")
        file_name = input("Enter file name: ").strip()
        backup_file(file_name)

    else:
        print("Command not recognized.")
    
    print(f"[Current Directory: {current_directory}] Enter command: ", end="")

def go_to_folder(folder: str):
    global previous_directory
    if os.path.isdir(folder):
        previous_directory = os.getcwd()
        os.chdir(folder)
        print(f"Changed directory to {folder}")
    else:
        print(f"Folder '{folder}' not found!")

def auto_suggest_directories(partial_dir):
    directories = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith(partial_dir)]
    return directories

def flush_dns():
    system_os = os.name
    if system_os == "nt":  # Windows
        try:
            subprocess.run("ipconfig /flushdns", check=True, shell=True)
            print("DNS cache flushed successfully on Windows.")
        except subprocess.CalledProcessError as e:
            print(f"Error flushing DNS: {e}")
    elif system_os == "posix":  # Linux/MacOS
        try:
            subprocess.run("sudo systemd-resolve --flush-caches", check=True, shell=True)
            print("DNS cache flushed successfully on Linux/MacOS.")
        except subprocess.CalledProcessError as e:
            print(f"Error flushing DNS: {e}")
    else:
        print("Unsupported OS for DNS flush.")

def run_script(script_path: str):
    if os.path.exists(script_path) and os.access(script_path, os.X_OK):
        try:
            subprocess.run([script_path], check=True)
            print(f"Script {script_path} ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")
    else:
        print(f"Script {script_path} not found or not executable.")

def show_help():
    help_text = """
Available commands:

1. 'open google' - Opens the Google homepage in a web browser.
2. 'list files' or 'list all files' - Lists all files in the current directory.
3. 'go to <folder_name>' - Navigates to the specified folder.
4. 'go back' - Goes back to the previous directory.
5. 'current folder' or 'where am i' - Displays the current directory.
6. 'create file' - Prompts to create a new file in the current directory.
7. 'flush dns' - Flushes the DNS cache.
8. 'run script' - Runs a specified script by providing its path.
9. 'help' - Displays this help message.
10. 'rename file' - Renames an existing file.
11. 'delete file' - Deletes a specified file.
12. 'create directory' - Creates a new directory.
13. 'search file' - Searches for a specified file.
14. 'system info' - Displays system information.
15. 'change permissions' - Changes file permissions.
16. 'disk usage' - Displays disk usage for the current directory.
17. 'backup file' - Backs up a specified file.
18. 'exit' - Exits the program.
    """
    print(help_text)

def rename_file(current_file_name, new_file_name):
    try:
        os.rename(current_file_name, new_file_name)
        print(f"File renamed from {current_file_name} to {new_file_name}.")
    except FileNotFoundError:
        print(f"File {current_file_name} not found!")
    except Exception as e:
        print(f"Error renaming file: {e}")

def delete_file(file_name):
    try:
        os.remove(file_name)
        print(f"File {file_name} deleted successfully.")
    except FileNotFoundError:
        print(f"File {file_name} not found!")
    except Exception as e:
        print(f"Error deleting file: {e}")

def create_directory(dir_name):
    try:
        os.mkdir(dir_name)
        print(f"Directory '{dir_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{dir_name}' already exists.")
    except Exception as e:
        print(f"Error creating directory: {e}")

def search_file(file_name):
    files = os.listdir('.')
    if file_name in files:
        print(f"File '{file_name}' found in the current directory.")
    else:
        print(f"File '{file_name}' not found.")

def display_system_info():
    print(f"Operating System: {platform.system()} {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"User: {getpass.getuser()}")
    print(f"Processor: {platform.processor()}")

def change_permissions(file_name, permissions):
    try:
        os.chmod(file_name, int(permissions, 8))  # Permissions in octal format
        print(f"Permissions for {file_name} changed to {permissions}.")
    except FileNotFoundError:
        print(f"File {file_name} not found!")
    except ValueError:
        print("Invalid permissions format. Use octal format (e.g., 755).")
    except Exception as e:
        print(f"Error changing permissions: {e}")

def show_disk_usage():
    total, used, free = shutil.disk_usage(".")
    print(f"Disk usage for the current directory:")
    print(f"Total: {total // (2**30)} GiB")
    print(f"Used: {used // (2**30)} GiB")
    print(f"Free: {free // (2**30)} GiB")

def backup_file(file_name):
    if os.path.exists(file_name):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_name = f"{file_name}_{timestamp}.bak"
        shutil.copy(file_name, backup_name)
        print(f"File backed up as {backup_name}.")
    else:
        print(f"File {file_name} not found!")

# Function to open in a new terminal window and execute the script
def open_in_new_window(script_name):
    if os.name == 'nt':  # Windows
        subprocess.Popen(["start", "cmd", "/K", f"python {script_name}"], shell=True)
    elif os.name == 'posix':  # Linux/Mac
        try:
            subprocess.Popen(["gnome-terminal", "--", "python3", script_name])  # Linux GNOME terminal
        except FileNotFoundError:
            try:
                subprocess.Popen(["xterm", "-e", f"python3 {script_name}"])  # Linux Xterm
            except FileNotFoundError:
                subprocess.Popen(["osascript", "-e", f'tell application "Terminal" to do script "python3 {script_name}"'])  # macOS
        except Exception as e:
            subprocess.Popen(["osascript", "-e", f'tell application "Terminal" to do script "python3 {script_name}"'])  # Fallback for macOS
    else:
        print("Unsupported OS for opening a new terminal window.")

if __name__ == "__main__":
    script_name = "nlp_cli.py"  # Replace this with the actual name of the script
    open_in_new_window(script_name)

    current_directory = os.getcwd()
    print(f"[Current Directory: {current_directory}] Enter command: ", end="")

    while True:
        user_input = input()
        if user_input.lower() == "exit":
            break
        execute_command(user_input)
