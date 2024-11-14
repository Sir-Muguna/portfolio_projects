import configparser
import logging
import time
import os
import matplotlib.pyplot as plt
from tabulate import tabulate
import mmap
import re
from typing import Dict

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

# Define the file names based on the sizes
file_names = {
    "10k": os.path.join(source_path, "test_10k.txt"),
    "100k": os.path.join(source_path, "test_100k.txt"),
    "500k": os.path.join(source_path, "test_500k.txt"),
    "1M": os.path.join(source_path, "test_1M.txt"),
}

# Search Implementations
def linear_search(file_path: str, search_string: str) -> float:
    """Linear search for a string in a file."""
    start_time = time.time()
    with open(file_path, 'r') as file:
        for line in file:
            if search_string in line:
                return time.time() - start_time
    return time.time() - start_time

def mmap_search(file_path: str, search_string: str) -> float:
    """Memory-Mapped search for a string in a file."""
    start_time = time.time()
    with open(file_path, 'r') as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            if mmap_obj.find(search_string.encode()) != -1:
                return time.time() - start_time
    return time.time() - start_time

def boyer_moore_search(file_path: str, search_string: str) -> float:
    """Boyer-Moore search for a string in a file."""
    start_time = time.time()
    with open(file_path, 'r') as file:
        content = file.read()
        if content.find(search_string) != -1:
            return time.time() - start_time
    return time.time() - start_time

def binary_search(file_path: str, search_string: str) -> float:
    """Binary search for a string in a sorted file."""
    start_time = time.time()
    with open(file_path, 'r') as file:
        lines = file.readlines()
    left, right = 0, len(lines) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_line = lines[mid].strip()
        if search_string == mid_line:
            return time.time() - start_time
        elif search_string < mid_line:
            right = mid - 1
        else:
            left = mid + 1
    return time.time() - start_time

def regex_search(file_path: str, pattern: str) -> float:
    """Regex search for a pattern in a file."""
    start_time = time.time()
    compiled_pattern = re.compile(pattern)
    with open(file_path, 'r') as file:
        for line in file:
            if compiled_pattern.search(line):
                return time.time() - start_time
    return time.time() - start_time

def benchmark_search_methods(search_string: str) -> Dict[str, Dict[str, float]]:
    """Benchmark various search methods."""
    methods = {
        "Linear Search": linear_search,
        "Memory-Mapped Search": mmap_search,
        "Boyer-Moore Search": boyer_moore_search,
        "Binary Search": binary_search,
        "Regex Search": regex_search
    }

    results: Dict[str, Dict[str, float]] = {method: {} for method in methods}

    for size, file_path in file_names.items():
        for method_name, method_func in methods.items():
            print(f"Benchmarking {size} file with {method_name}...")
            exec_time = method_func(file_path, search_string)
            results[method_name][size] = exec_time
            print(f"{size} file: Execution time for {method_name}: {exec_time:.6f} seconds")
    
    return results

# Plot the benchmarking results and create a table
def plot_results(results: dict) -> None:
    """Plot the benchmarking results and save a table."""
    sizes = list(file_names.keys())
    
    # Plotting the line graph
    plt.figure(figsize=(10, 6))
    
    for method_name, times_dict in results.items():
        times = [times_dict[size] for size in sizes]
        plt.plot(sizes, times, marker='o', label=method_name)

    plt.xlabel('File Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Search Method Benchmarking Results')
    plt.legend()
    plt.grid()

    # Save the plot to the specified output path
    png_path = os.path.join(output_path, 'benchmarking_results.png')
    plt.savefig(png_path)  
    print(f"Line graph saved to: {png_path}")
    
    # Generate table with formatted values
    table_headers = ["Method", "10k (seconds)", "100k (seconds)", "500k (seconds)", "1M (seconds)"]
    table_data = []

    for method_name, times_dict in results.items():
        row = [method_name] + [f"{times_dict[size]:.6f}" for size in sizes]
        table_data.append(row)

    # Sort the table data by the '1M (seconds)' column (which is index 4 in each row)
    table_data_sorted = sorted(table_data, key=lambda x: float(x[4]))  # Sort by 1M column

    # Create a Matplotlib figure for the table
    fig, ax = plt.subplots(figsize=(10, 4))  # Adjust size as needed
    ax.axis('tight')
    ax.axis('off')

    # Create the table and add it to the figure
    ax.table(cellText=table_data_sorted, colLabels=table_headers, cellLoc='center', loc='center')

    # Save the table as a PNG image
    table_png_path = os.path.join(output_path, 'benchmarking_results_table.png')
    plt.savefig(table_png_path, bbox_inches='tight', dpi=300)  # Save with tight bounding box for a clean look

    print(f"Table saved as PNG to: {table_png_path}")
    
    # Optionally show the plot
    # plt.show()

if __name__ == "__main__":
    search_string = input("Enter the string to search: ")  # User input for the search string
    results: Dict[str, Dict[str, float]] = benchmark_search_methods(search_string)
    plot_results(results)
