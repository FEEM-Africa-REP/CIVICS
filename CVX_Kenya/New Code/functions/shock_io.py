# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:52:35 2020

@author: Mohammad Amin Tahavori
"""
def Y_shock (path,Y):
    
    import pandas as pd 
    
    Y_sh = pd.read_excel(path, sheet_name = 'Y', index_col = [0] , header = [0])
    
    rows   = list(Y_sh['row'].values)
    values = list(Y_sh['value'].values)
    
    Y.loc[('Commodities',rows),'Total final demand'] = Y.loc[('Commodities',rows),'Total final demand'].values + values
          
    return Y
            
def Z_shock (path,z):
    
    import pandas as pd
    
    Z_sh = pd.read_excel(path, sheet_name = 'Z', index_col = [0] , header = [0])
    
    rows        = list(Z_sh['row'].values)
    level_rows  = list(Z_sh['level_row'].values)
    cols        = list(Z_sh['col'].values)
    level_cols  = list(Z_sh['level_col'].values)
    types       = list(Z_sh['types'].values)
    values      = list(Z_sh['values'].values)
    aggreg      = list(Z_sh['aggregated'].values)
    
    for i in range (len(rows)):
        if types[i] == 'Percentage':
            if aggreg[i] == 'No':
                z.loc[(level_rows[i],rows[i]),level_cols[i],cols[i]] = \
                    z.loc[(level_rows[i],rows[i]),level_cols[i],cols[i]].values * (1+values[i])
            elif aggreg[i] == 'Yes':
                z.loc[(level_rows[i],slice(None),slice(None),slice(None),rows[i]),level_cols[i],cols[i]] = \
                    z.loc[(level_rows[i],slice(None),slice(None),slice(None),rows[i]),level_cols[i],cols[i]].values * (1+values[i])      
            else: 
                raise ValueError('Aggregation could be /Yes/ or /No/. Please check shock excel file.')






