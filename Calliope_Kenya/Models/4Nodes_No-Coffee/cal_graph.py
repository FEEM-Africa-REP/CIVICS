# -*- coding: utf-8 -*-

"""
Created on Mon Aug 17 10:25:37 2020

@author: Amin
"""

class C_Graph:    
    
    def __init__(self,model,ex_path,unit):
        
        from calliope_graph.version import __version__
        
        from calliope_graph.matrixmaker import input_read
        from calliope_graph.matrixmaker import prod_matrix
        from calliope_graph.matrixmaker import imp_exp
        from calliope_graph.matrixmaker import dem_matrix
        
        from calliope_graph.units import unit_check  

        
        self.model = model
        self.m_unit = unit_check(unit)
        
        ex_inp = input_read(ex_path)
        
        self.co_techs    = ex_inp[0]
        self.carrier     = ex_inp[1]
        self.nodes       = ex_inp[2]
        self.pr_techs    = ex_inp[3]
        self.colors      = ex_inp[4]
        self.names       = ex_inp[5]
        self.tr_tech     = ex_inp[6]
        self.start       = ex_inp[7]
        self.end         = ex_inp[8]
        self.RES_ind     = ex_inp[9]
        
        self.production             = prod_matrix (model,self.pr_techs,self.nodes,self.carrier)
        self.imports,self.exports   = imp_exp(model,self.nodes,self.production,self.tr_tech,self.carrier)
        self.demand                 = dem_matrix (model,self.co_techs,self.carrier,self.nodes)
        
            

    def node_dispatch (self,nodes='All', fig_format = 'png' , unit= '' , style = 'ggplot' , date_format = '%d/%m/%y , %H:%M', title_font = 12,figsize=(8,6),xtick_rotate=70,average='hourly',sp_techs=None ,sp_nodes= None,directory='my_graphs'):

                
        from calliope_graph.units import unit_check  
        from calliope_graph.units import u_conv 
        
        from calliope_graph.graphs import node_disp   
        
        if unit == '' :
            unit = self.m_unit
        else:
            unit == unit
        
        unit = unit_check(unit)
        conversion = u_conv(self.m_unit,unit)
        
        if nodes == 'All':
            nodes = self.nodes  
        else: 
            nodes = nodes
            
        node_disp (nodes,fig_format,unit,conversion,style,date_format,title_font,self.production,self.imports,self.exports,figsize,self.demand,self.colors,self.names,xtick_rotate,average,sp_techs,sp_nodes,directory)
            
        
    
        
    def sys_dispatch (self, rational = 'techs' , fig_format = 'png' , unit= '' , style = 'ggplot' , date_format = '%d/%m/%y , %H:%M', title_font = 12,figsize=(8,6),xtick_rotate=70,average='hourly',sp_techs=None ,sp_nodes= None,directory='my_graphs'):            
        
        from calliope_graph.units import unit_check  
        from calliope_graph.units import u_conv     
        
        from calliope_graph.graphs import sys_disp
        
        
        if unit == '' :
            unit = self.m_unit
        else:
            unit == unit
        
        unit = unit_check(unit)
        conversion = u_conv(self.m_unit,unit)        
        
        sys_disp(rational,fig_format,unit,conversion,style,date_format,title_font,self.production,self.imports,self.exports,figsize,self.demand,self.colors,self.names,xtick_rotate,average,sp_techs,sp_nodes,directory)
        
    def node_pie (self,rational='production',nodes='All', fig_format = 'png' , unit= '' , style = 'ggplot' , date_format = '%d/%m/%y , %H:%M', title_font = 12 , figsize=(16, 8),xtick_rotate=70,average='hourly',sp_techs=None ,sp_nodes= None,directory='my_graphs',v_round=0):
       
        from calliope_graph.units import unit_check  
        from calliope_graph.units import u_conv         

        if unit == '' :
            unit = self.m_unit
        else:
            unit == unit
        
        unit = unit_check(unit)
        conversion = u_conv(self.m_unit,unit)
        
        if nodes == 'All':
            nodes = self.nodes  
        else: 
            nodes = nodes        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        

