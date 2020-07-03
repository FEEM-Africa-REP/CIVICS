# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:28:09 2020

@author: Amin

"""
import REP_CVX as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%% Step1: Investment
kenya.shock(path=r'Interventions\Roasting.xlsx', Y=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

kenya.plot_dx(unit='K EUR', level='Activities')
kenya.plot_dv(unit='K EUR', level='Commodities')
#%% Step2: Benefit)
kenya_r = cvx.C_SUT(r'Database\Kenya_2014_SAM_Roasting.xlsx')

SAV = kenya_r.VA.sum().sum()-kenya.VA.sum().sum()
INV = kenya.VA_c.sum()-kenya.VA.sum()

ROI = INV.sum()/SAV
#%%
# Focus on labour impact
kenya.plot_dv(unit='M KSH', main_title='Investment-induced Labour increase by skill and sector', level='Activities', percent=False, drop=['unused','Taxes','Import','Margins','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines'], 
              color='spring')

