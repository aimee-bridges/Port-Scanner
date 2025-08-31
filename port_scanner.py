# 🔌 Import the socket module to create network connections
import socket

# 🔄 Import threading to scan multiple ports concurrently
import threading

# 📅 Import datetime to timestamp open ports in the log file
from datetime import datetime

# ⏱️ Import time to measure how long the scan takes
import time
#Import port dictonary from services.py
from services import PORT_SERVICES
# 🔍 Define a function to scan a single port and log results
def scan_port_with_log(ip, port, open_ports):
    try:
        # Create a TCP socket using IPv4
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a timeout of 1 second to avoid hanging on closed ports
        sock.settimeout(1)

        # Attempt to connect to the target IP and port
        result = sock.connect_ex((ip, port))
        # Map the port to its service name if it exists
        service_name = PORT_SERVICES.get(port, "Unknown")
        # If result is 0, the port is open
        if result == 0:
            # Print open port to terminal
            print(f"✅ Port {port} is open")

            # Add the open port to the list for summary
            open_ports.append(port)

            # Open (or create) a log file and append the result
            with open("scan_results.txt", "a") as log:
                # Format the current time for logging
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Write the open port info to the file
                log.write(f"[{timestamp}] {ip}:{port} is open\n")

        # Close the socket after scanning
        sock.close()

    # Catch and print any errors that occur during scanning
    except Exception as e:
        print(f"❌ Error scanning port {port}: {e}")

# 🚀 Define the main function to handle user input and start scanning
def main():
    # Print a banner to introduce the tool
    print("🔍 Simple Port Scanner")

    # Ask the user for the target IP address
    target_ip = input("Enter IP address to scan: ")

    # Ask for the starting port number
    start_port = int(input("Enter start port: "))

    # Ask for the ending port number
    end_port = int(input("Enter end port: "))

    # Display the scan range to the user
    print(f"\nScanning {target_ip} from port {start_port} to {end_port}...\n")

    # Create a list to store open ports
    open_ports = []

    # Record the start time of the scan
    start_time = time.time()

    # Create a list to keep track of all threads
    threads = []

    # Loop through the specified port range
    for port in range(start_port, end_port + 1):
        # Create a new thread for each port scan
        thread = threading.Thread(target=scan_port_with_log, args=(target_ip, port, open_ports))

        # Start the thread (non-blocking)
        thread.start()

        # Add the thread to the list
        threads.append(thread)

    # Wait for all threads to finish before continuing
    for thread in threads:
        thread.join()

    # Record the end time of the scan
    end_time = time.time()

    # Calculate the total duration of the scan
    duration = round(end_time - start_time, 2)

    # 🧾 Print a summary of the scan results
    print("\n📋 Scan Summary")
    print(f"Target IP: {target_ip}")
    print(f"Ports scanned: {end_port - start_port + 1}")
    print(f"Open ports found: {len(open_ports)}")
    print(f"Time taken: {duration} seconds")

    # If any open ports were found, list them
    if open_ports:
        print("Open ports:", ", ".join(str(p) for p in open_ports))
    else:
        print("No open ports found.")

# 🧭 Run the main function only if the script is executed directly
if __name__ == "__main__":
    main()