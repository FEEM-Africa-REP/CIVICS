# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 10:19:55 2020

@author: nigolred
"""

import REP_CVX

ghana = REP_CVX.C_SUT(path = r'Database\GHANA_2015_CVX.xlsx', unit = 'M KSH', name='Ghana')

#%%
In_sec = ['Maize','Poultry','Grain milling','Electricity, gas and steam']

Z = ghana.Z
VA =ghana.VA

Use = Z.loc['Commodities',('Activities',In_sec)].append(VA.loc[:,('Activities',In_sec)]).groupby(level=1, sort=False).sum()
Use = Use.loc[(Use.sum(axis=1)) !=0]
Supply = Z.loc['Activities',('Commodities',In_sec)].append(VA.loc[:,('Commodities',In_sec)]).groupby(level=1, sort=False).sum()
Supply = Supply.loc[(Supply.sum(axis=1) !=0)]

from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=1, cols=1)

for u in Use.index:
    fig.add_trace(go.Bar(name=u, x=In_sec, y=Use.loc[u,:], showlegend=True, legendgroup=u), row=1, col=1)

fig.update_layout(barmode='relative', title='How to make these commodities')
fig.write_html('Use.html')
#%%

fig = make_subplots(rows=1, cols=1)
for s in Supply.index:
    fig.add_trace(go.Bar(name=s, x=In_sec, y=Supply.loc[s,:], showlegend=True, legendgroup=s), row=1, col=1)

fig.update_layout(barmode='relative', title='Who is providing these commodities')
fig.write_html('Supply.html')

