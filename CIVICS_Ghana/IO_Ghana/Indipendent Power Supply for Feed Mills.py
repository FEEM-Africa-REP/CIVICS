# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 09:24:15 2020

@author: nigolred
"""

import sys
sys.path.insert(1,r'C:\Users\Gollinucci\Documents\GitHub\CIVICS')

import REP_CVX

Case = 'Indipendent Power Supply for Feed Mills'
Scenarios = ['50% hybrid','100% hybrid', '50% solar','100% solar']
Delta = {}

for Scenario in Scenarios:

    Ghana = REP_CVX.C_SUT(path = r'C:\Users\Gollinucci\Documents\GitHub\CIVICS\CIVICS_Ghana\IO_Ghana\Database\GHANA_2015_CVX.xlsx', unit = 'M GHS', name=Case)
    #%%
    
    Ghana.shock_calc(path=r'Indipendent Power Supply for Feed Mills/'+Scenario+'.xlsx', Y=True)
    # Ghana.plot_dx()
    # Ghana.plot_dv(level='Activities', title='Required Value Added for producing the mini-grid for the mills in the Scenario '+Scenario)
    # Ghana.plot_dv(level='Commodities', title='Required Commodities for producing the mini-grid for the mills in the Scenario '+Scenario)
    
    #%% 
    Ghana.shock_calc(path=r'Indipendent Power Supply for Feed Mills/'+Scenario+'.xlsx', Z=True, VA=True, S=True)
    
    # Ghana.plot_dv(level='Activities', title='Saved Value Added using the mini-grid for grain milling in the Scenario '+Scenario)
    # Ghana.plot_dv(level='Commodities', title='Saved imports for using the mini-grid for grain milling in the Scenario '+Scenario)
    # Ghana.plot_ds(indicator='Water', color=['Blue','Green','Grey'])
    # Ghana.plot_ds(indicator='GHG')
    # Ghana.plot_ds(indicator='CO2', detail=False)
    # Ghana.plot_ds(indicator='Land')
    # Ghana.plot_ds(indicator='CH4', detail=True)
    # Ghana.plot_ds(indicator='N2O', detail=False)
    
    
    Res = Ghana.results
    
    
    #%%
    # Ghana.sensitivity(r'Indipendent Power Supply for Feed Mills/'+Scenario+'.xlsx')
    # Ghana.plot_sens('S', sc_num=2, indicator='Water')
    #%%
    '''
    Ghana.impact_assess(p_life=10, saving_sce=['sh', 2], invest_sce=['sh',1],imports=['Import'],
                        w_ext=['Water'], em_ext=['CO2'], land=['Land'], 
                        labour=['Labor'],
                        capital=['Capital'], save_excel=True)
    # #%%
    # Ghana.impact_assess(p_life=10, saving_sce=['sh', 2], invest_sce=['se',2],imports=['Import'],
    #                     w_ext=['Water'], em_ext=['GHG'], land=['Land'], 
    #                     labour=['Labor'],
    #                     capital=['Capital'], save_excel=True)
    '''
    Delta[Scenario] = Res['shock_2']['S_agg']-Res['baseline']['S_agg']
    Delta[Scenario] = Delta[Scenario]['Activities'].drop('unused')
#%% Plot


from plotly.subplots import make_subplots
import plotly.graph_objects as go

subtitles = ['+50% increase in local production of grain & hybrid system','+100% increase in local production of grain & hybrid system', '+50% increase in local production of grain & solar system', '+100% increase in local production of grain & solar system']
fig = make_subplots(rows=1, cols=len(Scenarios), subplot_titles=subtitles, shared_yaxes=True)
colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
sectors = list(Delta[Scenarios[0]].columns)
indicators = list(Delta[Scenarios[0]].index)
ind_unit = ['{} [{}]'.format(i,j) for i,j in indicators]

for c in Scenarios:
    for s in sectors:
        if Scenarios.index(c)==0:
            sl = True
        else:
            sl = False
        fig.add_trace(go.Bar(x=ind_unit,
                             y=Delta[c][s].values,
                             name=s,
                             legendgroup=s,
                             marker_color=colors[sectors.index(s)],
                             showlegend=sl), row=1, col=Scenarios.index(c)+1)
    fig.add_trace(go.Scatter(x=ind_unit,
                             y=Delta[c].sum(axis=1),
                             name='Overall',
                             legendgroup='Total',
                             marker_color='black',
                             mode='markers',
                             showlegend=sl), row=1, col=Scenarios.index(c)+1)

fig.update_layout(title='Use of Resources by Scenario with respect to the baseline with the dedicated stand-alone system', barmode='relative', 
                  legend_title_text='Sectors',
                  font_family='Palatino Linotype',
                  font_size=20)
fig.write_html('Resource Use.html')
fig.write_image('Resource Use.svg', width=2200, height=1000)

