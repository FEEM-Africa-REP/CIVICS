    # -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:53:57 2020

@author: Amin
"""
# Import the library and the database
import REP_CVX as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
sh_path = r'Interventions\Shading_nets.xlsx'
#r'Interventions\shading nets\0.9.xlsx'
#r'Interventions\Shading_nets.xlsx'

kenya.shock(path = sh_path, Y = True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

#%%
# kenya.plot_dv(unit='M USD', main_title='Change in the use of commodities', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'], color='ocean')
kenya.plot_dv(unit='K USD', main_title='Change in the output of activities', level='Activities', percent=False, drop=['unused', 'Taxes', 'Import','Margins'], color='Accent')

#%%
kenya.plot_dv(unit='K USD', main_title='Activity changes by Value Added for covering 100% cooperatives coffee fields', level='Activities', percent=False, drop=['unused', 'Taxes', 'Import','Margins'], color='Accent', ranshow=(10,-0.001), aggregation=True)

#%%
# kenya.plot_dx()
# kenya.plot_dp()

#kenya.plot_dS(indicator='CO2')
#%%
kenya.shock(path = sh_path, Z=True ,VA = True, S=True)

kenya.calc_all()
kenya.aggregate()
kenya.add_dict()

kenya.sensitivity(parameter='Z')
#%%
kenya.plot_dv(unit='K USD', main_title='Change in the use of commodities', level='Commodities', percent=False, drop=['unused','Capital - Land','Capital - Livestock','Capital - Agriculture','Capital - Machines','Labor - Skilled', 'Labor - Semi Skilled', 'Labor - Unskilled'], color='ocean', ranshow=(0.0001,-10))
kenya.plot_dv(unit='K USD', main_title='Change in the output of activities', level='Activities', percent=False, drop=['unused', 'Taxes', 'Import','Margins'], color='Accent',  ranshow=(0.0001,-10))

# kenya.plot_dv(unit='K USD', main_title='Change in the output of activities', level='Activities', percent=False, drop=['unused', 'Taxes', 'Import','Margins'], color='Pastel1', ranshow=(0.0001,-0.00001), aggregation=False)
# kenya.plot_dx(unit='K USD', level='Activities', percent=False, ranshow=(0.0001,-0.0001), aggregation=False)

# kenya.plot_dv()
# kenya.plot_dx()
# kenya.plot_dp()
kenya.plot_dS(main_title='Reduction in Carbon Dioxide emission by source and sector', indicator='CO2')
kenya.plot_dS(main_title='Reduction in Land Use by category and sector', indicator='Land', color='Wistia',  ranshow=(0,-0.05))

#%%
kenya.Int_Ass(sav_sen=['sensitivity',1],sce_name='Shading_prod')

# results= kenya.results