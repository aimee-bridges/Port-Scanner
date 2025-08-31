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
        sock = socket.scoket(socket.AF_INET, socket.SOCK_STREAM)
        #Set a timeout so the scanner doesn't hang on closed ports