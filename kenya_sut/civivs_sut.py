# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:56:55 2020

@author: negar & amin
"""

class C_SUT:
    
    
    def __init__(self,path):
        
        print('CIVCS SUT: A python Class for SUT Input Output Analysis Developed in Fondazione Eni Enrico Mattei')
        
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
        
        # creating indexes
        self.VA_ind = self.VA.index
        self.S_ind = self.S.index

        # computing matrices of coefficients
        self.z = pd.DataFrame(self.Z.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.Z.index, columns=self.Z.columns)
        self.va = pd.DataFrame(self.VA.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.VA.index, columns=self.VA.columns)
        self.s = pd.DataFrame(self.S.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.S.index, columns=self.S.columns)
        #self.imp = pd.DataFrame(self.IM.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.IM.index, columns=self.IM.columns)
        
# Probably I would delete this function...       
    def parse(self):
        
        import pandas as pd
        import numpy as np
        
        # Import on final demand 
        self.IM_fd = self.SUT.loc['Rest of the World', 'Households']
        self.IM_inv = self.SUT.loc['Rest of the World', 'Savings-Investment']

        self.l = np.linalg.inv(np.identity(len(self.z)) - self.z)


    def calc_all(self):        
        import pandas as pd
        import numpy as np
        
        
        
        try:
            
            self.l_c = np.linalg.inv(np.identity(len(self.z_c)) - self.z_c)
            self.X_c = pd.DataFrame(self.l_c @ self.Y_c.values , index = self.X.index , columns = self.X.columns)
                    # re-computing flow matrices
            self.VA_c = pd.DataFrame(self.va_c.values @ (self.X_c.values  * np.identity(len(self.X_c))),index = self.VA_ind,columns =  self.Z.columns)
                    #self.IMP_c = pd.DataFrame(self.imp_c.values @ (self.X_c.values  * np.identity(len(self.X))),index = self.IMP_ind,columns =  self.Z.columns)
            self.S_c = pd.DataFrame(self.s_c.values @ (self.X_c.values * np.identity(len(self.X_c))),index = self.S_ind , columns = self.Z.columns)
            self.Z_c = pd.DataFrame(self.z_c.values @ (self.X_c.values * np.identity(len(self.X_c))),index = self.Z.index , columns = self.Z.columns)
            
        except:
            raise ValueError('No Shock is Implemented Yet!')
        
  
    def aggregate(self, level_x= [0,4] , level_va = 3 , sort = False):

        
        try:
            
            self.X_agg = self.X.groupby(level=level_x , sort = sort).sum()
            self.X_c_agg = self.X_c.groupby(level=level_x , sort = sort).sum()
            
            self.Z_agg = self.Z.groupby(level = level_x,sort=sort).sum().groupby(axis = 1 , level = level_x , sort = sort)
            self.Z_c_agg = self.Z_c.groupby(level = level_x,sort=sort).sum().groupby(axis = 1 , level = level_x , sort = sort)
                      
            self.VA_agg = self.VA.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()
            self.VA_c_agg = self.VA_c.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()

            print('Both baseline and shocked results are aggregated')
            
            
            
        except:            

            self.X_agg = self.X.groupby(level=level_x , sort = sort).sum()
            
            self.Z_agg = self.Z.groupby(level = level_x,sort=sort).sum().groupby(axis = 1 , level = level_x , sort = sort)
            
            self.VA_agg = self.VA.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()

            print("Attention: As there is no shock, only the baseline matrices are aggregated")


      

    def shock(self, path , sensitivity = False,Y= False , S = False , Z= False , VA = False):
        import pandas as pd
        
        # Take a copy of all the things that can change to keep the original 
        # information and the shocked one
        self.Y_c   = self.Y.copy()
        self.va_c  = self.va.copy()
        #self.imp_c = self.imp.copy()
        self.s_c   = self.s.copy()
        self.z_c   = self.z.copy()
        
        if Y:
            Y_m = pd.read_excel(path, sheet_name = 'Y', index_col = [0] , header = [0])
            
            header = Y_m.columns.to_list()
            index  = Y_m.index.to_list()

            
            for i in range(len(Y_m)): 

                self.Y_c.loc[('Commodities',Y_m.loc[index[i],header[0]]),'Total final demand'] = \
                            self.Y_c.loc[('Commodities',Y_m.loc[index[i],header[0]]),'Total final demand'].values + Y_m.loc[index[i],header[1]]
            

        if Z:
            
            Z_m = pd.read_excel(path, sheet_name = 'Z', index_col = [0] , header = [0])

            header = Z_m.columns.to_list()
            index  = Z_m.index.to_list()

            
            for i in range(len(Z_m)): 
                
                # for every step, we should check if the changes should be
                # on the coefficients or the flow
                
                if Z_m.loc[index[i],header[4]] == 'Percentage':
                    
                    self.z_c.loc[(Z_m.loc[index[i],header[0]],Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])] = \
                        self.z.loc[(Z_m.loc[index[i],header[0]],Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])].values \
                            * ( 1 +  Z_m.loc[index[i],header[5]] )
                            
                        
                    
                    
        if VA:
            
            VA_m = pd.read_excel(path, sheet_name = 'VA', index_col = [0] , header = [0])
            
            header = VA_m.columns.to_list()
            index  = VA_m.index.to_list()

            
            for i in range(len(VA_m)): 
                
                if VA_m.loc[index[i],header[3]] == 'Percentage':
                    
                    self.va_c.loc[VA_m.loc[index[i],header[0]],(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])] = \
                        self.va.loc[VA_m.loc[index[i],header[0]],(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])].values \
                            * ( 1 + VA_m.loc[index[i],header[4]])
                        
        if S:
            
            S_m = pd.read_excel(path, sheet_name = 'S', index_col = [0] , header = [0])
            
            header = S_m.columns.to_list()
            index  = S_m.index.to_list()

            
            for i in range(len(S_m)): 
                
                if S_m.loc[index[i],header[2]] == 'Percentage':
                    
                    self.s_c.loc[S_m.loc[index[i],header[0]],('Activities',S_m.loc[index[i],header[1]])] = \
                        self.s.loc[S_m.loc[index[i],header[0]],('Activities',S_m.loc[index[i],header[1]])].values \
                            * ( 1 + S_m.loc[index[i],header[3]])
                    
              



#In this part of the code new functions for doing graphs will be added:
#the graphs will be divided into two different categories:
#    1. Shock graphs in which the user can do the graphs automatically for the 
#        baseline and the shock different
#    2. A general graph function in which user can choose what to graph        
    


    def plot_dx(self,aggregation = True, Kind = 'bar' , Unit = 'M KSH',stacked=True , level = None):
        import matplotlib.pyplot as plt

        
        # To check if the shock is implemented or not
        try:
            a = self.X_c
        except:
            raise ValueError('This function can not be used if no shock is impemented')

            
        # Checking the unit that user want to use for doing graphs
        if Unit == 'M KSH':
            ex_rate = 1.0
        elif Unit == 'M USD':
            ex_rate = 2.0
        elif Unit !='M KSH' or 'M USD' :
            raise ValueError('The unit should be {} or {}'.format('M KSH','M USD'))
        
        # Finding if the graphs should be aggregated or not
        if aggregation: 
            
            try:
                old = self.X_agg
                new = self.X_c_agg
            except: 
                raise ValueError('There is no aggregated result of {} and {}. Please Run the aggregation function first'.format('Baseline Prodction','New Production'))
                
        elif aggregation == False:
            
            old = self.X
            new = self.X_c
            
        if level == None:
            old = old
            new = new
        
        elif level == 'Activities' or 'Commodities':
            
            old = old.loc[level]
            new = new.loc[level]
            
        elif level != None or 'Activities' or 'Commodities':
            
            raise ValueError('The level should be {}, {} or {}'.format('None','Activities','Commodities'))
        
        
        dx = (new - old) * ex_rate
        
        dx.plot(kind = Kind , stacked = stacked)
        plt.title('Production Change')
        plt.ylabel(Unit)
        plt.legend(loc = 1,bbox_to_anchor = (1.5,1))
        plt.show()
        
  
    def plot_dv(self,aggregation = True, Kind = 'bar' , Unit = 'M KSH',stacked=True , level = None,drop='unused'):
        
        import matplotlib.pyplot as plt
        
        # To check if the shock is implemented or not
        try:
            a = self.X_c
        except:
            raise ValueError('This function can not be used if no shock is impemented')
            
        # Checking the unit that user want to use for doing graphs
        if Unit == 'M KSH':
            ex_rate = 1.0
        elif Unit == 'M USD':
            ex_rate = 2.0
        elif Unit !='M KSH' or 'M USD' :
            raise ValueError('The unit should be {} or {}'.format('M KSH','M USD'))
        
        # Finding if the graphs should be aggregated or not
        if aggregation: 

            
            try:

                old = self.VA_agg

                new = self.VA_c_agg
            except: 
                raise ValueError('There is no aggregated result of {} and {}. Please Run the aggregation function first'.format('Baseline Prodction','New Production'))
                
        elif aggregation == False:
            
            old = self.VA
            new = self.VA_c
            
        if level == None:
            old = old
            new = new
        
        elif level == 'Activities' or 'Commodities':
            
            old = old[level]
            new = new[level]
            
        elif level != None or 'Activities' or 'Commodities':
            
            raise ValueError('The level should be {}, {} or {}'.format('None','Activities','Commodities'))
        
        
        dv = (new - old) * ex_rate
        dv = dv.drop(drop)
        
        dv.plot(kind = Kind , stacked = stacked)
        plt.title('Value Added Change')
        plt.ylabel(Unit)
        plt.legend(loc = 1,bbox_to_anchor = (1.5,1))
        plt.show()        

    
    
#%%

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    