# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 11:31:13 2020

@author: Mohammad Amin Tahavori
"""
def unit_check(unit):
    unit_list = ['M USD','M EUR', 'M KSH','K KSH','K USD','K EUR']
    
    if unit not in unit_list:
        raise ValueError('Unit should be one of the followings: {}'.format(unit_list))
        
    return unit

def unit_converter(unit1,unit2):
    # For now, we use following simple script for the conversion. In the next step, a library will be added to the code.
    
    convert_list = {'M KSH_M USD': 0.00939548 ,'M KSH_M EUR': 0.00833961, 'M KSH_K USD': 0.00939548*1000 ,'M KSH_K EUR': 0.00833961*1000, 'M KSH_K KSH': 1000}
    
    return convert_list['{}_{}'.format(unit1,unit2)]
    