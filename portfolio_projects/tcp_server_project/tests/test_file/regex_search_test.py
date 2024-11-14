import re
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

def regex_search(file_path: str, pattern: str) -> bool:
    """Search for a regex pattern in a file."""
    start_time = time.time()
    compiled_pattern = re.compile(pattern)
    with open(file_path, 'r') as file:
        for line in file:
            if compiled_pattern.search(line):
                print(f"Pattern {pattern} found using Regex Search.")
                print(f"Execution time: {time.time() - start_time} seconds")
                return True
    print(f"Pattern {pattern} not found.")
    print(f"Execution time: {time.time() - start_time} seconds")
    return False

if __name__ == "__main__":
    search_string = input("Enter the string to search: ")
    regex_search(file_path, search_string)