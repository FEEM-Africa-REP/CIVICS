# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 10:42:47 2020

@author: Mohammad Amin Tahavori
"""
import REP_CVX 
eco_p = REP_CVX.C_SUT(path = r'Database\Kenya_2014_SAM.xlsx', unit='M KSH')
#%%
eco_p.shock_calc(path=r'Shock\Ecopulpers.xlsx',Y=True)
eco_p.plot_dx()
eco_p.plot_dv(level='Activities',drop='unused',unit='K USD')
eco_p.plot_dv(level='Commodities',drop='unused')
eco_p.plot_ds(indicator='CO2')
eco_p.plot_ds(indicator='Water',color=['Blue','Green','Gray'])
eco_p.plot_ds(indicator='Energy',color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
eco_p.plot_ds(indicator='FAO Land')
#%%
eco_p.shock_calc(path=r'Shock\Ecopulpers.xlsx',Z=True,VA=True,S=True)
eco_p.plot_dx()
eco_p.plot_dv(level='Activities',drop='unused')
eco_p.plot_dv(level='Commodities',drop='unused')
eco_p.plot_ds(indicator='CO2')
eco_p.plot_ds(indicator='Water',color=['Blue','Green','Gray'])
eco_p.plot_ds(indicator='Energy',color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
eco_p.plot_ds(indicator='FAO Land')
#%%
eco_p.sensitivity(path=r'Shock\Ecopulpers.xlsx')
#%%
eco_p.plot_sens(variable='X', sc_num=1)
#%%
eco_p.plot_sens(variable='X', sc_num=2)
#%%
eco_p.impact_assess(p_life=10, saving_sce=['sh',2], invest_sce=['sh',1])
#%%
eco_p.impact_assess(p_life=10, saving_sce=['se',1], invest_sce=['sh',1])
#%%
eco_p.impact_assess(p_life=10, saving_sce=['se',2], invest_sce=['sh',1])
#%%
results= eco_p.results

