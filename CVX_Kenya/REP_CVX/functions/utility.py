# -*- coding: utf-8 -*-
'''
utility Module
==============================================================================

A module for providing some useful functions

Functions
----------
indeces:        Provides a dict of the indeces that can be used for different purposes

dict_maker:     Stores the given information in a dictionary.
'''
import xlsxwriter
import os

def indeces (S,Z,VA,X):

    return {'Z_ind': Z.index , 'VA_ind':VA.index , 'S_ind': S.index , 
            'X_ind': X.index ,'Z_col': Z.columns , 'VA_col':VA.columns , 
            'S_col': S.columns , 'X_col':X.columns}

def dict_maker(Z=None,X=None,VA=None,p=None,Y=None,va=None,z=None,s=None,
               Z_agg=None,X_agg=None,VA_agg=None,Y_agg=None,S_agg=None,p_agg=None):
    
    inputs =  [Z,X,VA,p,Y,va,z,s,Z_agg,X_agg,VA_agg,Y_agg,S_agg,p_agg]
    outputs = ['Z','X','VA','p','Y','va','z','s','Z_agg','X_agg','VA_agg','Y_agg','S_agg','p_agg']
    
    dictionary = {}
    
    for i  in range(len(inputs)):
        if inputs[i] is not None:
            dictionary[outputs[i]]=inputs[i]
               
    return dictionary

def value_from_excel(path):
    
    import xlwings as xl
    app = xl.App(visible=False)
    book = app.books.open(path)
    book.save()
    app.kill()
    
def sh_excel(num_shock,indeces):

    level = ['Activities','Commodities']
    rc    = indeces['X_ind'].get_level_values(1).to_list()
    types = ['Percentage','Absolute']
    aggregated = ['Yes','No']
    
    
    
    file = 'my_shock1.xlsx'
    workbook = xlsxwriter.Workbook(file)
    indeces = workbook.add_worksheet('indeces')  
    for i in range(len(rc)):
        indeces.write('A{}'.format(i+1),rc[i])

    
    Z = workbook.add_worksheet('Z')
    
    # Add a format for the header cells.
    header_format = workbook.add_format({
        'border': 1,
        'bg_color': '#C6EFCE',
        'bold': True,
        'text_wrap': False,
        'valign': 'vcenter',
        'indent': 1,
    })
    
    # Write the header cells and some data that will be used in the examples.
    heading1 = 'Number'
    heading2 = 'level_row'
    heading3 = 'row'
    heading4 = 'level_col'
    heading5 = 'col'
    heading6 = 'type'
    heading7 = 'value'
    heading8 = 'aggregated'

    
    
    
    Z.write('A1', heading1, header_format)
    Z.write('B1', heading2, header_format)
    Z.write('C1', heading3, header_format)
    Z.write('D1', heading4, header_format)
    Z.write('E1', heading5, header_format)
    Z.write('F1', heading6, header_format)
    Z.write('G1', heading7, header_format)
    Z.write('H1', heading8, header_format)

    
    sheet_reference_str = '=indeces!$A$1:$A$1{}'.format(len(rc))
    
    for i in range(num_shock):
        
        Z.write('A{}'.format(i+2), str(i))
        
        Z.data_validation('B{}'.format(i+2), {'validate': 'list',
                                      'source': level})
        Z.data_validation('C{}'.format(i+2), {'validate': 'list',
                                      'source': sheet_reference_str})  
        Z.data_validation('D{}'.format(i+2), {'validate': 'list',
                                      'source': level})
        Z.data_validation('E{}'.format(i+2), {'validate': 'list',
                                      'source':  sheet_reference_str})
        Z.data_validation('F{}'.format(i+2), {'validate': 'list',
                                      'source': types})  
        Z.data_validation('H{}'.format(i+2), {'validate': 'list',
                                      'source': aggregated})

    workbook.close()

    
    
    
    