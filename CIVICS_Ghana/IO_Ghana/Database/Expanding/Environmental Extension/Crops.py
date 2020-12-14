# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 19:07:34 2020

@author: nigolred
"""

import pandas as pd

CVX_sec = list(pd.read_excel('Crop.xlsx', sheet_name='Sheet2'))
Crop = pd.read_excel('Crop.xlsx', index_col=[0])
Crop_prod = Crop.loc['I-RCROP-PRODUCTION',:].set_index('CVX_sec').groupby(level=0).sum()
Crop_area = Crop.loc['I-RCROP-AREA',:].set_index('CVX_sec').groupby(level=0).sum()

Info = pd.DataFrame(0, index=['Crop production [t]','Crop area [ha]'], columns=CVX_sec)

#%%
for s in CVX_sec:
    if s in Crop_area.index:
        Info.loc['Crop production [t]',s] = Crop_prod.loc[s].values
        Info.loc['Crop area [ha]',s] = Crop_area.loc[s].values
