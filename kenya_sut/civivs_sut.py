# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:56:55 2020

@author: negar & amin
"""

class C_SUT:
    
    
    def __init__(self,path):
        
        import pandas as pd
        import numpy as np
        self.path = path
        
        # importing the whole database (SUT)       
        self.SUT = pd.read_excel(self.path, index_col=[0,1,2,3,4], header = [0,1,2,3,4])

        # importing use (U), supply (V), supply-use together (Z) and satellite accounts (S)
        self.U = self.SUT.loc['Commodities','Activities']
        self.V = self.SUT.loc['Activities','Commodities']
        self.Z = self.SUT.loc[['Commodities','Activities'], ['Commodities','Activities']]
        self.S = self.SUT.loc['EORA Satellite Accounts',['Commodities','Activities']]
        
        
        # computing total final demand (Y) by importing households (HH), investment (IN), government (GO) and export (EX) 
        self.HH = self.SUT.loc[['Commodities','Activities'], 'Households']
        self.IN = self.SUT.loc[['Commodities','Activities'], 'Savings-Investment']
        self.GO = self.SUT.loc[['Commodities','Activities'], 'Government']
        self.EX = self.SUT.loc[['Commodities','Activities'], 'Rest of the World']
        
        self.Y = pd.DataFrame(self.HH.sum(axis=1) + self.IN.sum(axis=1) + self.GO.sum(axis=1) + self.EX.sum(axis=1), index=self.HH.index, columns=['Total final demand'])
        
        # computing total value added (VA) by importing factors of production (F), taxes (T) and import (IM)
        self.F = self.SUT.loc['Factors', ['Commodities', 'Activities']]
        self.T = self.SUT.loc['Government', ['Commodities','Activities']]
        self.IM = self.SUT.loc['Rest of the World', ['Commodities','Activities']]
        
        self.VA = self.F.append(self.T.append(self.IM))
        
        # computing total production vector (X)
        self.X = pd.DataFrame(self.Y.sum(axis=1) + self.Z.sum(axis=1), index=self.Z.index, columns=['Total Production'])
        
# Probably I would delete this function...       
    def parse(self):
        
        import pandas as pd
        import numpy as np
        
        # Import on final demand 
        self.IM_fd = self.SUT.loc['Rest of the World', 'Households']
        self.IM_inv = self.SUT.loc['Rest of the World', 'Savings-Investment']

        self.l = np.linalg.inv(np.identity(len(self.z)) - self.z)


    def plot_dx(self, old_x,new_x,level=False,Type='bar',Unit = 'M Ksh'):
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ax = plt.subplots()
        
        dx = new_x-old_x
        my_title = Unit
        
        if Type == 'bar':
            if level == False:
                
                y_pos = np.arange(len(dx))
                dx = dx.values.reshape((len(dx),))
                
                ax.barh(y_pos,dx,align='center')
                ax.set_yticks(y_pos)
                ax.set_yticklabels(new_x.index)
                ax.invert_yaxis()
                ax.set_xlabel('M Ksh')
                ax.set_title('Production Change')
                plt.show()
                
            else:
                
                dx = dx.loc[level]
                
                y_pos = np.arange(len(dx))
                dx = dx.values.reshape((len(dx),))
                
                ax.barh(y_pos,dx,align='center')
                ax.set_yticks(y_pos)
                ax.set_yticklabels(new_x.loc[level].index)
                ax.invert_yaxis()
                ax.set_xlabel('M Ksh')
                ax.set_title(level + ' Production Change')
                plt.show()
        
        
    def plot_dv(self, old_v,new_v,level=False,Type='bar'):
        import matplotlib.pyplot as plt
        import numpy as np

        dv = new_v-old_v
        dv.index = dv.index.get_level_values(0)
        
        if Type == 'bar':
            if level == False:
                
                dv.plot(kind='bar')
                plt.title('Value Added')
                plt.ylabel('M Ksh')
                plt.legend(loc=1,bbox_to_anchor = (1.5,1))
                plt.show()
                
            else:
                
                dv = dv[level]
                dv.plot(kind='bar')
                plt.title('Value Added')
                plt.ylabel('M Ksh')
                plt.legend(loc=1,bbox_to_anchor = (1.5,1))
                plt.show()    
        
                
    def calc_all(self):        
        import pandas as pd
        import numpy as np
        
        # creating indexes
        self.VA_ind = self.VA.index
        self.S_ind = self.S.index

        # computing matrices of coefficients
        self.z = pd.DataFrame(self.Z.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.Z.index, columns=self.Z.columns)
        self.va = pd.DataFrame(self.VA.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.VA.index, columns=self.VA.columns)
        self.s = pd.DataFrame(self.S.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.S.index, columns=self.S.columns)

        # re-computing flow matrices
        self.VA_c = pd.DataFrame(self.va.values @ (self.X.values  * np.identity(len(self.X))),index = self.VA_ind,columns =  self.Z.columns)
        self.IMP_c = pd.DataFrame(self.imp.values @ (self.X.values  * np.identity(len(self.X))),index = self.IMP_ind,columns =  self.Z.columns)
        self.E_c = pd.DataFrame(self.e.values @ (self.X.values * np.identity(len(self.X))),index = self.E_ind , columns = self.Z.columns)
        
        
# NG: I think we can more easly build a new function (aggregate) that ask for the level and simply use groupby for every objects returning aggregated version of objects
# like this:
        
    def aggregate(self, level=4):
        
        self.X = self.X.groupby(level=level).sum() #and so on
        # # Aggregating Results
        # # Aggregation of x Matrix
        # com_pr = self.x.loc['Commodities']
        # com_pr.index = com_pr.index.get_level_values(3)
        # com_pr = com_pr.groupby(axis=0,level=0).sum()
        
        # ind_pr = self.x.loc['Activities']
        # ind_pr.index = ind_pr.index.get_level_values(3)
        # ind_pr = ind_pr.groupby(axis=0,level=0).sum()
        
        # cmdt = []
        # for i in range(len(com_pr)):
        #     cmdt.append('Commodities')
        
        # inds = []
        # for i in range(len(ind_pr)):
        #     inds.append('Activities')    
            
        # new_x = pd.concat([com_pr,ind_pr],axis = 0)
        # new_x_index = [cmdt+inds,com_pr.index.to_list() + ind_pr.index.to_list()]
        # new_x.index = new_x_index
        
        # self.x_agg = new_x


        # # Aggregation of VA Matrix
        # com_va = self.VA['Commodities']
        # com_va.columns = com_va.T.index.get_level_values(3)
        # com_va = com_va.groupby(axis=1,level=0).sum()
        
        # ind_va = self.VA['Activities']
        # ind_va.columns = ind_va.T.index.get_level_values(3)
        # ind_va = ind_va.groupby(axis=1,level=0).sum()
        

        # new_va = pd.concat([com_va,ind_va],axis = 1)
        # new_va.columns = new_x_index
        
        # self.VA_agg = new_va
    

        # # Aggregation of IMP Matrix
        # com_im = self.IMP['Commodities']
        # com_im.columns = com_im.T.index.get_level_values(3)
        # com_im = com_im.groupby(axis=1,level=0).sum()
        
        # ind_im = self.IMP['Activities']
        # ind_im.columns = ind_im.T.index.get_level_values(3)
        # ind_im = ind_im.groupby(axis=1,level=0).sum()
        

        # new_im = pd.concat([com_im,ind_im],axis = 1)
        # new_im.columns = new_x_index
        
        # self.IMP_agg = new_im      
      

    def shock(self, path , sensitivity = False,Y= False , E = False , A= False , VA = False):
        import pandas as pd
        
        if Y:
            Y_m = pd.read_excel(path, sheet_name = 'Y', index_col = [0] , header = [0])
            
            header = Y_m.columns.to_list()
            for i in range(len(Y_m)):   
                
                self.Y.loc[['Commodities',Y_m.loc[str(i+1),header[0]]]] = \
                           self.Y.loc[['Commodities',Y_m.loc[str(i+1),header[0]]]] + Y_m.loc[str(i+1),header[1]].values
            
        if A:
            A_m = pd.read_excel(path, sheet_name = 'A', index_col = [0] , header = [0])
            
            header = A_m.columns.to_list()
            
            for i in range(len(A_m)):  
                
                if A_m.loc[str(i+1),header[4]] == 'Percentage':
                    
                    if A_m.loc[str(i+1),header[5]].values < 1.0 :
                        coeff = A_m.loc[str(i+1),header[5]].values
                    else:
                        coeff = A_m.loc[str(i+1),header[5]].values / 100.0
                
                    self.A.loc[[A_m.loc[str(i+1),header[0]]],A_m.loc[str(i+1),header[1]],[A_m.loc[str(i+1),header[2]]],A_m.loc[str(i+1),header[3]]] = \
                        self.A.loc[[A_m.loc[str(i+1),header[0]]],A_m.loc[str(i+1),header[1]],[A_m.loc[str(i+1),header[2]]],A_m.loc[str(i+1),header[3]]] \
                            * (1 + coeff )      
                    
                
        # if VA:
        #     VA_m = pd.read_excel(path, sheet_name = 'VA', index_col = [0] , header = [0])
        #     header = VA_m.columns.to_list()
            
        #     for i in range(len(VA_m)):  
            
            
        
        
        
        
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    