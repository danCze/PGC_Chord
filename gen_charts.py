import os
import matplotlib.pyplot as plt
import numpy as np
import sys
from getkeys import get_keys
from argparse import ArgumentParser

class Stats:
    def __init__(self):
        self.pareto = []
        self.p1 = []
        self.p5 = []
        self.p10 = []

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
            stats.pareto.append(amount)
        if i % 7 == 2:
            stats.pareto[-1] *= 100 / amount
        if i % 7 == 3:
            stats.p1.append(amount)
        if i % 7 == 4:
            stats.p5.append(amount)
        if i % 7 == 5:
            stats.p10.append(amount)
        if i % 7 == 6:
            stats.p1[-1] *= 100 / amount
            stats.p5[-1] *= 100 / amount
            stats.p10[-1] *= 100 / amount
    
    return stats

#plot and save charts
def save_charts(stats, length):
    #cast stats to correct type
    x1 = np.array(range(1, len(stats.p1) + 1))
    y1 = np.array(stats.p1)
    x2 = np.array(range(1, len(stats.p5) + 1))
    y2 = np.array(stats.p5)
    x3 = np.array(range(1, len(stats.p10) + 1))
    y3 = np.array(stats.p10)
    
    #plot axes
    fig, ax = plt.subplots()
    ax.set_xlabel("nível")
    ax.set_ylabel("%")
    
    ax.plot(x1, y1, label="maior nó", marker=".")
    ax.plot(x2, y2, label="5 maiores nós", marker=".")
    ax.plot(x3, y3, label="10 maiores nós", marker=".")
    
    # Shrink current axis"s height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15,
                     box.width, box.height * 0.85])
    
    # Put a legend below current axis
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15),
              fancybox=False, shadow=False, ncols=2)
    ax.set_xlim(1, x1.size)
    ax.set_ylim(0, 100)
    
    ax.set_xmargin(0)
    ax.set_ymargin(0)
    
    plt.grid(axis="both")
    
    plt.xticks(range(1, x1.size + 1))
    plt.yticks(range(0, 101, 10))
    
    #save and plot charts
    if length == None:
        name = get_keys() + "\\" + "metrics_amount_" + str(size) + "_" + get_keys()
    else:
        name = get_keys() + "\\" + "metrics_amount_" + str(size) + "_" + get_keys() + "_" + str(length)
    plt.savefig(name, dpi = 100)
    plt.show()

#plot and save pareto charts
def save_pareto(stats, length):
    #cast stats to correct type
    x1 = np.array(range(1, len(stats.pareto) + 1))
    y1 = np.array(stats.pareto)
    
    #plot axes
    fig, ax = plt.subplots()
    ax.set_xlabel("nível")
    ax.set_ylabel("%")
    
    ax.plot(x1, y1, label="pareto (80% subcaminhos)", marker=".")
    
    # Shrink current axis"s height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15,
                     box.width, box.height * 0.85])
    
    # Put a legend below current axis
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15),
              fancybox=False, shadow=False, ncols=1)
    ax.set_xlim(1, x1.size)
    ax.set_ylim(0, 100)
    
    ax.set_xmargin(0)
    ax.set_ymargin(0)
    
    plt.grid(axis="both")
    
    plt.xticks(range(1, x1.size + 1))
    plt.yticks(range(0, 101, 10))
    
    #save and plot charts
    if length == None:
        name = get_keys() + "\\" + "pareto_" + str(size) + "_" + get_keys()
    else:
        name = get_keys() + "\\" + "pareto_" + str(size) + "_" + get_keys() + "_" + str(length)
    plt.savefig(name, dpi = 100)
    plt.show()
    
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
        save_charts(stats, args.length_filter)
        save_pareto(stats, args.length_filter)
