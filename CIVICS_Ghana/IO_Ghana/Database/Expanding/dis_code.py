# -*- coding: utf-8 -*-
"""

@author: Amin
"""

import pandas as pd
import numpy as np

class AgDis():
    
    def __init__(self,concordance,E_matrix,E_index_col):
        
        if isinstance(E_index_col,int):
            E_index_col = [i for i in range(E_index_col+1)]


        self.concordance = pd.read_excel(concordance,index_col = 0)
        self.E           = pd.read_excel(E_matrix,index_col=E_index_col)
        
        self.index   = self.concordance.index.to_list()
        self.columns = self.concordance.columns.to_list()
        
        inds,cols = list(set(self.index)),list(set(self.E.columns.to_list()))
        if len(inds) != len(cols):
            raise ValueError('length mismatch between index of concordance and columns of E matrix.\n'
                             'Check if the E_col_index is given properly or not.')
        
        for i in range(len(inds)):
            if inds[i]!= cols[i]:
                raise ValueError('{} != {}'.format(inds[i],cols[i]))


        self.__list_aggregation()
        self.__list_disaggregation()
        self.__list_single_corr()
        
    def __list_single_corr(self):
        
        ''' 
        This function will find the sectors that are corresponding to one sector.
        and store them in a dictionary in which in the dictionary, the key representes
        the columns (No E database) and value is the index (E database). Why we do it?
        
        because the names are different and we want to avoid any issue.
        '''
        
        self.single_map={}
        
        for col in self.columns:
            
            if self.concordance[col].values.sum()<=1:
                
                for row in self.index:
                    if self.concordance.loc[row].values.sum()<=1 and self.concordance.loc[row,col]==1:
                        self.single_map[col] = row
                        break
    
    def __list_aggregation(self):
        
        '''
        in this function, the aggregations will be identified. how?
        
        the code checks every columns (sectors in no E databsae). if the sum of
        the rows for every column is > 1, it means that there are some rows 
        (sectors in E database) that should be aggregated to form a single industry
        with the name of the column. 
        
        The results are stored in a dictionary in which the key represntes the column
        and the values represents the rows that should be aggregated with the name of
        column.
        '''
        
        self.agg_map = {}

        for col in self.columns:
            _ = []           
            if self.concordance[col].values.sum()>1:
                for row in self.index:
                    # if it is 1, means that a sector in index should take the name
                    # of the sector in the column name
                    if self.concordance.loc[row,col] == 1 :
                        _.append(row)                                                

                self.agg_map[col]=_


        
    
    def get_proxy_excel(self,directory):
        
        
        '''
        This function will provide an excel file for the proxies for the disaggregation.
        '''
          
        level_0 = []
        level_1 = []
        for ind in [*self.disagg_map]:
            for val in self.disagg_map[ind]:
                level_0.append(ind)
                level_1.append(val)
                
        
        proxy = pd.DataFrame(columns = ['proxy'],index=[level_0,level_1]).fillna(0)
        
        with pd.ExcelWriter(directory) as writer:
            proxy.to_excel(writer)
        
    def __list_disaggregation(self):
        
        '''
        this function finds the rows (E database) that should be disaggreted into
        multiple columns (no E database sectors). how?
        
        it checks every row and if the sum of the all columns for every row is 
        >1, it means that the row should be disaggregated to the mutilpe columns.
        
        it stores the results in a dictionary in which the keys are the rows (E database sector)
        to the disaggregated sectors (columns or no E database sectors).
        '''
        
        self.disagg_map = {}

        for row in self.index:
            _ = []           
            if self.concordance.loc[row].values.sum()>1:
                for col in self.columns:
                    # if it is 1, means that a sector in index should take the name
                    # of the sector in the column name
                    if self.concordance.loc[row,col] == 1 :
                        _.append(col)                                                

                self.disagg_map[row]=_

        
    def run(self,proxy,save=True):
        
        '''
        This function reads the proxy file and fill the E_new matrix which
        is a dataframe whic the cols are the no E database sectors and the inds
        are the E matrix indeces.
        '''


        proxy = pd.read_excel(proxy, index_col=[0,1],header=[0])
            
        self.E_new = pd.DataFrame(np.zeros((self.E.shape[0],self.concordance.shape[1])),
                                  index =self.E .index,
                                  columns =self.concordance.columns )
                    
        for col in self.columns:
            
            if col in [*self.single_map]:
                
                'No aggregation and disaggregation exists'
                self.E_new[col] = self.E[self.single_map[col]]
                
            elif col in [*self.agg_map]:
                
                'Aggregation is needed'
                sum_ = 0
                for sector in self.agg_map[col]:
                    'Aggregate the corrosponding sectors in E database'
                    sum_ += self.E[sector].values 
                    
                self.E_new[col] = sum_
                
            else:
                
                'Disaggregation is needed'
                for key in self.disagg_map.keys():
                    'Find the corresponding sector in E database to be disaggregated'
                    if col in self.disagg_map[key]:
                        break

                'Using the given proxy (relateve value of a sector in the aggregated sector'
                self.E_new[col] = self.E[key] *\
                                proxy.loc[(key,col),'proxy']\
                                /proxy.loc[(key,slice(None)),'proxy'].values.sum()
                        
                    
        if save:
            'Save in an excel file'
            with pd.ExcelWriter('E_new.xlsx') as writer:
                self.E_new.to_excel(writer)

#%%        
ghana = AgDis(concordance = r'Concordance/C_EORA.xlsx',E_matrix=r'Environmental Extension/EE_EORA_W.xlsx',E_index_col= 3)
#%%
# ghana.get_proxy_excel(r'Proxy/P_EORA_W.xlsx')
#%%
ghana.run(proxy=r'Proxy/P_EORA_W.xlsx',save=True)
