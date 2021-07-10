#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_squared_error 
from sklearn.metrics import r2_score


def import_Excel_unknowns(file_name):
    myLiquids = pd.read_excel(file_name, usecols = "B:M", skiprows=1)
    myLiquids = myLiquids.fillna(0)
    
    myCPXs = pd.read_excel(file_name, usecols = "O:X", skiprows=1)
    myCPXs = myCPXs.fillna(0)
    myCPXs.columns = [c.replace('.1', '') for c in myCPXs.columns]
    
    myLabels = pd.read_excel(file_name, usecols = "A", skiprows=1)
    
    return myLiquids, myCPXs, myLabels
    
def import_Excel_experiments(file_name):
    
    myLiquids = pd.read_excel(file_name, usecols = "B:M", skiprows=1)
    myLiquids = myLiquids.fillna(0)
    
    myCPXs = pd.read_excel(file_name, usecols = "O:X", skiprows=1)
    myCPXs = myCPXs.fillna(0)
    myCPXs.columns = [c.replace('.1', '') for c in myCPXs.columns]
    
    Experimental_PT = pd.read_excel(file_name, usecols = "Z:AA", skiprows=1)
    myLabels = pd.read_excel(file_name, usecols = "A", skiprows=1)
    
    #print('myCPXs')
    #print(myCPXs)
    return myLiquids, myCPXs, Experimental_PT, myLabels  



# Import Training Data
myLiquids, myCPXs, Experimental_PT, myLabels = import_Excel_experiments('GlobalDataset_Final_rev9_TrainValidation.xlsx')
a = myLiquids.values
b = myCPXs.values
X = np.concatenate((a,b),axis=1)
Y = np.array([Experimental_PT.T_K]).T
Labels = np.array([myLabels.Sample_ID]).T

# Scaling Training Data
scaler = StandardScaler().fit(X)
X = scaler.transform(X)

# Define the regressor, in our case the Extra Tree Regressor
regr = ExtraTreesRegressor(n_estimators=550, criterion='mse', max_features=22, random_state=280) # random_state fixed for reproducibility

# Train the model
regr.fit(X, Y.ravel())

# Import Unknown Samples
myLiquids1, myCPXs1, Experimental_PT1, myLabels1 = import_Excel_experiments('GlobalDataset_Final_rev9_Test.xlsx')
Y_test1 = np.array([Experimental_PT1.P_GPa * 10]).T
a1 = myLiquids1.values
b1 = myCPXs1.values
X1 = np.concatenate((a1,b1),axis=1)
Y1 = np.array([Experimental_PT1.T_K]).T
Labels1 = np.array([myLabels1.Sample_ID]).T

# Scaling Unknown Samples
X1 = scaler.transform(X1)

# Predict Unknowns
predicted = regr.predict(X1)   
r2 = r2_score(Y1, predicted)

# Print R2 and RMSE
print('R2')
print(r2)
MSE_ML = mean_squared_error(predicted, Y1)
print('RMSE ML')
print(np.sqrt(MSE_ML))

# Plot data       
plt.figure()
plt.plot([1050,1850],[1050,1850], c='#000000', linestyle='--')
plt.scatter(Y1,predicted, color='#ad1010', edgecolor='#000000', label="ExtraTreesRegressor - R2=" + str(round(r2,2)) + " - RMSE="+ str(round(np.sqrt(MSE_ML),0))+" K") 
plt.legend()
plt.show()    
        

