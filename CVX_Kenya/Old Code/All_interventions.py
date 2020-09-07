# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 19:49:57 2020

@author: nigolred
"""

import REP_CVX as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%% Step1: Investment
kenya.shock(path=r'Interventions\All_interventions_side_policies.xlsx', Y=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

results = kenya.results

kenya.plot_dx(unit='K USD', level='Activities')
kenya.plot_dv(unit='K USD', level='Activities')

VA = results['VA_1'].groupby(axis=1, level=4).sum()
VA.to_excel('Labor_induced_by_roasting_add.xlsx', sheet_name='additional')
VA_base = results['VA'].groupby(axis=1, level=4).sum()
VA_base.to_excel('Labor_induced_by_roasting.xlsx', sheet_name='base')
#%% Step2: Benefit
kenya.shock(path=r'Interventions\All_interventions_side_policies.xlsx', VA=True, S=True, Z=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

#%%



kenya.Int_Ass(sce_name='All_opt_only_mon2')
