import sys
import glob
import read
import read_3pt_V
import numpy as np
import utils
from multiprocessing import Pool
import gc


argvs = sys.argv
org = "../srcX*/*/nuc3pt.dat.*x0y0z0t0"
org2 = "../srcX*/*/nuc3pt.dat.*x64y64z64t64"
ama = "../srcX*/*/nuc3pt.dat*ama*.x[0-9]*"
sink = 10
#n2pt = read.read_2pt(sorted(glob.glob(dir2pt)),len(glob.glob(dir2pt)),20)
#n3pt = read_3pt_V.read_3pt(sorted(glob.glob(dir2pt)),len(glob.glob(dir2pt)),"PPAR",20)
#n3ptZ = read_3pt_V.read_3pt(sorted(glob.glob(dir2pt)),len(glob.glob(dir2pt)),"PPAR_5Z",20)
nuc_2pt = []
nuc_2pt_2 = []
nuc_2pt_3 = []
nuc_2pt_4 = []
nuc_2pt_ama = []

def nuc3pt_PPAR(i):
     tmp = read_3pt_V.read_3pt_ama(sorted(glob.glob("../srcX*/" + i.split("/")[2] +"/*dat_ama*")),len(glob.glob(ama)),"PPAR",20).jack
     return tmp

def nuc3pt_PPAR5Z(i):
     tmp = read_3pt_V.read_3pt_ama(sorted(glob.glob("../srcX*/" + i.split("/")[2] +"/*dat_ama*")),len(glob.glob(ama)),"PPAR_5Z",20).jack
     return tmp







n3pt_rest = read_3pt_V.read_3pt_rest(sorted(glob.glob(org)),len(glob.glob(org)),"PPAR_5Z",20).jack
#n3pt_rest_2 = read_3pt_V.read_3pt_rest(sorted(glob.glob(org2)),len(glob.glob(org2)),"PPAR_5Z",20).jack
#n3pt_rest_3 = read_3pt_V.read_3pt_rest(sorted(glob.glob(org3)),len(glob.glob(org3)),"PPAR_5Z",20).jack
#n3pt_rest_4 = read_3pt_V.read_3pt_rest(sorted(glob.glob(org4)),len(glob.glob(org4)),"PPAR_5Z",20).jack

#n3pt_rest_2
#n3pt_rest = [[(n3pt_rest[i][j] + n3pt_rest_2[i][j] + n3pt_rest_3[i][j] + n3pt_rest_4[i][j]) / 4. for j in range(len(n3pt_rest[0]))] for i in range(len(n3pt_rest))]
#n3pt_rest = [[(n3pt_rest[i][j] + (n3pt_rest_2[i][j].set_zero())) / 2. for j in range(len(n3pt_rest[0]))] for i in range(len(n3pt_rest))]

with Pool(5) as p:
     n3pt_ama = p.map(nuc3pt_PPAR5Z,sorted(glob.glob(org)))

for i in range(len(n3pt_rest)):
    j = n3pt_rest[i]

    mom = j[0].opmom
    mom = str(25 * (int(mom[0]) + 2) + 5 * (int(mom[1]) + 2) + int(mom[2]) + 2)
    print(j[0].oper + "_" + mom)
    t_d = []
    t_u = []
    isovec = []
    t_ama_u = []
    t_ama_d = []
    for l in j:
         t_d.append(np.array(l.correlator_complex_d[:sink]))
         t_u.append(np.array(l.correlator_complex_u[:sink]))

    for k in range(len(n3pt_ama)):
         t_ama_d.append(np.array(n3pt_ama[k][i].correlator_complex_d[:sink]))
         t_ama_u.append(np.array(n3pt_ama[k][i].correlator_complex_u[:sink]))

    isovec = utils.jackknife([t_u[i] + t_ama_u[i] - t_d[i] - t_ama_d[i] for i in range(len(t_u))])

    for i in range(len(isovec)):
         for j in range(len(isovec[i])):
              tmp = isovec[i][j] 
                    
              print(tmp.real,tmp.imag)
    del j
    del t_d
    del t_u
    del isovec
    del t_ama_u
    del t_ama_d
    gc.collect()
n3pt_rest = read_3pt_V.read_3pt_rest(sorted(glob.glob(org)),len(glob.glob(org)),"PPAR",20).jack
n3pt_rest_2 = read_3pt_V.read_3pt_rest(sorted(glob.glob(org2)),len(glob.glob(org2)),"PPAR",20).jack
#n3pt_rest_3 = read_3pt_V.read_3pt_rest(sorted(glob.glob(org3)),len(glob.glob(org3)),"PPAR",20).jack
#n3pt_rest_4 = read_3pt_V.read_3pt_rest(sorted(glob.glob(org4)),len(glob.glob(org4)),"PPAR",20).jack

#n3pt_rest_2.set_zero()
#n3pt_rest = [[(n3pt_rest[i][j] + n3pt_rest_2[i][j] + n3pt_rest_3[i][j] + n3pt_rest_4[i][j]) / 4. for j in range(len(n3pt_rest[0]))] for i in range(len(n3pt_rest))]
n3pt_rest = [[(n3pt_rest[i][j] + (n3pt_rest_2[i][j].set_zero())) / 2. for j in range(len(n3pt_rest[0]))] for i in range(len(n3pt_rest))]

with Pool(5) as p:
     n3pt_ama = p.map(nuc3pt_PPAR,sorted(glob.glob(org)))


for i in range(len(n3pt_rest)):
     j = n3pt_rest[i]
#     k = n3pt_ama[i]
     mom = j[0].opmom
     mom = str(25 * (int(mom[0]) + 2) + 5 * (int(mom[1]) + 2) + int(mom[2]) + 2)
     print(j[0].oper + "_" + mom)
     t_d = []
     t_u = []
     isovec = []
     t_ama_u = []
     t_ama_d = []
     for l in j:
          t_d.append(np.array(l.correlator_complex_d[:sink]))
          t_u.append(np.array(l.correlator_complex_u[:sink]))

     for k in range(len(n3pt_ama)):
          t_ama_d.append(np.array(n3pt_ama[k][i].correlator_complex_d[:sink]))
          t_ama_u.append(np.array(n3pt_ama[k][i].correlator_complex_u[:sink]))

     isovec = utils.jackknife([t_u[i] + t_ama_u[i] - t_d[i] - t_ama_d[i] for i in range(len(t_u))])

     for i in range(len(isovec)):
          for j in range(len(isovec[i])):
               tmp = isovec[i][j] 
                    
               print(tmp.real,tmp.imag)
     del j
     del t_d
     del t_u
     del isovec
     del t_ama_u
     del t_ama_d
     gc.collect()
