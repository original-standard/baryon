import sys
import glob
import read
import read_3pt_V
import numpy as np
import utils
import gc
from multiprocessing import Pool
from memory_profiler import profile



argvs = sys.argv
org = "../srcX*/*/nuc3pt.dat.*x0y0z0t0"
org2 = "../srcX*/*/nuc3pt.dat.*x64y64z64t64"
org3 = "../srcX*/*/nuc3pt.dat.*x16y48z16t16"
org4 = "../srcX*/*/nuc3pt.dat.*x48y80z80t80"
ama = "../srcX*/*/nuc3pt.dat*ama*.x[0-9]*"

#n2pt = read.read_2pt(sorted(glob.glob(dir2pt)),len(glob.glob(dir2pt)),20)
#n3pt = read_3pt_V.read_3pt(sorted(glob.glob(dir2pt)),len(glob.glob(dir2pt)),"PPAR",20)
#n3ptZ = read_3pt_V.read_3pt(sorted(glob.glob(dir2pt)),len(glob.glob(dir2pt)),"PPAR_5Z",20)

nuc_2pt_ama = []

def memory_leak(i):
     nuc_2pt = []
     nuc_2pt_2 = []
     nuc_2pt_3 = []
     nuc_2pt_4 = []
     oper = nuc_2pt_ama[0][i].oper
     if(oper == "default"):
         return
     mom = nuc_2pt_ama[0][i].mom
     momorg = mom
     mom = str(25 * (int(mom[0]) + 2) + 5 * (int(mom[1]) + 2) + int(mom[2]) + 2)
     sink = nuc_2pt_ama[0][i].sink
     sinkorg = sink
     source = nuc_2pt_ama[0][i].source[0]
     if(sink == [1,0]):
         sink = "POINT"
     print(oper + "_" + source + "to" + sink + "_" + mom)
     ama = [np.array(nuc_2pt_ama[j][i].correlator_complex) for j in range(len(nuc_2pt_ama))]

     t = read.read_2pt_rest(sorted(glob.glob(org)),len(glob.glob(org)),20)
     for k in t.jack:
         if(k[0].oper == oper):
             if(k[0].mom == momorg):
                 if(k[0].sink == sinkorg):
                     nuc_2pt = [np.array((l.set_zero()).correlator_complex) for l in k]

     del t

     t = read.read_2pt_rest(sorted(glob.glob(org2)),len(glob.glob(org2)),20)
     for k in t.jack:
         if(k[0].oper == oper):
             if(k[0].mom == momorg):
                 if(k[0].sink == sinkorg):
                     nuc_2pt_2 = [np.array((l.set_zero()).correlator_complex) for l in k]

     del t


     nuc_2pt = [(nuc_2pt[i] + nuc_2pt_2[i]) /2. for i in range(len(nuc_2pt))]

     nuc_2pt = utils.jackknife([nuc_2pt[i] + ama[i] for i in range(len(nuc_2pt))])
     for i in range(len(nuc_2pt)):
         for j in nuc_2pt[i]:
            print(j.real,j.imag)
     del nuc_2pt
     del ama
     gc.collect()

def nuc2pt(i):
    str = "../srcX*/" + i.split("/")[2] +"/*dat_ama*"
    tmp = read.read_2pt_ama(sorted(glob.glob(str)),len(glob.glob(ama)),20).jack
    return tmp


def nuc3pt_PPAR(i):
     tmp = read_3pt_V.read_3pt_ama(sorted(glob.glob("../srcX*/" + i.split("/")[2] +"/*dat_ama*")),len(glob.glob(ama)),"PPAR",20).jack
     return tmp

def nuc3pt_PPAR5Z(i):
     tmp = read_3pt_V.read_3pt_ama(sorted(glob.glob("../srcX*/" + i.split("/")[2] +"/*dat_ama*")),len(glob.glob(ama)),"PPAR_5Z",20).jack
     return tmp



with Pool(5) as p:
     nuc_2pt_ama = p.map(nuc2pt,sorted(glob.glob(org)))


for i in range(len(nuc_2pt_ama[0])):
    memory_leak(i)
