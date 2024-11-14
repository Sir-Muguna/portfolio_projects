import logging
import socket
import configparser
import os
import time
from typing import List, Optional
import ssl
import re  # For input validation

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.txt file dynamically
config_file_path = os.path.join(script_dir, '..', 'config.txt')

# Load configuration settings from config.txt
config = configparser.ConfigParser()
config.read(config_file_path)

# Extract configuration values
file_path: str = config.get('DEFAULT', 'linuxpath')
log_path: str = config.get('DEFAULT', 'log_path')  # New log path from config
reread_on_query: bool = config.getboolean('DEFAULT', 'reread_on_query')
ssl_enabled: bool = config.getboolean('DEFAULT', 'ssl_enabled')  # New flag for SSL use
ssl_cert: str = config.get('DEFAULT', 'ssl_cert')  # SSL certificate
ssl_key: str = config.get('DEFAULT', 'ssl_key')  # SSL key

# Set up logging
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MAX_INPUT_SIZE = 1024  # Set a max size for input validation

def validate_input(input_data: str) -> bool:
    """
    Validates the input to prevent security risks like buffer overflows and invalid formats.
    Args:
        input_data (str): The data received from the client.
    Returns:
        bool: True if input is valid, False otherwise.
    """
    if len(input_data) > MAX_INPUT_SIZE:
        logging.error("Input size too large")
        return False
    # Example validation to only allow alphanumeric inputs and semicolons (adjust as needed)
    if not re.match(r'^[a-zA-Z0-9;]+$', input_data):
        logging.error("Invalid input format")
        return False
    return True

def read_file_contents() -> List[str]:
    """
    Reads the specified file and returns its contents as a list of lines.

    Returns:
        List[str]: File content as a list of lines.
    
    Raises:
        FileNotFoundError: If the file specified by file_path does not exist.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            logging.info(f"Opened file: {file_path}")
            return file.readlines()
    else:
        logging.error(f"File at {file_path} does not exist.")
        raise FileNotFoundError(f"File at {file_path} does not exist")

def search_string_in_file(search_string: str, file_contents: Optional[List[str]] = None) -> str:
    """
    Searches for a specified string within the file contents.

    Args:
        search_string (str): The string to search for in the file contents.
        file_contents (Optional[List[str]]): A list of lines from the file to search within.
    
    Returns:
        str: "STRING EXISTS" if the string is found; otherwise, "STRING NOT FOUND".
    
    Raises:
        ValueError: If cached_file_contents is None and no file_contents are provided.
    """
    if file_contents is None:
        if cached_file_contents is None:
            raise ValueError("Cached file contents are not available")
        file_contents = cached_file_contents

    logging.debug(f"Searching for string: {search_string}")
    result = "STRING EXISTS\n" if search_string.strip() in map(str.strip, file_contents) else "STRING NOT FOUND\n"
    logging.info(f"Search result: {result.strip()}")
    return result

# Cache the file content if reread_on_query is False
cached_file_contents: Optional[List[str]] = None
if not reread_on_query:
    cached_file_contents = read_file_contents()

def start_server(host: str = 'localhost', port: int = 65432) -> None:
    """
    Starts the TCP server to handle incoming search requests, with optional SSL encryption.

    Args:
        host (str): The server host address (default: 'localhost').
        port (int): The port number on which the server listens (default: 65432).
    """
    logging.info(f"Starting server on {host}:{port} {'with SSL' if ssl_enabled else 'without SSL'}...")

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if ssl_enabled:
        # Set up SSL context and wrap the server socket
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=ssl_cert, keyfile=ssl_key)
        server_socket = context.wrap_socket(server_socket, server_side=True)

    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server is now listening on {host}:{port} {'with SSL' if ssl_enabled else 'without SSL'}...")
    logging.info(f"Server is now listening on {host}:{port}...")

    while True:
        try:
            connection, client_address = server_socket.accept()

            # Log client connection
            logging.info(f"Connection established with {client_address}")

            with connection:
                start_time = time.time()  # Track the start of request handling
                search_string = connection.recv(MAX_INPUT_SIZE).decode('utf-8').strip()

                if not validate_input(search_string):
                    connection.sendall(b"Invalid input format\n")
                    continue

                logging.debug(f"Received query: {search_string} from {client_address}")

                result = search_string_in_file(search_string)
                connection.sendall(result.encode('utf-8'))

                execution_time = time.time() - start_time
                logging.info(f"Sent response: {result.strip()} to {client_address} | Execution time: {execution_time:.4f} seconds")
                logging.debug(f"Execution time for query '{search_string}': {execution_time:.4f} seconds")

        except ssl.SSLError as ssl_error:
            logging.error(f"SSL error: {ssl_error}")
            connection.sendall(f"SSL Error: {ssl_error}\n".encode('utf-8'))

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            connection.sendall(f"Error: {e}\n".encode('utf-8'))

        finally:
            connection.close()

# Execute the server
if __name__ == "__main__":
    start_server()
