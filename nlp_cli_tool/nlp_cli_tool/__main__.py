import os
from nlp_cli_tool import execute_command  # Import the function from the package

def main():
    while True:
        # Use f-string for dynamic directory path
        user_input = input(f"[Current Directory: {os.getcwd()}] Enter command: ")
        if user_input.lower() == "exit":
            break
        execute_command(user_input)
