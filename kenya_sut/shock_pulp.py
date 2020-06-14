# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:28:09 2020

@author: Amin

"""
import civivs_sut as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%%
#step1: Investment
kenya.shock(path = r'Database\Shock_pulp.xlsx' , Y = True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

#%%
#step2: benefit
kenya.shock(path = r'Database\Shock_pulp.xlsx' , VA=True, S=True, Z=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()


#%%
results = kenya.results

#%%
kenya.Int_Ass()



















