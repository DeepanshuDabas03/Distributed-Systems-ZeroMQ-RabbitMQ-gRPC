import pika
import ast

users = []
youtubers = []
videos = []
subscribedTo = {}
hasVideos = {}
hasSubscribers = {}

def consume_user_requests(ch, method, properties, body, users = users, subscribedTo = subscribedTo, hasSubscribers = hasSubscribers):
  b = body.decode("utf-8")

  if b.split(" ")[1] == "logged":
    if b.split(" ")[0] not in users:
      print(b)
      users.append(b.split(" ")[0])
      subscribedTo[b.split(" ")[0]] = []
    else:
      notify_users1(b.split(" ")[0], subscribedTo[b.split(" ")[0]])
      

  
  else:
    d = ast.literal_eval(b)
    u = d["user"]

    if u not in users:
      users.append(u)
      subscribedTo[u] = []

    y = d["youtuber"]
    s = d["subscribe"]

    if y not in youtubers:
      print(y + " is not a registered youtuber!")
      return

    if s == True:
      if y in subscribedTo[u]:
        print("Already subscribed!")
      else:
        print(u + " subscribed to " + y)
        subscribedTo[u].append(y)
        hasSubscribers[y].append(u)

    else:
      if y not in subscribedTo[u]:
        print("Already unsubscribed!")
      else:
        print(u + " unsubscribed to " + y)
        subscribedTo[u].remove(y)
        hasSubscribers[y].remove(u)

  print()

def consume_youtuber_requests(ch, method, properties, body, youtubers = youtubers, hasVideos = hasVideos, hasSubscribers = hasSubscribers):
  b = body.decode("utf-8")
  y = b.split(" ")[0]
  v = b.split(" ")[2:]

  if y not in youtubers:
    youtubers.append(y)
    hasVideos[y] = []
    hasSubscribers[y] = []
  
  print(b)
  videos.append(v)
  hasVideos[y].append(v)

  print()

  notify_users2(y, hasSubscribers[y], v)

def notify_users1(u, subTo, hasVideos = hasVideos):
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()

  channel.exchange_declare(exchange='user_notifications', exchange_type='direct')

  for y in subTo:
    for v in hasVideos[y]:
      str = " "
      noti = y + " uploaded " + str.join(v)
      channel.basic_publish(exchange = 'user_notifications', routing_key = u, body = noti)
  
  connection.close()


def notify_users2(y, hasSub, vid):
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()

  channel.exchange_declare(exchange='user_notifications', exchange_type='direct')

  for u in hasSub:
    str = " "
    noti = y + " uploaded " + str.join(vid)
    channel.basic_publish(exchange = 'user_notifications', routing_key = u, body = noti)
  
  


def on_open(connection):
    connection.channel(on_open_callback = on_channel_open)


def on_channel_open(channel):
    channel.queue_declare(queue='user_requests')
    channel.queue_declare(queue='youtuber_requests')
    channel.basic_consume(queue='user_requests', on_message_callback = consume_user_requests, auto_ack = True)
    channel.basic_consume(queue='youtuber_requests', on_message_callback = consume_youtuber_requests, auto_ack = True)


parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.SelectConnection(parameters = parameters,
                                   on_open_callback = on_open)




try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
