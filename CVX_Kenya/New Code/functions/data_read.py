# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 11:28:05 2020

@author: Mohammad Amin Tahavori
"""
def database(path):
    import pandas as pd
    
    SUT = pd.read_excel(path, index_col=[0,1,2,3,4], header = [0,1,2,3,4])
    
        # importing use (U), supply (V), supply-use together (Z) and satellite accounts (S)
    U = SUT.loc['Commodities','Activities']
    V = SUT.loc['Activities','Commodities']
    Z = SUT.loc[['Commodities','Activities'], ['Commodities','Activities']]
    S = SUT.loc['Satellite Accounts',['Commodities','Activities']]
        
        
        # computing total final demand (Y) by importing households (HH), investment (IN), government (GO) and export (EX) 
    HH  = SUT.loc[['Commodities','Activities'], 'Households']
    IN  = SUT.loc[['Commodities','Activities'], 'Savings-Investment']
    GO  = SUT.loc[['Commodities','Activities'], 'Government']
    EX  = SUT.loc[['Commodities','Activities'], 'Rest of the World']
    Y_M = SUT.loc[['Commodities','Activities'], 'Margins']
        
    Y = pd.DataFrame(HH.sum(axis=1) + IN.sum(axis=1) + GO.sum(axis=1) + EX.sum(axis=1) + Y_M.sum(axis=1), index=HH.index, columns=['Total final demand'])
        
        # computing total value added (VA) by importing factors of production (F), taxes (T), import (IM) and margins as factor (F_M)
    F   = SUT.loc['Factors', ['Commodities', 'Activities']]
    T   = SUT.loc['Government', ['Commodities','Activities']]
    IM  = SUT.loc['Rest of the World', ['Commodities','Activities']]
    F_M = SUT.loc['Margins', ['Commodities','Activities']]
        
    VA  = F.append(T.append(IM.append(F_M)))
        
        # computing total production vector (X)
    X = pd.DataFrame(Y.sum(axis=1) + Z.sum(axis=1), index=Z.index, columns=['Total Production'])
        
    return SUT,U,V,Z,S,Y,VA,X


        