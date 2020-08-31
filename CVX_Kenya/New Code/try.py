# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:12:55 2020

@author: Mohammad Amin Tahavori
"""

import REP_CVX as cvx

a = cvx.C_SUT(path=r'Database\Kenya_2014_SAM.xlsx',unit='M KSH') 
#%%
a.shock_calc(path=r'shading_trees.xlsx',Y=False,Z=True,VA=True,S=True)  
a.shock_calc(path=r'shading_trees.xlsx',Y=True,Z=False,VA=False,S=False)  
#%%
a.sensitivity(path=r'shading_trees.xlsx')
#%%
a.plot_dx(aggregated=False,style='classic',figsize=(30,10))
#%%
a.impact(saving_sce=['sh',1],invest_sce=['sh',2],p_life=10)
#%%
m_d = {'a':1,'b':2}
m_l = ['a','b']
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    