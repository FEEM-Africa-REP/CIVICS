# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:07:09 2020

@author: nigolred
"""
import civivs_sut as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')

Z = kenya.Z
VA = kenya.VA
Y = kenya.Y
GO = kenya.GO
HH = kenya.HH
IN = kenya.IN
X = kenya.X

#%%

a = kenya.VA
my_E = kenya.S
#%%
kenya.shock(path = r'Database\Shock.xlsx' , Y = True )
#%%kenya.calc_all()
X_new = kenya.X_c
#%%
kenya.calc_all()
#%%
kenya.aggregate()