# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 16:47:09 2020

@author: Mohammad Amin Tahavori
"""
def impact_check(inv,sav,results):
    
    list1 = {'sh':'shock','se':'sensitivity'}
    sav_list,inv_list = [],[]
    save_out,inv_out  = {},{}
    
    if len(inv)!=2 or len(sav) != 2:
        raise ValueError('Wrong input for invest_sce and saving_sce. \n Two valuse should be given as follow:\
                          \n [type of the input,the number of the specifict input] ')
    if  inv[0] not in list1 or sav[0] not in list1:
        raise ValueError('The first argument can be one of the followings: {}'.format(list1))       
    if inv[0]  == 'se' and sav[0] == 'se':
        raise ValueError('both \'saving_sce\' and \'invest_sce\' cannot be based on \'sensitivity\' level.')
        
    # Check if the entered information exists or not. Then fill the list
    try: 
        results['{}_{}'.format(list1[inv[0]],inv[1])]
        if inv[0]=='se':
            for key, value in results['{}_{}'.format(list1[inv[0]],inv[1])].items(): 
               if key != 'information':
                   inv_list.append(key)
    except: 
        raise ValueError('{}_{} does not exists in results dictionary'.format(list1[inv[0]],inv[1]))
      
    # Check if the entered information exists or not. Then fill the list
    try: 
        results['{}_{}'.format(list1[sav[0]],sav[1])]
        if sav[0]=='se':
            for key, value in results['{}_{}'.format(list1[sav[0]],sav[1])].items(): 
               if key != 'information':
                   sav_list.append(key)    
                   
    except: raise ValueError('{}_{} does not exists in results dictionary'.format(list1[sav[0]],sav[1])) 
    
    
    # Making the dictionaries for outout
    if len(sav_list)>len(inv_list):
        for i in sav_list:
            save_out[i]= results['{}_{}'.format(list1[sav[0]],sav[1])][i]
            inv_out [i]= results['{}_{}'.format(list1[inv[0]],inv[1])]
            
            
    elif len(sav_list)<len(inv_list):
        for i in inv_list:
            save_out[i]= results['{}_{}'.format(list1[sav[0]],sav[1])]
            inv_out [i]= results['{}_{}'.format(list1[inv[0]],inv[1])][i] 
            sav_list = inv_list
        
    else: 
        sav_list = ['single']
        save_out['single'] = results['{}_{}'.format(list1[sav[0]],sav[1])]
        inv_out ['single'] = results['{}_{}'.format(list1[inv[0]],inv[1])]
        
        
    return save_out,inv_out,sav_list

def impact_assessment(invest_sce,saving_sce,results,p_life,w_ext,em_ext,land,labour,capital,imports):
    
    import pandas as pd
    
    save_out,inv_out,sav_list = impact_check(invest_sce,saving_sce,results)
    
    columns = ['Saving','Investment','Water Saving','Water Investment',
               'Emission Saving','Emission Investment', 'Land Saving',
               'Land Investment','Workforce Saving','Workforce Investment',
               'Capital Saving','Capital Investment','Import Saving',
               'Import Investment','PROI','PPBT','Water Total Impact',
               'Emission Total Impact','Land Total Impact','Import Total Impact',
               'Workforce Total Impact','Capital Total Impact']
    
    Imp = pd.DataFrame(index=sav_list,columns=columns)
    Imp.fillna(0)
    
    for i in sav_list:
        
        Imp.loc[i,'Investment'] = inv_out[i]['VA'].values.sum().sum() - results['baseline']['VA'].sum().sum()
        Imp.loc[i,'Saving'] = + results['baseline']['VA'].sum().sum()-save_out[i]['VA'].values.sum().sum()
        
        Imp.loc[i,'Water Investment'] =  inv_out[i]['S_agg'].loc[w_ext].sum().sum() - results['baseline']['S_agg'].loc[w_ext].sum().sum()
        Imp.loc[i,'Water Saving'] =  -save_out[i]['S_agg'].loc[w_ext].sum().sum() + results['baseline']['S_agg'].loc[w_ext].sum().sum()
            
        Imp.loc[i,'Emission Investment'] =  inv_out[i]['S_agg' ].loc[em_ext].sum().sum() - results['baseline']['S_agg'].loc[em_ext].sum().sum()
        Imp.loc[i,'Emission Saving'] = -save_out[i]['S_agg'].loc[em_ext].sum().sum() + results['baseline']['S_agg'].loc[em_ext].sum().sum()    
            
        Imp.loc[i,'Land Investment'] =  inv_out[i]['S_agg'].loc[land].sum().sum() - results['baseline']['S_agg'].loc[land].sum().sum()
        Imp.loc[i,'Land Saving'] = -save_out[i]['S_agg'].loc[land].sum().sum() + results['baseline']['S_agg'].loc[land].sum().sum()    


        Imp.loc[i,'Workforce Investment'] = inv_out[i]['VA'].groupby(level=3).sum().loc[labour].sum().sum() - results['baseline']['VA'].groupby(level=3).sum().loc[labour].sum().sum()   
        Imp.loc[i,'Workforce Saving'] = -save_out[i]['VA'].groupby(level=3).sum().loc[labour].sum().sum() + results['baseline']['VA'].groupby(level=3).sum().loc[labour].sum().sum() 
            
        Imp.loc[i,'Capital Investment'] = inv_out[i]['VA'].groupby(level=3).sum().loc[capital].sum().sum() - results['baseline']['VA'].groupby(level=3).sum().loc[capital].sum().sum()   
        Imp.loc[i,'Capital Saving'] = -save_out[i]['VA'].groupby(level=3).sum().loc[capital].sum().sum() + results['baseline']['VA'].groupby(level=3).sum().loc[capital].sum().sum() 
            
        Imp.loc[i,'Import Investment'] = inv_out[i]['VA'].groupby(level=3).sum().loc[imports].sum().sum() - results['baseline']['VA'].groupby(level=3).sum().loc[imports].sum().sum()
        Imp.loc[i,'Import Saving'] = -save_out[i]['VA'].groupby(level=3).sum().loc[imports].sum().sum() + results['baseline']['VA'].groupby(level=3).sum().loc[imports].sum().sum()    
 
        Imp.loc[i,'PROI'] = Imp.loc[i,'Saving'] / Imp.loc[i,'Investment']
        Imp.loc[i,'PPBT'] = 1 / Imp.loc[i,'PROI'] 
    
    
        # Total Impacts
        Imp.loc[i,'Water Total Impact']         = Imp.loc[i,'Water Investment'] - p_life * Imp.loc[i,'Water Saving']
        Imp.loc[i,'Emission Total Impact']      = Imp.loc[i,'Emission Investment'] - p_life * Imp.loc[i,'Emission Saving']
        Imp.loc[i,'Land Total Impact']          = Imp.loc[i,'Land Investment'] - p_life * Imp.loc[i,'Land Saving']
        Imp.loc[i,'Import Total Impact']        = Imp.loc[i,'Import Investment'] - p_life * Imp.loc[i,'Import Saving']
        Imp.loc[i,'Workforce Total Impact']     = Imp.loc[i,'Workforce Investment'] - p_life * Imp.loc[i,'Workforce Saving']
        Imp.loc[i,'Capital Total Impact']       = Imp.loc[i,'Capital Investment'] - p_life * Imp.loc[i,'Capital Saving']  
  
    
    return Imp
    
    
    
    
    
    
    
    
    
    
    
    
    
