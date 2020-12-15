# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 09:24:15 2020

@author: nigolred
"""

import sys
sys.path.insert(1,r'C:\Users\Gollinucci\Documents\GitHub\CIVICS')

import REP_CVX

Ghana = REP_CVX.C_SUT(path = r'C:\Users\Gollinucci\Documents\GitHub\CIVICS\CIVICS_Ghana\IO_Ghana\Database\GHANA_2015_CVX.xlsx', unit = 'M GHS', name='Pumpfed Irrigation for Maize')
#%%
Ghana.shock_calc(path=r'Pumpfed Irrigation for Maize/Shock1_inputs.xlsx', Y=True)
Ghana.plot_dx()
Ghana.plot_dv(level='Activities', title='Required Value Added for producing the wells and pumps')
Ghana.plot_dv(level='Commodities', title='Required Commodities for producing the wells and pumps')

#%%
Ghana.shock_calc(path=r'Pumpfed Irrigation for Maize/Shock1_inputs.xlsx', Z=True, S=True)

Ghana.plot_dv(level='Activities', title='Saved Value Added using pumpfed irrigation')
Ghana.plot_dv(level='Commodities', title='Saved imports for using pumpfed irrigation', drop=['Traders','Indirect Taxes'], color='red')
Ghana.plot_ds(indicator='Water', color=['Blue','Green','Grey'])
Ghana.plot_ds(indicator='CO2', detail=False)
Res = Ghana.results

#%%
Ghana.sensitivity(r'Pumpfed Irrigation for Maize/Shock1_inputs.xlsx')
Ghana.plot_sens('S', sc_num=2, indicator='Water')
#%%

Ghana.impact_assess(p_life=10, saving_sce=['se', 3], invest_sce=['sh',1],imports=['Import'],
                    w_ext=['Water'], em_ext=['CO2'], land=['Land'], 
                    labour=['Labor'],
                    capital=['Capital'], save_excel=True)
#%%
Ghana.impact_assess(p_life=10, saving_sce=['sh', 2], invest_sce=['se',2],imports=['Import'],
                    w_ext=['Water'], em_ext=['CO2'], land=['Land'], 
                    labour=['Labor'],
                    capital=['Capital'], save_excel=True)

    