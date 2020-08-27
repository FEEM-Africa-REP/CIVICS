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


def delta_xv(X_c,X,style,unit,m_unit,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,info,drop):
    
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
    
    
    #reshaping X matrix for better representation and Taking the level
    if info == 'X':
        X_c = x_reshape(X_c)
        X   = x_reshape(X)
        X_c = X_c.loc[level,level]
        X   = X.loc[level,level]
    elif info == 'VA':
        X_c = X_c[level]
        X   = X[level]
        
    # defining the d_x matrix 
    if kind == 'Absolute': d_x = (X_c - X) * conversion
    else: d_x ,unit = (X_c - X)/X * 100 ,'%'
        
    # Check the title
    if info == 'X':
        if title == 'default': title = 'Production Change{}'.format(tit)
        else: title = title
        
    elif info == 'VA':
        if title == 'default': title = 'Value Added Change{}'.format(tit)
        else: title = title
        
    # Reindexing to avoid showing multiple indeces: only the second level
    if info == 'X': d_x.index = X.index.get_level_values(1)
    elif info == 'VA': 
        if len(level) == 2: d_x.index , d_x.columns =  X.index.get_level_values(0) , [d_x.columns.get_level_values(0),d_x.columns.get_level_values(1)]
        else: d_x.index , d_x.columns =  X.index.get_level_values(0) , d_x.columns.get_level_values(1)
    
    # Droping some of the categories based on the user input
    if drop:
        d_x = d_x.drop(drop)

        
    # defining the range of the valuse to be shown 
    if info     == 'X' : d_x = drop_fun(data=d_x.T, ranshow=ranshow)
    elif info   == 'VA': d_x = drop_fun(data=d_x  , ranshow=ranshow)
    
    d_x = d_x.T
    
    # Removing the name of the indeces for better representation
    d_x.index.name   = None
    d_x.columns.name = None
    
    # Plotting
    if info == 'X':
        if len(level) == 2:
            # Depending on the input of the color, the code will be different
            try:    d_x.plot(kind='bar',figsize=figsize,stacked=True,colormap=color) # colormap if a color map is given
            except: d_x.plot(kind='bar',figsize=figsize,stacked=True,color=color) # color if a color list is given
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fancybox=True, shadow=True)
        else:
            try:    d_x.plot(kind='bar',figsize=figsize,legend=None,stacked=True,colormap=color)
            except: d_x.plot(kind='bar',figsize=figsize,legend=None,stacked=True,color=color)
            
    if info == 'VA':
        try:    d_x.plot(kind='bar',figsize=figsize,stacked=True,colormap=color)
        except: d_x.plot(kind='bar',figsize=figsize,stacked=True,color=color)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fancybox=True, shadow=True)      
        
    # Due to competutional errors, even in the case that one thing is not changed, we may have very small differences 
    # This makes the graphs ugly!! To solve the issue we print an error for the user to make them understand.
    
    if abs(d_x.sum().sum() <= 0.000001):
        print('The following matrix seems to be unchanged in the implemented shock, Maybe the numbers represented in the graph are very small and related to computational errors.')
        
    
        
    plt.title(title,fontsize=title_font)
    plt.ylabel(unit)
    plt.savefig('{}\{}.{}'.format(directory,title,fig_format),bbox_inches='tight',dpi=150)
    plt.show()

 
def delta_s(X_c,X,style,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,indicator,detail,indeces):
    
    import matplotlib.pyplot as plt
    from functions.check import style_check
    from functions.check import level_check
    from functions.check import kind_check
    from functions.check import indic_check

    # As some processes are needed to be done on the inputs, to keep the main variable unchanged, we will make a copy of them  
    X_c = X_c.copy()
    X   = X.copy() 
    
    # Checking the styles
    style       = style_check(style)
    tit,level   = level_check(level)
    kind        = kind_check (kind)
    indicator   = indic_check (indicator,list(indeces['S_ind'].get_level_values(3)))
    
    # Implementing the plot style
    plt.style.use(style)   
    
    if detail:
        X_c = X_c.loc[(slice(None),slice(None),slice(None),indicator),level].groupby(axis=1,level=4).sum().groupby(axis=0,level=0).sum()
        X   = X.loc[(slice(None),slice(None),slice(None),indicator),level].groupby(axis=1,level=4).sum().groupby(axis=0,level=0).sum()
    else:
        X_c = X_c.loc[indicator,level].groupby(axis=1,level=3).sum()
        X   = X.loc[indicator,level].groupby(axis=1,level=3).sum() 
        
    # defining the d_x matrix 
    if kind == 'Absolute': 
        d_x,unit = (X_c - X),''
        print('The unit of the graph is the same of the database.')  
    else: d_x,unit = (X_c - X)/X * 100,'%'
    
    # if detail is True, we need to reindex it
    if detail:
        d_x.index = d_x.index.get_level_values(0) 
        
    if abs(d_x.sum().sum() <= 0.000001):
        print('The following matrix seems to be unchanged in the implemented shock, Maybe the numbers represented in the graph are very small and related to computational errors.')
       
    # Specifing the range of showing results
    d_x = drop_fun(data=d_x, ranshow=ranshow)
    d_x = d_x.T

    # Removing the name of the indeces for better representation
    d_x.index.name   = None
    d_x.columns.name = None

    # Title Definition
    if title == 'default': title = '{} Change{}'.format(indicator, tit)
    else: title = title
        
    if detail:
        try:    d_x.plot(kind = 'bar' , stacked = True,colormap=color)
        except: d_x.plot(kind = 'bar' , stacked = True,color=color)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fancybox=True, shadow=True)
    else:
        try:    d_x.plot(kind = 'bar' , stacked = True,legend=False,colormap=color)
        except: d_x.plot(kind = 'bar' , stacked = True,legend=False,color=color)
    
    plt.title(title)  
    plt.ylabel(unit)

       
    plt.savefig('{}\{}.{}'.format(directory,title,fig_format),bbox_inches='tight',dpi=150)
    plt.show()    
    

    
    
    
    
    
    
    
    
    
    