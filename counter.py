import os
from getkeys import get_keys
from argparse import ArgumentParser

#count how many hops a simulation has
def count_hops(net_size, verbose):
    sizes = {}
    dir_list = [x[0] for x in os.walk(".\\" + get_keys() + "\\" + str(net_size))]
    for d in dir_list[1:]:
        filename = d + "\\output6.txt"
        file = open(filename)
        
        lines = file.readlines()
        size = int(((len(lines) - 1) / 5) + 2)
        if size not in sizes:
            sizes[size] = []
        sizes[size].append(d.split("\\")[-1])
        
        file.close()
    
    sizes = dict(sorted(sizes.items()))
    if verbose == False:
        for k in sizes.keys():
            sizes[k] = len(sizes[k])
        print(net_size + ": ", end="")
        print(sizes)
    else:
        print("net_size: " + str(net_size))
        for k in sizes.keys():
            print("number_of_hops: " + str(k))
            print(sizes[k])
            #for size in sizes[k]:
            #    print(size)
        print()

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument("-v", "--verbose", action='store_true')
    
    args = parser.parse_args()
    
    print()
    print("number of hops including first and last hops that aren't plotted. first hop's index is 0. last hop's index is <number of hops-1>.")
    print()
    for net_size in [f.name for f in os.scandir(get_keys()) if f.is_dir()]:
        count_hops(net_size, args.verbose)