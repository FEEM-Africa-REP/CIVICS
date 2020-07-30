# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:53:57 2020

@author: Amin
"""

import REP_CVX as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
env0=kenya.S
kenya.shock(path = r'Interventions\Biomass_ongrid.xlsx' , Y = True )

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()

kenya.plot_dS(indicator='CO2')
#%%
kenya.shock(path = r'Interventions\Biomass_ongrid.xlsx' , Z=True ,VA = True, S=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

kenya.plot_dv(unit='M KSH', main_title='Change in the use of commodities', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'], color='ocean')
kenya.plot_dx()
kenya.plot_dp()
kenya.plot_dS()
#%%
kenya.sensitivity(parameter='Z')

results= kenya.results
#%%
kenya.Int_Ass(sav_sen=['sensitivity',1], sce_name='Biomass_price_petr')
# print(kenya.ROI)