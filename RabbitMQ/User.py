import pika
import sys
import uuid

class User:
    def __init__(self, u):
        self.username = u
        self.parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = 'user_requests')
        self.channel.queue_declare(queue = u)
        self.channel.exchange_declare(exchange='user_notifications', exchange_type='direct')
        self.channel.queue_bind(exchange='user_notifications', queue=u, routing_key=u)


    def userLogin(self, user):
        message = f"{user} logged in"

        self.channel.basic_publish(exchange='', routing_key='user_requests', body=str(message))


    def updateSubscription(self, user, youtuber, subscribe):
        message = {
            "user": user,
            "youtuber": youtuber,
            "subscribe": subscribe
        }


        self.channel.basic_publish(exchange='', routing_key='user_requests', body=str(message))
        print("SUCCESS: Subscribed/Unsubscribed request sent")
        print()

    def receiveNotifications(self):
        method_frame, header_frame, body = self.channel.basic_get(queue=self.username, auto_ack=True)
        while method_frame:
            print(f"Existing Notification: {body.decode()}")
            method_frame, header_frame, body = self.channel.basic_get(queue=self.username, auto_ack=True)

  
        
    def receiveRealTimeNotis(self):
        def callback(ch, method, properties, body):
            print(f"New Notification: {body.decode()}")

        self.channel.basic_consume(queue=self.username, on_message_callback=callback, auto_ack=True)
        print("Waiting for notifications...")
        self.channel.start_consuming()
        

# Running the User service
user = User(sys.argv[1])

user.userLogin(sys.argv[1])

if len(sys.argv) == 4:
    if sys.argv[2] == 's':
        user.updateSubscription(sys.argv[1], sys.argv[3], True)
    elif sys.argv[2] == 'u':
        user.updateSubscription(sys.argv[1], sys.argv[3], False)
        
#user.receiveNotifications()
user.receiveRealTimeNotis()

