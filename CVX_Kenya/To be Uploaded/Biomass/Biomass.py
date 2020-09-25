# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 15:42:14 2020

@author: Mohammad Amin Tahavori
"""
import REP_CVX 
bio = REP_CVX.C_SUT(path = r'Database\Kenya_2014_SAM.xlsx', unit='M KSH')
#%%
bio.shock_calc(path=r'Shock\Biomass_ongrid.xlsx',Y=True)
bio.plot_dx()
bio.plot_dv(level='Activities',drop='unused')
bio.plot_dv(level='Commodities',drop='unused')
bio.plot_ds(indicator='CO2')
bio.plot_ds(indicator='Water',color=['Blue','Green','Gray'])
bio.plot_ds(indicator='Energy',color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
bio.plot_ds(indicator='FAO Land')
#%%
bio.shock_calc(path=r'Shock\Biomass_ongrid.xlsx',Z=True,VA=True,S=True)
bio.plot_dx()
bio.plot_dv(level='Activities',drop='unused')
bio.plot_dv(level='Commodities',drop='unused')
bio.plot_ds(indicator='CO2')
bio.plot_ds(indicator='Water',color=['Blue','Green','Gray'])
bio.plot_ds(indicator='Energy',color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
bio.plot_ds(indicator='FAO Land')
#%%
bio.sensitivity(path=r'Shock\Biomass_ongrid.xlsx')
#%%
bio.plot_sens(variable='X', sc_num=1)
#%%
bio.impact_assess(p_life=10, saving_sce=['sh',2], invest_sce=['sh',1])
#%%
bio.impact_assess(p_life=10, saving_sce=['se',1], invest_sce=['sh',1])

#%%
results= bio.results