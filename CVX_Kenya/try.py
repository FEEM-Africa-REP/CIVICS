# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:12:55 2020

@author: Mohammad Amin Tahavori
"""

import REP_CVX


a = REP_CVX.C_SUT(path=r'Database\Kenya_2014_SAM.xlsx',unit='M KSH')
#%%
#a.shock_calc(path=r'Ecopulpers.xlsx',Y=False,Z=True,VA=True,S=True)  
a.shock_calc(path=r'Ecopulpers.xlsx',Y=True,Z=False,VA=False,S=False)  
#%%
a.sensitivity(path=r'Ecopulpers.xlsx')
#%%
a.plot_ds(indicator='Water',kind='Percentage',color=['blue','green','grey'])
#%%
a.impact(saving_sce=['se',1],invest_sce=['sh',1],p_life=10)
#%%
a.plot_dx()
#%%
a.obj_save(file_name='kenya') 
#%%
a.plot_sens
#%% 

a.plot_sens(variable='X',sc_num=1,level='Activities',indicator='Activities')
  #%%
import pandas as pd
#%%
q=pd.read_excel(r'C:\Users\payam\Documents\GitHub\CIVICS_Kenya\CVX_Kenya\New Code\sens_Productivity increase due to 100% new machines (not spoiling the cerry)\case_0.5.xlsx',sheet_name='Z')

#%%
antar=[]
for key, value in a.results['sensitivity_1'].items(): 
    if key != 'information':
        antar.append(a.results['sensitivity_1'][key]['X_agg'].loc['Activities'].values-a.X_agg.loc['Activities'].values)
for i in range(len(antar)):
    antar[i]=antar[i].ravel()
   #%% 
aq=[]
for i in range(len(antar[0])):
    na=[]
    for j in range(len(antar)):
        na.append(antar[j][i])
    aq.append(na)
    #%%
import matplotlib.pyplot as plt 
plt.style.use('ggplot') 
fig = plt.figure(2, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)

# Create the boxplot
bp = ax.boxplot(aq,manage_ticks=True,patch_artist=True)
for i in range(len(a.X_agg.loc['Activities'].index)):
    label = ax.xaxis.get_major_ticks()[i].label
    
    label.set_rotation('vertical')
    
## change outline color, fill color and linewidth of the boxes
for box in bp['boxes']:
    # change outline color
    box.set( color='black', linewidth=1)
    # change fill color
    box.set( facecolor = 'dodgerblue' )

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='black', linewidth=1)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='black', linewidth=1)

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='black', linewidth=1)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', color='#e7298a', alpha=0.5)
    
plt.legend(labels=[my_l],loc='upper center', bbox_to_anchor=(0.5,0),
          fancybox=True, shadow=True,bbox_transform=fig.transFigure,columnspacing=2)
# plt.tight_layout(rect=[1,1,0.0,0])
#plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
plt.title('hi',fontsize=40)
plt.show()    
#%%
my_l = '{}, \n range= {} to {}'.format(a.results['sensitivity_1']['information']['parameter'],a.results['sensitivity_1']['information']['minimum'],a.results['sensitivity_1']['information']['maximum'])
    legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
#%%  
index = ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']    
    
    
    