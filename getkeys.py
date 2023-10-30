def get_keys():
    f = open("keys.cfg")
    keys = f.read().rstrip()
    f.close()
    if get_keys.first == True: print("number of keys: " + keys)
    get_keys.first = False
    return keys
get_keys.first = True
get_keys()