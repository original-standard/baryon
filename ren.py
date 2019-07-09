import sys
import copy
import math

conf = []
for i in sys.argv[2:]:
    corr = []
    with open(i,"r") as file:
        for line in file:
            corr.append(float(line))
    conf.append(corr)

ave = copy.deepcopy(conf[0]) 

for i in conf[1:]:
    for j in range(len(i)):
        ave[j] = ave[j] + i[j]

for i in range(len(ave)):
    ave[i] = ave[i] / len(conf)

jack = [0. for i in range(len(conf[0]))]

for i in conf:
    for j in range(len(i)):
        jack[j] = jack[j] + (ave[j] - i[j]) * (ave[j] - i[j]) * (len(conf)  - 1.) / len(conf) 

for i in range(len(ave)):
    print("%d %e %e" % (i,ave[i] * float(sys.argv[1]),math.sqrt(jack[i]) * float(sys.argv[1]) ))
