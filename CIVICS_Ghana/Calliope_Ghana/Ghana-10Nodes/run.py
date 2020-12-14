# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:06:55 2020

@author: payam
"""
import calliope
try:
    calliope.set_log_level('INFO')
except:
    calliope.set_log_verbosity('INFO')
model = calliope.Model('model.yaml')
model.run()
#%%
import cal_graph as CG
variable=CG.C_Graph(model=model,ex_path=r'Graph_inputs.xlsx',unit='kW')
#%%
variable.system_pie(table_font=12)