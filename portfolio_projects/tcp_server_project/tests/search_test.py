import mmap
import configparser
import logging
import os
import time
import re
from typing import NoReturn

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the logs directory exists
log_dir = os.path.join(script_dir, '..', 'logs')
os.makedirs(log_dir, exist_ok=True)

# Configure logging to output to a file and the console
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the logging level for the root logger

# Create a file handler to write log messages to a file
file_handler = logging.FileHandler(os.path.join(log_dir, 'server.log'))
file_handler.setLevel(logging.DEBUG)

# Create a console handler to output log messages to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Change this to INFO or ERROR as needed

# Create a formatter and set it for both handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Load configuration settings from config.txt
config = configparser.ConfigParser()

# Get the path to config.txt relative to the script directory
config_path = os.path.join(script_dir, '..', 'config.txt')

# Read the configuration file
if not os.path.exists(config_path):
    logger.error(f"Configuration file not found at: {config_path}")
    raise FileNotFoundError(f"Configuration file not found at: {config_path}")

config.read(config_path)

# Extract the file path from the configuration file
try:
    file_path = config.get('DEFAULT', 'linuxpath')
except configparser.NoOptionError:
    logger.error("The 'linuxpath' key is missing in the configuration file.")
    raise KeyError("The 'linuxpath' key is missing in the configuration file.")

# Check if the file exists
if not os.path.exists(file_path):
    logger.error(f"The file specified in linuxpath does not exist: {file_path}")
    raise FileNotFoundError(f"The file specified in linuxpath does not exist: {file_path}")

def mmap_search(file_path: str, search_string: str) -> bool:
    start_time: float = time.time()
    
    with open(file_path, 'r') as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            if mmap_obj.find(search_string.encode()) != -1:
                logger.info(f"Found {search_string} using Memory-Mapped Search.")
                logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
                return True
    
    logger.info(f"{search_string} not found.")
    logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
    return False

def boyer_moore_search(file_path: str, search_string: str) -> bool:
    start_time: float = time.time()
    
    with open(file_path, 'r') as file:
        content: str = file.read()
        index: int = content.find(search_string)
        
        if index != -1:
            logger.info(f"Found {search_string} using Boyer-Moore Search.")
            logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
            return True
    
    logger.info(f"{search_string} not found.")
    logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
    return False

def binary_search(file_path: str, search_string: str) -> bool:
    start_time: float = time.time()
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    left, right = 0, len(lines) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_line: str = lines[mid].strip()
        
        if search_string == mid_line:
            logger.info(f"Found {search_string} using Binary Search.")
            logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
            return True
        elif search_string < mid_line:
            right = mid - 1
        else:
            left = mid + 1
    
    logger.info(f"{search_string} not found.")
    logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
    return False

def regex_search(file_path: str, pattern: str) -> bool:
    start_time: float = time.time()
    compiled_pattern = re.compile(pattern)
    
    with open(file_path, 'r') as file:
        for line in file:
            if compiled_pattern.search(line):
                logger.info(f"Pattern {pattern} found using Regex Search.")
                logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
                return True
    
    logger.info(f"Pattern {pattern} not found.")
    logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
    return False

def linear_search(file_path: str, search_string: str) -> bool:
    start_time: float = time.time()
    
    with open(file_path, 'r') as file:
        for line in file:
            if search_string in line:
                logger.info(f"Found '{search_string}' using Linear Search.")
                logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
                return True
    
    logger.info(f"'{search_string}' not found.")
    logger.info(f"Execution time: {time.time() - start_time:.6f} seconds")
    return False

if __name__ == "__main__":
    search_string = input("Enter the string to search: ")

    print("Choose a search method:")
    print("1. Memory-Mapped Search")
    print("2. Boyer-Moore Search")
    print("3. Binary Search")
    print("4. Regex Search")
    print("5. Linear Search")

    choice = input("Enter the number corresponding to your choice: ")

    if choice == '1':
        mmap_search(file_path, search_string)
    elif choice == '2':
        boyer_moore_search(file_path, search_string)
    elif choice == '3':
        binary_search(file_path, search_string)
    elif choice == '4':
        regex_search(file_path, search_string)
    elif choice == '5':
        linear_search(file_path, search_string)
    else:
        print("Invalid choice. Please select a valid option.")

    exit(0)
