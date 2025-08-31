#import socket module for for port scanning & network connections
import socket
#For concurrent scanning of multiple ports
import threading
#Import the time for tracking scan duration
import time
#Import datetime to timestamp open ports in the log file
from datetime import datetime

#Define a function to scan a single port on the target IP
def scan_port(ip, port):
    try:
        #Create TCP socket using IPv4
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Set a timeout so the scanner doesn't hang on closed ports
        sock.settimeout(1)
        #Attempt to connect to the target IP and Port
        result = sock.connect_ex((ip, port))
        #If result = 0, the port is open
        if result ==0:
            print(f"Port {port} is open")
            #Open a log file and append result
            with open("scan_results.txt", "a") as log:
                #Format the current time for logging
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #Write the open port info to the file
                log.write(f"[{timestamp}] {ip}:{port} is open\n")
        #Close the socket after scanning
        sock.close()
    #Catch and print any errors that occur during scanning
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
#Define the main function to handle user input and start scanning
def main():
    print("🔍 Simple Port Scanner")

    target_ip = input("Enter IP address to scan: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    print(f"\nScanning {target_ip} from port {start_port} to {end_port}...\n")

    open_ports = []  # List to store open ports
    start_time = time.time()  # Record start time

    threads = []  # Track all threads

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port_with_log, args=(target_ip, port, open_ports))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # Wait for all threads to finish

    end_time = time.time()  # Record end time
    duration = round(end_time - start_time, 2)

    # 🧾 Print summary
    print("\n📋 Scan Summary")
    print(f"Target IP: {target_ip}")
    print(f"Ports scanned: {end_port - start_port + 1}")
    print(f"Open ports found: {len(open_ports)}")
    print(f"Time taken: {duration} seconds")
    if open_ports:
        print("Open ports:", ", ".join(str(p) for p in open_ports))
    else:
        print("No open ports found.")
#Run main function only if script is executed directly
if __name__ == "__main__":
    main()