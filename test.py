import socket
import threading

class MessageReceiver(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.running = True

    def run(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
#            print("\nMessageReceiver: Listening for messages...")
            while self.running:
                client_socket, addr = server_socket.accept()
                data = client_socket.recv(1024).decode()
                if data == 'CORTANAPING':
                    # Respond to PING with PONG
                    client_socket.send('CORTANAPONG'.encode())
                elif data:
                    print(data)
                client_socket.close()
        except Exception as e:
            print("MessageReceiver: Error -", str(e))

    def stop(self):
        self.running = False

# Define the host and port to listen on
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 3074

# Start the message receiver thread
message_receiver = MessageReceiver(HOST, PORT)
message_receiver.start()

# Get user input for username and IP address to mention
username = input("Enter your username: \n")
ip_address = input("Enter IP address to mention: \n")

# Main loop to send messages
try:
    while True:
        message = input("Enter message: \n")
        if message:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((ip_address, PORT))
                client_socket.send("{}: {}".format(username, message).encode())
                client_socket.close()
            except Exception as e:
                print("Error sending message -", str(e))
except KeyboardInterrupt:
    pass

# Stop the message receiver thread when the script is terminated
message_receiver.stop()
