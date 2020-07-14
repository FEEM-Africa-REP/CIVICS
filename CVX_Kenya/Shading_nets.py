    # -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:53:57 2020

@author: Amin
"""
# Import the library and the database
import REP_CVX as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')

kenya.shock(path = r'Interventions\Shading_nets.xlsx' , Y = True )

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

#%%
kenya.plot_dv(unit='M KSH', main_title='Change in the use of commodities', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'], color='ocean')
kenya.plot_dv(unit='M KSH', main_title='Change in the output of activities', level='Activities', percent=False, drop=['unused', 'Taxes', 'Import','Margins'], color='Accent')
kenya.plot_dx()
kenya.plot_dp()

kenya.plot_dS(indicator='CO2')
#%%
kenya.shock(path = r'Interventions\Shading_nets.xlsx' , Z=True ,VA = True, S=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()
kenya.plot_dv(unit='M KSH', main_title='Change in the use of commodities', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'], color='ocean')
kenya.plot_dv(unit='M KSH', main_title='Change in the output of activities', level='Activities', percent=False, drop=['unused', 'Taxes', 'Import','Margins'], color='Accent')

kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()
kenya.plot_dS()
#%%
results= kenya.results
#%%
kenya.Int_Ass()
print('ROI = '+str(round(kenya.ROI,4)))
print('Annual Savings = '+str(round(kenya.SAV,4)))