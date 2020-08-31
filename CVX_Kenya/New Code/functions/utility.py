# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:00:29 2020

@author: Mohammad Amin Tahavori
"""
def indeces (S,Z,VA,X):
    
    return {'Z_ind': Z.index , 'VA_ind':VA.index , 'S_ind': S.index , 'X_ind': X.index ,'Z_col': Z.columns , 'VA_col':VA.columns , 'S_col': S.columns , 'X_col':X.columns}

def dict_maker(Z=None,X=None,VA=None,p=None,Y=None,va=None,z=None,s=None,
               Z_agg=None,X_agg=None,VA_agg=None,Y_agg=None,S_agg=None,p_agg=None):
    
    inputs =  [Z,X,VA,p,Y,va,z,s,Z_agg,X_agg,VA_agg,Y_agg,S_agg,p_agg]
    outputs = ['Z','X','VA','p','Y','va','z','s','Z_agg','X_agg','VA_agg','Y_agg','S_agg','p_agg']
    
    dictionary = {}
    
    for i  in range(len(inputs)):
        if inputs[i] is not None:
            dictionary[outputs[i]]=inputs[i]
               
    return dictionary

