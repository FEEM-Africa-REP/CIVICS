# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 09:24:15 2020

@author: nigolred
"""

import sys
sys.path.insert(1,r'C:\Users\Gollinucci\Documents\GitHub\CIVICS')

import REP_CVX

Case = 'Indipendent Power Supply for Feed Mills'
Scenario = '50% solar'

Ghana = REP_CVX.C_SUT(path = r'C:\Users\Gollinucci\Documents\GitHub\CIVICS\CIVICS_Ghana\IO_Ghana\Database\GHANA_2015_CVX.xlsx', unit = 'M GHS', name=Case)
#%%
Ghana.shock_calc(path=r'Indipendent Power Supply for Feed Mills/'+Scenario+'.xlsx', Y=True)
Ghana.plot_dx()
Ghana.plot_dv(level='Activities', title='Required Value Added for producing the mini-grid for the mills in the Scenario '+Scenario)
Ghana.plot_dv(level='Commodities', title='Required Commodities for producing the mini-grid for the mills in the Scenario '+Scenario)

#%%
Ghana.shock_calc(path=r'Indipendent Power Supply for Feed Mills/'+Scenario+'.xlsx', Z=True, VA=True)

Ghana.plot_dv(level='Activities', title='Saved Value Added using the mini-grid for grain milling in the Scenario '+Scenario)
Ghana.plot_dv(level='Commodities', title='Saved imports for using the mini-grid for grain milling in the Scenario '+Scenario)
Ghana.plot_ds(indicator='Water', color=['Blue','Green','Grey'])
Ghana.plot_ds(indicator='GHG')
# Ghana.plot_ds(indicator='CO2', detail=False)
# Ghana.plot_ds(indicator='CH4', detail=False)
# Ghana.plot_ds(indicator='N2O', detail=False)


Res = Ghana.results


#%%
# Ghana.sensitivity(r'Indipendent Power Supply for Feed Mills/'+Scenario+'.xlsx')
# Ghana.plot_sens('S', sc_num=2, indicator='Water')
#%%

Ghana.impact_assess(p_life=10, saving_sce=['sh', 2], invest_sce=['sh',1],imports=['Import'],
                    w_ext=['Water'], em_ext=['GHG'], land=['Land'], 
                    labour=['Labor'],
                    capital=['Capital'], save_excel=True)
# #%%
# Ghana.impact_assess(p_life=10, saving_sce=['sh', 2], invest_sce=['se',2],imports=['Import'],
#                     w_ext=['Water'], em_ext=['GHG'], land=['Land'], 
#                     labour=['Labor'],
#                     capital=['Capital'], save_excel=True)