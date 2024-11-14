import configparser
import os
import random
import logging

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.txt file dynamically
config_file_path = os.path.join(script_dir, '..', 'config.txt')

# Load configuration settings from config.txt
config = configparser.ConfigParser()
config.read(config_file_path)

# Extract the source path, output path, and log path from the config file
source_path = config.get('DEFAULT', 'linuxpath_1')
output_path = config.get('DEFAULT', 'linuxpath_2')
log_path = config.get('DEFAULT', 'log_path')

# Ensure the output directory exists
os.makedirs(output_path, exist_ok=True)

# Configure logging to use the path from the config file
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,  # Enable DEBUG level to log more detailed information
    format="%(asctime)s - %(levelname)s - %(message)s"
) 


def generate_test_file(file_name: str, num_rows: int) -> None:
    """
    Generates a test file with random data.

    Args:
        file_name: The name of the file to generate.
        num_rows: The number of rows to generate in the file.
    
    Example:
        generate_test_file('test_10k.txt', 10000)
    """
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'w') as file:
        for _ in range(num_rows):
            # Generate a random string of numbers for the test file
            line = ';'.join(str(random.randint(0, 20)) for _ in range(10)) + '\n'
            file.write(line)
    print(f"Generated {file_name} with {num_rows} rows at {file_path}.")
    
    return None

# Generate files of different sizes
generate_test_file('test_10k.txt', 10000)
generate_test_file('test_100k.txt', 100000)
generate_test_file('test_500k.txt', 500000)
generate_test_file('test_1M.txt', 1000000)
