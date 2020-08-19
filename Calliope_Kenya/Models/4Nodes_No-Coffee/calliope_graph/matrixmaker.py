# -*- coding: utf-8 -*-
"""
Matrix Maker Functions

Functions are used to read the information from the excel files, making the matrices which are complicated.
"""

def input_read (path):

    
    """
    input_read function:
    A function to read the information from the excel input file
    
    """

    import pandas as pd
    
    # Reading the excel
    
    Cons_Techs  = pd.read_excel(path,sheet_name = 'Consumption Techs',index_col=[0],header=[0])
    Nodes       = pd.read_excel(path,sheet_name = 'Nodes',index_col=[0],header=[0])
    Pr_Techs    = pd.read_excel(path,sheet_name = 'Production Techs',index_col = [0],header=[0])
    colname     = pd.read_excel(path,sheet_name = 'Col_Name',index_col = [0],header =[0])
    Trans       = pd.read_excel(path,sheet_name = 'Transmission',index_col = [0],header =[0])
    date        = pd.read_excel(path,sheet_name = 'Date',index_col = [0],header =[0])

    co_techs    = Cons_Techs['Tech'].to_list()
    carr        = Cons_Techs['Carrier'].to_list()
    nodes       = Nodes['Location'].to_list()
    pr_techs    = Pr_Techs['Tech'].to_list()
    colors      = colname['Color']
    names       = colname['Name']
    tr_tech     = Trans['Tech'].to_list()
    start       = date['Value'][0]
    end         = date['Value'][1]
    
    # making renewable indicator
    RES_ind = []
    for i in range(len(pr_techs)):
        if Pr_Techs['RES'][i] == 1:
            RES_ind.append('Renewable')
        else:
            RES_ind.append('Conventional')
    
    RES_ind = RES_ind * len(nodes)
    
    
    return co_techs,carr,nodes,pr_techs,colors,names,tr_tech,start,end,RES_ind

def prod_matrix (model,pr_techs,nodes,carr):

    
    """
    input_read function:
    A function to read the information from the excel input file
    
    """
    import pandas as pd
    
    prod = model.get_formatted_array('carrier_prod').loc[{'techs':pr_techs,'carriers':carr,'locs':[nodes[0]]}].sum('locs').sum('carriers').to_pandas().T
    prod = pd.concat([prod],keys=[nodes[0]],axis=1)
    
    for i in  range (1,len(nodes)):
        prod0 = model.get_formatted_array('carrier_prod').loc[{'techs':pr_techs,'carriers':carr,'locs':[nodes[i]]}].sum('locs').sum('carriers').to_pandas().T
        prod0 = pd.concat([prod0],keys=[nodes[i]],axis=1)
        prod = pd.concat([prod,prod0],axis=1)
        
    return prod

def imp_exp (model,nodes,prod,tr_tech,carr):
    
    """
    input_read function:
    A function to read the information from the excel input file
    """        
    
    import pandas as pd 
    
    node = nodes[0]
    r_nodes = nodes.copy()
    r_nodes.remove(node)    
        
    exp = r_nodes.copy()
    imp = r_nodes.copy()    
    
    node_index = []
        
    for j in range(len(r_nodes)):
            
        node_index.append(nodes[0]) 
        node_index.append(nodes[0]) 
            
        exp[j] = exp[j] + '_exp'
        imp[j] = imp[j] + '_imp'
    
    exports = pd.DataFrame(index=prod.index,columns=exp)
    imports = pd.DataFrame(index=prod.index,columns=imp)    
    
    tran_get = []
    
    for i in r_nodes:
        tr = []
        for j in tr_tech:
            tr.append(j + ':' + i)
        tran_get.append(tr)    
    
    for i in range(len(exp)):
        
        exports[exp[i]] = model.get_formatted_array('carrier_con').loc[{'techs':tran_get[i],'carriers':carr,'locs':[node]}].sum('locs').sum('techs').to_pandas().T
        imports[imp[i]] = model.get_formatted_array('carrier_prod').loc[{'techs':tran_get[i],'carriers':carr,'locs':[node]}].sum('locs').sum('techs').to_pandas().T
        
    imports = pd.concat([imports],keys=[node],axis=1)
    exports = pd.concat([exports],keys=[node],axis=1)        
    
    for i in range(1,len(nodes)):
        node = nodes[i]
        r_nodes = nodes.copy()
        r_nodes.remove(node)    
    
        exp = r_nodes.copy()
        imp = r_nodes.copy()
        
        node_index = []
        
        for j in range(len(r_nodes)):
            
            node_index.append(nodes[i]) 
            node_index.append(nodes[i]) 
            
            exp[j] = exp[j] + '_exp'
            imp[j] = imp[j] + '_imp'   
            
        exports0 = pd.DataFrame(0,index=prod.index,columns=exp)
        imports0 = pd.DataFrame(0,index=prod.index,columns=imp)    
    
        tran_get = []
    
        for h in r_nodes:
            tr = []
            for p in tr_tech:
                tr.append(p + ':' + h)
            tran_get.append(tr)
    
        for n in range(len(exp)):
            exports0[exp[n]] = model.get_formatted_array('carrier_con').loc[{'techs':tran_get[n],'carriers':carr,'locs':[node]}].sum('locs').sum('techs').to_pandas().T
            imports0[imp[n]] = model.get_formatted_array('carrier_prod').loc[{'techs':tran_get[n],'carriers':carr,'locs':[node]}].sum('locs').sum('techs').to_pandas().T
    
        imports0 = pd.concat([imports0],keys=[node],axis=1)
        exports0 = pd.concat([exports0],keys=[node],axis=1)
        
        imports = pd.concat([imports,imports0],axis=1)
        exports = pd.concat([exports,exports0],axis=1)    
    
    return imports,exports


def dem_matrix (model,co_techs,carr,nodes):
    
    return -model.get_formatted_array('carrier_con').loc[{'techs':co_techs,'carriers':carr,'locs':nodes}].sum('techs').sum('carriers').to_pandas().T

def prod_imp_exp (production,imports,exports,node):
    
    import pandas as pd
    
    in_node  = pd.concat([production[node],imports[node]],axis=1)
    out_node = exports[node]
    
    return in_node,out_node

def system_matrix(production,demand,exports=None,imports=None): # Then the exports and imports of the external nodes should be inserted to take the external points
    
    import pandas as pd
    
    tech_production = production.groupby(level=1,axis=1,sort=False).sum()
    reg_production  = production.groupby(level=0,axis=1,sort=False).sum()
    
    demand = pd.DataFrame(demand.sum(axis=1),index=demand.index,columns=['Demand'])
    
    
    return demand,tech_production,reg_production
    
    
    
    
    
    
    
    
    