import configparser
import os
import time

# Load configuration settings from config.txt
config = configparser.ConfigParser()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to config.txt relative to the script's directory
config_path = os.path.join(script_dir, '..', 'config.txt')
config.read(config_path)

# Extract the file path from the config file
file_path = config.get('DEFAULT', 'linuxpath')

def linear_search(file_path: str, search_string: str) -> bool:
    """Linear search for a string in a file."""
    start_time = time.time()
    with open(file_path, 'r') as file:
        for line in file:
            if search_string in line:
                print(f"Found '{search_string}' using Linear Search.")
                print(f"Execution time: {time.time() - start_time:.6f} seconds")
                return True
    print(f"'{search_string}' not found.")
    print(f"Execution time: {time.time() - start_time:.6f} seconds")
    return False

if __name__ == "__main__":
    search_string = input("Enter the string to search: ")
    linear_search(file_path, search_string)
