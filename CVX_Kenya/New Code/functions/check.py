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
    
    if unit1 == unit2: conversion = 1
    else: conversion = convert_list['{}_{}'.format(unit1,unit2)]

    
    return conversion

def style_check(style):
    
    styles = ['defualt','classic','Solarize_Light2','_classic_test','bmh',
              'dark_background','fast','fivethirtyeight','ggplot','grayscale',
              'seaborn','seaborn-bright','seaborn-colorblind','seaborn-dark',
              'seaborn-dark-palette','seaborn-darkgrid','seaborn-deep',
              'seaborn-muted','seaborn-notebook','seaborn-paper',
              'seaborn-pastel','seaborn-poster','seaborn-talk','seaborn-ticks',
              'seaborn-white','seaborn-whitegrid','tableau-colorblind10']
    
    if style not in styles:
        
        raise ValueError ('{} is not correct. Acceptable styles are : \n {} \n For more information: https://matplotlib.org/3.1.1/gallery/style_sheets/style_sheets_reference.html'.format(style,styles))
        
    return style

def level_check(level):
    
    levels = ['Activities' , 'Commodities']
    if level != None :
        if level not in levels: raise ValueError('/level/ can be: \n 1. /Activities/ \n 2. /Commodities/ \n 3. /None/ ')
        else: title , level = ' by {}'.format(level) , [level]
    else: title , level = '' , levels
        
    return title,level

def kind_check (kind):
    
    kinds = ['Absolute','Percentage']
    if kind not in kinds:
        raise ValueError('/kind/ can be: \n 1. /Absolute/ /n 2. {Percentage}')
    
    return kind
    
    
    
    
    
    
    
    
    
    
    
    