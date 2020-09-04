# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:12:55 2020

@author: Mohammad Amin Tahavori
"""

import REP_CVX


a = REP_CVX.C_SUT(path=r'Database\Kenya_2014_SAM.xlsx',unit='M KSH')
#%%
#a.shock_calc(path=r'Ecopulpers.xlsx',Y=False,Z=True,VA=True,S=True)  
a.shock_calc(path=r'Ecopulpers.xlsx',Y=True,Z=False,VA=False,S=False)  
#%%
a.sensitivity(path=r'Ecopulpers.xlsx')
#%%
a.plot_ds(indicator='Water',kind='Percentage',color=['blue','green','grey'])
#%%
a.impact(saving_sce=['se',1],invest_sce=['sh',1],p_life=10)
#%%
a.plot_dx()
#%%
a.obj_save(file_name='kenya') 
#%% 

  #%%

import pandas as pd
#%%
q=pd.read_excel(r'C:\Users\payam\Documents\GitHub\CIVICS_Kenya\CVX_Kenya\New Code\sens_Productivity increase due to 100% new machines (not spoiling the cerry)\case_0.5.xlsx',sheet_name='Z')


    
    
    
    
    
    
    
    