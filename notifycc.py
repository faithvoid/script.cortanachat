import socket
import threading
import os
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
            print("MessageReceiver: Listening for messages...")
            while self.running:
                # Accept incoming connections
                client_socket, addr = server_socket.accept()
                # Receive data from the client
                data = client_socket.recv(1024)
                if data:
                    # Display a notification for new chat messages
                    xbmc.executebuiltin('Notification(%s, %s)' % ("New chat!", data))
                    # Save the received message
                    save_received_message(data.decode())
                client_socket.close()
        except Exception as e:
            xbmc.log("MessageReceiver: Error - %s" % str(e))

    def stop(self):
        self.running = False

# Function to save received messages
def save_received_message(message):
    # Extract sender's name from the message
    name = message.split(':')[0].strip()

    # Format the current date
    current_date = datetime.now().strftime('%m%d%y')

    # Create a log file for the sender if it doesn't exist
    log_file_path = os.path.join('Q:\\scripts\\CortanaChat\\Received_Messages', '{}-{}.txt'.format(name, current_date))
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w'):
            pass

    # Append the message to the log file
    with open(log_file_path, 'a') as f:
        f.write(message + '\n')

# Define the host and port to listen on
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 5555

# Start the message receiver thread
message_receiver = MessageReceiver(HOST, PORT)
message_receiver.start()