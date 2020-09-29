# -*- coding: utf-8 -*-
"""
Extra Functions
"""
# The function aims drop the columns that their sum is in a specific
# range for better representation

# inputs: 1. data: dataframe to be processed, ranshow: range to represent
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

# The function aims aggregate the columns that their sum is in a specific
# range for better representation
    
def agg_fun(data,ranshow):
    
    categ = list(data.columns.get_level_values(0))
    categ = list(dict.fromkeys(categ))
    
    my_list = []
    
    for h in categ:
        data_0 = data[h]
        col_list = list(data_0.columns)
        
        for i in range (data_0.shape[1]):
            col_sum=0
            for j in range (data_0.shape[0]):
                col_sum += data_0.iloc[j,i]
            if col_sum <= ranshow[0] and col_sum>= ranshow[1]:
                my_list.append('rest')
            else:
                my_list.append(col_list[i])
    
    new_ind = [list(data.columns.get_level_values(0)),my_list]
    data.columns = new_ind

    data=data.groupby(axis=1,sort=False,level = [0,1]).sum()
    
    return data
    
    
    
    
    
