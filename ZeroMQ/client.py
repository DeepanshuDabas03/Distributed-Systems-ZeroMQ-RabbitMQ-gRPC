import zmq
import uuid

class User:
    def __init__(self, server_ip,server_port):
        self.uuid = str(uuid.uuid1())
        self.groups = {}
        # Connect to the message server
        self.server_socket = zmq.Context().socket(zmq.REQ)
        self.server_socket.connect(f"tcp://{server_ip}:{server_port}")

    def get_group_list(self):
        # Get the list of groups from the message server
        self.server_socket.send_json({'type': 'get_groups', 'user_uuid': self.uuid})
        group_list = self.server_socket.recv_json()
        for group,ip in group_list.items():
            print(f'{group}  - IP: {ip}')

    def join_group(self, group_name, group_ip,group_port):
        self.groups[group_name] = zmq.Context().socket(zmq.REQ)
        self.groups[group_name].connect(f"tcp://{group_ip}:{group_port}")
        self.groups[group_name].send_json({'type': 'join', 'user_uuid': self.uuid, 'group_name': group_name})
        response = self.groups[group_name].recv_json()
        if(response['status'] == 'SUCCESS'):
            print(f'Joined group {group_name}')
        else:
            print(f'Error joining group {group_name}')
            del self.groups[group_name]

    def leave_group(self, group_name):
        # If you are in the group, leave the group by sending a leave message to the group and then deleting the group from the user's group list
        if group_name in self.groups:
            self.groups[group_name].send_json({'type': 'leave', 'user_uuid': self.uuid})
            response=self.groups[group_name].recv_json()
            print(response)
            if response['status'] == 'SUCCESS':
                del self.groups[group_name]
                print(f'left group {group_name}')
            else:
                print(f'Error leaving group {group_name}')   
        

    def send_message(self, group_name, message):
        # If you are in the group, send a message to the group
        if group_name in self.groups:
            self.groups[group_name].send_json({'type': 'message', 'message': message, 'user_uuid': self.uuid})
            response = self.groups[group_name].recv_json()
            print(response)


    def get_messages(self, group_name, timestamp=None):
        # If you are in the group, get the messages from the group
        if group_name in self.groups:
            self.groups[group_name].send_json({'type': 'get_messages', 'timestamp': timestamp, 'user_uuid': self.uuid})
            messages = self.groups[group_name].recv_json()
            for message in messages:
                print("Message from", message['user'], ":", message['message'], "at", message['timestamp'])
        else:
            print(f'You are not in group {group_name}')

def main():
    print("Welcome to the chat app user")
    ip_address=input("Please enter your server ip address: ")
    port=input("Please enter your server port: ")
    user =User(ip_address,port)
    print("Your user UUID is: ",user.uuid)
    try:
        # User choice menu loop, to exit the program the user must press 6 or ctrl+c
        while(True):
            choice=input("Enter 1 to get group list\nEnter 2 to join group\nEnter 3 to leave group\nEnter 4 to send message\nEnter 5 to get messages\nEnter 6 to exit\n")
            if choice=='1':
                user.get_group_list()
            elif choice=='2':
                group_name=input("Enter group name: ")
                group_ip=input("Enter group ip: ")
                group_port=input("Enter group port: ")
                user.join_group(group_name,group_ip,group_port)
            elif choice=='3':
                group_name=input("Enter group name: ")
                user.leave_group(group_name)
            elif choice=='4':
                group_name=input("Enter group name: ")
                message=input("Enter message: ")
                user.send_message(group_name,message)
            elif choice=='5':
                group_name=input("Enter group name: ")
                user.get_messages(group_name)
            elif choice=='6':
                break
            else:
                print("Invalid choice")
    except KeyboardInterrupt:
        print("Exiting...")
    
if (__name__ == "__main__"):
    main()