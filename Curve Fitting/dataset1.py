# Import libraries such as numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt

# File opening to extract the datapoints from dataset1.txt and then added to two different lists
f=open("dataset1.txt",'r')
X=[]
Y=[]
for i in f:
    k=i.split( )
    X.append(float(k[0]))
    Y.append(float(k[1]))
f.close()

# Constructing the matrix M, whose first column is filled with x coordinates and second with ones
matX=np.column_stack([X,np.ones(len(X))])    
matY=np.column_stack([Y])

# 'var' contains the estimated values of slope and intercept 
var = np.linalg.lstsq(matX,matY,rcond=None)
M,C = var[0][0][0],var[0][1][0]

print("Slope of the line is "+str(round(M,3)))
print("Intercept of the line is "+str(round(C,3)))

# New set of Y coordinates were obtained by putting the estimaed M and C
y=[]
for i in X:
    y.append(M*i+C)
    
# Plotting
plt.plot(X,Y,label="Original",color="#00BFFF")
plt.plot(X,y,label="Estimated",color="red")
plt.errorbar(X[::25],Y[::25],fmt="o-k",ms=3.8,label="Errorbar")
plt.legend()
plt.savefig('dataset1.png')