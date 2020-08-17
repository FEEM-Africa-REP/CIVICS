# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:28:09 2020

@author: Amin

"""
import REP_CVX as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%% Step1: Investment
kenya.shock(path=r'Interventions\Ecopulpers.xlsx', Y=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

#%%
# Focus on labour impact
kenya.plot_dv(unit='K USD', main_title='Investment-induced Labour increase by skill and sector for renewing 40% of wet mills', level='Commodities', color='Accent', drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'])
kenya.plot_dv(unit='K USD', main_title='Investment-induced Labour increase by skill and sector for renewing 40% of wet mills', level='Activities', drop=['unused','Taxes','Import','Margins','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines'], color='Accent')


kenya.plot_dS(indicator='Water',  Type='percentage', main_title='Decrease in the use of green water', color='ocean')
#%% Step2: Benefit
kenya.shock(path=r'Interventions\Ecopulpers.xlsx', VA=True, S=True, Z=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()
#%%
kenya.sensitivity(parameter='Z')

kenya.plot_dv(unit='K USD', main_title='Annual impact of using more efficient machines', level='Activities', percent=False, drop=['unused','Taxes','Import','Margins'], color='terrain')

kenya.plot_dS(indicator='Water',  Type='absolute', main_title='Decrease in the use of water due to use of eco-pulpers', color='ocean')
kenya.plot_dS(indicator='CO2',  Type='absolute', main_title='Changes in CO2 emissions due to the use of eco-pulpers')

#%%
#results = kenya.results
#%%
kenya.Int_Ass(sav_sen=['sensitivity',1], sce_name='Ecopulpers_petr')
