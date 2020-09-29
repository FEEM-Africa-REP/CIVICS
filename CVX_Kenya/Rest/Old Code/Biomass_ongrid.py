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

# kenya.plot_dv()
# kenya.plot_dx()
# kenya.plot_dp()

kenya.plot_dS(indicator='CO2', main_title='Carbon footprint of the set-up of the power plant')
#%%
kenya.shock(path = r'Interventions\Biomass_ongrid.xlsx' , Z=True ,VA = True, S=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

kenya.plot_dv(unit='K USD', main_title='Change in the use of commodities', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled','Taxes','Margins'], color='ocean', ranshow=(0.0001,-10))
kenya.plot_dv(unit='K USD', main_title='Changes avoiding electricity production from oil derivatives and own-producing fertilizers', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'], color='ocean')
# kenya.plot_dx()
# kenya.plot_dp()
# kenya.plot_dS()
#%%
kenya.sensitivity(parameter='Z')

#results= kenya.results
#%%
kenya.Int_Ass(sce_name='Biomass_12')
# print(kenya.ROI)