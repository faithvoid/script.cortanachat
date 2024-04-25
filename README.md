# Cortana Chat
## 1-on-1 IP-based instant messaging for XBMC4Xbox, complete with friends list!
![menu1](https://github.com/faithvoid/script.cortanachat/assets/56975081/638e1f82-708d-4ca5-bea8-d17300487b60)
![messagemenu](https://github.com/faithvoid/script.cortanachat/assets/56975081/bccf1a84-b0b0-4cfe-81a1-f50ffa5edfec)
![receivedmessages](https://github.com/faithvoid/script.cortanachat/assets/56975081/9f3db6d2-5332-49dd-b7f9-2c79c46cb492)
![sentmessages](https://github.com/faithvoid/script.cortanachat/assets/56975081/d55d4b84-b81b-4800-b709-53312443b83b)
![friendmenu](https://github.com/faithvoid/script.cortanachat/assets/56975081/84673169-a13f-4b2b-a4e6-1d1747947dc0)
![friends](https://github.com/faithvoid/script.cortanachat/assets/56975081/b0f9de41-05fe-43e1-a6c7-76829861c467)
![settingsmenu](https://github.com/faithvoid/script.cortanachat/assets/56975081/7652fcc7-3e96-4bae-9eca-4335adfbb6fe)
![notification](https://github.com/faithvoid/script.cortanachat/assets/56975081/a9498a0d-9fea-4338-9abe-5d48e901239e)

## Features:
- Have 1-on-1 chats with your friends, directly on your Xbox!
- Integrated Friends List capabilities lets you message/add/remove/block friends quickly, check their online statuses, and more!
- Check your sent & received messages & compose a new message to users not on your friends list easily!
- No backend servers means never (and always) out of date! As long as you've got an IPv4 address, you've got a chat client for your Xbox!
- Don't know your external IP? Go into Settings and click "Show IP Address"!
- UI is designed to be close to the Xbox 360's for ease of use!

## Installation:
- Grab current release file.
- Unzip "CortanaChat" into the scripts folder your XBMC4Xbox installation, usually "Q:/scripts/". DO NOT RENAME THE FOLDER!
- Run the script and it will ask for your username and save it to name.txt.

# How to use:
- Make sure port 3074 is forwarded on your router! This is the same as Xbox Live / Insignia's port, so if you're using these services you should have it forwarded already!
- Run Cortana Chat and a menu will pop up, with the notification script automatically running in the background, even if you close the menu! This means you can still get messages even when watching movies or listening to music.
- To send a message, you need to know your friend's IP address. You can send a message directly to their IP via the "Send Message" button, which prompts you for their IP and the message you'd like to send, or you can add them as a friend (which has you input their name and IP address) so you can instantly message them!
- You can view your sent or received messages in the "Sent Messages" or "Received Messages" menus!
- Don't know your external IP address? Click "Show IP Address", tell your friend your IP, and now you both can chat Xbox to Xbox!

# FAQ:
- "My friends list is a bit slow to load?"
- This is to be expected, as when you open your friends list, a "PING" request is sent from your console to all of your friends' consoles to verify their online status. This can take a second or two, especially on slower connections / if you have more friends added.
- "I was able to message my friend, but now I can't?"
- Your friend's IP probably changed, you can edit their IP in the "Edit Friends" section on the Friends menu!
- "How secure is this?"
- Not very. It's all plaintext sent with no encryption from IP to IP, a-la IRC, so don't send anything you wouldn't want the entire world seeing. Also, be careful who you give your IP address to, as there are bad actors out there who could use it for nefarious purposes! Only add people you trust! I'd recommend using a VPN/proxy if you're concerned, but also you're already connecting to the internet on a 20+ year old console, so... (although I do want to see how feasible integrating SSL is after the primary code is complete).

## To Do:
- Add anti-spam functionality. 
  Try to keep messages within 512 bytes (iirc Xbox 360 messages work this way, with a 500 character limit with the first 12 characters being reserved for the Gamertag).
- Integrate some sort of user authentication? SSL?
- Group chat support? (likely possible with one host as a message relay)
- VoIP / voice chat? (most likely impossible)
- Basic file transfer? (possible, but needs to be there for a reason). 

## Bugs:
- Currently, messages with commas (,) don't show up properly in the notifications. but they'll show up just fine in the "Received Messages" section! So if you receive a (half) blank message, that's probably why. Try not to use them!
