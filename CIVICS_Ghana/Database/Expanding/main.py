# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:04:39 2020

@author: Amin

Goal:
    Adding additional layer of environemtal extansions to the CVX SUT
    using EORA Database.
    
    The idea is to have an environmental extension in the form of CVX SUT.
"""
# This parameter tells the model inf it should make a new proxy matrix or not
rewrite = True
#%%
# Importing the needed libraries
import pandas as pd
import numpy as np
import os
#%%
"""
First step:
    the user has to build the a concordance matrix with the following structure:
        1. indeces: EORA Industries
        2. columns: CVX SUT Industries
    this matrix should be filled with 0 or 1 showing the concordance of the
    different sectors in the tables.
    There should not be any rows or sectors without at least one cell equal to 0,
    which means that at the end, two tables are representating the same economy 
    with differnet representation.
"""
# Reading the concordance matrix
Gi = pd.read_excel(r'Concordance Matrix.xlsx', index_col = [0], header = [0])

# Building the main lists
eora_sec = Gi.index.to_list()
sam_sec  = Gi.columns.to_list()

# Checking the rows:
for i in range (len(eora_sec)):
    if Gi.loc[eora_sec[i]].sum() == 0 :
        raise ValueError("sector {} in EORA has now concordance sector in CVX SUT".format(eora_sec[i]))

# Cheking the columns:
for i in range(len(sam_sec)):
    if Gi[sam_sec[i]].sum() == 0 :
        raise ValueError("sector {} in SAM has now concordance sector in EORA".format(sam_sec[i]))

#%%
"""
We may need to do both aggregation and disaggregation on EORA in order to reach
to the same structure of CVX SUT.
The structure of concordance matrix tells us if we need to aggregation or 
disaggregation.

HOW?

Looking at the structure of the excel file, it can be understood if the sum of
a row is greater than 1, it means that some sectors in EORA belong to 1 sector
in CVX SUT together and should be aggregated and vice versa.

Lets start with aggregation which is easier
"""
# Make the list of the sectors that needs to be aggregated with their corresponding sector
eora_agg = []
eora_to_sam_ag = []
agg_list = []
for i in range(len(sam_sec)):
    if Gi[sam_sec[i]].sum() > 1 :

        for j in range(len(eora_sec)):
            if Gi.values[j,i] == 1:
                eora_agg.append(eora_sec[j])
                eora_to_sam_ag.append(sam_sec[i])
                
eora_dis = []
eora_to_sam_dis = []
for i in range (len(eora_sec)):
    if Gi.loc[eora_sec[i]].sum() > 1 :
        for j in range(len(sam_sec)):
            if Gi.values[i,j] == 1:
                eora_dis.append(eora_sec[i])
                eora_to_sam_dis.append(sam_sec[j])
                
#%%
# Reading EORA Datbase 
Eora = pd.read_excel(r'IO_GHA_2015_BasicPrice.xlsx',index_col = [0,1,2] , columns = [0])
#%%

for i in range (len(eora_agg)):
    Gi = Gi.rename(index = {eora_agg[i]:eora_to_sam_ag[i]})
    Eora = Eora.rename(columns = {eora_agg[i]:eora_to_sam_ag[i]})
    
#%%
Gi = Gi.groupby(level = 0,sort = False, axis = 0).mean()
Eora = Eora.groupby(level = 0 , sort = False, axis = 1).sum()
#%%
eora_dis_single = list(dict.fromkeys(eora_dis))
#%%
# Find the position in data frame
number = []
for i in range(len(eora_dis_single)):
    counter = 0
    for j in range (len(eora_dis)):
        if eora_dis_single[i] == eora_dis [j]:
            counter += 1
    number.append(counter)
#%%
my_list = []
for i in range(len(eora_dis_single)):
    location = Eora.columns.get_loc(eora_dis_single[i])
    my_list.append(eora_dis_single[i])
    for j in range(number[i]-1):
        Eora.insert(location+j+1,eora_dis_single[i] + str(j+1),'0',True)
        my_list.append(eora_dis_single[i] + str(j+1))
                
#%%
if rewrite:
    proxy = pd.DataFrame(np.zeros((len(eora_dis_single),len(my_list))),index=eora_dis_single,columns = [eora_to_sam_dis,my_list] )        
    with pd.ExcelWriter(r'proxy.xlsx') as writer:
        proxy.to_excel(writer)
    os.startfile(r'proxy.xlsx')
    
    input('Click on Enter to Continue:')      
#%% 
proxy = pd.read_excel(r'Results\proxy.xlsx',index_col = [0] , header = [0,1])
#%%
Eora_calc = Eora.copy()
#%%
for i in range (len(eora_dis_single)):
    for j in range(number[i]):
        if j ==0:
            ind = my_list.index(eora_dis_single[i])
            Eora[eora_dis_single[i]] = Eora_calc[eora_dis_single[i]].astype(float) \
                * proxy.loc[eora_dis_single[i],(eora_to_sam_dis[ind],my_list[ind])].astype(float)
            print(proxy.loc[eora_dis_single[i],(eora_to_sam_dis[ind],my_list[ind])])
        else :
            
            ind = my_list.index(eora_dis_single[i] + str(j))
            Eora[eora_dis_single[i] + str(j)] = Eora_calc[eora_dis_single[i]].astype(float) \
                * proxy.loc[eora_dis_single[i],(eora_to_sam_dis[ind],my_list[ind])].astype(float)  
            print(proxy.loc[eora_dis_single[i],(eora_to_sam_dis[ind],my_list[ind])])
    



#%%       
for i in range(len(my_list)):
    Eora = Eora.rename(columns = {my_list[i]:eora_to_sam_dis[i]})            
        
  
#%%
"""
Now it is time to disaggregate the final demand resource extention.
The input file should be the resource use matrix of final demand of EORA.
On the other side, the proxy should be driven from SAM. The proxy which is used
to disaggregate the matrix, is:
            
                Zinf / (Zinf + ytot)
                
All the matrices should be well prepared as can be seen in this code.
"""
# First step: read the file
fd_res = pd.read_excel(r'Databases\fd_res2.xlsx', index_col = [0,1,2] , header = [0,1])

#%%
# Building the new matrix
informal_ind = pd.read_excel(r'Databases\informal.xlsx',index_col = [0] , header = [0,1])
informal_ind_list = pd.read_excel(r'Databases\informal_list.xlsx',index_col = [0] , header = [0]) 
inf_ind_list = informal_ind_list['informal industries'].dropna().to_list()
#%%
proxy = pd.DataFrame(np.zeros((1,len(inf_ind_list))),index = ['value'],columns = inf_ind_list )
E = pd.DataFrame(np.zeros((len(fd_res.index),len(inf_ind_list))),index =fd_res.index , columns = inf_ind_list)
#%%

# par_1: sum industry inputs for whole informal industry + sum of final demand
par_1 = informal_ind.sum().sum()

# par_2: sum of the industry output for every informal industry
par_2 = informal_ind.sum()['informal industries']

#%%
for i in range (len(inf_ind_list)):
    proxy[inf_ind_list[i]] = par_2[inf_ind_list[i]] / par_1
    
#%%  
for i in range (len(inf_ind_list)):
    E[inf_ind_list[i]] = proxy[inf_ind_list[i]].value * fd_res

#%%
E_ext = pd.concat([E,Eora],axis = 1)
    
    
    

#%%
# In order to calculate the coefficients, we need to divide E matrix with x which is production
x = pd.read_excel(r'Databases\production.xlsx',index_col = [0],header = [0])
#%%
x_cal = x.values * np.identity(len(x))   
#%%     
E_coef = E_ext @ np.linalg.inv(x_cal)   
E_coef.columns = x.index 
#%%
with pd.ExcelWriter('E.xlsx') as writer:
    E_ext.to_excel(writer,sheet_name = 'Flow')  
    E_coef.to_excel(writer,sheet_name = 'Coefficient')
        
        
        
        