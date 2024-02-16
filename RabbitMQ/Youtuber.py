import pika
import sys
import uuid

class Youtuber:
    def __init__(self):
        self.parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='youtuber_requests')
        self.youtuber_tag = f"youtuber_consumer_{uuid.uuid4().hex}"

    def publishVideo(self, youtuber, videoName):
        message = youtuber + " uploaded " + videoName
        self.channel.basic_publish(exchange='', routing_key='youtuber_requests', body=str(message))
        print("SUCCESS: Video received by server")
        print()

# Running the Youtuber service to publish a video
youtuber = Youtuber()
youtuber.publishVideo(sys.argv[1], ' '.join(sys.argv[2:]))
