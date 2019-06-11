import re
import copy
import sys
import math

class baryon_3pt(object):
        def __init__(self):
                self.conf = "default"
                self.quark = "default"
                self.source = []
                self.sink = []
                self.sinkmom = []
                self.opmom = []
                self.fact = "default"
                self.proj = "default"
                self.matrix = "default"
                self.masses = []
                self.type = "default"
                self.oper = "default"
                self.correlator_complex_u = []
                self.correlator_complex_d = []
        def __add__(self,obj):
                if(self.source[0] != obj.source[0] or self.source[1] != obj.source[1]):
                        sys.stderr.write("ALERT!! (SOURCE)\n")
                if(self.sink != obj.sink):
                        sys.stderr.write("ALERT!! (SINK)\n")
                if(self.conf != obj.conf):
                        sys.stderr.write("ALERT!! (CONF)\n") # fatal
                if(self.sinkmom != obj.sinkmom):
                        sys.stderr.write("ALERT!! (MOM)\n")
                if(self.oper != obj.oper):
                        sys.stderr.write("ALERT!! (OPER)\n")
                if(self.matrix != obj.matrix):
                        print("ALERT!! (MATRIX)") # fatal
                
                result = copy.deepcopy(self)
                
                shift = - int(self.source[-1]) + int(obj.source[-1])
                if(shift < 0):
                        shift = shift + len(result.correlator_complex_d)



                cor_complex_d = []
                cor_complex_u = []


                for i in obj.correlator_complex_d[shift:]:
                        cor_complex_d.append(i)
                for i in obj.correlator_complex_d[0:shift]:
                        cor_complex_d.append(i)
                for i in range(len(result.correlator_complex_d)):
                        result.correlator_complex_d[i] = result.correlator_complex_d[i] + cor_complex_d[i]

                for i in obj.correlator_complex_u[shift:]:
                        cor_complex_u.append(i)
                for i in obj.correlator_complex_u[0:shift]:
                        cor_complex_u.append(i)
                for i in range(len(result.correlator_complex_u)):
                        result.correlator_complex_u[i] = result.correlator_complex_u[i] + cor_complex_u[i]


                return result
                
        def __truediv__(self,obj):
                result = copy.deepcopy(self)

                for i in range(len(result.correlator_complex_u)):
                        result.correlator_complex_u[i] = result.correlator_complex_u[i] / obj

                for i in range(len(result.correlator_complex_d)):
                        result.correlator_complex_d[i] = result.correlator_complex_d[i] / obj
                return result
        def __div__(self,obj):
                result = copy.deepcopy(self)

                for i in range(len(result.correlator_complex_u)):
                        result.correlator_complex_u[i] = result.correlator_complex_u[i] / obj

                for i in range(len(result.correlator_complex_d)):
                        result.correlator_complex_d[i] = result.correlator_complex_d[i] / obj
                return result

        def __mul__(self,obj):
                result = copy.deepcopy(self)


                for i in range(len(result.correlator_complex_u)):
                        result.correlator_complex_u[i] = result.correlator_complex_u[i] * obj

                for i in range(len(result.correlator_complex_d)):
                        result.correlator_complex_d[i] = result.correlator_complex_d[i] * obj

                return result

        def __sub__(self,obj):
                result = copy.deepcopy(self)
                sub = copy.deepcopy(obj)
                sub = sub * (-1.)
                result = result + sub
                return result
        def set_zero(self):
                shift = - int(self.source[-1])
                shift = shift + len(self.correlator_complex_d)
                self.source[-1] = "0"

                cor_complex_d = []
                cor_complex_u = []


                for i in self.correlator_complex_d[shift:]:
                        cor_complex_d.append(i)
                for i in self.correlator_complex_d[0:shift]:
                        cor_complex_d.append(i)
                for i in range(len(self.correlator_complex_d)):
                        self.correlator_complex_d[i] = cor_complex_d[i]

                
                for i in self.correlator_complex_u[shift:]:
                        cor_complex_u.append(i)
                for i in self.correlator_complex_u[0:shift]:
                        cor_complex_u.append(i)
                for i in range(len(self.correlator_complex_u)):
                        self.correlator_complex_u[i] = cor_complex_u[i]
                return self

def read_baryon_3pt(file,N,conf):
        num = 0
        temp = baryon_3pt()
        temp2 = baryon_3pt()
        for line in file:
                line = line.rstrip()
                if(line == "END_NUC3PT"):
                        isovector = temp
                        isovector.correlator_complex_u = temp.correlator_complex_u
                        isovector.correlator_complex_d = temp2.correlator_complex_d
                        isovector.conf = conf
                        return isovector
                if(1 == 1):
                        words = re.split(" +",line)
                        if(words[0] == "SOURCE:"):
                                temp.source = words[1:]
                                temp2.source = words[1:]
                        elif(words[0] == "SINK:"):
                                if(words[1] == "POINT"):
                                        temp.sink = [1,0]
                                        temp2.sink = [1,0]
                                else:
                                        temp.sink = words[1:]
                                        temp2.sink = words[1:]
                        elif(words[0] == "SNK_MOM:"):
                                temp.sinkmom = words[1:]
                                temp2.sinkmom = words[1:]
                        elif(words[0] == "OPER:"):
                                temp.oper = words[1]
                                temp2.oper = words[1]
                        elif(words[0] == "OP_MOM:"):
                                temp.opmom = words[1:]
                                temp2.opmom = words[1:]
                        elif(words[0] == "FACT:"):
                                temp.fact = words[1]
                                temp2.fact = words[1]
                        elif(words[0] == "PROJ:"):
                                temp.proj = words[1]
                                temp2.proj = words[1]
                        elif(words[0] == "MTRX:"):
                                temp.matrix = words[1]
                                temp2.matrix = words[1]
                        elif(words[0] == "MASSES:"):
                                temp.masses = words[1:]
                                temp2.masses = words[1:]
                        elif(words[0] == "TYPE:"):
                                temp.type = words[1]
                        elif(words[0] == "QUARKS:"):
                                temp.quark = words[1]
                                temp2.quark = words[2]
                        else:

                                temp.correlator_complex_u.insert(int(words[0]),complex(float(words[1]),float(words[2])))
                                temp2.correlator_complex_d.insert(int(words[0]),complex(float(words[3]),float(words[4])))
                num = num + 1
        N = N + num
