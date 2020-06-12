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
kenya.add_dict()

#detailed
X_1 = kenya.X_c
p_1 = kenya.p_c
VA_1= kenya.VA_c
S_1 = kenya.S_c
Y_1 = kenya.Y_c
Z_1 = kenya.Z_c
#%%

#aggregated
kenya.aggregate()
X_1_agg = kenya.X_c_agg
p_1_agg = kenya.p_c_agg
VA_1_agg = kenya.VA_c_agg
S_1_agg = kenya.S_c_agg
Y_1_agg = kenya.Y_c_agg
Z_1_agg = kenya.Z_c_agg
#%%
kenya.plot_dv(level='Commodities', percent=False)
kenya.plot_dx(level='Commodities', percent=False)
kenya.plot_dp(level='Activities')
#%%

#step2: benefit
kenya.shock(path = r'Database\Shock_pulp.xlsx' , VA=True, S=True, Z=True)

kenya.calc_all()
kenya.add_dict()
#detailed
X_2 = kenya.X_c
p_2 = kenya.p_c
VA_2= kenya.VA_c
S_2 = kenya.S_c
Y_2 = kenya.Y_c
Z_2 = kenya.Z_c


#%%

#aggregated
kenya.aggregate()
X_2_agg = kenya.X_c_agg
p_2_agg = kenya.p_c_agg
VA_2_agg = kenya.VA_c_agg
S_2_agg = kenya.S_c_agg
Y_2_agg = kenya.Y_c_agg
Z_2_agg = kenya.Z_c_agg

kenya.plot_dv(level='Activities')
kenya.plot_dx(level='Commodities', Unit='M USD')
kenya.plot_dp(level='Commodities')
kenya.plot_dS(indicator='Green Water')

#%%
database = kenya.database

#%%
base_S = kenya.S_agg
#%%
D_S = base_S -S_1_agg