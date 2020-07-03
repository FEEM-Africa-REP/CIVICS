# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:28:09 2020

@author: Amin

"""
import REP_CVX as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%% Step1: Investment
kenya.shock(path=r'Interventions\Pulping_machines.xlsx', Y=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

kenya.plot_dx(unit='M KSH', level='Activities')
kenya.plot_dv(unit='M KSH', level='Activities')
#%%
# Focus on labour impact
kenya.plot_dv(unit='M KSH', main_title='Investment-induced Labour increase by skill and sector', level='Activities', percent=False, drop=['unused','Taxes','Import','Margins','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines'], 
              color='spring')
#%%
# Focus on land
kenya.plot_dv(unit='M KSH', main_title='Investment-induced Capital - Land increase by sector', level='Activities', percent=False, drop=['unused','Taxes','Import','Margins','Labor - Skilled','Labor - Unskilled','Labor - Semi Skilled','Capital - Livestock','Capital - Agriculture','Capital - Machines'], color='spring')


kenya.plot_dS(indicator='Green Water')
#%% Step2: Benefit
kenya.shock(path=r'Interventions\Pulping_machines.xlsx', VA=True, S=True, Z=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

kenya.plot_dx(unit='K EUR', level='Activities')
kenya.plot_dv(unit='K EUR', level='Activities')
kenya.plot_dS(indicator='Green Water')
#%%
results = kenya.results
#%%
kenya.Int_Ass()
print('ROI = '+str(round(kenya.ROI,4)))
print('Annual Savings = '+str(round(kenya.SAV,4)))
