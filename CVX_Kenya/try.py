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

a.plot_sens(variable='X',sc_num=1,level='Commodities',indicator='Activities')
  #%%
import pandas as pd
#%%
q=pd.read_excel(r'C:\Users\payam\Documents\GitHub\CIVICS_Kenya\CVX_Kenya\New Code\sens_Productivity increase due to 100% new machines (not spoiling the cerry)\case_0.5.xlsx',sheet_name='Z')

#%%
antar=[]
for key, value in a.results['sensitivity_1'].items(): 
    if key != 'information':
        antar.append(a.results['sensitivity_1'][key]['X_agg'].loc['Activities'].values-a.X_agg.loc['Activities'].values)
#%%
for i in range(len(antar)):
    antar[i]=antar[i].ravel()
#%%
aq=[]
#%%
for i in range(len(antar[0])):
    na=[]
    for j in range(len(antar)):
        na.append(antar[j][i])
    aq.append(na)
    
#%%
antar=[]
for key, value in a.results['sensitivity_1'].items(): 
    if key != 'information':
        antar.append(a.results['sensitivity_1'][key]['X_agg'].loc['Commodities'].values-a.X_agg.loc['Commodities'].values)
for i in range(len(antar)):
    antar[i]=antar[i].ravel()

aq2=[]
for i in range(len(antar[0])):
    na=[]
    for j in range(len(antar)):
        na.append(antar[j][i])
    aq2.append(na)
    #%%
import matplotlib.pyplot as plt 
plt.style.use('ggplot') 
fig = plt.figure(3, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)

# Create the boxplot
bp = ax.boxplot(lst1[2],labels=acts,manage_ticks=True,patch_artist=True)
#bq = ax.boxplot(aq2,manage_ticks=True,patch_artist=True)
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
    
plt.legend(labels=['Activities'],loc='center left', bbox_to_anchor=(.93, 0.5),
          fancybox=True, shadow=True,bbox_transform=fig.transFigure,columnspacing=2)
# plt.tight_layout(rect=[1,1,0.0,0])
#plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
plt.title('hi',fontsize=40)
props = dict(boxstyle='square', facecolor='wheat', alpha=1)

# place a text box in upper left in axes coords
ax.text(1.05, .9, my_l, transform=ax.transAxes, fontsize=14,
        verticalalignment='center', bbox=props)
plt.show()    
#%%
my_l = '{}, \n range= {} to {}'.format(a.results['sensitivity_1']['information']['parameter'],a.results['sensitivity_1']['information']['minimum'],a.results['sensitivity_1']['information']['maximum'])
#legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          #fancybox=True, shadow=True, ncol=5)
#%%  
level='Activities'
s_range = len(a.results['sensitivity_1'])-1
s_list=[]
col_len=len(a.results['sensitivity_1']['0']['VA_agg'][level].T)
acts=a.results['sensitivity_1']['0']['VA_agg'][level].T.index.to_list()

fst_col=[]
snd_col=[]

for key, value in a.results['sensitivity_1'].items(): 
    if key != 'information':
        s_list.append(key)
for i in range(col_len):        
    for j in range(s_range):
    
        fst_col.append(s_list[j])
        snd_col.append(acts[i])
    
to_be_filled = pd.DataFrame(columns=[snd_col,fst_col],index=a.results['sensitivity_1']['0']['VA_agg'][level].index)

for i in range(len(acts)):
    for j in range(len(s_list)):
        to_be_filled[(acts[i],s_list[j])] = a.results['sensitivity_1'][s_list[j]]['VA_agg'][level][acts[j]].values - a.results['baseline']['VA_agg'][level][acts[j]].values
        
to_be_filled=to_be_filled.drop('unused')
#%%
lst1=[None]*len(to_be_filled)
for i in range(len(lst1)):
    lst_hlp=[]
    for j in range(len(acts)):
        lst_hlp.append(to_be_filled.loc[to_be_filled.index.to_list()[i],acts[j]].values.tolist())
        
    lst1[i]=lst_hlp
#%%
# --- Your data, e.g. results per algorithm:
data1 = [5,5,4,3,3,5]
data2 = [6,6,4,6,8,5]
data3 = [7,8,4,5,8,2]
data4 = [6,9,3,6,8,4]

# --- Combining your data:
data_group1 = lst1[0]
data_group2 = lst1[1]

# --- Labels for your data:
labels_list = acts
xlocations  = range(len(data_group1))
width       = 0.3
symbol      = 'r+'


ax = plt.gca()

ax.set_xticklabels( labels_list, rotation=0 )
ax.grid(True, linestyle='dotted')
ax.set_axisbelow(True)
ax.set_xticks(xlocations)
plt.xlabel('X axis label')
plt.ylabel('Y axis label')
plt.title('title')

# --- Offset the positions per group:
positions_group1 = [x-(width+0.01) for x in xlocations]
positions_group2 = xlocations

plt.boxplot(data_group1, 
            sym=symbol,
            labels=['']*len(labels_list),
            positions=positions_group1, 
            widths=width, 
#           notch=False,  
#           vert=True, 
#           whis=1.5,
#           bootstrap=None, 
#           usermedians=None, 
#           conf_intervals=None,
#           patch_artist=False,
            )

plt.boxplot(data_group2, 
            labels=labels_list,
            sym=symbol,
            positions=positions_group2, 
            widths=width, 
#           notch=False,  
#           vert=True, 
#           whis=1.5,
#           bootstrap=None, 
#           usermedians=None, 
#           conf_intervals=None,
#           patch_artist=False,
            )

        
plt.show()