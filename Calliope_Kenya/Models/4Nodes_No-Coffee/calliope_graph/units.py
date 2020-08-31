# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 13:22:27 2020

@author: Amin
"""



def unit_check(unit):
    
    units = ['W','kW','MW','GW','TW']
    
    if unit not in units:
        raise ValueError ('{} is not correct. Unit should be one of the followings: \n {}'.format(unit,units))
        
    return unit
        

def u_conv (unit1,unit2):
    
    converter = {'W':1,'kW':10**3,'MW':10**6,'GW':10**9,'TW':10**12}
    
    
    return converter[unit1]/converter[unit2]   
            
            
            
            
            
            
            