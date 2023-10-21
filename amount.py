import os
from getkeys import get_keys
from argparse import ArgumentParser

class Sim:
    def __init__(self):
        self.pareto1 = []
        self.pareto2 = []
        self.m1 = []
        self.m5 = []
        self.m10 = []
        self.total = []

# read files and store the data
def extract_data(folder):
    dir_list = [x[0] for x in os.walk(".\\" + get_keys() + "\\" + str(folder))]
    dir_list.pop(0)

    sim_list = []
    for i in range(len(dir_list)):
        sim = Sim()
        input_file = open(dir_list[i] + "\\" + "output6.txt", "r", 1)
        lines_list = input_file.readlines()
        
        for j in range(len(lines_list)):
            line = lines_list[j]
            line_len = len(line)
            if(line_len == 1):
                pass
            elif(line_len < 30):
                coord = line.split()
                #perc = 100 * int(coord[0]) / int(coord[1])
                if(j % 5 == 0):
                    sim.pareto1.append(int(coord[0]))
                    sim.pareto2.append(int(coord[1]))
                if(j % 5 == 1):
                    sim.m1.append(int(coord[0]))
                    sim.total.append(int(coord[1]))
                if(j % 5 == 2):
                    sim.m5.append(int(coord[0]))
                if(j % 5 == 3):
                    sim.m10.append(int(coord[0]))
            else:
                sim_list.append(sim)
    return sim_list

# max num of hops in all files
def calc_max_sim_size(sim_list):
    max_sim_size = 0
    for sim in sim_list:
        sim_size = len(sim.m1)
        if(sim_size > max_sim_size):
            max_sim_size = sim_size
    return max_sim_size

# calc mean
def calc_mean(sim_list, max_sim_size, length_filter):
    sims_mean = Sim()
    for i in range(max_sim_size):
        sim_in_hop_counter = 0
        sims_mean.pareto1.append(0)
        sims_mean.pareto2.append(0)
        sims_mean.m1.append(0)
        sims_mean.m5.append(0)
        sims_mean.m10.append(0)
        sims_mean.total.append(0)
        for sim in sim_list:
            sim_size = len(sim.m1)
            if length_filter == True and max_sim_size != sim_size:
                continue
            if i < sim_size:
                sim_in_hop_counter +=1
                sims_mean.pareto1[i] += sim.pareto1[i]
                sims_mean.pareto2[i] += sim.pareto2[i]
                sims_mean.m1[i] += sim.m1[i]
                sims_mean.m5[i] += sim.m5[i]
                sims_mean.m10[i] += sim.m10[i]
                sims_mean.total[i] += sim.total[i]
        sims_mean.pareto1[i] /= sim_in_hop_counter
        sims_mean.pareto2[i] /= sim_in_hop_counter
        sims_mean.m1[i] /= sim_in_hop_counter
        sims_mean.m5[i] /= sim_in_hop_counter
        sims_mean.m10[i] /= sim_in_hop_counter
        sims_mean.total[i] /= sim_in_hop_counter
    return sims_mean

# calc std_dev
def calc_std_dev(sim_list, sims_mean, max_sim_size, length_filter): 
    std_dev = Sim()
    for i in range(max_sim_size):
        counter = 0;
        std_dev.append(0)
        for sim in sim_list:
            sim_size = len(sim.m1)
            if length_filter == True and max_sim_size != sim_size:
                continue
            if i < sim_size:
                counter += 1
                std_dev.pareto1[i] += (sims_mean.pareto1[i] - sim[i])**2
                std_dev.pareto2[i] += (sims_mean.pareto2[i] - sim[i])**2
                std_dev.m1[i] += (sims_mean.m1[i] - sim[i])**2
                std_dev.m5[i] += (sims_mean.m5[i] - sim[i])**2
                std_dev.m10[i] += (sims_mean.m10[i] - sim[i])**2
                std_dev.total[i] += (sims_mean.total[i] - sim[i])**2
        std_dev.pareto1[i] /= counter
        std_dev.pareto2[i] /= counter
        std_dev.m1[i] /= counter
        std_dev.m5[i] /= counter
        std_dev.m10[i] /= counter
        std_dev.total[i] /= counter
        std_dev.pareto1[i] **= 0.5
        std_dev.pareto2[i] **= 0.5
        std_dev.m1[i] **= 0.5
        std_dev.m5[i] **= 0.5
        std_dev.m10[i] **= 0.5
        std_dev.total[i] **= 0.5
    return std_dev

# save mean and std_dev
#def save_data(size, sims_mean, std_dev, max_sim_size, is_filtered):
def save_data(size, sims_mean, max_sim_size, is_filtered):
    if is_filtered == False:
        filename = get_keys() + "\\" + "amount_" + str(size) + ".txt"
    else:
        filename = get_keys() + "\\" + "amount_" + str(size) + "_" + str(max_sim_size) + ".txt"
    f = open(filename, "w")
    for i in range(max_sim_size):
        f.write("hop: " + str(i+1) + "\n")
        f.write(str(sims_mean.pareto1[i]) + "\n")
        #f.write(str(std_dev.pareto1[i]) + "\n")
        f.write(str(sims_mean.pareto2[i]) + "\n")
        #f.write(str(std_dev.pareto2[i]) + "\n")
        f.write(str(sims_mean.m1[i]) + "\n")
        #f.write(str(std_dev.m1[i]) + "\n")
        f.write(str(sims_mean.m5[i]) + "\n")
        #f.write(str(std_dev.m5[i]) + "\n")
        f.write(str(sims_mean.m10[i]) + "\n")
        #f.write(str(std_dev.m10[i]) + "\n")
        f.write(str(sims_mean.total[i]) + "\n")
        #f.write(str(std_dev.total[i]) + "\n")

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument("-l","--length_filter", type=int)
    parser.add_argument("-n","--network_filter", type=int)
    
    args = parser.parse_args()
    #using output 2 instead of 6
    #if args.length_filter != None:
    #   args.length_filter -= 2 #output 6 lacks first and last hop
    
    if args.network_filter == None:
        sizes = [f.name for f in os.scandir(get_keys()) if f.is_dir()]
    else:
        sizes = [str(args.network_filter)]
    for size in sizes:
        print("Computing data for network size: " + size)
        sim_list = extract_data(size)
        if args.length_filter == None:
            max_sim_size = calc_max_sim_size(sim_list)
            mean = calc_mean(sim_list, max_sim_size, False)
            #std_dev = calc_std_dev(sim_list, mean, max_sim_size, False)
            #save_data(size, mean, std_dev, max_sim_size)
            save_data(size, mean, max_sim_size, False)
        else:
            try:
                mean = calc_mean(sim_list, args.length_filter, True)
            except ZeroDivisionError as e:
                exit("This network size has no simulations with this amount of hops. Aborting.")
            #std_dev = calc_std_dev(sim_list, mean, args.length_filter, True)
            #save_data(size, mean, std_dev, args.length_filter)
            save_data(size, mean, args.length_filter, True)
        
        #max_sim_size = calc_max_sim_size(sim_list)
        #mean = calc_mean(sim_list, max_sim_size)
        #print(mean.m1)
        ##import inspect
        ##for sim in inspect.getmembers(mean): print(sim)
        ##std_dev = calc_std_dev(sim_list, mean, max_sim_size)
        ##save_data(size, mean, std_dev, max_sim_size)
        #save_data(size, mean, max_sim_size)
