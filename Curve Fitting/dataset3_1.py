# Import libraries such as numpy,scipy and matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# File opening to extract the datapoints from dataset3.txt and then added to two different lists
f=open("dataset3.txt",'r')
X=[]
Y=[]
for i in f:
    k=i.split( )
    X.append(float(k[0]))
    Y.append(float(k[1]))
f.close()

# Declaring the values for speed of light, plancks constant and boltzmanns constant
h,k,c = 6.62607015e-34, 1.380649e-23, 299792458

# Creating a new set of coordinates having the output as 1/Temperature
val = []
for i in range(len(X)):
    v = (2*h*(X[i]**3))/((c**2)*abs(Y[i]))+1
    val.append((k*np.log(v))/(h*X[i]))
    
# Function which returns inverse of temperature, is used in curve fit
def temperature(x,t):
    return 1/t

# Starting and ending points where the curve fit converges and would give better estimates
# temp is the estimated temperature by curve fit
s,e = 2000,2800
temp,_ = curve_fit(temperature,X[s:e],val[s:e])
print("Estimated Temperature: "+str(round(temp[0],3))+"K")