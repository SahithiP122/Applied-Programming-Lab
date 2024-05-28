# Importing the required libraries, it is used to estimate the unknown parameters in linear model
import numpy as np

# Collecting the data from the csv file into different lists
# These lists contain the fraction of values for each parameter relative to their maximum values
serial,gre_score,toefl_score = [],[],[]
rating,sop,lor,cgpa,research,chance = [],[],[],[],[],[]
f = open('Admission_Predict_Ver1.1.csv','r')
for a in f:
    j = a.split(',')
    if j[0]!='Serial No.':
        j[8] = j[8].split('\n')[0]
        serial.append(int(j[0])), gre_score.append(int(j[1])/360)
        toefl_score.append(int(j[2])/120), rating.append(int(j[3])/5)
        sop.append(float(j[4])/5), lor.append(float(j[5])/5), cgpa.append(float(j[6])/10)
        research.append(int(j[7])), chance.append(float(j[8]))
f.close()

# Setting up the matrix equation Mx = b
# The elements in the column matrix 'b' represents chance to admit
# Considering only the data points with research == 1
# 'M' is a matrix with 7 columns; 1st column with gre_score, 2nd with toefl_score.....
# Considering only the data points with research == 1
M,b = [],[]
for i in range(len(serial)):
    if research[i]==1:
        M.append([gre_score[i],toefl_score[i],rating[i],sop[i],lor[i],cgpa[i],1])
        b.append(chance[i])
        
# Finding the coefficients using linalg.lstsq()
p,_,_,_ = np.linalg.lstsq(M,b,rcond=None)

# Using the estimated values, estimating chance to admit, these values are stored in 'predicted[]'
predicted = []
for i in range(len(serial)):
    s = p[0]*gre_score[i] + p[1]*toefl_score[i] + p[2]*rating[i] + p[3]*sop[i] + p[4]*lor[i] + p[5]*cgpa[i]  + p[6]
    predicted.append(s)

print("Estimated Equation for chance of admit:")
print(f"--> {round(p[0],3)}*(gre score/360) + {round(p[1],3)}*(toefl score/120) + {round(p[2],3)}*(rating/5) + {round(p[3],3)}*(sop/5) + {round(p[4],3)}*(lor/5) + {round(p[5],3)}*(cgpa/10) - {round(abs(p[6]),3)}")

# Calculating Square root of Mean Square Error and Average error
sqerror, mnerror = 0,0
for i in range(len(serial)):
    v = (chance[i]-predicted[i])**2
    sqerror += v
    mnerror += v**0.5
print("Square root of mean square error is "+ str(round((sqerror/len(serial))**0.5,5)))
print("Average absolute error is "+str(round(mnerror/len(serial),5)))

# Finding the average ratio of estimated chance to given chance of admit
y = 0
for i in range(len(chance)):
    y+=(chance[i]/predicted[i])
print("Average ratio of estimated chance of admit to given chance of admit is "+str(round(y/len(chance),5)))