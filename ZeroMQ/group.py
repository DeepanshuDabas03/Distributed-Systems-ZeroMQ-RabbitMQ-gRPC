import zmq
import threading
import time

class Group:
    def __init__(self, group_name, server_ip, server_port, group_port=5556):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{server_ip}:{server_port}")
        self.group_port = group_port
        self.client_socket = self.context.socket(zmq.REP)
        self.client_socket.bind(f"tcp://*:{group_port}")

        self.group_name = group_name
        self.users = {}
        self.messages = []
        self.lock = threading.Lock()

    def run(self):
        while True:
            try:
                message = self.client_socket.recv_json()
                if message['type'] == 'join':
                    self.add_user(message['user_uuid'], message['group_name'])
                elif message['type'] == 'leave':
                    self.remove_user(message['user_uuid'])
                elif message['type'] == 'message':
                    self.add_message(message['user_uuid'], message['message'])
                elif message['type'] == 'get_messages':
                    messages = self.get_messages(message['user_uuid'], message.get('timestamp'))
                    self.client_socket.send_json(messages)
            except Exception as e:
                print(e)

    def register_to_server(self):
        self.socket.send_json({'type': 'register', 'group_name': self.group_name, 'ip_address': 'localhost:'+str(self.group_port)})
        message = self.socket.recv_json()
        print(message)

    def add_user(self, user_uuid, group_name):
        if group_name == self.group_name and user_uuid not in self.users:
            self.users[user_uuid] = True
            print(f"Join request from {user_uuid}")
            self.client_socket.send_json({'status': 'SUCCESS'})
        else:
            print(f"User {user_uuid} could not join the group")
            self.client_socket.send_json({'status': 'FAIL'})

    def remove_user(self, user_uuid):
        if user_uuid in self.users:
            del self.users[user_uuid]
            print(f"Leave request from {user_uuid}")
            self.client_socket.send_json({'status': 'SUCCESS'})
        else:
            print(f'User {user_uuid} is not in the group')
            self.client_socket.send_json({'status': 'FAIL'})

    def add_message(self, user_uuid, message):
        with self.lock:
            if user_uuid in self.users:
                timestamp = time.time()  # Add timestamp
                self.messages.append({'user': user_uuid, 'message': message, 'timestamp': timestamp})
                print(f'Message sent from {user_uuid}: {message}')
                self.client_socket.send_json({'status': 'SUCCESS'})
            else:
                print(f'User {user_uuid} is not in the group')
                self.client_socket.send_json({'status': 'FAILED'})

    def get_messages(self, user_uuid, timestamp=None):
        print("Message request from user_uuid:", user_uuid)
        if user_uuid in self.users:
            with self.lock:
                if timestamp:
                    return [msg for msg in self.messages if msg['timestamp'] > timestamp]
                else:
                    return self.messages
        else:
            return {'status': 'FAIL', 'message': 'User not in group'}

def main():
    print("Welcome to the chat app group")
    ip_addr = input("Please enter the server IP address: ")
    port = input("Please enter the server port: ")
    group_port = input("Please enter the desired group port: ")
    name = input("Please enter the group name: ")
    group = Group(name, ip_addr, port, group_port)
    group.register_to_server()
    group_thread = threading.Thread(target=group.run)
    group_thread.start()

if __name__ == "__main__":
    main()
