#import socket module for for port scanning & network connections
import socket
#For concurrent scanning of multiple ports
import threading
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
    print("Simple Port Scanner")
    #Ask the user for target IP address
    target_ip = input("Enter IP address to scan: ")
    #Ask the user for the starting port number
    start_port = int(input("Enter start port: "))
    #Ask the user for end port number
    end_port = int(input("Enter start port: "))
    #Display the scan range to the user
    print(f"\nScanning {target_ip} from port {start_port} to {end_port}...\n")
    #Loop through the specified port range
    for port in range(start_port, end_port + 1):
        #Create a new thread per individual port scan
        thread = threading.Thread(target=scan_port, args=(target_ip, port))
        #Start the thread(non-blocking)
        thread.start()
#Run main function only if script is executed directly
if __name__ == "__main__":
    main()