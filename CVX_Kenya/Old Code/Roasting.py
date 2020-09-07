# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:28:09 2020

@author: Amin

"""
import REP_CVX as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%% Step1: Investment
kenya.shock(path=r'Interventions\Roasting.xlsx', Y=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

results = kenya.results

kenya.plot_dx(unit='K USD', level='Activities')
kenya.plot_dv(unit='K USD', level='Commodities')

# Focus on labour impact
kenya.plot_dv(unit='K USD', main_title='Additional labour input for each 1 M KSH unit of final demand of roasted coffee', level='Activities', percent=False, drop=['unused','Taxes','Import','Margins','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines'], 
              color='Accent')

#%% Step2: Benefit
kenya_r = cvx.C_SUT(r'Database\Kenya_2014_SAM_Roasting.xlsx')

kenya_r.shock(path=r'Interventions\Roasting - Sector analysis.xlsx', Y=True)

kenya_r.calc_all()
kenya_r.aggregate()

kenya_r.add_dict()
results = kenya_r.results
#%%
# Focus on labour impact
kenya_r.plot_dv(unit='K USD', main_title='Additional labour input for each 1 M KSH unit of final demand of roasted coffee', level='Activities', percent=False, drop=['unused','Taxes','Import','Margins','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines'], 
              color='Accent')

#%%

X_base = results['X']
Z_base = results['Z']

X_roast = results['X_1']
Z_roast = results['Z_1']

X_net = (X_roast - X_base).groupby(level=[0,4]).sum()
Z_net = (Z_roast - Z_base).groupby(level=4).sum().groupby(axis=1, level=4).sum().unstack()

# Conversion in dollars
ex_rate = 0.00928158 # From M KSH to M USD
X_plot = X_net * ex_rate * 10**6
Z_plot = Z_net * ex_rate * 10**6

