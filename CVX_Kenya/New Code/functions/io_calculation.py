# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:16:32 2020

@author: Mohammad Amin Tahavori
"""

def cal_z(Z,X):
    import pymrio
    
    return pymrio.calc_A (Z,X)

def cal_s(S,X):
    # can be used for both S and VA
    import pymrio
    
    return pymrio.calc_S (S,X)

def cal_l(z):
    import pymrio
    
    return pymrio.calc_L(z)

def cal_p(va,l):
    import pandas as pd
    
    return pd.DataFrame(va.sum().values.reshape(1,len(va.columns)) @ l.values, index=['Price'], columns=va.columns)

def cal_coef (Z,S,VA,X):
    import pymrio
    import pandas as pd 
    
    z  = pymrio.calc_A (Z,X)
    s  = pymrio.calc_S (S,X)
    va = pymrio.calc_S (VA,X)
    l  = pymrio.calc_L(z)
    p  = pd.DataFrame(va.sum().values.reshape(1,len(va.columns)) @ l.values, index=['Price'], columns=va.columns)
    
    return z,s,va,l,p
    