import os
import matplotlib.pyplot as plt
import numpy as np
import sys
from getkeys import get_keys
from argparse import ArgumentParser

class Stats:
    def __init__(self):
        self.subpath_amount = []
        self.no_subpath_amount = []

# read files and store the data
def extract_data(size, length):
    stats = Stats()
    if length == None:
        filename = get_keys() + "\\subpath_" + str(size) + ".txt"
    else:
        filename = get_keys() + "\\subpath_" + str(size) + "_" + str(length) + ".txt"
    input_file = open(filename, "r", 1)
    lines_list = input_file.readlines()
    
    for i in range(len(lines_list)):
        if i % 4 == 0 or i % 4 == 3:
            continue
        
        line = lines_list[i]
        amount = float(line)
        if i % 4 == 1:
            stats.subpath_amount.append(amount)
        if i % 4 == 2:
            stats.no_subpath_amount.append(amount)
    
    return stats

# save_data
def save_data(stats, length):
    if length == None:
        name = get_keys() + "\\" + "subpath_high_level_" + str(size) + "_" + get_keys() + ".txt"
    else:
        name = get_keys() + "\\" + "subpath_high_level_" + str(size) + "_" + get_keys() + "_" + str(length) + ".txt"
    f = open(name, "w")
    for i in range(1, len(stats.subpath_amount)-1):
        f.write("hop: " + str(i+1) + "\n")
        f.write(str(stats.no_subpath_amount[i] / stats.subpath_amount[i]) + "\n")
    
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
