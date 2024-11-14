import mmap
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

def mmap_search(file_path: str, search_string: str) -> bool:
    """Memory-mapped search for a string in a file."""
    start_time = time.time()
    with open(file_path, 'r') as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            if mmap_obj.find(search_string.encode()) != -1:
                print(f"Found {search_string} using Memory-Mapped Search.")
                print(f"Execution time: {time.time() - start_time} seconds")
                return True
    print(f"{search_string} not found.")
    print(f"Execution time: {time.time() - start_time} seconds")
    return False

if __name__ == "__main__":
    search_string = input("Enter the string to search: ")
    mmap_search(file_path, search_string)