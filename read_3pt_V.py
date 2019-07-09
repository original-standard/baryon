import baryon_3pt
import re
import utils
import copy
import math

class read_3pt_rest:
    jack = []
    def __init__(self,argvs,argc,proj,C):
        self.jack = []
        # proj = PPAR_5Z , PPAR
        CONF = C
        conf = []
        conf_ama = []
        fold = []
        for i in argvs:
#            print(i)
            baryons = []
            baryons_ama = []
            tmp = i
            src = []
            for j in ['x','y','z','t']:
                src.append(tmp.split(j)[0])
                tmp = tmp.split(j)[1]
            src = src[1:]
            with open(i,"r") as file:
                num = 0
                for line in file:
                    line = line.rstrip()
                    if(re.split(" +",line)[0] == 'START_NUC3PT'):
                        a = copy.deepcopy(baryon_3pt.read_baryon_3pt(file,num,i.split("/")[2],src))
                        if(a.proj == proj):
                            baryons.append(a)
            with open(i.replace("dat","dat_ama"),"r") as file:
                num = 0
                for line in file:
                    line = line.rstrip()
                    if(re.split(" +",line)[0] == 'START_NUC3PT'):
                        a = copy.deepcopy(baryon_3pt.read_baryon_3pt(file,num,i.split("/")[2],src))
                        if(a.proj == proj):
                            baryons_ama.append(a)
            conf.append(baryons)
            conf_ama.append(baryons_ama)

        for i in range(len(conf[0])):
            self.jack.append([conf[j][i] - conf_ama[j][i] for j in range(len(conf))])

class read_3pt_ama:
    jack = []
    def __init__(self,argvs,argc,proj,C):
        self.jack = []
        CONF = C
        conf = []
        fold = []
        for i in argvs:
            baryons = []
            tmp = i
            src = []
            for j in ['x','y','z','t']:
                src.append(tmp.split(j)[0])
                tmp = tmp.split(j)[1]
            src = src[1:]
            with open(i,"r") as file:
                num = 0
                for line in file:
                    line = line.rstrip()
                    if(re.split(" +",line)[0] == 'START_NUC3PT'):
                        a = copy.deepcopy(baryon_3pt.read_baryon_3pt(file,num,i.split("/")[2],src))
                        if(a.proj == proj):
                            baryons.append(a)

            conf.append(baryons)
        

        GT = copy.deepcopy(conf[0])
        for i in conf[1:]:
            for j in range(len(i)):
                GT[j] = GT[j] + i[j]

        self.jack = list(map(lambda x : x / len(conf),GT))
