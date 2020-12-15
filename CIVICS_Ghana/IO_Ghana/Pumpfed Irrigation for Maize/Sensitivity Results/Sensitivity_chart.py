import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


sen1 = pd.read_excel(r'Pumpfed Irrigation for Maize - Increase in electricity consumption (physical).xlsx',index_col=[0,1,2],header=[0,1])
sen3 = pd.read_excel(r'Pumpfed Irrigation for Maize - Increase in maize productivity.xlsx',index_col=[0,1,2],header=[0,1])
sen4 = pd.read_excel(r'Pumpfed Irrigation for Maize - Increase in blue water consumption.xlsx',index_col=[0,1,2],header=[0,1])

data = sen1.append((sen3.append(sen4)))

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

fig.update_layout(title='Impact Assessment of Pump-fed Irrigation for Maize - Sensitivity on new maize productivity, electricity and blue water consumption',
                  legend_title_text='Indicators',
                  font_family='Palatino Linotype',
                  font_size=20)
fig.write_html('Impact assessment Pumps.html')
fig.update_layout(showlegend=False)
fig.write_image('Impact assessment Pumps.svg', width=2200, height=1000)
