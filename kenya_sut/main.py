# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 16:06:38 2020

@author: negar
"""
# Setting the directory:

# Please insert the directory in which you store the code in your computer
path = r'F:\FEEM\input_output\kenya_sut'
import os
os.getcwd()
os.chdir(path)
os.getcwd()
import pandas as pd
import numpy as np
#from numpy import *
#%%
SUT=pd.read_excel('Kenya_2014_SAM_0.xlsx',sheet_name='Sheet1',index_col=[0,1,2,3],header=[0,1,2,3])
#%%
Z=SUT.loc[['commodity','industry'],['commodity','industry']]
#%%
#This is the local final demand
F=SUT.loc[['commodity','industry'],'final demand']
#%%
INV=SUT.loc[['commodity','industry'],'investment']
#%%
EXP=SUT.loc[['commodity','industry'],'export']
#%%
Y=pd.DataFrame(F.sum(axis=1)+INV.sum(axis=1)+EXP.sum(axis=1),index=Z.index,columns=['total final demand'])
#%%
x=pd.DataFrame(F.sum(axis=1)+INV.sum(axis=1)+EXP.sum(axis=1)+Z.sum(axis=1),index=Z.index,columns=['total production'])
#%%
A=Z.values@np.linalg.inv(x.values*np.identity(len(x)))
#%%
IMP=SUT.loc['import',['commodity','industry']]
#%%
VA=SUT.loc[['value added0','value added1','taxes','investment','extra taxes'],['commodity','industry']]
#%%
imp=IMP.values@np.linalg.inv(x.values*np.identity(len(x)))
#%%
va=VA.values@np.linalg.inv(x.values*np.identity(len(x)))
#%%
 