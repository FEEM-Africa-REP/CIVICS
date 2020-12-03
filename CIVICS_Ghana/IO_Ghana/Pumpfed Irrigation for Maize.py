# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 09:24:15 2020

@author: nigolred
"""

import sys
sys.path.insert(1,r'C:\Users\Gollinucci\Documents\GitHub\CIVICS')

import REP_CVX

Ghana = REP_CVX.C_SUT(path = r'Database\GHANA_2015_CVX.xlsx', unit = 'M GHS', name='Pumpfed Irrigation for Maize')
#%%
Ghana.shock_calc(path=r'Pumpfed Irrigation for Maize/Shock1_inputs.xlsx', Y=True)
Ghana.plot_dx()
Ghana.plot_dv(level='Activities', title='Required Value Added for producing the wells')
Ghana.plot_dv(level='Commodities', title='Required Commodities for producing the wells')

#%%
Ghana.shock_calc(path=r'Pumpfed Irrigation for Maize/Shock1_inputs.xlsx', Z=True)

Ghana.plot_dv(level='Activities', title='Saved Value Added for using the wells')
Ghana.plot_dv(level='Commodities', title='Saved Commodities for using the wells')

Ghana.impact_assess(p_life=10, saving_sce=['sh', 2], invest_sce=['sh',1], labour=['Labor'], capital=['Capital'])

