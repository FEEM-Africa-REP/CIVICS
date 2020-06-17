# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:53:57 2020

@author: Amin
"""

import civivs_sut as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
env0=kenya.S
kenya.shock(path = r'Database\Shock_shading_update.xlsx' , Y = True )
kenya.calc_all()
kenya.aggregate()
kenya.add_dict()
kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()
kenya.plot_dS(indicator='CO2')
#%%
kenya.shock(path = r'Database\Shock_shading_update.xlsx' , Z=True ,VA = True, S=True)
kenya.calc_all()
kenya.aggregate()
kenya.add_dict()
kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()
kenya.plot_dS()
#%%
results= kenya.results
#%%
kenya.Int_Ass()