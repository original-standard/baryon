import re
import copy
import sys
import math

class baryon_prop(object):
        def __init__(self):
                self.masses = []
                self.source = []
                self.sink = []
                self.sinks = "default"
                self.mom = []
                self.oper = "default"
                self.state = "default"
                self.correlator = []
                self.correlator_img = []
                self.correlator_complex = []
        def __add__(self,obj):
                if(self.masses != obj.masses):
                        sys.stderr.write("ALERT!! (MASS)\n")
                if(self.source[0] != obj.source[0] or self.source[1] != obj.source[1]):
                        sys.stderr.write("ALERT!! (SOURCE)\n")
                if(self.sink != obj.sink):
                        sys.stderr.write("ALERT!! (SINK)\n")
                if(self.mom != obj.mom):
                        sys.stderr.write("ALERT!! (MOM)\n")
                if(self.oper != obj.oper):
                        sys.stderr.write("ALERT!! (OPER)\n")
                
                result = copy.deepcopy(self)
                
                shift = - int(self.source[-1]) + int(obj.source[-1])
                if(shift < 0):
                        shift = shift + len(result.correlator)


                cor = []
                cor_img = []
                cor_complex = []
                
                for i in obj.correlator[shift:]:
                        cor.append(i)
                for i in obj.correlator[0:shift]:
                        cor.append(i)

                for i in obj.correlator_img[shift:]:
                        cor_img.append(i)
                for i in obj.correlator_img[0:shift]:
                        cor_img.append(i)

                for i in obj.correlator_complex[shift:]:
                        cor_complex.append(i)
                for i in obj.correlator_complex[0:shift]:
                        cor_complex.append(i)
                for i in range(len(result.correlator_complex)):
                        result.correlator_complex[i] = result.correlator_complex[i] + cor_complex[i]

                for i in range(len(result.correlator)):
                        result.correlator[i] = result.correlator[i] + cor[i]

                for i in range(len(result.correlator_img)):
                        result.correlator_img[i] = result.correlator_img[i] + cor_img[i]
                return result
                
        def __truediv__(self,obj):
                result = copy.deepcopy(self)

                for i in range(len(result.correlator)):
                        result.correlator[i] = result.correlator[i] / obj

                for i in range(len(result.correlator_img)):
                        result.correlator_img[i] = result.correlator_img[i] / obj

                for i in range(len(result.correlator_complex)):
                        result.correlator_complex[i] = result.correlator_complex[i] / obj
                return result
        def __div__(self,obj):
                result = copy.deepcopy(self)

                for i in range(len(result.correlator)):
                        result.correlator[i] = result.correlator[i] / obj

                for i in range(len(result.correlator_img)):
                        result.correlator_img[i] = result.correlator_img[i] / obj

                for i in range(len(result.correlator_complex)):
                        result.correlator_complex[i] = result.correlator_complex[i] / obj
                return result

        def __mul__(self,obj):
                result = copy.deepcopy(self)

                for i in range(len(result.correlator)):
                        result.correlator[i] = result.correlator[i] * obj
                for i in range(len(result.correlator_img)):
                        result.correlator_img[i] = result.correlator_img[i] * obj
                for i in range(len(result.correlator_complex)):
                        result.correlator_complex[i] = result.correlator_complex[i] * obj
                return result

        def __sub__(self,obj):
                result = copy.deepcopy(self)
                sub = copy.deepcopy(obj)
                sub = sub * (-1.)
                result = result + sub
                return result
        def timereversal(self):
                shift = int(self.source[-1])
                real = [self.correlator[shift]]
                for i in reversed(self.correlator[:shift]):
                        real.append(i)
                for i in reversed(self.correlator[shift + 1:]):
                        real.append(i)
                img = [self.correlator_img[shift]]
                for i in reversed(self.correlator_img[:shift]):
                        img.append(i)
                for i in reversed(self.correlator_img[shift + 1:]):
                        img.append(i)
                self.correlator = real
                self.correlator_img = img
                self.source[3] = "0"
        def abs(self):
                for i in range(len(self.correlator)):
                        self.correlator[i] = math.sqrt(self.correlator[i] * self.correlator[i] + self.correlator_img[i] * self.correlator_img[i])
                
        def set_zero(self):
                shift = - int(self.source[-1])
                shift = shift + len(self.correlator_complex)
                self.source[-1] = "0"

                cor_complex = []


                for i in self.correlator_complex[shift:]:
                        cor_complex.append(i)
                for i in self.correlator_complex[0:shift]:
                        cor_complex.append(i)
                for i in range(len(self.correlator_complex)):
                        self.correlator_complex[i] = cor_complex[i]

                
                return self


def sym(obj):
        baryon_propobj = copy.deepcopy(obj)
        baryon_propobj.timereversal()
        return (obj + baryon_propobj) /2.

def read_baryon_prop(file,N,l,s):
        num = 0
        temp = baryon_prop()
        temp2 = baryon_prop()
        ml = l
        ms = s
        for line in file:
                line = line.rstrip()
                if(line == "ENDPROP"):
                        return temp
                        #temp2.timereversal()
                        #return (temp + temp2) / 2.
                        #return temp2
                if(1 == 1):
                        words = re.split(" +",line)
                        if(words[0] == "MASSES:"):
                                temp.masses = words[1:]
                                temp2.masses = words[1:]
                                mass = 0.
                                for i in words[1:]:
                                        mass = mass + float(i)

                                if(mass == l * 3.):
                                        temp.state = "NUCLEON"
                                        temp2.state = "NUCLEON"

                        elif(words[0] == "SOURCE:"):
                                temp.source = words[1:]
                                if(len(temp.source) < 2):
                                        temp.source = ['EXP','0','0','0','0']
                                temp2.source = words[1:]
                        elif(words[0] == "SINKS:"):
                                temp.sinks = words[1]
                                temp2.sinks = words[1]
                        elif(words[0] == "SINK:"):
                                if(words[1] == "POINT"):
                                        temp.sink = [1,0]
                                        temp2.sink = [1,0]
                                else:
                                        temp.sink = words[1]
                                        temp2.sink = words[1]
                        elif(words[0] == "MOM:"):
                                temp.mom = words[1:]
                                temp2.mom = words[1:]
                        elif(words[0] == "OPER:"):
                                temp.oper = words[1]
                                temp2.oper = words[2]
                        else:
                                temp.correlator.insert(int(words[0]),float(words[1]))
                                temp.correlator_img.insert(int(words[0]),float(words[2]))
                                temp.correlator_complex.insert(int(words[0]),complex(float(words[1]),float(words[2])))

                                if(temp.sinks == "default"):
                                        temp2.correlator.insert(int(words[0]),float(words[3]))
                                        temp2.correlator_img.insert(int(words[0]),float(words[4]))
                                        temp2.correlator_complex.insert(int(words[0]),complex(float(words[3]),float(words[4])))
                num = num + 1
        N = N + num
