# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:12:55 2020

@author: Mohammad Amin Tahavori
"""
import REP_CVX as aa


amin = aa.C_SUT(path=r'Database\Kenya_2014_SAM - New.xlsx',unit='M KSH')
#%%
#a.shock_calc(path=r'Ecopulpers.xlsx',Y=False,Z=True,VA=True,S=True)  
amin.shock_calc(path=r'Ecopulpers.xlsx',Y=True,Z=False,VA=False,S=False)  
#%%
amin.sensitivity(path=r'Ecopulpers.xlsx')
#%%
amin.plot_ds(indicator='Water',color=['blue','green','grey'])
#%%
amin.impact_assess(saving_sce=['se',1],invest_sce=['sh',1],p_life=10)
#%%
amin.plot_ds(indicator='CO2',detail=True)
#%%
amin.obj_save(file_name='kenya') 
#%%
amin.plot_sens
#%% 

amin.plot_sens(variable='S',sc_num=1,level='Activities',indicator='CO2',rational=0)
 #%%
import pymrio
#%%
amin.get_excel_shock()
#%%

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        