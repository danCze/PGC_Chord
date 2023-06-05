import os
import matplotlib.pyplot as plt
import numpy as np
import sys

class Stats:
    def __init__(self):
        self.p80 = []
        self.std80 = []
        self.p1 = []
        self.std1 = []
        self.p5 = []
        self.std5 = []
        self.p10 = []
        self.std10 = []

# read files and store the data
def extract_data(size):
    stats = Stats()
    input_file = open("stats_" + str(size) + ".txt", "r", 1)
    lines_list = input_file.readlines()
    
    for i in range(len(lines_list)):
        if i % 7 == 0:
            continue
        
        line = lines_list[i]
        coord = line.split()
        perc = float(coord[0])
        std = float(coord[1])
        if i % 7 == 3:
            stats.p80.append(perc)
            stats.std80.append(std)
        if i % 7 == 4:
            stats.p1.append(perc)
            stats.std1.append(std)
        if i % 7 == 5:
            stats.p5.append(perc)
            stats.std5.append(std)
        if i % 7 == 6:
            stats.p10.append(perc)
            stats.std10.append(std)
    
    return stats

#plot and save charts
def save_charts(stats, plot):
    #cast stats to correct type
    x1 = np.array(range(1, len(stats.p80) + 1))
    y1 = np.array(stats.p80)
    e1 = np.array(stats.std80)
    x2 = np.array(range(1, len(stats.p1) + 1))
    y2 = np.array(stats.p1)
    e2 = np.array(stats.std1)
    x3 = np.array(range(1, len(stats.p5) + 1))
    y3 = np.array(stats.p5)
    e3 = np.array(stats.std5)
    x4 = np.array(range(1, len(stats.p10) + 1))
    y4 = np.array(stats.p10)
    e4 = np.array(stats.std10)

    #plot axes
    fig, ax = plt.subplots()
    ax.set_xlabel("nível")
    ax.set_ylabel("%")
    
    if plot == "simple":
        ax.plot(x1, y1, label="80% subcaminhos", marker=".")
        ax.plot(x2, y2, label="maior peer", marker=".")
        ax.plot(x3, y3, label="5 maiores peers", marker=".")
        ax.plot(x4, y4, label="10 maiores peers", marker=".")
    else:
        ax.errorbar(x1, y1, e1, label="80% subcaminhos", marker=".")
        ax.errorbar(x2, y2, e2, label="maior peer", marker=".")
        ax.errorbar(x3, y3, e3, label="5 maiores peers", marker=".")
        ax.errorbar(x4, y4, e4, label="10 maiores peers", marker=".")
    
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
    name = "metrics_" + str(size) + "_" + sys.argv[1]
    plt.savefig(name, dpi = 100)
    plt.show()
    
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        exit("call program like this:\npython gen.py <1+2*<bidirectionalKeys>> [e]")
    if int(sys.argv[1]) % 2 != 1:
        exit("number of keys must be an odd number")
    if len(sys.argv) > 2 and sys.argv[2] == "e":
        plot = "std_dev"
    else:
        plot = "simple"
    for size in [1000, 10000, 100000, 1000000]:
        stats = extract_data(size)
        save_charts(stats, plot)
