import zmq
import threading

class Message_Server:
    def __init__(self,port):
        # Create a ZeroMQ context and socket for Request-Reply communication
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{port}")
        self.groups = {}

    def run(self):
        try:
            # Server loop to handle incoming messages continuously
            while True:
                message = self.socket.recv_json()
                if message['type'] == 'register':
                    self.register_group(message['group_name'], message['ip_address'])
                elif message['type'] == 'get_groups':
                    self.send_group_list(message['user_uuid'])
        except:
            print("Server shutting down")
            self.socket.close()
            self.context.term()

    def register_group(self, group_name, ip_address):
        # Check if the group name is already in use, if it is, send a fail message
        if(group_name in self.groups):
            self.socket.send_json({'status': 'FAIL'})
            return
        # If the group name is not in use, add it to the list of groups and send a success message
        print("Join request from", group_name, "at", ip_address)
        self.groups[group_name] = ip_address
        self.socket.send_json({'status': 'SUCCESS'})


    def send_group_list(self, user_uuid):
        # send the list of groups to the user
        print(f"Group list request from {user_uuid}")
        self.socket.send_json(self.groups)

def main():
    print("Welcome to the chat app server")
    port=input("Enter the port number for the server:")
    server = Message_Server(port)
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
if(__name__ == "__main__"):
    main()