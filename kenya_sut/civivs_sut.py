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
        
        # computing matrices of coefficients
        self.z = pd.DataFrame(self.Z.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.Z.index, columns=self.Z.columns)
        self.va = pd.DataFrame(self.VA.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.VA.index, columns=self.VA.columns)
        self.s = pd.DataFrame(self.S.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.S.index, columns=self.S.columns) 
        
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
 

      
# This function will calculate all the flows with new names in a way after
# implementing a shock, the user can have access to all the information before 
# and after shock impelementation.



    def calc_all(self):

                
        import pandas as pd
        import numpy as np
        
        # creating indexes
        self.VA_ind = self.VA.index
        self.S_ind = self.S.index

        try:
            # computing The New X_c
            self.X_c = pd.DataFrame(self.l @ self.Y_c.values , index = self.X.index , columns = self.X.columns)
            # re-computing flow matrices
            self.VA_c = pd.DataFrame(self.va.values @ (self.X_c.values  * np.identity(len(self.X_c))),index = self.VA_ind,columns =  self.Z.columns)
            self.IMP_c = pd.DataFrame(self.imp.values @ (self.X_c.values  * np.identity(len(self.X_c))),index = self.IMP_ind,columns =  self.Z.columns)
            self.E_c = pd.DataFrame(self.e.values @ (self.X_c.values * np.identity(len(self.X_c))),index = self.E_ind , columns = self.Z.columns)
            self.Z_c = pd.DataFrame(self.z.values @  (self.X_c.values * np.identity(len(self.X_c))),index = self.Z.index , columns = self.Z.columns)
            
        except:
            raise ValueError('A shock should be Implemented to calculate the new matrices!')
        
        

        
    def aggregate(self, level=4):
        
        # To consider the case that the user did not calculate the new matrices
        try:
            self.X_agg   = self.X.groupby(level=level,sort = False).sum()
            self.X_c_agg = self.X_c.groupby(level=level,sort = False).sum()
            
            self.VA_agg  = self.VA.groupby(level=level,sort = False).sum()
            self.VA_c_agg= self.VA_c.groupby(level=level,sort = False).sum()
            
            self.Z_agg  = self.Z.groupby(level=level,sort = False).sum()
            self.Z_c_agg= self.Z_c.groupby(level=level,sort = False).sum()
            
        except:
            
            self.X_agg   = self.X.groupby(level=level,sort = False).sum()           
            self.VA_agg  = self.VA.groupby(level=level,sort = False).sum()           
            self.Z_agg  = self.Z.groupby(level=level,sort = False).sum()
            
        


    def shock(self, path , sensitivity = False,Y= False , E = False , A= False , VA = False):
        import pandas as pd
        # In order to keep the original Y, a copy of that will be used for the case
        # that a shock is going to be implemented
        
        
        self.Y_c = self.Y.copy()
        
        if Y:
            Y_m = pd.read_excel(path, sheet_name = 'Y', index_col = [0] , header = [0])

            header = Y_m.columns.to_list()
            index  = Y_m.index.to_list()
            print(Y_m)
            
            for i in range(len(Y_m)): 
                
              
                            
                self.Y_c.loc[['Commodities',Y_m.loc[i+1,header[0]]],'Total final demand'] = \
                            self.Y_c.loc[['Commodities',Y_m.loc[i+1,header[0]]],'Total final demand'] + Y_m.loc[i+1,header[1]]
            

            
        
        
        
        
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    