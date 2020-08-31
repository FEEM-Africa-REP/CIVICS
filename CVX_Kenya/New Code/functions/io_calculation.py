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

    
    z  = pymrio.calc_A (Z,X)
    s  = pymrio.calc_S (S,X)
    va = pymrio.calc_S (VA,X)
    l  = pymrio.calc_L(z)
    p  = cal_p(va,l)
    
    return z,s,va,l,p

def cal_Z (z,X):
    import pymrio 
    
    return pymrio.calc_Z(z, X)
    
def cal_X(l,Y,index):
    import pandas as pd
    
    return pd.DataFrame(l.values @ Y.values , index = index['X_ind'] , columns =  index['X_col'])
    
def  cal_X_from_L(L, y):  
    import pymrio
    
    return pymrio.calc_x_from_L(L, y)
    
def cal_flows(z,Y,va,s,index):
    import pymrio
    
    l  = pymrio.calc_L(z)
    X  = cal_X(l,Y,index)
    VA = pymrio.calc_F(va, X)
    S  = pymrio.calc_F(s, X)
    Z  = pymrio.calc_Z(z, X)
    p  = cal_p(va,l)
    
    return l,X,VA,S,Z,p
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    