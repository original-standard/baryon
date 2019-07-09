import copy

def jackknife(data):
    conf = len(data)
    ret = []
    GT = summation(data)
    for i in range(conf):
        ret.append(GT)
    for i in range(conf):
        ret[i] = (ret[i] - data[i]) / (conf - 1.)

    return ret

def median(data):
    GT = copy.deepcopy(data[0])
    for i in data[1:]:
        GT = GT + i
    GT = GT / len(data)
    return GT

def conv(source,sink,op):
    return (12 * (sink + 7 * source) + op)

def summation(data):
    GT = copy.deepcopy(data[0])
    for i in data[1:]:
        GT = GT + i
    return GT
