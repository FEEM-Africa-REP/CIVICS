# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:07:09 2020

@author: nigolred
"""
import civivs_sut as cvx

kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')

Z = kenya.Z
Z.to_excel('Z.xlsx')
VA = kenya.VA
VA.to_excel('VA.xlsx')
Y = kenya.Y
Y.to_excel('Y.xlsx')
GO = kenya.GO
HH = kenya.HH
IN = kenya.IN
X = kenya.X
T = kenya.T
V = kenya.V

#%%
# kenya.calc_all()
VA_r = VA.sum(axis=0)
Z_r = Z.sum(axis=0)
ROW = VA_r + Z_r
Y_c = Y.sum(axis=1)
Z_c = Z.sum(axis=1)
COL = Y_c + Z_c
delta = ROW - COL
