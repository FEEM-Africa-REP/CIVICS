import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

h50 = pd.read_excel('50% hybrid - baseline.xlsx',index_col=[0,1,2],header=[0,1])
h100 = pd.read_excel('100% hybrid - baseline.xlsx',index_col=[0,1,2],header=[0,1])
s50 = pd.read_excel('50% solar - baseline.xlsx',index_col=[0,1,2],header=[0,1])
s100 = pd.read_excel('100% solar - baseline.xlsx',index_col=[0,1,2],header=[0,1])

data = h50.append(h100.append(s50.append(s100)))

#%%

indicators = ['Water Saving','Emission Saving','Land Saving','PPBT','Import Saving','Capital Saving','Workforce Saving']
subtitles = ['Water Saving','Emission Saving','Land Saving','Policy Pay Back Time','Savings of Factors of Production']
fig = make_subplots(rows=1, cols=len(subtitles), subplot_titles=subtitles, column_widths=[.2,.2,.2,.2,.6])

indicators_ = data.columns.get_level_values(0).to_list()
units = data.columns.get_level_values(1).to_list()

for indicator in indicators:
    if indicator in ['Import Saving','Capital Saving','Workforce Saving']:
        column=5
    else:
        column=indicators.index(indicator)+1
    fig.add_trace(go.Box(y=data.iloc[:,indicators_.index(indicator)],
                         name = '{} ({})'.format(indicator,units[indicators_.index(indicator)])),
                  row=1, col=column)

fig.update_layout(title='Impact Assessment of Independent  Power Supply for Feed Mills - 4 scenarios based on technology of the stand-alone system and increase in production', 
                  legend_title_text='Indicators',
                  font_family='Palatino Linotype',
                  font_size=20)
fig.write_html('Impact assessment Mills.html')
fig.update_layout(showlegend=False)
fig.write_image('Impact assessment Mills.svg', width=2200, height=1000)
