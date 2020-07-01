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

kenya.plot_dx(unit='K EUR', level='Activities')
kenya.plot_dv(unit='K EUR', level='Commodities')
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
print(kenya.ROI)