### Messaging App



#### Overview:

This repository contains a simple chat application consisting of three main components:

1. **client.py**: This script represents a user client that can interact with the chat server to join groups, send messages, receive messages, and perform other actions.

2. **group.py**: This script represents a chat group where users can join, send messages, and leave. Each group is managed independently.

3. **message_Server.py**: This script acts as the central server responsible for managing groups and facilitating communication between clients.



#### Setup Instructions:

1. Ensure you have Python installed on your system.

2. Install the required dependencies:

   - ZeroMQ: `pip install pyzmq`

3. Run the Message Server:

   - Execute `python message_Server.py` in your terminal.

   - Enter the desired port number when prompted.

4. Run the Group:

   - Execute `python group.py` in your terminal.

   - Provide the server IP address, server port, group port, and group name when prompted.

5. Run the Client:

   - Execute `python client.py` in your terminal.

   - You will need to provide central message server ip address and port number. If you wanna join group you will need to provide ip address and port of the group along with name. Name act as unique identifier and project will not handle duplicate names. Same IP Address Can have multiple groups but they need to have different port.
   - Dictonary is used for storing group and user information. 



#### Usage:

1. **Client.py**:

   - This script represents a user client. You can run this script multiple times and each will have unique id(uuid) which act as unique identifier for a user in group side. 

   - Users can perform various actions such as:

     - Get the list of available groups.

     - Join a group by providing the group name, IP, and port.

     - Leave a group.

     - Send messages to a group.

     - Retrieve messages from a group.
   - Run the script and follow the on-screen instructions to interact with the chat application.



2. **group.py**:

   - This script represents a chat group.

   - Groups are created and managed by the server.

   - Users can join, leave, and communicate within groups.

   - Run the script and provide the necessary information to create a group.



3. **message_Server.py**:

   - This script acts as the central server for managing groups and facilitating communication between clients.

   - Run the script to start the server.

   - The server listens for incoming requests from clients and handles group management.



#### Notes:

- This chat application uses ZeroMQ for message passing between components.

- Each component (client, group, server) plays a specific role in facilitating communication and managing groups.

- Users can interact with the application through the client interface, joining groups, sending and receiving messages.



#### Troubleshooting:

- Ensure that the required dependencies are installed correctly.

- Check that the server and group scripts are running and accessible.

- Verify network connectivity and firewall settings if encountering connection issues.



#### Contributors:

-	This project was developed by Deepanshu Dabas and Rudra Jyotirmay as part of Assignment 1.







