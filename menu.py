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
    current_time = datetime.now().strftime('%H:%M:%S')

    # Create a log file for the recipient if it doesn't exist
    log_file_path = os.path.join('Q:\\scripts\\CortanaChat\\Sent_Messages', '{}-{}.txt'.format(name, current_date))
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w'):
            pass

    # Append the message to the log file
    with open(log_file_path, 'a') as f:
        f.write("[{}][{}] {}\n".format(current_time, "0.0.0.0", message))

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

    # Parse timestamps and messages
    parsed_messages = []
    for msg in messages:
        # Extract timestamp and message content
        timestamp_start = msg.find('[')
        timestamp_end = msg.find(']')
        if timestamp_start != -1 and timestamp_end != -1:
            timestamp = msg[timestamp_start + 1:timestamp_end]
            message_content = msg[timestamp_end + 1:].strip()
            # Append (timestamp, message) tuple to parsed_messages list
            parsed_messages.append((timestamp, message_content))

    # Sort messages by timestamp in descending order (most recent first)
    parsed_messages.sort(key=lambda x: datetime.strptime(x[0], '%H:%M:%S'), reverse=True)

    # Format messages for display (without timestamp and IP)
    formatted_messages = [msg[1][msg[1].find(']') + 1:].strip() for msg in parsed_messages]

    # Display messages in a dialog with scrollable list
    dialog = xbmcgui.Dialog()
    index = dialog.select("{} Messages".format(message_type), formatted_messages)
    if index != -1:
        selected_message = parsed_messages[index][1]  # Extract selected message
        options = ["View Message", "Reply", "Add As Friend", "Delete", "Block User", "Back"]
        option_choice = dialog.select("Message Options", options)
        if option_choice == 0:  # View Message
            dialog.ok("Selected Message", selected_message)
        elif option_choice == 1:  # Reply
            reply_to_user(selected_message)
        elif option_choice == 2:  # Add As Friend
            add_as_friend(selected_message)
        elif option_choice == 3:  # Delete Message
            dialog.ok("Not Yet Implemented", "Coming soon!")
        elif option_choice == 4:  # Block User
            block_user(selected_message)


# Function to add the user as a friend
def add_as_friend(message):
    # Splitting the message to get the IP address and username
    parts = message.split(']')
    if len(parts) < 2:
        xbmcgui.Dialog().ok("Error", "Invalid message format.")
        return
    
    sender_ip = parts[0].split('[')[-1].strip()
    username_message_part = parts[-1].split(':')
    
    if len(username_message_part) < 2:
        xbmcgui.Dialog().ok("Error", "Invalid message format.")
        return
    
    sender_name = username_message_part[0].split(' ')[-1].strip()
    
    # Check if the friend already exists in the friends list
    friend_exists = False
    try:
        with open('Q:\\scripts\\CortanaChat\\friends.txt', 'r') as file:
            for line in file:
                if sender_name in line and sender_ip in line:
                    friend_exists = True
                    break
    except FileNotFoundError:
        pass
    
    if not friend_exists:
        # Append sender's name and IP address to the friends list file
        with open('Q:\\scripts\\CortanaChat\\friends.txt', 'a') as file:
            file.write('{}:{}\n'.format(sender_name, sender_ip))
        xbmcgui.Dialog().ok("Success", "{} added as a friend.".format(sender_name))
    else:
        xbmcgui.Dialog().ok("Already Exists", "{} is already in your friends list.".format(sender_name))

# Function to block the user
def block_user(message):
    # Splitting the message to get the IP address and username
    parts = message.split(']')
    if len(parts) < 2:
        xbmcgui.Dialog().ok("Error", "Invalid message format.")
        return
    
    sender_ip = parts[0].split('[')[-1].strip()
    username_message_part = parts[-1].split(':')
    
    if len(username_message_part) < 2:
        xbmcgui.Dialog().ok("Error", "Invalid message format.")
        return
    
    sender_name = username_message_part[0].split(' ')[-1].strip()
    
    # Check if the user is already blocked
    user_blocked = False
    try:
        with open('Q:\\scripts\\CortanaChat\\blocklist.txt', 'r') as file:
            for line in file:
                if sender_name in line and sender_ip in line:
                    user_blocked = True
                    break
    except FileNotFoundError:
        pass
    
    if not user_blocked:
        # Append sender's name and IP address to the blocklist file
        with open('Q:\\scripts\\CortanaChat\\blocklist.txt', 'a') as file:
            file.write('{}:{}\n'.format(sender_name, sender_ip))
        xbmcgui.Dialog().ok("Success", "{} blocked successfully.".format(sender_name))
    else:
        xbmcgui.Dialog().ok("Already Blocked", "{} is already blocked.".format(sender_name))



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

# Function to delete a friend from the friends list
def delete_friend():
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
    index = dialog.select("Delete Friend", ["{} - {}".format(friend_info[0], friend_info[1]) for friend_info in friend_info_list])
    if index != -1:
        selected_friend = friend_info_list[index]
        delete_confirmation = dialog.yesno("Delete Friend", "Are you sure you want to delete {}?".format(selected_friend[0]))
        if delete_confirmation:
            try:
                # Remove the selected friend from the friends list file
                with open('Q:\\scripts\\CortanaChat\\friends.txt', 'w') as file:
                    for friend in friends:
                        if friend.split(':')[0] != selected_friend[0]:
                            file.write(friend)
                xbmcgui.Dialog().ok("Success", "{} deleted successfully.".format(selected_friend[0]))
            except Exception as e:
                xbmc.log("Error deleting friend - %s" % str(e))
    xbmc.sleep(1000)

# Function to delete a blocked user from the blocklist
def delete_blocked_user():
    # Read and display the blocklist
    blocked_users = []
    try:
        with open('Q:\\scripts\\CortanaChat\\blocklist.txt', 'r') as file:
            blocked_users = file.readlines()
    except FileNotFoundError:
        pass
    
    # Create a list of tuples with blocked user name and IP
    blocked_user_info_list = []
    for blocked_user in blocked_users:
        # Check if the line contains at least two values separated by colon
        if ':' in blocked_user:
            blocked_user_name, blocked_user_ip = blocked_user.strip().split(':', 1)
            blocked_user_info_list.append((blocked_user_name, blocked_user_ip))
        else:
            xbmc.log("Invalid format in blocklist.txt: {}".format(blocked_user))
    
    # Display a dialog with the list of blocked users
    dialog = xbmcgui.Dialog()
    index = dialog.select("Delete Blocked User", ["{} - {}".format(blocked_user_info[0], blocked_user_info[1]) for blocked_user_info in blocked_user_info_list])
    if index != -1:
        selected_blocked_user = blocked_user_info_list[index]
        delete_confirmation = dialog.yesno("Delete Blocked User", "Are you sure you want to unblock {}?".format(selected_blocked_user[0]))
        if delete_confirmation:
            try:
                # Remove the selected blocked user from the blocklist file
                with open('Q:\\scripts\\CortanaChat\\blocklist.txt', 'w') as file:
                    for blocked_user in blocked_users:
                        if blocked_user.split(':')[0] != selected_blocked_user[0]:
                            file.write(blocked_user)
                xbmcgui.Dialog().ok("Success", "{} unblocked successfully.".format(selected_blocked_user[0]))
            except Exception as e:
                xbmc.log("Error unblocking user - %s" % str(e))
    xbmc.sleep(1000)

# Function to send a message to a recipient
def reply_to_user(message):
    # Splitting the message to get the IP address
    parts = message.split(']')
    if len(parts) < 2:
        xbmcgui.Dialog().ok("Error", "Invalid message format.")
        return
    
    ip_address = parts[0].split('[')[-1].strip()
    username = get_username()
    sender_name = message.split(']')[-1].split(':')[0].split()[-1]
    
    # Prompt user to enter message
    keyboard = xbmc.Keyboard('', 'Enter your message to {}:'.format(sender_name))
    keyboard.doModal()
    message_text = keyboard.getText()
    
    # Check if user confirmed message input
    if keyboard.isConfirmed() and message_text:
        try:
            # Connect to the recipient and send the message
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip_address, 3074))  # Change port number if needed
            client_socket.send("{}: {}".format(username, message_text).encode())
            client_socket.close()
            
            # Display confirmation message
            xbmcgui.Dialog().ok("Message Sent", "Message sent to {} at IP address {}.".format(ip_address))
        except Exception as e:
            xbmc.log("Error sending message - %s" % str(e))


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
        choice = dialog.select("Friends", ["Friends List", "Add Friend", "Edit Friend", "Delete Friend", "Unblock User", "Back"])

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

        elif choice == 3:  # Delete Friend
            delete_friend()

        elif choice == 4:  # Back
            delete_blocked_user()

        elif choice == 5:  # Back
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
        choice = dialog.select("Cortana Chat", ["Friends", "Messages", "Settings", "Exit"])

        if choice == 0:  # Friends
            friend_options(username)

        elif choice == 1:  # Messages
            message_options(username)

        elif choice == 2:  # Settings
            settings_options()

        elif choice == 3:  # Exit
            break  # Exit the loop
		
	else:
	    break

# Entry point
if __name__ == '__main__':
    main()
