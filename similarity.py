from collections import defaultdict
from collections import OrderedDict
from collections import Counter
import math
import time
import numpy as np
import re
from nltk.tokenize import TreebankWordTokenizer

def split_by_person(msg_dict):
    msg_dict_by_person = defaultdict()

    for time in msg_dict:
        message = msg_dict[time]
        name = message[0]
        msg_type = message[1][0]
        if msg_type != "content":
            continue
        text = message[1][1]
        text = re.findall("[a-z]+", text.lower())
        if name in msg_dict_by_person:
            msg_dict_by_person[name].append(text)
        else:
            msg_dict_by_person[name] = text
    return msg_dict_by_person


def build_inverted_index(msg_dict_by_person):
    inverted_index = defaultdict()
    name_counter = 0
    for name in msg_dict_by_person:
        names_messages = msg_dict_by_person[name]
        for message in names_messages:
            freqs = Counter(message)
            for word in freqs:
                if word not in inverted_index:
                    inverted_index[word] = [0, 0]
                inverted_index[word][name_counter] += freqs[word]
        name_counter += 1
    return inverted_index

def create_word_ids(inv_idx):
    word_ids = defaultdict()
    words = sorted(inv_idx)
    counter = 0
    for word in words:
        word_ids[word] = counter
        counter += 1
    return word_ids


def word_frequencies(word_ids, inv_idx):
    array = np.zeros(shape=(2, len(inv_idx)))
    for word in inv_idx:
        for person in range(2):
            array[person][word_ids[word]] = inv_idx[word][person]
    return array


def create_weighted_word_freq_array(word_freqs):
    array_t = np.transpose(word_freqs)
    for i in range(len(array_t)):
        sum_col = np.sum(array_t[i]) + 1
        for j in range(len(array_t[i])):
            word_freqs[j][i] = word_freqs[j][i]/sum_col
    return word_freqs

def weighted_ranked_words(word_ids, weighted_words, name1, name2, num):
    names = [name1, name2]
    tops = {}
    for id in range(2):
        tops[names[id]] = []
        top_fifty = sorted(weighted_words[id], reverse=True)[:num]
        top_fifty_indexes = []
        count = 0
        for freq in top_fifty:
            for elem in np.where(weighted_words[id]==freq)[0]:
                if elem not in top_fifty_indexes and count < num:
                    top_fifty_indexes.append(elem)
                    count += 1
                    tops[names[id]].append((freq, sorted(word_ids.keys())[elem]))
    return tops