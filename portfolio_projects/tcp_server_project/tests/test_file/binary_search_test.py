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

def binary_search(file_path: str, search_string: str) -> bool:
    """Binary search for a string in a sorted file."""
    start_time = time.time()
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    left, right = 0, len(lines) - 1
    while left <= right:
        mid = (left + right) // 2
        if search_string == lines[mid].strip():
            print(f"Found {search_string} using Binary Search.")
            print(f"Execution time: {time.time() - start_time} seconds")
            return True
        elif search_string < lines[mid].strip():
            right = mid - 1
        else:
            left = mid + 1
    print(f"{search_string} not found.")
    print(f"Execution time: {time.time() - start_time} seconds")
    return False

if __name__ == "__main__":
    search_string = input("Enter the string to search: ")
    binary_search(file_path, search_string)