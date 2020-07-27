# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:53:57 2020

@author: Amin
"""

import REP_CVX_sens as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')

kenya.shock(path = r'Interventions\Shading_trees.xlsx' , Y = True )
kenya.calc_all()
kenya.aggregate()
kenya.add_dict()
#%%
kenya.sensitivity(parameter='Y')

# kenya.plot_dv()
# kenya.plot_dx()
# kenya.plot_dp()

#kenya.plot_dS(indicator='CO2')

#%%
kenya.plot_dv(unit='M KSH', main_title='Change in the use of commodities', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'], color='ocean')
kenya.plot_dv(unit='M KSH', main_title='Change in the output of activities', level='Activities', percent=False, drop=['unused', 'Taxes', 'Import','Margins'], color='Accent')
#%%
kenya.shock(path = r'Interventions\Shading_trees.xlsx' , Z=True ,VA = True, S=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

# kenya.plot_dv() 
# kenya.plot_dx()
# kenya.plot_dp()
# kenya.plot_dS(Type='absolute')
#%%
kenya.plot_dv(unit='M KSH', main_title='Change in the use of commodities', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'], color='ocean')
kenya.plot_dv(unit='M KSH', main_title='Change in the output of activities', level='Activities', percent=False, drop=['unused', 'Taxes', 'Import','Margins'], color='Accent')

#%%
results= kenya.results
#%%
kenya.Int_Ass(inv_sen=['sensitivity',1],sav_sen=['main',2],sce_name='Sens_Try')
#print(kenya.ROI)
#%%
sens = kenya.X_s
sens0 = kenya.VA_s
#%%
a1 = results['S_s_agg_1'].loc['0.06','Energy'].sum().sum()
#%%
labour=['Labor - Skilled','Labor - Semi Skilled','Labor - Unskilled']
#%%
a=kenya.Y_s-kenya.Y