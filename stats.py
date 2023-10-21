import os
import matplotlib.pyplot as plt
import numpy as np
import sys
from getkeys import get_keys
from argparse import ArgumentParser

class Stats:
    def __init__(self):
        self.pareto1 = []
        self.pareto2 = []
        self.m1 = []
        self.m5 = []
        self.m10 = []
        self.total = []

# read files and store the data
def extract_data(size, length):
    stats = Stats()
    if length == None:
        filename = get_keys() + "\\amount_" + str(size) + ".txt"
    else:
        filename = get_keys() + "\\amount_" + str(size) + "_" + str(length) + ".txt"
    input_file = open(filename, "r", 1)
    lines_list = input_file.readlines()
    
    for i in range(len(lines_list)):
        if i % 7 == 0:
            continue
        
        line = lines_list[i]
        amount = float(line)
        if i % 7 == 1:
            stats.pareto1.append(amount)
        if i % 7 == 2:
            stats.pareto2.append(amount)
        if i % 7 == 3:
            stats.m1.append(amount)
        if i % 7 == 4:
            stats.m5.append(amount)
        if i % 7 == 5:
            stats.m10.append(amount)
        if i % 7 == 6:
            stats.total.append(amount)
    
    return stats

# save data
def save_data(stats, length):
    if length == None:
        name = get_keys() + "\\" + "stats_size-" + str(size) + "_key-" + get_keys() + ".txt"
    else:
        name = get_keys() + "\\" + "stats_size-" + str(size) + "_key-" + get_keys() + "_length-" + str(length) + ".txt"
    f = open(name, "w")
    for i in range(len(stats.m1)):
        f.write("hop: " + str(i+1) + "\n")
        f.write(str(100 * stats.pareto1[i] / stats.pareto2[i]) + "\n")
        f.write(str(100 * stats.m1[i] / stats.total[i]) + "\n")
        f.write(str(100 * stats.m5[i] / stats.total[i]) + "\n")
        f.write(str(100 * stats.m10[i] / stats.total[i]) + "\n")

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument("-l","--length_filter", type=int)
    parser.add_argument("-n","--network_filter", type=int)
    
    args = parser.parse_args()
    
    if args.network_filter == None:
        sizes = [f.name for f in os.scandir(get_keys()) if f.is_dir()]
    else:
        sizes = [str(args.network_filter)]
    for size in sizes:
        print("Computing data for network size: " + size)
        stats = extract_data(size, args.length_filter)
        save_data(stats, args.length_filter)
