# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 15:12:57 2020

@author: Mohammad Amin Tahavori
"""
import REP_CVX 

sh_nets = REP_CVX.C_SUT(path = r'Database\Kenya_2014_SAM.xlsx', unit='M KSH')
#%%
sh_nets.shock_calc(path=r'Shock\Shading_nets.xlsx',Y=True)
sh_nets.plot_dx()
sh_nets.plot_dv(level='Activities',drop='unused')
sh_nets.plot_dv(level='Commodities',drop='unused')
sh_nets.plot_ds(indicator='CO2')
sh_nets.plot_ds(indicator='Water',color=['Blue','Green','Gray'])
sh_nets.plot_ds(indicator='Energy',color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
sh_nets.plot_ds(indicator='FAO Land')
#%%
sh_nets.shock_calc(path=r'Shock\Shading_nets.xlsx',Z=True)
sh_nets.plot_dx()
sh_nets.plot_dv(level='Activities',drop='unused')
sh_nets.plot_dv(level='Commodities',drop='unused')
sh_nets.plot_ds(indicator='CO2')
sh_nets.plot_ds(indicator='Water',color=['Blue','Green','Gray'])
sh_nets.plot_ds(indicator='Energy',color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
sh_nets.plot_ds(indicator='FAO Land')
#%%
sh_nets.sensitivity(path=r'Shock\Shading_nets.xlsx')
#%%
sh_nets.plot_sens(variable='X', sc_num=1)
#%%
sh_nets.plot_sens(variable='X', sc_num=2)
#%%
sh_nets.plot_sens(variable='S', sc_num=1,indicator='CO2')
#%%
sh_nets.plot_sens(variable='S', sc_num=2,indicator='CO2')
#%%
sh_nets.impact_assess(p_life=10, saving_sce=['sh',2], invest_sce=['sh',1])
#%%
sh_nets.impact_assess(p_life=10, saving_sce=['se',1], invest_sce=['sh',1])
#%%
sh_nets.impact_assess(p_life=10, saving_sce=['se',2], invest_sce=['sh',1])
#%%
results= sh_nets.results