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
    
    Y.loc[('Commodities',rows),'Total final demand'] = \
        Y.loc[('Commodities',rows),'Total final demand'].values + values
          
    return Y
            
def Z_shock (path,z,Z,X):
    
    import pandas as pd
    from functions.io_calculation import cal_z
    
    Z_sh = pd.read_excel(path, sheet_name = 'Z', index_col = [0] , header = [0])
    
    rows        = list(Z_sh['row'].values)
    level_rows  = list(Z_sh['level_row'].values)
    cols        = list(Z_sh['col'].values)
    level_cols  = list(Z_sh['level_col'].values)
    types       = list(Z_sh['type'].values)
    values      = list(Z_sh['value'].values)
    aggreg      = list(Z_sh['aggregated'].values)
    
    for i in range (len(rows)):
        if types[i] == 'Percentage':
            if aggreg[i] == 'No':
                z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])] = \
                    z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])].values * (1+values[i])
            elif aggreg[i] == 'Yes':
                z.loc[(level_rows[i],slice(None),slice(None),slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    z.loc[(level_rows[i],slice(None),slice(None),slice(None),rows[i]),(level_cols[i],cols[i])].values * (1+values[i])      
            else: 
                raise ValueError('Aggregation could be /Yes/ or /No/. Please check shock excel file.')
                
        elif types[i] == 'Absolute':
            if aggreg[i] == 'No':
                
                Z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])] = \
                    Z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])].values + values[i]
                
                new_z = cal_z(Z,X)
                
                z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])] = \
                    new_z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])].values 
                
            elif aggreg[i] == 'Yes':
                Z.loc[(level_rows[i],slice(None),slice(None),slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    Z.loc[(level_rows[i],slice(None),slice(None),slice(None),rows[i]),level_cols[i],cols[i]].values + values[i]
                
                new_z = cal_z(Z,X)
                
                z.loc[(level_rows[i],slice(None),slice(None),slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    new_z.loc[(level_rows[i],slice(None),slice(None),slice(None),rows[i]),level_cols[i],cols[i]].values    
            else: 
                raise ValueError('Aggregation could be /Yes/ or /No/. Please check shock excel file.')  
                
        else:
            raise ValueError('Type of the shock can be /Absolute/ or /Percentage/. Please check shock excel file.')

    return z

def VA_shock(path,va,VA,X):
    
    import pandas as pd
    from functions.io_calculation import cal_s
    
    VA_sh = pd.read_excel(path, sheet_name = 'VA', index_col = [0] , header = [0])    

    rows        = list(VA_sh['row'].values)
    cols        = list(VA_sh['col'].values)
    level_cols  = list(VA_sh['level_col'].values)
    types       = list(VA_sh['type'].values)
    values      = list(VA_sh['value'].values)
    aggreg      = list(VA_sh['aggregated'].values)

    for i in range (len(rows)):
        if types[i] == 'Percentage':
            if aggreg[i] == 'No':
                va.loc[rows[i],(level_cols[i],cols[i])] = \
                    va.loc[rows[i],(level_cols[i],cols[i])].values * (1+values[i])
            elif aggreg[i] == 'Yes':
                va.loc[(slice(None),slice(None),slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    va.loc[(slice(None),slice(None),slice(None),rows[i]),(level_cols[i],cols[i])].values * (1+values[i])      
            else: 
                raise ValueError('Aggregation could be /Yes/ or /No/. Please check shock excel file.')
                
        elif types[i] == 'Absolute':
            if aggreg[i] == 'No':
                
                VA.loc[rows[i],(level_cols[i],cols[i])] = \
                    VA.loc[rows[i],(level_cols[i],cols[i])].values + values[i]
                
                new_va = cal_s(VA,X)
                
                va.loc[rows[i],(level_cols[i],cols[i])] = \
                    new_va.loc[rows[i],(level_cols[i],cols[i])].values
                
            elif aggreg[i] == 'Yes':
                VA.loc[(slice(None),slice(None),slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    VA.loc[(slice(None),slice(None),slice(None),rows[i]),level_cols[i],cols[i]].values + values[i]
                
                new_va = cal_s(VA,X)
                
                va.loc[(slice(None),slice(None),slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    new_va.loc[(slice(None),slice(None),slice(None),rows[i]),level_cols[i],cols[i]].values     
            else: 
                raise ValueError('Aggregation could be /Yes/ or /No/. Please check shock excel file.')  
                
        else:
            raise ValueError('Type of the shock can be /Absolute/ or /Percentage/. Please check shock excel file.')

    return va

def S_shock(path,s,S,X):
    
    import pandas as pd
    from functions.io_calculation import cal_s
    
    S_sh = pd.read_excel(path, sheet_name = 'S', index_col = [0] , header = [0])
    
    rows        = list(S_sh['row'].values)
    cols        = list(S_sh['col'].values)
    types       = list(S_sh['type'].values)
    values      = list(S_sh['value'].values)
    level_cols  = 'Activities'
    
    
    for i in range (len(rows)):
        if types[i] == 'Percentage':
            s.loc[rows[i],(level_cols,cols[i])] = \
                    s.loc[rows[i],(level_cols,cols[i])].values * (1+values[i])
            
        elif types[i] == 'Absolute':
            S.loc[rows[i],(level_cols,cols[i])] = \
                    S.loc[rows[i],(level_cols,cols[i])].values + values[i]
            new_s = cal_s(S,X)
            
            s.loc[rows[i],(level_cols,cols[i])] = \
                new_s.loc[rows[i],(level_cols,cols[i])] .values
            
    return s
































