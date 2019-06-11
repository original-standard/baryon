import baryon
import re
import utils
import math
import copy

class read_2pt_rest:
    jack = []
    def __init__(self,argvs,argc,C):
        self.jack = []
        CONF = C
        conf = []
        conf_ama = []
        fold = []
        for i in argvs:
            ml = 0.
            ms = 0.
            baryons = []
            baryons_ama = []
            with open(i,"r") as file:
                num = 0
                for line in file:
                    line = line.rstrip()
                    if(re.split(" +",line)[0] == 'STARTPROP'):
                        baryons.append(baryon.read_baryon_prop(file,num,ml,ms))

            with open(i.replace("dat","dat_ama"),"r") as file:
                num = 0
                for line in file:
                    line = line.rstrip()
                    if(re.split(" +",line)[0] == 'STARTPROP'):
                        baryons_ama.append(baryon.read_baryon_prop(file,num,ml,ms))
            conf.append(baryons)
            conf_ama.append(baryons_ama)

        for i in range(len(conf[0])):
            self.jack.append([conf[j][i] - conf_ama[j][i] for j in range(len(conf))])




class read_2pt_ama:
    jack = []
    def __init__(self,argvs,argc,C):
        self.jack = []
        CONF = C
        conf = []
        fold = []
        for i in argvs:
            ml = 0.
            ms = 0.
            baryons = []
            baryons_ama = []
            with open(i,"r") as file:
                num = 0
                for line in file:
                    line = line.rstrip()
                    if(re.split(" +",line)[0] == 'STARTPROP'):
                        baryons.append(baryon.read_baryon_prop(file,num,ml,ms))

            conf.append(baryons)

        GT = copy.deepcopy(conf[0])
        for i in conf[1:]:
            for j in range(len(i)):
                GT[j] = GT[j] + i[j]
        self.jack = list(map(lambda x : x / len(conf),GT))
