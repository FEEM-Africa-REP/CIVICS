# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:53:57 2020

@author: Amin
"""

import civivs_sut as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
kenya.shock(path = r'Database\Shock_shading.xlsx' , Y = True )
kenya.calc_all()
kenya.add_dict()
kenya.aggregate()
kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()
#%%
kenya.shock(path = r'Database\Shock_shading.xlsx' , Z=True ,VA = True )
kenya.calc_all()
kenya.add_dict()
kenya.aggregate()
kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()
#%%
