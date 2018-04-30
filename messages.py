import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import datetime
import time
import numpy as np

name1 = "Jordan Stern"
name2 = "Person 2"

with open('message.json', 'r') as fr:
    messages_dict = OrderedDict(json.load(fr))
messages = messages_dict["messages"]


def build_msg_dict(messages):
    name1_msgs = {}
    name2_msgs = {}
    times_dict = {name1: [], name2: []}
    for message in messages:
        name = message["sender_name"]
        time = message["timestamp"]
        
        times_dict[name].append(time)
        
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
    return name1_msgs, name2_msgs, times_dict

def print_timestamp(timestamp):
    print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))    

def add_day_to_name(name, times_dict, dates):
    for date_time in times_dict[name]:
        date = datetime.datetime.fromtimestamp(date_time).strftime('%Y-%m-%d')
        if date not in dates:
            dates[date] = 0
        dates[date] += 1
        
def by_day(times_dict, name1, name2):
    dates1 = OrderedDict()
    dates2 = OrderedDict()

    add_day_to_name(name1, times_dict, dates1)
    add_day_to_name(name2, times_dict, dates2)
            
    return dates1, dates2

name1_msgs, name2_msgs, times_dict = build_msg_dict(messages)
name1_count, name2_count = len(name1_msgs), len(name2_msgs)
total_count = name1_count+name2_count
dates1, dates2 = by_day(times_dict, name1, name2)

maxx = datetime.datetime(*(time.strptime(max(max(dates1), max(dates2)), '%Y-%m-%d')[:3]))
minn = datetime.datetime(*(time.strptime(min(min(dates1), min(dates2)), '%Y-%m-%d')[:3]))
time_elapsed = (maxx-minn).days

dates_list =[]
for i in range(time_elapsed + 1):
    dates_list.append((minn + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))

person1_data = []
person2_data = []

for i in dates_list:
    if i in dates1:
        person1_data.append(dates1[i])
    else: person1_data.append(0)
    
for i in dates_list:
    if i in dates2:
        person2_data.append(dates2[i])
    else: person2_data.append(0)

ind = np.arange(time_elapsed+1)
p1 = plt.bar(ind, person1_data, color='green')
p2 = plt.bar(ind, person2_data, color='blue')

plt.xticks(ind, dates_list, rotation=90)
plt.legend((p1[0], p2[0]), (name1, name2))
plt.title('Message distribution by date')

'''Person1_data and person2_data are both correct, but the bar graph is not for some inexplicable reason'''
    
##piechart = plt.subplot()                                   
##labels = name1 + ": " + str(name1_count), name2 + ": " + str(name2_count)
##sizes = [name1_count/total_count, name2_count/total_count]
##piechart.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
##piechart.axis('equal')
##plt.title('Message distribution')
plt.show()

