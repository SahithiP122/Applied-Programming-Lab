# Import libraries such as numpy,scipy and matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import splrep,splev

# File opening to extract the datapoints from dataset2.txt and then added to two different lists
f = open('dataset2.txt','r')
X=[]
Y=[]
for i in f:
    k=i.split( )
    X.append(float(k[0]))
    Y.append(float(k[1]))
f.close()

# Dividing the whole set of datapoints into 150 data points of equal gap using linspace
spline = splrep(X,Y)
disx = np.linspace(X[0],X[len(X)-1],150)
disy = splev(disx,spline)

# Finding the index of the x coordinate where the value of disx becomes zero
p0 = 0
for i in range(len(disx)):
    if abs(disx[i])<0.05:
        p0 += i
        break

# Calculation of index x coordinates of two points whose y coordinates are around zero
# One of the coordinate is leftmost to the positive x axis, another is the righmost to the negative x axis
l = []
for i in range(len(disy)):
    if i>p0:
        if disy[i]<0:
            l.append(i)
            break
for i in range(len(disy)):
    if i<p0:
        if disy[p0-i]>0:
            l.append(p0-i)
            break

# Interpolation of x coordinate so that y coordinate would become zero, this can be done by taking 
# the two nearest points to the x axis
rp = disx[l[0]] - disy[l[0]]/((disy[l[0]+1]-disy[l[0]])/(disx[l[0]+1]-disx[l[0]]))
lp = disx[l[1]] - disy[l[1]]/((disy[l[1]+1]-disy[l[1]])/(disx[l[1]+1]-disx[l[1]]))

# Difference of rp and lp is nothing but the period of the signal
per = rp-lp
print("Periodicity is "+str(round(per,3)))
Xn = np.array(X)
Yn = np.array(Y)

# Using least squares, we were trying to estimate the amplitudes of the individual sine waves
# Matrix M is constructed with 3 columns in it. 
# First column wiith sin(2*np.pi*Xn/per), second with sin(6*np.pi*Xn/per), third with sin(10*np.pi*Xn/per)
M = np.column_stack([np.sin(2*np.pi*Xn/per),np.sin(6*np.pi*Xn/per),np.sin(10*np.pi*Xn/per)])
(amp1,amp2,amp3),_,_,_ = np.linalg.lstsq(M,Y,rcond=None)
print("Amplitudes using least squares are "+str(round(amp1,3))+", "+str(round(amp2,3))+", "+str(round(amp3,3)))

# New list of Y coordinates were obtained by putting the estimated values obtained from least squares 
ls = []
for i in X:
    ls.append(amp1*np.sin(2*np.pi*i/per) + amp2*np.sin(6*np.pi*i/per) + amp3*np.sin(10*np.pi*i/per))

# Typical model of function whose output is same as that of signal
def sup_of_signals(X,c1,c2,c3,perc):
    return (c1*np.sin(2*np.pi*X/perc)+c2*np.sin(6*np.pi*X/perc)+c3*np.sin(10*np.pi*X/perc))

# Starting and ending points where the curve fit converges and would give better estimates
s,e = 370,649

# c1,c2,c3 will give the amplitudes, perc will give the least frequency
(c1,c2,c3,perc),_ = curve_fit(sup_of_signals,X[s:e],Y[s:e])
print("Periodicity using curve fit is "+str(round((2*np.pi)/perc,3)))
print("Amplitudes using curve fit are "+str(round(c1,3))+", "+str(round(c2,3))+", "+str(round(c3,3)))

# New list of Y coordinates were obtained by putting the estimated values obtained curve fit
cf = []
for i in X:
    cf.append(c1*np.sin(2*np.pi*i/perc) + c2*np.sin(6*np.pi*i/perc) + c3*np.sin(10*np.pi*i/perc))

# Plotting
plt.plot(X,Y,color="#00BFFF",label="Original")
plt.plot(X,ls,label="Least squares",color="red")
plt.plot(X,cf,color="k",label="Curve Fit")
plt.legend()
plt.savefig('dataset2.png')