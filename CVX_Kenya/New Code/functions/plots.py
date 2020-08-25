# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:36:58 2020

@author: Mohammad Amin Tahavori
"""
def x_reshape(X):
    
    import pandas as pd
    X_r = pd.DataFrame(columns = ['Activities','Commodities'],index=X.index)
    X_r = X_r.fillna(0)
    
    X_r.loc['Activities','Activities']   = X.loc['Activities','Total Production'].values
    X_r.loc['Commodities','Commodities'] = X.loc['Commodities','Total Production'].values
    

    
    return X_r

def drop_fun(data,ranshow):

    col_list = list(data.columns)
    
    drop_list=[]
    
    for i in range (data.shape[1]):
        col_sum = 0
        for j in range (data.shape[0]):
            col_sum += data.iloc[j,i]
            
        if col_sum <= ranshow[0] and col_sum>= ranshow[1]:
            drop_list.append(col_list[i])
            
    return data.drop(columns=drop_list)


def dx(X_c,X,style,unit,m_unit,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color):
    
    import matplotlib.pyplot as plt
    from functions.check import unit_check
    from functions.check import unit_converter
    from functions.check import style_check
    from functions.check import level_check
    from functions.check import kind_check
    

    # As some processes are needed to be done on the inputs, to keep the main variable unchanged, we will make a copy of them  
    X_c = X_c.copy()
    X   = X.copy() 
    
    # default unit
    if unit == 'default':
        unit = m_unit
    
    # Checking the units and styles
    unit        = unit_check(unit)
    style       = style_check(style)
    conversion  = unit_converter(m_unit,unit)
    tit,level   = level_check(level)
    kind        = kind_check (kind)
    
    # Implementing the plot style
    plt.style.use(style)
    
    #reshaping X matrix for better representation
    X_c = x_reshape(X_c)
    X   = x_reshape(X)
    
    # Taking the level
    X_c = X_c.loc[level,level]
    X   = X.loc[level,level]
    
    # defining the d_x matrix 
    if kind == 'Absolute': 
        d_x = (X_c - X) * conversion
    else:
        d_x = (X_c - X)/X * 100
        unit = '%'
        
    # Check the title
    if title == 'default': title = 'Production Change{}'.format(tit)
    else: title = title

    # Reindexing to avoid showing multiple indeces: only the second level
    d_x.index = X.index.get_level_values(1)
    
    # defining the range of the valuse to be shown   
    d_x = drop_fun(data=d_x.T, ranshow=ranshow)
    d_x = d_x.T
    
    # Plotting
    # if the two level exist, the legend is needed. Otherwise, legend is not necessary
    if len(level) == 2:
        d_x.plot(kind='bar',figsize=figsize,stacked=True,colormap=color) 
        plt.legend(loc = 1,bbox_to_anchor = (1.3,1))
    else:
        d_x.plot(kind='bar',figsize=figsize,legend=None,stacked=True)
        
    plt.title(title,fontsize=title_font)
    plt.ylabel(unit)
    plt.show()
    
    plt.savefig('{}\{}.{}'.format(directory,title,fig_format),bbox_inches='tight',dpi=150)

    
    
    
    
    