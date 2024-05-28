# Import libraries such as numpy,scipy and matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Declaring the values for speed and temperature(estimated in the first part)
speed,temp = 299792458, 4994.763989764206

# File opening to extract the datapoints from dataset3.txt and then added to two different lists
f=open("dataset3.txt",'r')
X=[]
Y=[]
for i in f:
    k=i.split( )
    X.append(float(k[0]))
    Y.append(float(k[1]))
f.close()

# A typical model of the function with output as Y, unknown parameters as planks and boltzmanns constant
def h_and_k_est(x,h,k):
    u = (2*h*(x**3))
    v = (np.exp((h*x)/(k*temp))-1)*(speed**2)
    return u/v

# Starting and ending points where the curve fit converges and would give better estimates
s,e = 2219, 2994

# Giving an initial guess for h and k
initial_guess = [6.626e-34,1.38e-23]
var,_ = curve_fit(h_and_k_est,X[s:e],Y[s:e],p0=initial_guess)

print("Planck's constant: "+str(var[0]))
print("Boltzmann's constant: "+str(var[1]))

# New set of Y coordinates are created by putting the estimated values
est_Y2 = []
for i in range(len(X)):
    u = (2*var[0]*(X[i]**3))
    v = (np.exp((var[0]*X[i])/(var[1]*temp))-1)*(speed**2)
    est_Y2.append(u/v)
    
# New set of Y coordinates are created by putting the estimated values in first part
# It is just used to plot the both curves at a time
est_Y1 = []
for i in range(len(X)):
    u = (2*6.62607015e-34*(X[i]**3))
    v = (np.exp((6.62607015e-34*X[i])/(1.380649e-23*temp))-1)*(speed**2)
    est_Y1.append(u/v)
    
# Plotting
plt.plot(X,Y,label = "Original",color="#00BFFF")
plt.plot(X,est_Y1,label = "Part1 Estimation", color = '#FFD700')
plt.plot(X,est_Y2,label = "Part2 Estimation", color = '#FF1493')
plt.legend()
plt.savefig('dataset3.png')