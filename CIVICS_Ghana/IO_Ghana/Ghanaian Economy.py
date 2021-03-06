# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 18:03:02 2020

@author: nigolred
"""
import sys
sys.path.insert(1,r'C:\Users\Gollinucci\Documents\GitHub\CIVICS')

import REP_CVX

gha15 = REP_CVX.C_SUT(path = r'Database\GHANA_2015_CVX.xlsx', unit = 'M GHS', name='Ghana 2015')
gha13 = REP_CVX.C_SUT(path=r'Database\GHANA_2013_CVX.xlsx', unit= 'M GHS', name='Ghana 2013')

#%% Analysis for 2015

Z_15 = gha15.Z
z_15 = gha15.z
va_15 = gha15.va
VA_15 = gha15.VA
Y_15 = gha15.Y
X_15 = gha15.X

col_sum_15 = z_15.sum() + va_15.sum()
COL_SUM_15 = Z_15.sum() + VA_15.sum()
ROW_SUM_15 = Z_15.sum(axis=1) + Y_15.sum(axis=1)
zero = COL_SUM_15 - ROW_SUM_15

GDP_15 = VA_15.drop(['Rest of world']).groupby(level=1).sum().groupby(axis=1, level=2, sort=False).sum()
GDP_15_tot = GDP_15.sum().sum() / 1000 # Value in B LCU
sGDP_15 = GDP_15.sum() / GDP_15.sum().sum()

#%% Analysis for 2013

Z_13 = gha13.Z
z_13 = gha13.z
va_13 = gha13.va
VA_13 = gha13.VA
Y_13 = gha13.Y
X_13 = gha13.X

col_sum_13 = z_13.sum() + va_13.sum()
COL_SUM_13 = Z_13.sum() + VA_13.sum()
ROW_SUM_13 = Z_13.sum(axis=1) + Y_13.sum(axis=1)
zero = COL_SUM_13 - ROW_SUM_13

GDP_13 = VA_13.drop(['Rest of world']).groupby(level=1).sum().groupby(axis=1, level=2, sort=False).sum()
GDP_13_tot = GDP_13.sum().sum() / 1000 # Value in B LCU
sGDP_13 = GDP_15.sum() / GDP_15.sum().sum()


#%%
dva = (va_15-va_13)/va_15*100
growth = (GDP_15_tot - GDP_13_tot)/GDP_15_tot *100
