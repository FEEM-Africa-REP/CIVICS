# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:53:57 2020

@author: Amin
"""

import civivs_sut as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
env0=kenya.S
kenya.shock(path = r'Database\Shock_pulp.xlsx' , Y = True )
kenya.calc_all()
kenya.add_dict()
kenya.aggregate()
kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()
kenya.plot_dS(indicator='CO2')
#%%
env1=kenya.S_c
Investment=kenya.Y_c.sum().sum()-kenya.Y.sum().sum()
#%%
kenya.shock(path = r'Database\Shock_pulp.xlsx' , Z=True ,VA = True, S=True)
kenya.calc_all()
kenya.add_dict()
kenya.aggregate()
kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()
kenya.plot_dS()
env2=kenya.S_c
Savings=kenya.VA_c.sum().sum()-kenya.VA.sum().sum()
kenya.optimize(scenario=2)
#%%
X_opt = kenya.X_opt
Y_opt = kenya.Y_opt
#%%
results= kenya.results
#%%
env_del1 = env2 - env0
change = env_del1 / env0 * 100

#%%

#%%
kenya.plot_dS(indicator='Energy',details=True,Type='change')