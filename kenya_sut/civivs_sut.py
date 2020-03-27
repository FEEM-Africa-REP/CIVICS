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
        
        
        try:
            
            self.l_c = np.linalg.inv(np.identity(len(self.z_c)) - self.z_c)
            self.X_c = pd.DataFrame(self.l @ self.Y_c.values , index = self.X.index , columns = self.X.columns)
            # re-computing flow matrices
            self.VA_c = pd.DataFrame(self.va_c.values @ (self.X_c.values  * np.identity(len(self.X))),index = self.VA_ind,columns =  self.Z.columns)
            self.IMP_c = pd.DataFrame(self.imp_c.values @ (self.X_c.values  * np.identity(len(self.X))),index = self.IMP_ind,columns =  self.Z.columns)
            self.S_c = pd.DataFrame(self.s_c.values @ (self.X_c.values * np.identity(len(self.X))),index = self.S_ind , columns = self.Z.columns)
            
        except:
            raise ValueError('No Shock is Implemented Yet!')
        
# NG: I think we can more easly build a new function (aggregate) that ask for the level and simply use groupby for every objects returning aggregated version of objects
# like this:
        
    def aggregate(self, level=4):
        
        self.X_agg = self.X.groupby(level=level).sum() #and so on
        self.VA_agg = self.VA.groupby(level=level).sum() #and so on
        self.Z_agg = self.VA.groupby(level=level).sum() #and so on



      

    def shock(self, path , sensitivity = False,Y= False , S = False , Z= False , VA = False):
        import pandas as pd
        
        # Take a copy of all the things that can change to keep the original 
        # information and the shocked one
        self.Y_c   = self.Y.copy()
        self.va_c  = self.va.copy()
        self.imp_c = self.imp.copy()
        self.s_c   = self.s.copy()
        
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
                    
              



        
        
        
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    