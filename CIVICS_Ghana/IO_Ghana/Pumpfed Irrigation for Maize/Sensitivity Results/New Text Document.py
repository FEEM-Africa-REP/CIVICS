import plotly.graph_objects as go
import pandas as pd
from plotly.offline import plot 


path = r'C:\Users\payam\Documents\GitHub\CIVICS_Kenya\CIVICS_Ghana\IO_Ghana\Pumpfed Irrigation for Maize\Sensitivity Results\Pumpfed Irrigation for Maize - Increase in maize productivity.xlsx'
data = pd.read_excel(path,index_col=[0,1,2],header=[0,1])

indicators_ = data.columns.get_level_values(0).to_list()
units = data.columns.get_level_values(1).to_list()
indicators = ['Water Saving','Emission Saving','Land Saving','Import Saving']
data_=[]

for indicator in indicators:
    
    data_.append(go.Box(y=data.iloc[:,indicators_.index(indicator)],
                       name = '{} ({})'.format(indicator,units[indicators_.index(indicator)])))


plot(data_,filename='hi', image='svg')
