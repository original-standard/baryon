import os
from numpy import sqrt
import numpy as np
import sys

CONF = 20
TN = 128

mom = int(sys.argv[1])
ts = 10

MASS = [0.4041,0.4073,0.4105,0.4137,0.4159,0.4192,0.4222,0.0,0.4278]



def mom_assign(a,b,c):
    return (a + 2) * 25 + (b + 2) * 5 + c + 2

def read(F):
    conf = [float(i.split(" ")[0]) for i in open(F,"r")]
    return [[conf[TN * i + j] for j in range(TN) ]for i in range(CONF)]

def read_3p(F):
    conf = [float(i.split(" ")[0]) for i in open(F,"r")]
    return [[conf[ts * i + j] for j in range(ts) ]for i in range(CONF)]

result = [[0. for i in range(CONF)] for i in range(ts)]
nofd = 0
for i in range(-2,3):
    for j in range(-2,3):
        for k in range(-2,3):
            if(i * i + j * j + k * k != mom):
                continue
            # main
            m = mom_assign(i,j,k)
            mz = mom_assign(0,0,0)
            ss_m = read("split_2pt/NUC_G5C_PP_EXPtoEXP_" + str(m))
            ss_mz = read("split_2pt/NUC_G5C_PP_EXPtoEXP_" + str(mz))
            sl_m = read("split_2pt/NUC_G5C_PP_EXPtoPOINT_" + str(m))
            sl_mz = read("split_2pt/NUC_G5C_PP_EXPtoPOINT_" + str(mz))
            f = [[sqrt(sl_m[j][ts - i] / sl_mz[j][ts - i] * ss_mz[j][i] / ss_m[j][i] * sl_mz[j][ts] / sl_m[j][ts])  for j in range(CONF) ] for i in range(ts)]
            op = read_3p("split_3pt/G4_" + str(m))
            fact = 1./sqrt((MASS[mom] + MASS[0])/ 2. / MASS[mom]) *  0.126117 * 2. * 0.95153
            f = [[f[i][j] * op[j][i] * fact / ss_mz[j][ts] for j in range(CONF)] for i in range(ts)]
       #     f = [[op[j][i] / ss_m[j][ts] for j in range(CONF)] for i in range(ts)]
            tmp = result
            result = [[tmp[i][j] + f[i][j] for j in range(CONF)] for i in range(ts)]
            nofd += 1
result = [[result[i][j] / nofd for j in range(CONF)] for i in range(ts)]

for i in result:
    print(np.average(i), sqrt(np.var(i) * (CONF - 1.)) )


