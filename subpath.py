import os
from getkeys import get_keys
from argparse import ArgumentParser

class Sim:
    def __init__(self):
        self.subpath_amount = []
        self.no_subpath_amount = []
        self.total = []

# read files and store the data
def extract_data(folder):
    dir_list = [x[0] for x in os.walk(".\\" + get_keys() + "\\" + str(folder))]
    dir_list.pop(0)

    sim_list = []
    for i in range(len(dir_list)):
        sim = Sim()
        input_file1 = open(dir_list[i] + "\\" + "output2.txt", "r", 1)
        input_file2 = open(dir_list[i] + "\\" + "output3.txt", "r", 1)
        
        def get_file_data(input_file):
            data = []
            i = 0
            line_len = 0;
            while line_len != 1:
                line = input_file.readline()
                line_len = len(line)    
                
                if i % 3 == 2:
                    data.append(int(line.split()[-1]))
                
                i += 1
            return data
        
        
        data1 = get_file_data(input_file1)
        data2 = get_file_data(input_file2)
        input_file1.close()
        input_file2.close()
        
        for j in range(len(data1)):
            sim.subpath_amount.append(data2[j])
            sim.no_subpath_amount.append(data1[j]-data2[j])
            sim.total.append(data1[j])
        
        sim_list.append(sim)
    return sim_list

# max num of hops in all files
def calc_max_sim_size(sim_list):
    max_sim_size = 0
    for sim in sim_list:
        sim_size = len(sim.subpath_amount)
        if(sim_size > max_sim_size):
            max_sim_size = sim_size
    return max_sim_size

# calc mean
def calc_mean(sim_list, max_sim_size, length_filter):
    sims_mean = Sim()
    for i in range(max_sim_size):
        sim_in_hop_counter = 0;
        sims_mean.subpath_amount.append(0)
        sims_mean.no_subpath_amount.append(0)
        sims_mean.total.append(0)
        for sim in sim_list:
            sim_size = len(sim.subpath_amount)
            if(length_filter == True and max_sim_size != sim_size):
                continue
            if(i < sim_size):
                sim_in_hop_counter +=1
                sims_mean.subpath_amount[i] += sim.subpath_amount[i]
                sims_mean.no_subpath_amount[i] += sim.no_subpath_amount[i]
                sims_mean.total[i] += sim.total[i]
        sims_mean.subpath_amount[i] /= sim_in_hop_counter
        sims_mean.no_subpath_amount[i] /= sim_in_hop_counter
        #print(sims_mean.total[i], end=" ")
        #print(sim_in_hop_counter)
        sims_mean.total[i] /= sim_in_hop_counter
    return sims_mean

# calc std_dev
def calc_std_dev(sim_list, sims_mean, max_sim_size, length_filter): 
    std_dev = Hop()
    for i in range(max_sim_size):
        counter = 0;
        std_dev.append(0)
        for sim in sim_list:
            sim_size = len(sim.subpath_amount)
            if(length_filter == True and max_sim_size != sim_size):
                continue
            if(i < sim_size):
                counter += 1
                std_dev.subpath_amount[i] += (sims_mean.subpath_amount[i] - sim[i])**2
                std_dev.no_subpath_amount[i] += (sims_mean.no_subpath_amount[i] - sim[i])**2
                std_dev.total[i] += (sims_mean.total[i] - sim[i])**2
        std_dev.subpath_amount[i] /= counter
        std_dev.no_subpath_amount[i] /= counter
        std_dev.total[i] /= counter
        std_dev.subpath_amount[i] **= 0.5
        std_dev.no_subpath_amount[i] **= 0.5
        std_dev.total[i] **= 0.5
    return std_dev

# save mean and std_dev
#def save_data(size, sims_mean, std_dev, max_sim_size, is_filtered):
def save_data(size, sims_mean, max_sim_size, is_filtered):
    if is_filtered == False:
        filename = get_keys() + "\\" + "subpath_" + str(size) + ".txt"
    else:
        filename = get_keys() + "\\" + "subpath_" + str(size) + "_" + str(max_sim_size) + ".txt"
    f = open(filename, "w")
    for i in range(max_sim_size):
        f.write("hop: " + str(i) + "\n")
        f.write(str(sims_mean.subpath_amount[i]) + "\n")
        #f.write(str(std_dev.subpath_amount[i]) + "\n")
        f.write(str(sims_mean.no_subpath_amount[i]) + "\n")
        #f.write(str(std_dev.no_subpath_amount[i]) + "\n")
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
        ##print(mean.m1)
        ##import inspect
        ##for sim in inspect.getmembers(mean): print(sim)
        ##std_dev = calc_std_dev(sim_list, mean, max_sim_size)
        ##save_data(size, mean, std_dev, max_sim_size)
        #save_data(size, mean, max_sim_size)
