import socket
import ssl
import configparser

# Load configuration settings from config.txt
config = configparser.ConfigParser()
config.read('config.txt')

# Extract configuration values
HOST = config.get('CLIENT', 'host', fallback='127.0.0.1')  # Server IP
PORT = config.getint('CLIENT', 'port', fallback=65432)      # Server port
ssl_enabled = config.getboolean('CLIENT', 'ssl_enabled', fallback=False)  # Toggle for SSL
ssl_cert = config.get('CLIENT', 'ssl_cert', fallback=None)  # SSL certificate (optional)

def send_query(query: str) -> str:
    """
    Sends the query string to the server using either a standard or SSL socket, based on configuration.

    Args:
        query (str): The string to be sent to the server.

    Returns:
        str: The server's response to the query.
    """
    if ssl_enabled:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        if ssl_cert:  # If a certificate is provided, load it
            context.load_verify_locations(ssl_cert)

        with socket.create_connection((HOST, PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as ssock:
                ssock.sendall(query.encode('utf-8'))  # Send query to server
                data = ssock.recv(1024).decode('utf-8')  # Receive response from server
    else:
        # Standard socket (non-SSL)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))  # Connect to server
            s.sendall(query.encode('utf-8'))  # Send query to server
            data = s.recv(1024).decode('utf-8')  # Receive response from server
    return data  # Return the server response

if __name__ == "__main__":
    query = input("Enter a string to search: ")
    response = send_query(query)  # Store the response
    print(f'Server response: {response}')  # Print the response
