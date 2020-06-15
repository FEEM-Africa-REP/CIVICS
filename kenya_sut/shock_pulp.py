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

kenya.plot_dx(Unit = 'K EUR')
kenya.plot_dv(Unit = 'K EUR')
kenya.plot_dS(indicator='Green Water')
#%%
#step2: Benefit
kenya.shock(path = r'Database\Shock_pulp.xlsx' , VA=True, S=True, Z=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

kenya.plot_dx(Unit = 'K EUR')
kenya.plot_dv(Unit = 'K EUR')
kenya.plot_dS(indicator='CO2')
#%%
results = kenya.results

#%%
kenya.Int_Ass()



















