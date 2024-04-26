import socket
import threading
import os
import re
from datetime import datetime

# Define a class for receiving messages in a separate thread
class MessageReceiver(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.running = True
        self.daemon = True  # Set the thread as daemon

    def run(self):
        try:
            # Set up a server socket to listen for incoming messages
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print("MessageReceiver: Listening for messages on {}:{}".format(self.host, self.port))
            while self.running:
                # Accept incoming connections
                client_socket, addr = server_socket.accept()
                # Check if the sender is in the blocklist
                if not is_blocked(addr[0]):
                    # Receive data from the client
                    data = client_socket.recv(512)
                    if data:
                        # Handle PING/PONG mechanism
                        if data.decode() == 'CORTANAPING':
                            client_socket.send(b'CORTANAPONG')
                        else:
                            # Save the received message
                            save_received_message(data.decode(), addr[0])
                    client_socket.close()
                else:
                    client_socket.close()
        except Exception as e:
            print("MessageReceiver: Error - %s" % str(e))

    def stop(self):
        self.running = False

# Function to check if the sender is in the blocklist
def is_blocked(ip_address):
    blocklist_file = 'Q:\\scripts\\CortanaChat\\blocklist.txt'
    if os.path.exists(blocklist_file):
        with open(blocklist_file, 'r') as f:
            for line in f:
                if ip_address in line:
                    return True
    return False

# Function to sanitize file names
def sanitize_file_name(name):
    # Replace special characters with underscores
    sanitized_name = re.sub(r'[^\w\-_. ]', '_', name)
    # Limit the length of the name to accommodate date and extension
    max_name_length = 38  # Adjusted to accommodate date and extension
    return sanitized_name[:max_name_length]

# Function to save received messages
def save_received_message(message, ip_address):
    # Extract sender's name from the message
    name = message.split(':')[0].strip()

    # Format the current date
    current_date = datetime.now().strftime('%m%d%y')
    current_time = datetime.now().strftime('%H-%M-%S')

    # Sanitize the name for use in the file name
    sanitized_name = sanitize_file_name(name)

    # Create a log file for the sender if it doesn't exist
    log_file_name = '{}-{}.txt'.format(sanitized_name, current_date)
    log_file_path = os.path.join('Q:\\scripts\\CortanaChat\\Received_Messages', log_file_name)
    
    # Check if the total length exceeds 42 characters
    if len(log_file_path) > 42:
        # Calculate the maximum length for the sender's name
        max_name_length = 38 - (len(current_date) + len('.txt') + 1)  # 1 for the hyphen before the timestamp
        # Truncate the sender's name
        sanitized_name = sanitized_name[:max_name_length]

        # Recreate the log file path
        log_file_name = '{}-{}.txt'.format(sanitized_name, current_date)
        log_file_path = os.path.join('Q:\\scripts\\CortanaChat\\Received_Messages', log_file_name)

    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w'):
            pass

    # Append the message to the log file
    with open(log_file_path, 'a') as f:
        f.write("[{}][{}] {}\n".format(current_time.replace('-', ':'), ip_address, message))

    # Notify XBMC about the new message
    xbmc.executebuiltin('Notification(%s, %s)' % ("New chat!", message))

# Define the host and port to listen on
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 3074

# Start the message receiver thread
message_receiver = MessageReceiver(HOST, PORT)
message_receiver.start()
