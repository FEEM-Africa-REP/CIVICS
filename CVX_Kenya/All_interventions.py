# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 19:49:57 2020

@author: nigolred
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:28:09 2020

@author: Amin

"""
import REP_CVX as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%% Step1: Investment
kenya.shock(path=r'Interventions\All_interventions.xlsx', Y=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

results = kenya.results

kenya.plot_dx(unit='K USD', level='Activities')
kenya.plot_dv(unit='K USD', level='Commodities')

#%%

VA = results['VA_1'].groupby(axis=1, level=4).sum()
VA.to_excel('Labor_induced_by_roasting_add.xlsx', sheet_name='additional')
VA_base = results['VA'].groupby(axis=1, level=4).sum()
VA_base.to_excel('Labor_induced_by_roasting.xlsx', sheet_name='base')

