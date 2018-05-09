import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import datetime
import time
import numpy as np
from dateutil.relativedelta import *
import similarity


name1 = "Jordan Stern"
name2 = "Person 2"

with open('message.json', 'r') as fr:
    messages_dict = OrderedDict(json.load(fr))
messages = messages_dict["messages"]


def build_msg_dict(messages):
    msg_dict ={}
    times_dict = {name1: [], name2: []}
    name1_count, name2_count = 0, 0
    for message in messages:
        name = message["sender_name"]
        time = message["timestamp"]

        times_dict[name].append(time)

        if "photos" in message:
            msg_dict[time] = (name, ("photos", message["photos"]))
        elif "gifs" in message:
            msg_dict[time] = (name, ("gifs", message["gifs"]))
        elif "sticker" in message:
            msg_dict[time] = (name, ("sticker", message["sticker"]))
        elif "files" in message:
            msg_dict[time] = (name, ("files", message["files"]))
        elif "content" in message:
            msg_dict[time] = (name, ("content", message["content"]))
        elif "share" in message:
            msg_dict[time] = (name, ("share", message["share"]))
        elif "videos" in message:
            msg_dict[time] = (name, ("videos", message["videos"]))
        else:
            continue

        if name == name1:
            name1_count += 1
        else:
            name2_count += 1

    return name1_count, name2_count, times_dict, msg_dict

def print_timestamp(timestamp):
    print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))

def add_day_to_name(name, times_dict, dates):
    for date_time in times_dict[name]:
        date = datetime.datetime.fromtimestamp(date_time).strftime('%Y-%m-%d')
        if date not in dates:
            dates[date] = 0
        dates[date] += 1

def add_month_to_name(name, times_dict, months):
    for date_time in times_dict[name]:
        month = datetime.datetime.fromtimestamp(date_time).strftime('%Y-%m-01')
        if month not in months:
            months[month] = 0
        months[month] += 1

def add_week_to_name(name, first_day, times_dict, weeks):
    for date_time in times_dict[name]:
        day = datetime.datetime.fromtimestamp(date_time)
        day_delta = (day - first_day).days
        week_num = (day_delta)/7
        week = (first_day + relativedelta(weeks=+week_num)).strftime('%Y-%m-%d')
        if week not in weeks:
            weeks[week] = 0
        weeks[week] += 1

def by_day(times_dict, name1, name2):
    dates1 = OrderedDict()
    dates2 = OrderedDict()

    add_day_to_name(name1, times_dict, dates1)
    add_day_to_name(name2, times_dict, dates2)

    return dates1, dates2

def by_month(times_dict, name1, name2):
    dates1 = OrderedDict()
    dates2 = OrderedDict()

    add_month_to_name(name1, times_dict, dates1)
    add_month_to_name(name2, times_dict, dates2)

    return dates1, dates2

def by_week (times_dict, first_day, name1, name2):
    dates1 = OrderedDict()
    dates2 = OrderedDict()

    add_week_to_name(name1, first_day, times_dict, dates1)
    add_week_to_name(name2, first_day, times_dict, dates2)

    return dates1, dates2

def plot_by_day (times_dict):
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

    plot_by_time(person1_data, person2_data, dates_list, "Day", 2)

def plot_by_month (times_dict):
    dates1, dates2 = by_month(times_dict, name1, name2)

    maxx = datetime.datetime(*(time.strptime(max(max(dates1), max(dates2)), '%Y-%m-01')[:3]))
    minn = datetime.datetime(*(time.strptime(min(min(dates1), min(dates2)), '%Y-%m-01')[:3]))
    time_elapsed = (maxx.year - minn.year) * 12 + (maxx.month - minn.month) + 1
    dates_list =[]
    for i in range(time_elapsed):
        dates_list.append((minn + relativedelta(months=+i)).strftime('%Y-%m'))

    person1_data = []
    person2_data = []

    for i in dates_list:
        temp_date = (i+"-01")
        if temp_date in dates1:
            person1_data.append(dates1[temp_date])
        else: person1_data.append(0)

    for i in dates_list:
        temp_date = (i+"-01")
        if temp_date in dates2:
            person2_data.append(dates2[temp_date])
        else: person2_data.append(0)

    plot_by_time(person1_data, person2_data, dates_list, "Month", 4)

def plot_by_week (times_dict):
    first_week = datetime.datetime.fromtimestamp(min(min(times_dict[name1]), min(times_dict[name2])))
    dates1, dates2 = by_week(times_dict, first_week, name1, name2)
    last_week = max(max(dates1), max(dates2))
    last_week = datetime.datetime.strptime(last_week, '%Y-%m-%d')
    time_elapsed = (((last_week - first_week).days)/7) + 1

    dates_list = []
    for i in range(time_elapsed+1):
        dates_list.append((first_week + relativedelta(weeks=+i)).strftime('%Y-%m-%d'))

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

    plot_by_time(person1_data, person2_data, dates_list, "Week", 3)

def plot_piechart(name1_count, name2_count, total_count):
    piechart = plt.subplot(2, 2, 1)
    labels = name1 + ": " + str(name1_count), name2 + ": " + str(name2_count)
    sizes = [float(name1_count)/total_count, float(name2_count)/total_count]
    piechart.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    piechart.axis('equal')
    plt.title('Message Distribution')

def plot_by_time (person1_data, person2_data, dates_list, period, num):
    ind = np.arange(len(dates_list))
    width = 0.35
    p1 = plt.subplot(2, 2, num)
    p2 = plt.subplot(2, 2, num)
    p1 = plt.bar(ind, person1_data, color='royalblue')
    p2 = plt.bar(ind, person2_data, bottom=person1_data, color='seagreen')
    plt.xticks(ind)
    plt.xticks(ind, dates_list, rotation=90)
    plt.legend((p1[0], p2[0]), (name1, name2))
    plt.title('Message Distribution by ' + period)

def plot(name1_count, name2_count, total_count, time_dict):
    plot_piechart(name1_count, name2_count, total_count)
    plot_by_day(time_dict)
    plot_by_week(time_dict)
    plot_by_month(time_dict)
    plt.show()

def plot_avg_msg_length(name1_count, name2_count, msg_dict):
    name1_dict = {
                  "content": 0,
                  "photos": 0,
                  "gifs": 0,
                  "sticker": 0,
                  "files": 0,
                  "share": 0,
                  "videos": 0,
              }
    name2_dict = {
                  "content": 0,
                  "photos": 0,
                  "gifs": 0,
                  "sticker": 0,
                  "files": 0,
                  "share": 0,
                  "videos": 0,
                }

    for time in msg_dict:
        message = msg_dict[time]
        name = message[0]
        if name == name1:
            curr_dict = name1_dict
        else:
            curr_dict = name2_dict
        msg_type = message[1][0]
        if msg_type == "content":
            msg_length = len(message[1][1])
        else:
            msg_length = 1
        curr_dict[msg_type] += msg_length
    name1_dict["content"] /= name1_count
    name2_dict["content"] /= name2_count

    name1_list = sorted(name1_dict.values())
    name2_list = sorted(name2_dict.values())

    total_count = name1_count + name2_count

    messages = plt.subplot(2, 2, 1)
    labels =str(name1_count), str(name2_count)
    messages.pie([float(name1_count)/total_count, float(name2_count)/total_count], labels=labels)
    messages.axis('equal')
    messages.set_title("Message Count")

    photos = plt.subplot(2, 2, 2)
    amt1, amt2 = name1_dict["photos"], name2_dict["photos"]
    labels = str(amt1), str(amt2)
    photos.pie([amt1/float(amt1+amt2), amt2/float(amt1+amt2)], labels=labels)
    photos.axis('equal')
    photos.set_title("Photo Count")

    gifs = plt.subplot(2, 2, 3)
    amt1, amt2 = name1_dict["gifs"], name2_dict["gifs"]
    labels = str(amt1), str(amt2)
    gifs.pie([amt1/float(amt1+amt2), amt2/float(amt1+amt2)], labels=labels)
    gifs.axis('equal')
    gifs.set_title("Gif Count")

    sticker = plt.subplot(2, 2, 4)
    amt1, amt2 = name1_dict["sticker"], name2_dict["sticker"]
    labels = str(amt1), str(amt2)
    sticker.pie([amt1/float(amt1+amt2), amt2/float(amt1+amt2)], labels=labels)
    sticker.axis('equal')
    sticker.set_title("Sticker Count")

    plt.legend([name1, name2])

    print(name1_dict)
    print(name2_dict)
    plt.show()

def top_words_dict(msg_dict, num):
    msg_dict_by_person = similarity.split_by_person(msg_dict)
    inv_idx = similarity.build_inverted_index(msg_dict_by_person)
    word_ids = similarity.create_word_ids(inv_idx)
    word_freqs = similarity.word_frequencies(word_ids, inv_idx)
    weighted_words = similarity.create_weighted_word_freq_array(word_freqs)
    weighted_top = similarity.weighted_ranked_words(word_ids, weighted_words, name1, name2, num)
    return weighted_top

def plot_top_words(top_words, name1, name2):
    scores = {}
    words = {}
    for name in top_words:
        scores[name] = []
        words[name] = []
        for result in top_words[name]:
            scores[name].append(result[0])
            words[name].append(result[1])

    ind = np.arange(len(top_words[name1]))
    ind2 = np.arange(len(top_words[name2]))

    p1 = plt.subplot(2, 1, 1)
    plt.title('Most Frequent Words - ' + name1)
    p1 = plt.bar(ind2, scores[name1], tick_label=words[name1], color='blue')
    plt.xticks(rotation=75)

    p2 = plt.subplot(2, 1, 2)
    plt.title('Most Frequent Words - ' + name2)
    p2 = plt.bar(ind, scores[name2], tick_label=words[name2], color='orange')
    plt.xticks(rotation=75)

    plt.show()

def main():
    name1_count, name2_count, times_dict, msg_dict = build_msg_dict(messages)
    total_count = name1_count+name2_count
    #plot(name1_count, name2_count, total_count, times_dict)
    #plot_avg_msg_length(name1_count, name2_count, msg_dict)
    top_words = top_words_dict(msg_dict, 25)
    plot_top_words(top_words, name1, name2)

main()
