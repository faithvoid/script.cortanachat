import xbmc
import xbmcgui
import socket
import os
import sys
import urllib2
from datetime import datetime

# Function to save sent messages
def save_sent_message(message):
    # Extract recipient's name from the message
    name = message.split(':')[0].strip()

    # Format the current date
    current_date = datetime.now().strftime('%m%d%y')

    # Create a log file for the recipient if it doesn't exist
    log_file_path = os.path.join('Q:\\scripts\\CortanaChat\\Sent_Messages', '{}-{}.txt'.format(name, current_date))
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w'):
            pass

    # Append the message to the log file
    with open(log_file_path, 'a') as f:
        f.write(message + '\n')

# Function to add a friend
def add_friend():
    keyboard = xbmc.Keyboard('', 'Enter friend name')
    keyboard.doModal()
    friend_name = keyboard.getText()
    if not friend_name:
        return
    
    keyboard = xbmc.Keyboard('', 'Enter friend IP address')
    keyboard.doModal()
    friend_ip = keyboard.getText()
    if not friend_ip:
        return

    # Append friend's name and IP address to the friends list file
    with open('Q:\\scripts\\CortanaChat\\friends.txt', 'a') as file:
        file.write('{}:{}\n'.format(friend_name, friend_ip))

# Function to display the list of friends
def display_friends_list(ip_addresses):
    # Read and display the friends list
    friends = []
    try:
        with open('Q:\\scripts\\CortanaChat\\friends.txt', 'r') as file:
            friends = file.readlines()
    except FileNotFoundError:
        pass
    
    # Display a dialog with the list of friends
    dialog = xbmcgui.Dialog()
    index = dialog.select("Friends List", [friend.strip() for friend in friends])
    if index != -1:
        return ip_addresses[index]
    else:
        return None

# Function to display messages (sent or received)
def display_messages(message_type):
    if message_type == 'Sent':
        folder = 'Q:\\scripts\\CortanaChat\\Sent_Messages'
    elif message_type == 'Received':
        folder = 'Q:\\scripts\\CortanaChat\\Received_Messages'

    # Read all messages from log files
    messages = []
    try:
        files = os.listdir(folder)
        for file_name in files:
            with open(os.path.join(folder, file_name), 'r') as file:
                messages.extend(file.readlines())
    except FileNotFoundError:
        pass

    # Sort messages by date in descending order (most recent first)
    try:
        messages.sort(key=lambda x: datetime.strptime(x.split('-')[1].strip().split('.')[0], '%m%d%y'), reverse=True)
    except (IndexError, ValueError):
        xbmc.log("Error sorting messages: Invalid date format or file naming convention.")

    # Display messages in a dialog with scrollable list
    dialog = xbmcgui.Dialog()
    dialog.select("{} Messages".format(message_type), messages)

# Function to get username from the user
def get_username():
    try:
        with open('Q:\\scripts\\CortanaChat\\name.txt', 'r') as file:
            return file.read().strip()
    except IOError:
        xbmc.log("Username file not found. Please enter your name to save into the file.")
        keyboard = xbmc.Keyboard('', 'Enter your name')
        keyboard.doModal()
        username = keyboard.getText()
        if not username:
            xbmc.log("No name entered. Exiting.")
            sys.exit()
        
        # Save the entered name into the file
        try:
            with open('Q:\\scripts\\CortanaChat\\name.txt', 'w') as file:
                file.write(username)
            return username
        except Exception as e:
            xbmc.log("Error saving username - %s" % str(e))
            sys.exit()

# Function to get external IP address
def get_external_ip():
    try:
        external_ip = urllib2.urlopen('http://api.ipify.org').read()
        return external_ip
    except Exception as e:
        xbmc.log("Error fetching external IP address - %s" % str(e))
        return None

# Main loop to interact with the user and send/receive messages

def main():
    # Get username from file
    username = get_username()

    while True:
        xbmc.executebuiltin('Action(Back)')  # Handle XBMC's back action

        dialog = xbmcgui.Dialog()
        # Present options to the user
        choice = dialog.select("Cortana Chat", ["Send Message", "Received Messages", "Sent Messages", "Friends List", "Add Friend", "Show IP Address", "Exit"])

        if choice == 0:  # Send Message
            keyboard = xbmc.Keyboard('', 'Enter IP address to message')
            keyboard.doModal()
            if keyboard.isConfirmed():
                ip_address = keyboard.getText()
            else:
                continue

            keyboard = xbmc.Keyboard('', 'Enter message')
            keyboard.doModal()
            message = keyboard.getText()
            if message:
                try:
                    # Connect to the recipient and send the message
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip_address, 3074))
                    client_socket.send("{}: {}".format(username, message).encode())
                    client_socket.close()
                    # Save the sent message
                    save_sent_message("{}: {}".format(username, message))
                except Exception as e:
                    xbmc.log("Error sending message - %s" % str(e))
            xbmc.sleep(1000)

        elif choice == 1:  # Received Messages
            display_messages('Received')

        elif choice == 2:  # Sent Messages
            display_messages('Sent')

        elif choice == 3:  # Friends List
            # Get list of IP addresses from friends list
            ip_addresses = []
            try:
                with open('Q:\\scripts\\CortanaChat\\friends.txt', 'r') as file:
                    for line in file:
                        ip_address = line.strip().split(':')[-1]
                        ip_addresses.append(ip_address)
            except FileNotFoundError:
                pass

            selected_ip = display_friends_list(ip_addresses)
            if selected_ip:
                keyboard = xbmc.Keyboard('', 'Enter message')
                keyboard.doModal()
                message = keyboard.getText()
                if message:
                    try:
                        # Connect to the selected friend and send the message
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.connect((selected_ip, 3074))
                        client_socket.send("{}: {}".format(username, message).encode())
                        client_socket.close()
                        # Save the sent message
                        save_sent_message("{}: {}".format(username, message))
                    except Exception as e:
                        xbmc.log("Error sending message - %s" % str(e))
            xbmc.sleep(1000)

        elif choice == 4:  # Add Friend
            add_friend()

        elif choice == 5:  # Show External IP
            external_ip = get_external_ip()
            if external_ip:
                dialog = xbmcgui.Dialog()
                dialog.ok("External IP Address", "Your current external IP address is: {}".format(external_ip))
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Error", "Failed to fetch external IP address.")

        elif choice == 6:  # Exit
            break  # Exit the loop


        else:
            break

if __name__ == '__main__':
    main()
