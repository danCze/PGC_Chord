import os

class Stats:
    def __init__(self):
        self.min80 = []
        self.num80 = []
        self.p80 = []
        self.p1 = []
        self.p5 = []
        self.p10 = []

# read files and store the data
def extract_data(folder):
    dir_list = [x[0] for x in os.walk(".\\" + str(folder))]
    dir_list.pop(0)

    stats_list = []
    for i in range(30):
        stats = Stats()
        input_file = open(dir_list[i] + "\\" + "output6.txt", "r", 1)
        lines_list = input_file.readlines()
        
        for j in range(len(lines_list)):
            line = lines_list[j]
            line_len = len(line)
            if(line_len == 1):
                pass
            elif(line_len < 30):
                coord = line.split()
                perc = 100 * int(coord[0]) / int(coord[1])
                if(j % 5 == 0):
                    stats.min80.append(int(coord[0]))
                    stats.num80.append(int(coord[1]))
                    stats.p80.append(perc)
                if(j % 5 == 1):
                    stats.p1.append(perc)
                if(j % 5 == 2):
                    stats.p5.append(perc)
                if(j % 5 == 3):
                    stats.p10.append(perc)
            else:
                stats_list.append(stats)
    return stats_list

# max num of hops in all files
def calc_max_hop(stats_list):
    max_hop = 0
    for i in range(30):
        curr_len = len(stats_list[i].p80)
        if(curr_len > max_hop):
            max_hop = curr_len
    return max_hop

# calc mean
def calc_mean(stats_list, max_hop):
    stats_mean = Stats()
    for i in range(max_hop):
        counter = 0;
        stats_mean.min80.append(0)
        stats_mean.num80.append(0)
        stats_mean.p80.append(0)
        stats_mean.p1.append(0)
        stats_mean.p5.append(0)
        stats_mean.p10.append(0)
        for j in range(30):
            curr_max_hop = len(stats_list[j].p80)
            if(i < curr_max_hop):
                counter += 1
                stats_mean.min80[i] += stats_list[j].min80[i]
                stats_mean.num80[i] += stats_list[j].num80[i]
                stats_mean.p80[i] += stats_list[j].p80[i]
                stats_mean.p1[i] += stats_list[j].p1[i]
                stats_mean.p5[i] += stats_list[j].p5[i]
                stats_mean.p10[i] += stats_list[j].p10[i]
        stats_mean.min80[i] /= counter
        stats_mean.num80[i] /= counter
        stats_mean.p80[i] /= counter
        stats_mean.p1[i] /= counter
        stats_mean.p5[i] /= counter
        stats_mean.p10[i] /= counter
    return stats_mean

# calc std_dev
def calc_std_dev(stats_list, stats_mean, max_hop): 
    std_dev = Stats()
    for i in range(max_hop):
        counter = 0;
        std_dev.min80.append(0)
        std_dev.num80.append(0)
        std_dev.p80.append(0)
        std_dev.p1.append(0)
        std_dev.p5.append(0)
        std_dev.p10.append(0)
        for j in range(30):
            curr_max_hop = len(stats_list[j].p80)
            if(i < curr_max_hop):
                counter += 1
                std_dev.min80[i] += (stats_mean.min80[i] - stats_list[j].min80[i])**2
                std_dev.num80[i] += (stats_mean.num80[i] - stats_list[j].num80[i])**2
                std_dev.p80[i] += (stats_mean.p80[i] - stats_list[j].p80[i])**2
                std_dev.p1[i] += (stats_mean.p1[i] - stats_list[j].p1[i])**2
                std_dev.p5[i] += (stats_mean.p5[i] - stats_list[j].p5[i])**2
                std_dev.p10[i] += (stats_mean.p10[i] - stats_list[j].p10[i])**2
        std_dev.min80[i] /= counter
        std_dev.num80[i] /= counter
        std_dev.p80[i] /= counter
        std_dev.p1[i] /= counter
        std_dev.p5[i] /= counter
        std_dev.p10[i] /= counter
        std_dev.min80[i] **= 0.5
        std_dev.num80[i] **= 0.5
        std_dev.p80[i] **= 0.5
        std_dev.p1[i] **= 0.5
        std_dev.p5[i] **= 0.5
        std_dev.p10[i] **= 0.5
    return std_dev

# save mean and std_dev
def save_data(size, stats_mean, std_dev, max_hop):
    f = open("stats_" + str(size) + ".txt", "w")
    for i in range(max_hop):
        f.write("hop: " + str(i + 1) + "\n")
        f.write(str(stats_mean.min80[i]) + " ")
        f.write(str(std_dev.min80[i]) + "\n")
        f.write(str(stats_mean.num80[i]) + " ")
        f.write(str(std_dev.num80[i]) + "\n")
        f.write(str(stats_mean.p80[i]) + " ")
        f.write(str(std_dev.p80[i]) + "\n")
        f.write(str(stats_mean.p1[i]) + " ")
        f.write(str(std_dev.p1[i]) + "\n")
        f.write(str(stats_mean.p5[i]) + " ")
        f.write(str(std_dev.p5[i]) + "\n")
        f.write(str(stats_mean.p10[i]) + " ")
        f.write(str(std_dev.p10[i]) + "\n")

if __name__ == "__main__":
    for size in [1000, 10000, 100000, 1000000]:
        stats = extract_data(size)
        max_hop = calc_max_hop(stats)
        mean = calc_mean(stats, max_hop)
        std_dev = calc_std_dev(stats, mean, max_hop)
        save_data(size, mean, std_dev, max_hop)
