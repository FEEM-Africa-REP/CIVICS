# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:27:10 2020

@author: Mohammad Amin Tahavori
"""
import REP_CVX as rc

sh_tree = rc.C_SUT(path = r'Database\Kenya_2014_SAM.xlsx', unit='M KSH')
#%%
sh_tree.shock_calc(path=r'Shock\Shading_trees.xlsx',Y=True)
sh_tree.plot_dx()
sh_tree.plot_dv(level='Activities',drop='unused')
sh_tree.plot_dv(level='Commodities',drop='unused')
sh_tree.plot_ds(indicator='CO2')
sh_tree.plot_ds(indicator='Water',color=['Blue','Green','Gray'])
sh_tree.plot_ds(indicator='Energy',color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
sh_tree.plot_ds(indicator='FAO Land')
#%%
sh_tree.shock_calc(path=r'Shock\Shading_trees.xlsx',Z=True,VA=True,S=True)
sh_tree.plot_dx()
sh_tree.plot_dv(level='Activities',drop='unused')
sh_tree.plot_dv(level='Commodities',drop='unused')
sh_tree.plot_ds(indicator='CO2')
sh_tree.plot_ds(indicator='Water',color=['Blue','Green','Gray'])
sh_tree.plot_ds(indicator='Energy',color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
sh_tree.plot_ds(indicator='FAO Land')
#%%
sh_tree.sensitivity(path=r'Shock\Shading_trees.xlsx')

#%%
sh_tree.plot_sens(variable='X', sc_num=1)
#%%
sh_tree.plot_sens(variable='X', sc_num=2)
#%%
sh_tree.impact_assess(p_life=20, saving_sce=['sh',2], invest_sce=['sh',1])
#%%
sh_tree.impact_assess(p_life=20, saving_sce=['se',2], invest_sce=['sh',1])
#%%
sh_tree.impact_assess(p_life=20, saving_sce=['sh',2], invest_sce=['se',1])
#%%
results= sh_tree.results