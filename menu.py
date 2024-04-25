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
    
    # Create a list of tuples with friend name, IP, and online/offline status
    friend_info_list = []
    for friend in friends:
        friend_name, friend_ip = friend.strip().split(':')
        is_online = ping_friend(friend_ip)
        if is_online:
            status = "Online"
        else:
            status = "Offline"
        friend_info_list.append((friend_name, friend_ip, status))
    
    # Display a dialog with the list of friends and online/offline status
    dialog = xbmcgui.Dialog()
    index = dialog.select("Friends List", ["{} - {}".format(friend_info[0], friend_info[2]) for friend_info in friend_info_list])
    if index != -1:
        return friend_info_list[index][1]  # Return the selected friend's IP address
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

# Function to send a PING message to check online status
def ping_friend(ip_address):
    try:
        # Connect to the friend with a timeout of 3 seconds
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(3)
        client_socket.connect((ip_address, 3074))
        client_socket.send(b'CORTANAPING')
        # Wait for a response (CORTANAPONG)
        response = client_socket.recv(1024)
        client_socket.close()
        if response.decode() == 'CORTANAPONG':
            return True  # Friend is online
        else:
            return False  # Friend is offline
    except Exception as e:
        return False  # Connection attempt failed or timed out, friend is offline

# Function to edit username
def edit_username():
    keyboard = xbmc.Keyboard('', 'Enter new username')
    keyboard.doModal()
    new_username = keyboard.getText()
    if new_username:
        try:
            with open('Q:\\scripts\\CortanaChat\\name.txt', 'w') as file:
                file.write(new_username)
            xbmcgui.Dialog().ok("Success", "Username updated successfully.")
        except Exception as e:
            xbmc.log("Error updating username - %s" % str(e))
    else:
        xbmcgui.Dialog().ok("Error", "No username entered.")

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

# Function to edit friends (name and IP address)
def edit_friends():
    # Read and display the friends list
    friends = []
    try:
        with open('Q:\\scripts\\CortanaChat\\friends.txt', 'r') as file:
            friends = file.readlines()
    except FileNotFoundError:
        pass
    
    # Create a list of tuples with friend name, IP, and online/offline status
    friend_info_list = []
    for friend in friends:
        friend_name, friend_ip = friend.strip().split(':')
        friend_info_list.append((friend_name, friend_ip))
    
    # Display a dialog with the list of friends
    dialog = xbmcgui.Dialog()
    index = dialog.select("Edit Friends", ["{} - {}".format(friend_info[0], friend_info[1]) for friend_info in friend_info_list])
    if index != -1:
        selected_friend = friend_info_list[index]
        edit_friend(selected_friend[0], selected_friend[1])

# Function to edit friend's name and IP address
def edit_friend(friend_name, friend_ip):
    keyboard = xbmc.Keyboard(friend_name, 'Enter new name for {}'.format(friend_name))
    keyboard.doModal()
    new_name = keyboard.getText()
    if not new_name:
        new_name = friend_name
    
    keyboard = xbmc.Keyboard(friend_ip, 'Enter new IP address for {}'.format(new_name))
    keyboard.doModal()
    new_ip = keyboard.getText()
    if not new_ip:
        new_ip = friend_ip

    try:
        # Read the friends list
        with open('Q:\\scripts\\CortanaChat\\friends.txt', 'r') as file:
            friends = file.readlines()
        # Modify the name and IP address for the selected friend
        with open('Q:\\scripts\\CortanaChat\\friends.txt', 'w') as file:
            for friend in friends:
                if friend.split(':')[0] == friend_name:
                    file.write('{}:{}\n'.format(new_name, new_ip))
                else:
                    file.write(friend)
        xbmcgui.Dialog().ok("Success", "Details for {} updated successfully.".format(new_name))
    except Exception as e:
        xbmc.log("Error updating details for %s - %s" % (new_name, str(e)))

# Function to handle message-related options
def message_options(username):
    while True:
        dialog = xbmcgui.Dialog()
        # Present message-related options to the user
        choice = dialog.select("Messages", ["New Message", "Received Messages", "Sent Messages", "Back"])

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

        elif choice == 3:  # Back
            break

	else:
	    break

# Function to handle friend-related options
def friend_options(username):
    while True:
        dialog = xbmcgui.Dialog()
        # Present friend-related options to the user
        choice = dialog.select("Friends", ["Friends List", "Add Friend", "Edit Friends", "Back"])

        if choice == 0:  # Friends List
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

        elif choice == 1:  # Add Friend
            add_friend()

        elif choice == 2:  # Edit Friends
            edit_friends()

        elif choice == 3:  # Back
            break

	else:
	    break

# Function for settings-related options
def settings_options():
    while True:
        xbmc.executebuiltin('Action(Back)')  # Handle XBMC's back action
        dialog = xbmcgui.Dialog()
        # Present settings options to the user
        choice = dialog.select("Settings", ["Edit Username", "Show IP Address", "Back"])

        if choice == 0:  # Edit Username
            edit_username()

        elif choice == 1:  # Show External IP
            external_ip = get_external_ip()
            if external_ip:
                dialog = xbmcgui.Dialog()
                dialog.ok("External IP Address", "Your current external IP address is: {}".format(external_ip))
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Error", "Failed to fetch external IP address.")

        elif choice == 2:  # Back
            break
				
	else:
	    break

# Main loop to interact with the user and send/receive messages
def main():
    # Get username from file
    username = get_username()

    while True:
        xbmc.executebuiltin('Action(Back)')  # Handle XBMC's back action
        dialog = xbmcgui.Dialog()
        # Present options to the user
        choice = dialog.select("Cortana Chat", ["Messages", "Friends", "Settings", "Exit"])

        if choice == 0:  # Messages
            message_options(username)

        elif choice == 1:  # Friends
            friend_options(username)

        elif choice == 2:  # Settings
            settings_options()

        elif choice == 3:  # Exit
            break  # Exit the loop
		
	else:
	    break

# Entry point
if __name__ == '__main__':
    main()
