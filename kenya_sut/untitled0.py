# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:28:09 2020

@author: Amin
"""
import civivs_sut as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')

kenya.shock(path = r'Database\Shock_pulp.xlsx' , Y=True)

kenya.calc_all()
x_1 = kenya.X_c
S_1 = kenya.S_c
#%%
kenya.shock(path = r'Database\Shock_pulp.xlsx' , Z=True,VA=True)
kenya.calc_all()