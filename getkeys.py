def get_keys():
    f = open("keys.cfg")
    keys = f.read().rstrip()
    f.close()
    return keys