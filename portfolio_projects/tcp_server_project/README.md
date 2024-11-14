# TCP Server Project

## Overview
This project implements a simple TCP server in Python, with multithreaded client handling and configurable options via a configuration file. It also includes a client script for testing the server.

## Project Structure
- `server.py`: The main server script.
- `client.py`: The client script for testing.
- `config.txt`: Configuration file with server settings.
- `logs/`: Stores server log files.

To break this project into five sequential, manageable tasks, here’s a suggested approach:

### **Task 1: TCP Server Setup and Basic Functionality**
- **Objective**: Set up a TCP server that can handle multiple concurrent connections using multithreading.
- **Subtasks**:
  1. Create a TCP server that binds to a specific port and listens for incoming connections.
  2. Implement multithreading to handle multiple client connections concurrently.
  3. Accept and parse the incoming "String" data from clients.
  4. Add basic logging for requests (IP address, timestamp, etc.).

**Outcome**: A multithreaded TCP server that can receive string inputs from clients and log basic connection details.

---

### **Task 2: File Handling and String Search**
- **Objective**: Implement file handling and search functionality.
- **Subtasks**:
  1. Parse the configuration file to extract the file path (`linuxpath=/path/to/file`).
  2. Implement file reading and ensure the file can be opened and read efficiently.
  3. Implement full-string search functionality (ignore partial matches) in the file.
  4. Add the ability to toggle between re-reading the file on each query (`REREAD_ON_QUERY=True`) and reading it once (`REREAD_ON_QUERY=False`).

**Outcome**: The server can read a file, search for a full string match, and re-read the file if necessary based on configuration settings.

---

### **Task 3: Performance Optimization and Benchmarking**
- **Objective**: Optimize string search and benchmark different search algorithms.
- **Subtasks**:
  1. Research and implement at least 5 different file-search methods (e.g., linear search, binary search on sorted files, mmap, regex search, etc.).
  2. Benchmark the search methods against different file sizes (e.g., 10k, 100k, 500k, 1M rows).
  3. Measure the execution time for each search method and compare performance.
  4. Create a report that includes a table and chart comparing the search methods based on performance.

**Outcome**: A PDF report that documents the benchmarking process, with the most performant search method chosen for the final implementation.

---

### **Task 4: Security Implementation and Error Handling**
- **Objective**: Add security features, SSL authentication, and robust error handling.
- **Subtasks**:
  1. Implement SSL authentication for secure client-server communication (configurable through the configuration file).
  2. Ensure proper input validation (e.g., check for buffer overflows, invalid requests).
  3. Add detailed error handling for cases such as file not found, incorrect input format, and unexpected errors.
  4. Log errors and security-related events (e.g., invalid SSL handshake).

**Outcome**: The server is secured with SSL, and robust error handling is in place to deal with potential security vulnerabilities and user errors.

---

### **Task 5: Finalization, Testing, and Packaging**
- **Objective**: Finalize the project by adding tests, packaging the code, and creating installation instructions.
- **Subtasks**:
  1. Write **unit tests** using `pytest` to cover edge cases, exceptions, and typical workflows (file size variations, high query load, etc.).
  2. Test the server under various conditions (multiple concurrent clients, large files, varying query loads).
  3. Package the code as a **Linux daemon/service** with detailed installation instructions.
  4. Verify PEP8 and PEP20 compliance, add docstrings and comments to make the code clean and professional.

**Outcome**: A fully tested, packaged, and documented TCP server that meets all project requirements, including installation as a Linux service, with clear user instructions.

---

### Sequential Breakdown:
1. **TCP Server Setup and Basic Functionality** (Task 1)
2. **File Handling and String Search** (Task 2)
3. **Performance Optimization and Benchmarking** (Task 3)
4. **Security Implementation and Error Handling** (Task 4)
5. **Finalization, Testing, and Packaging** (Task 5)

This breakdown provides a structured approach, where each task builds on the previous one, leading to a final, comprehensive solution.