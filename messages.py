import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import datetime


name1 = "Jordan Stern"
name2 = "Person2"

with open('message.json', 'r') as fr:
    messages_dict = OrderedDict(json.load(fr))
messages = messages_dict["messages"]


def build_msg_dict(messages):
    name1_msgs = {}
    name2_msgs = {}
    for message in messages:
        name = message["sender_name"]
        time = message["timestamp"]
        print_timestamp(time)
        if name == name1:
            msg_dict = name1_msgs
        elif name == name2:
            msg_dict = name2_msgs
        
        if "photos" in message:
            msg_dict[time] = message["photos"]
        elif "gifs" in message:
            msg_dict[time] = message["gifs"]
        elif "sticker" in message:
            msg_dict[time] = message["sticker"]
        elif "files" in message:
            msg_dict[time] = message["files"]
        elif "content" in message:
            msg_dict[time] = message["content"]
        elif "share" in message:
            msg_dict[time] = message["share"]
        elif "videos" in message:
            msg_dict[time] = message["videos"]
        else:
            msg_dict[time] = None
    return name1_msgs, name2_msgs

def print_timestamp(timestamp):
    print(datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))

name1_msgs, name2_msgs = build_msg_dict(messages)
name1_count, name2_count = len(name1_msgs), len(name2_msgs)
total_count = name1_count+name2_count

piechart = plt.subplot()                                   
labels = name1 + ": " + str(name1_count), name2 + ": " + str(name2_count)
sizes = [name1_count/total_count, name2_count/total_count]
piechart.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
piechart.axis('equal')
plt.title('Message distribution')
plt.show()

