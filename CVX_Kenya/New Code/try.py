# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:12:55 2020

@author: Mohammad Amin Tahavori
"""

import REP_CVX as cvx

a=cvx.C_SUT(path=r'Database\Kenya_2014_SAM.xlsx',unit='M KSH') 
#%%
a.shock_calc(path=r'Shading_trees.xlsx',Y=True)  
#%%
a.plot_dv(unit='M USD',level='Activities')
