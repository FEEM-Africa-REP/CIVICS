# -*- coding: utf-8 -*-
"""
REP CVX: A Tool for Input Output Analysis with Supply and Use Format 
@ FEEM: Fondazione Eni Enrico Mattei - Africa REP
@authors: 1. Negar Namazifard , Nicolo Golinucci, Mohammad Amin Tahavori
"""

class C_SUT:
    
    def __init__(self,path):

        print('REP-CVX: A python class for Supply and Use input-output analysis developed in Fondazione Eni Enrico Mattei by Africa REP')
        import pandas as pd
        import pymrio
        import warnings
        
        self.path = path
        warnings.filterwarnings("ignore") 
        
        # importing the whole Database (SUT)       
        self.SUT = pd.read_excel(self.path, index_col=[0,1,2,3,4], header = [0,1,2,3,4])

        # importing use (U), supply (V), supply-use together (Z) and satellite accounts (S)
        self.U = self.SUT.loc['Commodities','Activities']
        self.V = self.SUT.loc['Activities','Commodities']
        self.Z = self.SUT.loc[['Commodities','Activities'], ['Commodities','Activities']]
        self.S = self.SUT.loc['Satellite Accounts',['Commodities','Activities']]
        
        
        # computing total final demand (Y) by importing households (HH), investment (IN), government (GO) and export (EX) 
        self.HH = self.SUT.loc[['Commodities','Activities'], 'Households']
        self.IN = self.SUT.loc[['Commodities','Activities'], 'Savings-Investment']
        self.GO = self.SUT.loc[['Commodities','Activities'], 'Government']
        self.EX = self.SUT.loc[['Commodities','Activities'], 'Rest of the World']
        self.Y_M = self.SUT.loc[['Commodities','Activities'], 'Margins']
        
        self.Y = pd.DataFrame(self.HH.sum(axis=1) + self.IN.sum(axis=1) + self.GO.sum(axis=1) + self.EX.sum(axis=1) + self.Y_M.sum(axis=1), index=self.HH.index, columns=['Total final demand'])
        
        # computing total value added (VA) by importing factors of production (F), taxes (T), import (IM) and margins as factor (F_M)
        self.F = self.SUT.loc['Factors', ['Commodities', 'Activities']]
        self.T = self.SUT.loc['Government', ['Commodities','Activities']]
        self.IM = self.SUT.loc['Rest of the World', ['Commodities','Activities']]
        self.F_M = self.SUT.loc['Margins', ['Commodities','Activities']]
        
        self.VA = self.F.append(self.T.append(self.IM.append(self.F_M)))
        
        # computing total production vector (X)
        self.X = pd.DataFrame(self.Y.sum(axis=1) + self.Z.sum(axis=1), index=self.Z.index, columns=['Total Production'])
        
        # creating indexes
        self.VA_ind = self.VA.index
        self.S_ind = self.S.index

        # computing matrices of coefficients
        self.z = pymrio.calc_A(self.Z, self.X)
        self.va = pymrio.calc_S(self.VA, self.X)
        self.s = pymrio.calc_S(self.S, self.X)
        #self.imp = pd.DataFrame(self.IM.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.IM.index, columns=self.IM.columns)
        self.l = pymrio.calc_L(self.z)
        #leontief price model
        self.p = pd.DataFrame(self.va.sum().values.reshape(1,len(self.va.columns)) @ self.l.values, index=['Price'], columns=self.VA.columns)
        
        # useful lifetime of the project
        
        self.results = {'Z':self.Z, 'Y':self.Y,'X':self.X,'VA':self.VA,'p':self.p,'va':self.va,'z':self.z}
        self.counter = 1    # A counter for saving the results in a dictionary
        self.s_counter = 1  # A counter for saving the sensitivity results in the dictionary 
        
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
            self.p_c=pd.DataFrame(self.va_c.sum().values.reshape(1,len(self.va_c.columns)) @ self.l_c, index=['Price'], columns=self.VA_c.columns)
            p_0 = self.p_c.values @ self.Y_c.values
            p_1 = self.va_c.sum().values.reshape(1,len(self.va_c.columns)) @ self.X_c.values
            
            print('vx = {}, pY= {} '.format(p_0,p_1))
            
        except:
            raise ValueError('No Shock is Implemented Yet!')
        
  
    def aggregate(self, level_x= [0,4] , level_va = 3 , sort = False):

        # To check if the shock function is used or not. 
        # if Yes:  do the aggregation for both 
        # if No:   do the aggregation only for baseline
        try:
            
            self.X_agg = self.X.groupby(level=level_x , sort = sort).sum()
            self.X_c_agg = self.X_c.groupby(level=level_x , sort = sort).sum()
            
            self.Y_agg = self.Y.groupby(level=level_x, sort=sort).sum()
            self.Y_c_agg = self.Y_c.groupby(level=level_x, sort=sort).sum()
            
            self.Z_agg = self.Z.groupby(level = level_x,sort=sort).sum().groupby(axis = 1 , level = level_x , sort = sort).sum()
            self.Z_c_agg = self.Z_c.groupby(level = level_x,sort=sort).sum().groupby(axis = 1 , level = level_x , sort = sort).sum()
                      
            self.VA_agg = self.VA.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()
            self.VA_c_agg = self.VA_c.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()
            
            self.p_agg= self.p.groupby(axis=1, level=level_x, sort=sort).sum()
            self.p_c_agg= self.p_c.groupby(axis=1, level=level_x, sort=sort).sum()
            
            self.S_agg = self.S.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()
            self.S_c_agg = self.S_c.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()            
         

            print('Both baseline and shocked results are aggregated')
       
        except:            

            self.X_agg = self.X.groupby(level=level_x , sort = sort).sum()
            
            self.Y_agg = self.Y.groupby(level=level_x, sort=sort).sum()
            
            self.Z_agg = self.Z.groupby(level = level_x,sort=sort).sum().groupby(axis = 1 , level = level_x , sort = sort).sum()
            
            self.VA_agg = self.VA.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()
            
            self.p_agg= self.p.groupby(axis=1, level=level_x, sort=sort).sum()
            
            self.S_agg = self.S.groupby(level=level_va,sort = sort).sum().groupby(axis = 1 , level=level_x,sort = sort).sum()
            

            print("Attention: As there is no shock, only the baseline matrices are aggregated")


      

    def shock(self, path , sensitivity = False , Y= False , S = False , Z= False , VA = False):
        import pandas as pd
        import numpy as np
        
        self.sh_path = path
        
        # Loop for the shock
        
        # Take a copy of all the things that can change to keep the original 
        # information and the shocked one
        self.Y_c   = self.Y.copy()
        self.va_c  = self.va.copy()
        #self.imp_c = self.imp.copy()
        self.s_c   = self.s.copy()
        self.z_c   = self.z.copy()
        self.UL = pd.read_excel(path,sheet_name = 'UL',index_col=[0],header=[0]).loc['Useful life','Value']
        
        if Y:
            Y_m = pd.read_excel(path, sheet_name = 'Y', index_col = [0] , header = [0])
            
            header = list(Y_m.columns)
            index  = list(Y_m.index)

            
            for i in range(len(Y_m)): 

                self.Y_c.loc[('Commodities',Y_m.loc[index[i],header[0]]),'Total final demand'] = \
                            self.Y_c.loc[('Commodities',Y_m.loc[index[i],header[0]]),'Total final demand'].values + Y_m.loc[index[i],header[1]]
            

        if Z:
            
            Z_m = pd.read_excel(path, sheet_name = 'Z', index_col = [0] , header = [0])

            header = list(Z_m.columns)
            index  = list(Z_m.index)
            

            
            for i in range(len(Z_m)): 
                
                # for every step, we should check if the changes should be
                # on the coefficients or the flow
                
                # IF the changes are going to be imposed on unaggregated levels
                if Z_m.loc[index[i],'Aggregated'] == 'No':
                
                    if Z_m.loc[index[i],'type'] == 'Percentage':
                        
                        self.z_c.loc[(Z_m.loc[index[i],header[0]],Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])] = \
                            self.z.loc[(Z_m.loc[index[i],header[0]],Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])].values \
                                * ( 1 +  Z_m.loc[index[i],header[5]] )
                                
                    if Z_m.loc[index[i],'type'] == 'Absolute':
                        my_Z=self.Z.copy()
                        
                        my_Z.loc[(Z_m.loc[index[i],header[0]],Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])] = \
                            my_Z.loc[(Z_m.loc[index[i],header[0]],Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])].values \
                                + Z_m.loc[index[i],header[5]]
                                
                        my_z= pd.DataFrame(my_Z.values @ np.linalg.inv (self.X.values * np.identity(len(self.X))),index = self.Z.index , columns = self.Z.columns)
                        self.z_c.loc[(Z_m.loc[index[i],header[0]],Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])] = \
                             my_z.loc[(Z_m.loc[index[i],header[0]],Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])].values
                
                
                # If changes are going to implemented on the aggregated level
                elif  Z_m.loc[index[i],'Aggregated'] == 'Yes': 
                    
                    try:
                    
                        if Z_m.loc[index[i],'type'] == 'Percentage':
                            
                            self.z_c.loc[(Z_m.loc[index[i],header[0]],slice(None),slice(None),slice(None),Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])] = \
                                self.z.loc[(Z_m.loc[index[i],header[0]],slice(None),slice(None),slice(None),Z_m.loc[index[i],header[1]]),(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])].values \
                                    * ( 1 +  Z_m.loc[index[i],header[5]] )  
                            

                    except:
                    
                        if Z_m.loc[index[i],'type'] == 'Percentage':
                            
                            self.z_c.loc[Z_m.loc[index[i],header[0]],(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])] = \
                                self.z.loc[Z_m.loc[index[i],header[0]],(Z_m.loc[index[i],header[2]],Z_m.loc[index[i],header[3]])].values \
                                    * ( 1 +  Z_m.loc[index[i],header[5]] )                              

                    
        if VA:
            
            VA_m = pd.read_excel(path, sheet_name = 'VA', index_col = [0] , header = [0])
            
            header = list(VA_m.columns)
            index  = list(VA_m.index)

            
            for i in range(len(VA_m)):
                
                # IF the changes are going to be imposed on unaggregated levels
                if VA_m.loc[index[i],'Aggregated'] == 'No':

                
                    if VA_m.loc[index[i],'type'] == 'Percentage':
                        
                        self.va_c.loc[VA_m.loc[index[i],header[0]],(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])] = \
                            self.va.loc[VA_m.loc[index[i],header[0]],(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])].values \
                                * ( 1 + VA_m.loc[index[i],header[4]])
                                
                    if VA_m.loc[index[i],'type'] == 'Absolute':
                        
                        my_VA= self.VA.copy()
                        
                        my_VA.loc[VA_m.loc[index[i],header[0]],(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])] = \
                            my_VA.loc[VA_m.loc[index[i],header[0]],(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])].values \
                                + VA_m.loc[index[i],header[4]]
                        my_va= pd.DataFrame(my_VA.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.VA.index, columns=self.VA.columns)
    
                        self.va_c.loc[VA_m.loc[index[i],header[0]],(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])] = \
                            my_va.loc[VA_m.loc[index[i],header[0]],(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])].values \
                                
                # If changes are going to implemented on the aggregated level
                elif  VA_m.loc[index[i],'Aggregated'] == 'Yes':
                    

                    if VA_m.loc[index[i],'type'] == 'Percentage':
                        
                        self.va_c.loc[(slice(None), slice(None), slice(None), VA_m.loc[index[i],header[0]]),(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])] = \
                            self.va.loc[(slice(None), slice(None), slice(None),VA_m.loc[index[i],header[0]]),(VA_m.loc[index[i],header[1]],VA_m.loc[index[i],header[2]])].values \
                                * ( 1 + VA_m.loc[index[i],header[4]])
                        
                        
                    
        if S:
            
            S_m = pd.read_excel(path, sheet_name = 'S', index_col = [0] , header = [0])
            
            header = list(S_m.columns)
            index  = list(S_m.index)

            
            for i in range(len(S_m)): 
                
                if S_m.loc[index[i],header[2]] == 'Percentage':
                    
                    self.s_c.loc[S_m.loc[index[i],header[0]],('Activities',S_m.loc[index[i],header[1]])] = \
                        self.s.loc[S_m.loc[index[i],header[0]],('Activities',S_m.loc[index[i],header[1]])].values \
                            * ( 1 + S_m.loc[index[i],header[3]])
                    
##################################################################################################################              

    def Save_all(self, path='Result',level = None,drop='unused'):
        
        import pandas as pd
        import xlsxwriter
        
        if drop != None:
        
            S   = self.S.drop(drop,level = 3)
            S_c = self.S_c.drop(drop,level = 3)
            s   = self.s.drop(drop,level = 3)
            s_c = self.s_c.drop(drop,level = 3)
            S_agg   = self.S_agg.drop(drop)
            S_c_agg = self.S_c_agg.drop(drop) 
            
            VA   = self.VA.drop(drop,level = 3)
            VA_c = self.VA_c.drop(drop,level = 3)
            va   = self.va.drop(drop,level = 3)
            va_c = self.va_c.drop(drop,level = 3)
            VA_agg   = self.VA_agg.drop(drop)
            VA_c_agg = self.VA_c_agg.drop(drop)    
            
        elif drop == None:

            S   = self.S
            S_c = self.S_c
            s   = self.s
            s_c = self.s_c
            S_agg   = self.S_agg
            S_c_agg = self.S_c_agg
            
            VA   = self.VA
            VA_c = self.VA_c
            va   = self.va
            va_c = self.va_c
            VA_agg   = self.VA_agg
            VA_c_agg = self.VA_c_agg
            

            
        if level == None:
            
            try:
        
                with pd.ExcelWriter(path + '\ Shock_agg_flows.xlsx') as writer:
                    
                    self.Z_c_agg.to_excel(writer,sheet_name='Z')
                    self.X_c_agg.to_excel(writer,sheet_name='X')
                    VA_c_agg.to_excel(writer,sheet_name='VA')
                    S_c_agg.to_excel(writer,sheet_name='S')
                    self.Y_c_agg.to_excel(writer,sheet_name='Y')
                    
                with pd.ExcelWriter(path + '\ Shock_coeff.xlsx') as writer:
                    
                    self.z_c.to_excel(writer,sheet_name='z')
                    va_c.to_excel(writer,sheet_name='va')
                    s_c.to_excel(writer,sheet_name='s')
        
                with pd.ExcelWriter(path + '\ Baseline_agg_flows.xlsx') as writer:
                    
                    self.Z_agg.to_excel(writer,sheet_name='Z')
                    self.X_agg.to_excel(writer,sheet_name='X')
                    VA_agg.to_excel(writer,sheet_name='VA')
                    S_agg.to_excel(writer,sheet_name='S')
                    self.Y_agg.to_excel(writer,sheet_name='Y')
                    
                with pd.ExcelWriter(path + '\ Baseline_coeff.xlsx') as writer:
                    
                    self.z.to_excel(writer,sheet_name='z')
                    va.to_excel(writer,sheet_name='va')
                    s.to_excel(writer,sheet_name='s')
    
                with pd.ExcelWriter(path + '\ Baseline_flows.xlsx') as writer:
                    
                    self.Z.to_excel(writer,sheet_name='Z')
                    self.X.to_excel(writer,sheet_name='X')
                    VA.to_excel(writer,sheet_name='VA')
                    S.to_excel(writer,sheet_name='S')
                    self.Y.to_excel(writer,sheet_name='Y')
                    
                with pd.ExcelWriter(path + '\ Shock_flows.xlsx') as writer:
                    
                    self.Z_c.to_excel(writer,sheet_name='Z')
                    self.X_c.to_excel(writer,sheet_name='X')
                    VA_c.to_excel(writer,sheet_name='VA')
                    S_c.to_excel(writer,sheet_name='S')
                    self.Y_c.to_excel(writer,sheet_name='Y') 
                    
                    
                with pd.ExcelWriter(path + '\ Change_flows.xlsx') as writer:

                    (self.X_c-self.X).to_excel(writer,sheet_name='X')
                    (VA_c-VA).to_excel(writer,sheet_name='VA')
                    (S_c-S).to_excel(writer,sheet_name='S')
                    (self.X_c_agg-self.X_agg).to_excel(writer,sheet_name='X_agg')
                    (VA_c_agg-VA_agg).to_excel(writer,sheet_name='VA_agg')
                    (S_c_agg-S_agg).to_excel(writer,sheet_name='S_agg')                                                                         
            except:
                raise ValueError('No Shock Implemented so, the level could be only {}'.format('baseline'))
                
                
        elif level=='baseline':

    
            with pd.ExcelWriter(path + '\ Baseline_agg_flows.xlsx') as writer:
                
                self.Z_agg.to_excel(writer,sheet_name='Z')
                self.X_agg.to_excel(writer,sheet_name='X')
                VA_agg.to_excel(writer,sheet_name='VA')
                S_agg.to_excel(writer,sheet_name='S')
                self.Y_agg.to_excel(writer,sheet_name='Y')
                
            with pd.ExcelWriter(path + '\ Baseline_coeff.xlsx') as writer:
                
                self.z.to_excel(writer,sheet_name='z')
                va.to_excel(writer,sheet_name='va')
                s.to_excel(writer,sheet_name='s')

            with pd.ExcelWriter(path + '\ Baseline_flows.xlsx') as writer:
                
                self.Z.to_excel(writer,sheet_name='Z')
                self.X.to_excel(writer,sheet_name='X')
                VA.to_excel(writer,sheet_name='VA')
                S.to_excel(writer,sheet_name='S')
                self.Y.to_excel(writer,sheet_name='Y')
                
              
        elif level=='shock':
            
            with pd.ExcelWriter(path + '\ Shock_agg_flows.xlsx') as writer:
                
                self.Z_c_agg.to_excel(writer,sheet_name='Z')
                self.X_c_agg.to_excel(writer,sheet_name='X')
                VA_c_agg.to_excel(writer,sheet_name='VA')
                S_c_agg.to_excel(writer,sheet_name='S')
                self.Y_c_agg.to_excel(writer,sheet_name='Y')
                
            with pd.ExcelWriter(path + '\ Shock_coeff.xlsx') as writer:
                
                self.z_c.to_excel(writer,sheet_name='z')
                va_c.to_excel(writer,sheet_name='va')
                s_c.to_excel(writer,sheet_name='s')

                
            with pd.ExcelWriter(path + '\ Shock_flows.xlsx') as writer:
                
                self.Z_c.to_excel(writer,sheet_name='Z')
                self.X_c.to_excel(writer,sheet_name='X')
                VA_c.to_excel(writer,sheet_name='VA')
                S_c.to_excel(writer,sheet_name='S')
                self.Y_c.to_excel(writer,sheet_name='Y') 

                          

##################################################################################################################

#In this part of the code new functions for doing graphs will be added:
#the graphs will be divided into two different categories:
#    1. Shock graphs in which the user can do the graphs automatically for the 
#        baseline and the shock different
#    2. A general graph function in which user can choose what to graph        
    

    def plot_dx(self, aggregation=True, kind='bar', unit='M KSH', stacked=True, level=None, percent=False,ranshow=(0,0)):
        import matplotlib.pyplot as plt
        import EX_func
        plt.style.use(['ggplot'])

        
        # To check if the shock is implemented or not
        try:
            a = self.X_c
        except:
            raise ValueError('This function can not be used if no shock is impemented')
            
        # Checking the unit that user want to use for doing graphs
        if unit == 'M KSH':
            ex_rate = 1.0
        elif unit == 'M USD':
            ex_rate = 0.00939548
        elif unit == 'K USD':
            ex_rate = 0.00939548*1000
        elif unit == 'K EUR':
            ex_rate = 0.00833961*1000
            
        elif unit !='M KSH' or 'M USD'or'K USD'or'K EUR' :
            raise ValueError('The unit should be {} or {}'.format('M KSH','M USD','K USD','K EUR'))
        
        # Finding if the graphs should be aggregated or not
        if aggregation: 
            
            try:
                old = self.X_agg.copy()
                new = self.X_c_agg.copy()
            except: 
                raise ValueError('There is no aggregated result of {} and {}. Please Run the aggregation function first'.format('Baseline Prodction','New Production'))
                
        elif aggregation == False:
            
            old = self.X.copy()
            new = self.X_c.copy()
            ind=[old.index.get_level_values(0),old.index.get_level_values(1)]
            old.index=ind
            new.index=ind
            
        if level == None:
            old = old
            new = new
        
        elif level == 'Activities' or 'Commodities':
            
            old = old.loc[level]
            new = new.loc[level]
            
        elif level != None or 'Activities' or 'Commodities':
            
            raise ValueError('The level should be {}, {} or {}'.format('None','Activities','Commodities'))
        
        if percent:
            dx = (new - old)/old
            unit = '%'
            
        if percent == False:
            dx = (new - old) * ex_rate
            
        if level == None:
            title=''
        else:
            title=' by '+str(level)
        dx=EX_func.drop_fun(data=dx.T, ranshow=ranshow)
        dx=dx.T
        dx.plot(kind=kind, stacked=stacked)
        plt.title('Production Change'+title)
        plt.ylabel(unit)
        plt.legend(loc = 1,bbox_to_anchor = (1.5,1))
        plt.show()
        
  
    def plot_dv(self,aggregation=True, kind='bar', unit='M KSH', stacked=True, level=None, drop='unused', percent=False, main_title = 'default', color='terrain',ranshow=(0,0)):
        
        import matplotlib.pyplot as plt
        import EX_func
        plt.style.use(['ggplot'])
        
        # To check if the shock is implemented or not
        try:
            a = self.X_c
        except:
            raise ValueError('This function can not be used if no shock is impemented')
            
        # Checking the unit that user want to use for doing graphs
        if unit == 'M KSH':
            ex_rate = 1.0
        elif unit == 'M USD':
            ex_rate = 0.00939548
        elif unit == 'K USD':
            ex_rate = 0.00939548*1000
        elif unit == 'K EUR':
            ex_rate = 0.00833961*1000
            
            
        elif unit !='M KSH' or 'M USD'or'K USD'or'K EUR' :
            raise ValueError('The unit should be {} , {},{} or {}'.format('M KSH','M USD','K USD','K EUR'))
        
        # Finding if the graphs should be aggregated or not
        if aggregation: 

            
            try:

                old = self.VA_agg.copy()

                new = self.VA_c_agg.copy()
            except: 
                raise ValueError('There is no aggregated result of {} and {}. Please Run the aggregation function first'.format('Baseline Prodction','New Production'))
                
        elif aggregation == False:
            
            old = self.VA.copy()
            new = self.VA_c.copy()
            ind=old.index.get_level_values(0)
            col=[old.columns.get_level_values(0),old.columns.get_level_values(1)]
            old.index=ind
            new.index=ind
            old.columns=col
            new.columns=col
            
        if level == None:
            old = old
            new = new
        
        elif level == 'Activities' or 'Commodities':
            
            old = old[level]
            new = new[level]
            
        elif level != None or 'Activities' or 'Commodities':
            
            raise ValueError('The level should be {}, {} or {}'.format('None','Activities','Commodities'))
        
        if percent:
            dv = (new - old) / old
            unit = '%'
            
        if percent == False:
            dv = (new - old) * ex_rate
        
        if main_title == 'default':        
            if level == None:
                title='Value Added Change'
            else:
                title='Value Added Change by '+str(level)
        
        else:
             title = main_title
        
        if aggregation == True:
            dv = dv.drop(drop)
            
        dv=EX_func.drop_fun(data=dv,ranshow=ranshow)
        dv=dv.T
        
        
        dv.plot(kind = kind , stacked = stacked, colormap=color)
        plt.title(title)
        plt.ylabel(unit)
        plt.legend(loc = 1,bbox_to_anchor = (1.8,1))
        plt.show()        

    
    def plot_dp(self,aggregation = True,level = None):
        
        import matplotlib.pyplot as plt
        import seaborn as sns
        plt.style.use(['ggplot'])
        
        # To check if the shock is implemented or not
        try:
            a = self.X_c
        except:
            raise ValueError('This function can not be used if no shock is impemented')
            
        # Finding if the graphs should be aggregated or not
        if aggregation: 

            
            try:

                old = self.p_agg

                new = self.p_c_agg
            except: 
                raise ValueError('There is no aggregated result of {} and {}. Please Run the aggregation function first'.format('Baseline Prodction','New Production'))
                
        elif aggregation == False:
            
            old = self.p
            new = self.p_c
            
        if level == None:
            old = old
            new = new
        
        elif level == 'Activities' or 'Commodities':
            
            old = old[level]
            new = new[level]
            
        elif level != None or 'Activities' or 'Commodities':
            
            raise ValueError('The level should be {}, {} or {}'.format('None','Activities','Commodities'))

        dp = new/old
        dp = dp.T
        
        fig = plt.figure()
        ax = sns.heatmap(dp , annot=False)

        
        # dp.plot(kind = kind )
        # plt.title('Price Change')
        plt.ylabel('price ratio')
        # plt.legend(loc = 1,bbox_to_anchor = (1.5,1))
        plt.show()    
    
    
    def plot_dS(self, details=True, kind='bar', stacked=True, indicator='CO2', Type='absolute',main_title = 'default',color ='terrain'):
        
        import matplotlib.pyplot as plt
        plt.style.use(['ggplot'])
        
        # To check if the shock is implemented or not
        # try:
        #     a = self.X_c
        # except:
        #     raise ValueError('This function can not be used if no shock is impemented')
            
        
        # set the title
            
        if main_title == 'default':
            title = 'Change in {}'.format(indicator)
        else:
            title = main_title

            
        check = 0
        S_list = self.S_agg.index.to_list()
        
        for i in S_list:
            if indicator == i :
                check = 1
                break
            else:
                check = 0
        
        if check == 0:
            raise ValueError('indicator {} does not exist in the indictors'.format(indicator))
            
        # Finding if the graphs should be aggregated or not
        if details: 
            
            old = self.S.loc[(slice(None),slice(None),slice(None),indicator),'Activities'].groupby(axis=1,level=3).sum()
            new = self.S_c.loc[(slice(None),slice(None),slice(None),indicator),'Activities'].groupby(axis=1,level=3).sum()
            
            old.index = old.index.get_level_values(0)
            new.index = old.index


        elif details == False:
            try:
                old = self.S_agg
                new = self.S_c_agg
                old = old.loc[indicator,'Activities']
                new = new.loc[indicator,'Activities']
            except:
                raise ValueError('There is no aggregated result of {} and {}. Please Run the aggregation function first'.format('Baseline Prodction','New Production'))

        # To Take the unit
        
        if Type == 'percentage':
            
            unit = "%"
            
            dS = (new  - old) / old * 100
            dS=dS.groupby(level=0).sum().T
            
            if details:
                dS.plot(kind = kind , stacked = stacked,colormap=color)
                plt.title(title)     
                plt.legend(loc = 1,bbox_to_anchor = (1.9,1))
                plt.ylabel(unit)
                
            if details == False:
                dS.plot(kind = kind , stacked = stacked,legend=False,colormap=color)
                plt.title(title)  
                plt.ylabel(unit)
                
        if Type == 'absolute':
            
            if indicator=='CO2':
                unit="ton"
            
            else:
                if indicator=='Green Water':
                    unit='m$^3$'
                else:                
                    unit='?'
            
            
            dS = (new  - old)*1000 
            
            dS=dS.groupby(level=0).sum().T
            
            if details:
                dS.plot(kind = kind , stacked = stacked,colormap=color)
                plt.title(title)     
                plt.legend(loc = 1,bbox_to_anchor = (1.9,1))
                plt.ylabel(unit)
            if details == False:
                dS.plot(kind = kind , stacked = stacked,legend=False,colormap=color)
                plt.title(title)  
                plt.ylabel(unit)
                
        if Type == 'change':
            
            unit = "?"
            
            coffee = new['HIGH RAINFALL (CP)'] + new['COFFEE PROD']
            print(coffee)
            dS = (new  - old)  / coffee.values
            print(dS)
            dS=dS.T
            
            if details:
                dS.plot(kind = kind , stacked = stacked)
                plt.title(title)     
                plt.legend(loc = 1,bbox_to_anchor = (1.7,1))
                plt.ylabel(unit)
            if details == False:
                dS.plot(kind = kind , stacked = stacked,legend=False,colormap=color)
                plt.title(title)  
                plt.ylabel(unit)           
        plt.show()  
      


    def add_dict(self):
                
        self.results['Z_' + str(self.counter)]= self.Z_c
        self.results['X_' + str(self.counter)]= self.X_c
        self.results['VA_'+ str(self.counter)]= self.VA_c
        self.results['p_' + str(self.counter)]= self.p_c
        self.results['Y_' + str(self.counter)]= self.Y_c
        self.results['va_' + str(self.counter)]= self.va_c
        self.results['z_' + str(self.counter)]= self.z_c
        self.results['S_' + str(self.counter)]= self.S_c
        self.results['S_agg_' + str(self.counter)]= self.S_c_agg
        
        self.counter += 1

    def Int_Ass(self,inv_sen=['main',1],sav_sen=['main',2],sce_name='Unknown',directory=r'Optimization\Optimization.xlsx',imports=['Import'],w_ext=['Green Water'], em_ext=['CO2'], land=['Land'], labour=['Labor - Skilled','Labor - Semi Skilled','Labor - Unskilled'],capital=['Capital - Machines']):
        import pandas as pd
        
        # Let's assume that the inv and sav senario is the same for sensitivity and main results
        
        # There are different possibilities for intervent assessments. First of all we shoudl define the levels:
        # the investment and the saving scenarios can be in sensitivity levels or in the main level
        
        # if inv_sce[0]=='main':
        #     inv_par = str(inv_sen[1])
            
        # elif inv_sce[0]=='sensitivity':
        #     inv_par = 's_'+str(inv_sen[1])
        # else:
        #     raise ValueError ('The Investment scenario could be main or sensitivity') 
            
        # if sav_sce[0]=='main':
        #     sav_par = str(sav_sce[1])
        # elif sav_sce[0] == 'sensitivity':
        #     sav_par = 's_' + str(sav_sce[1])
        # else:
        #     raise ValueError ('The Investment scenario could be main or sensitivity')         
        
        
           
        OPT = pd.read_excel(directory,sheet_name='input',index_col=[0,1],header=[0,1])
        
        if inv_sen[0]=='main' and sav_sen[0]=='main':
            
        
        # Calculateing different invoces using dictionaries and the number of senarios
            INV = self.results['VA_'+ str(inv_sen[1])].values.sum().sum() - self.VA.sum().sum()
            SAV = -self.results['VA_'+ str(sav_sen[1])].values.sum().sum() + self.VA.sum().sum()
            
            W_I =  self.results['S_agg_' + str(inv_sen[1])].loc[w_ext].sum().sum() - self.S_agg.loc[w_ext].sum().sum()
            W_S = -self.results['S_agg_' + str(sav_sen[1])].loc[w_ext].sum().sum() + self.S_agg.loc[w_ext].sum().sum()
            
            E_I =  self.results['S_agg_' + str(inv_sen[1])].loc[em_ext].sum().sum() - self.S_agg.loc[em_ext].sum().sum()
            E_S = -self.results['S_agg_' + str(sav_sen[1])].loc[em_ext].sum().sum() + self.S_agg.loc[em_ext].sum().sum()    
            
            L_I =  self.results['S_agg_' + str(inv_sen[1])].loc[land].sum().sum() - self.S_agg.loc[land].sum().sum()
            L_S = -self.results['S_agg_' + str(sav_sen[1])].loc[land].sum().sum() + self.S_agg.loc[land].sum().sum()    

            F_I = self.results['VA_'+ str(inv_sen[1])].groupby(level=3).sum().loc[labour].sum().sum() - self.VA.groupby(level=3).sum().loc[labour].sum().sum()   
            F_S = -self.results['VA_'+ str(sav_sen[1])].groupby(level=3).sum().loc[labour].sum().sum() + self.VA.groupby(level=3).sum().loc[labour].sum().sum() 
            
            C_I = self.results['VA_'+ str(inv_sen[1])].groupby(level=3).sum().loc[capital].sum().sum() - self.VA.groupby(level=3).sum().loc[capital].sum().sum()
            C_S = -self.results['VA_'+ str(sav_sen[1])].groupby(level=3).sum().loc[capital].sum().sum() + self.VA.groupby(level=3).sum().loc[capital].sum().sum()
            
            IM_I = self.results['VA_'+ str(inv_sen[1])].groupby(level=3).sum().loc[imports].sum().sum() - self.VA.groupby(level=3).sum().loc[imports].sum().sum()
            IM_S = -self.results['VA_'+ str(sav_sen[1])].groupby(level=3).sum().loc[imports].sum().sum() + self.VA.groupby(level=3).sum().loc[imports].sum().sum()   
            
            
            # Writing the results on the data frame
            # OPT.loc['Scenario',('ROI','years')]=self.ROI
            OPT.loc['Scenario',('Saving','M kSh/FU')]=SAV
            
            OPT.loc['Scenario',('Investment','M kSh')]=INV
            
            OPT.loc['Scenario',('Water Saving','m3/FU')]=W_S 
            OPT.loc['Scenario',('Water Investment','m3/FU')]=W_I
            
            OPT.loc['Scenario',('Emission Saving','kton/FU')]=E_S 
            OPT.loc['Scenario',('Emission Investment','kton/FU')]=E_I
    
            OPT.loc['Scenario',('Land Saving','kha/FU')]=L_S           
            OPT.loc['Scenario',('Land Investment','kha/FU')]=L_I           
    
            OPT.loc['Scenario',('Workforce Saving','M kSh/FU')]=F_S           
            OPT.loc['Scenario',('Workforce Investment','M kSh/FU')]=F_I 
            
            OPT.loc['Scenario',('Capital Saving','M kSh/FU')] = C_S
            OPT.loc['Scenario',('Capital Investment','M kSh/FU')] = C_I
            
            OPT.loc['Scenario',('Import Saving','M kSh/FU')] = IM_S
            OPT.loc['Scenario',('Import Investment','M kSh/FU')] = IM_I  
            
            OPT.loc['Scenario',('PROI','M kSh/FU')] = SAV / INV 
            OPT.loc['Scenario',('PPBT','years')] = INV / SAV
            
            # Total Impacts
            OPT.loc['Scenario',('Water Total Impact','m3/FU')] = W_I + self.UL * W_S
            OPT.loc['Scenario',('Emission Total Impact','kton/FU')] = E_I + self.UL * E_S
            OPT.loc['Scenario',('Land Total Impact','kha/FU')] = L_I + self.UL * L_S
            OPT.loc['Scenario',('Import Total Impact','M kSh/FU')] = IM_I + self.UL * IM_S
            OPT.loc['Scenario',('Workforce Total Impact','M kSh/FU')] = F_I + self.UL * F_S
            OPT.loc['Scenario',('Capital Total Impact','M kSh/FU')] = C_I + self.UL * C_S
            
            
            
            
            
        if inv_sen[0]=='main' and sav_sen[0]=='sensitivity':
            indeces=list(self.S_s_agg.index.get_level_values(0))
            indeces = list(dict.fromkeys(indeces))
            
            
            for i in indeces:
                # Investments 
                
                INV = self.results['VA_'+ str(inv_sen[1])].values.sum().sum() - self.VA.sum().sum()  
                W_I =  self.results['S_agg_' + str(inv_sen[1])].loc[w_ext].sum().sum() - self.S_agg.loc[w_ext].sum().sum()
                E_I =  self.results['S_agg_' + str(inv_sen[1])].loc[em_ext].sum().sum() - self.S_agg.loc[em_ext].sum().sum()                
                L_I = self.results['S_agg_' + str(inv_sen[1])].loc[land].sum().sum() - self.S_agg.loc[land].sum().sum() 
                F_I = self.results['VA_'+ str(inv_sen[1])].groupby(level=3).sum().loc[labour].sum().sum() - self.VA.groupby(level=3).sum().loc[labour].sum().sum()   
                C_I = self.results['VA_'+ str(inv_sen[1])].groupby(level=3).sum().loc[capital].sum().sum() - self.VA.groupby(level=3).sum().loc[capital].sum().sum()            
                IM_I = self.results['VA_'+ str(inv_sen[1])].groupby(level=3).sum().loc[imports].sum().sum() - self.VA.groupby(level=3).sum().loc[imports].sum().sum()
                
                OPT.loc[i,('Investment','M kSh')]=INV
                OPT.loc[i,('Water Investment','m3/FU')]=W_I
                OPT.loc[i,('Emission Investment','kton/FU')]=E_I
                OPT.loc[i,('Land Investment','kha/FU')]=L_I           
                OPT.loc[i,('Workforce Investment','M kSh/FU')]=F_I  
                OPT.loc[i,('Capital Investment','M kSh/FU')] = C_I
                OPT.loc[i,('Import Investment','M kSh/FU')] = IM_I                 
              
                SAV = -self.results['VA_s_'+ str(sav_sen[1])].loc[i].values.sum().sum() + self.VA.sum().sum()
                W_S = -self.results['S_s_agg_' + str(sav_sen[1])].loc[i].loc[w_ext].sum().sum() + self.S_agg.loc[w_ext].sum().sum()
                E_S = -self.results['S_s_agg_' + str(sav_sen[1])].loc[i].loc[em_ext].sum().sum() + self.S_agg.loc[em_ext].sum().sum()         
                L_S = -self.results['S_s_agg_' + str(sav_sen[1])].loc[i].loc[land].sum().sum() + self.S_agg.loc[land].sum().sum()         
                F_S = -self.results['VA_s_'+ str(sav_sen[1])].groupby(level=[0,4]).sum().loc[i].loc[labour].sum().sum() + self.VA.groupby(level=3).sum().loc[labour].sum().sum() 
                C_S = -self.results['VA_s_'+ str(sav_sen[1])].groupby(level=[0,4]).sum().loc[i].loc[capital].sum().sum() + self.VA.groupby(level=3).sum().loc[capital].sum().sum()
                IM_S = -self.results['VA_s_'+ str(sav_sen[1])].groupby(level=[0,4]).sum().loc[i].loc[imports].sum().sum() + self.VA.groupby(level=3).sum().loc[imports].sum().sum() 
                    
          
                OPT.loc[i,('Saving','M kSh/FU')]=SAV
                OPT.loc[i,('Water Saving','m3/FU')]=W_S                 
                OPT.loc[i,('Emission Saving','kton/FU')]=E_S        
                OPT.loc[i,('Land Saving','kha/FU')]=L_S           
                OPT.loc[i,('Workforce Saving','M kSh/FU')]=F_S       
                OPT.loc[i,('Import Saving','M kSh/FU')] = IM_S
                OPT.loc[i,('Capital Saving','M kSh/FU')] = C_S
                
                # Total Impacts
                OPT.loc[i,('Water Total Impact','m3/FU')] = W_I + self.UL * W_S
                OPT.loc[i,('Emission Total Impact','kton/FU')] = E_I + self.UL * E_S
                OPT.loc[i,('Land Total Impact','kha/FU')] = L_I + self.UL * L_S
                OPT.loc[i,('Import Total Impact','M kSh/FU')] = IM_I + self.UL * IM_S
                OPT.loc[i,('Workforce Total Impact','M kSh/FU')] = F_I + self.UL * F_S
                OPT.loc[i,('Capital Total Impact','M kSh/FU')] = C_I + self.UL * C_S


                OPT.loc[i,('PROI','M kSh/FU')] = SAV / INV 
                OPT.loc[i,('PPBT','years')] = INV / SAV   
                
        if inv_sen[0]=='sensitivity' and sav_sen[0]=='main':
            indeces=list(self.S_s_agg.index.get_level_values(0))
            indeces = list(dict.fromkeys(indeces))
            
            
            for i in indeces:
                # Investments 
                
                INV = self.results['VA_s_'+ str(inv_sen[1])].loc[i].values.sum().sum() - self.VA.sum().sum()  
                W_I =  self.results['S_s_agg_' + str(inv_sen[1])].loc[i].loc[w_ext].sum().sum() - self.S_agg.loc[w_ext].sum().sum()
                E_I =  self.results['S_s_agg_' + str(inv_sen[1])].loc[i].loc[em_ext].sum().sum() - self.S_agg.loc[em_ext].sum().sum()
                L_I =  self.results['S_s_agg_' + str(inv_sen[1])].loc[i].loc[land].sum().sum() - self.S_agg.loc[land].sum().sum()
                F_I = self.results['VA_s_'+ str(inv_sen[1])].groupby(level=[0,4]).sum().loc[i].loc[labour].sum().sum() - self.VA.groupby(level=3).sum().loc[labour].sum().sum()   
                C_I = self.results['VA_s_'+ str(inv_sen[1])].groupby(level=[0,4]).sum().loc[i].loc[capital].sum().sum() - self.VA.groupby(level=3).sum().loc[capital].sum().sum()            
                IM_I = self.results['VA_s_'+ str(inv_sen[1])].groupby(level=[0,4]).sum().loc[i].loc[imports].sum().sum() - self.VA.groupby(level=3).sum().loc[imports].sum().sum()
                
                OPT.loc[i,('Investment','M kSh')]=INV
                OPT.loc[i,('Water Investment','m3/FU')]=W_I
                OPT.loc[i,('Emission Investment','kton/FU')]=E_I
                OPT.loc[i,('Land Investment','M kSh/FU')]=L_I           
                OPT.loc[i,('Workforce Investment','M kSh/FU')]=F_I  
                OPT.loc[i,('Capital Investment','M kSh/FU')] = C_I
                OPT.loc[i,('Import Investment','M kSh/FU')] = IM_I                 
              
                SAV = -self.results['VA_'+ str(sav_sen[1])].values.sum().sum() + self.VA.sum().sum()
                W_S = -self.results['S_agg_' + str(sav_sen[1])].loc[w_ext].sum().sum() + self.S_agg.loc[w_ext].sum().sum()
                E_S = -self.results['S_agg_' + str(sav_sen[1])].loc[em_ext].sum().sum() + self.S_agg.loc[em_ext].sum().sum()         
                L_S = -self.results['S_agg_' + str(sav_sen[1])].loc[land].sum().sum() + self.S_agg.loc[land].sum().sum()         
                F_S = -self.results['VA_'+ str(sav_sen[1])].groupby(level=3).sum().loc[labour].sum().sum() + self.VA.groupby(level=3).sum().loc[labour].sum().sum() 
                C_S = -self.results['VA_'+ str(sav_sen[1])].groupby(level=3).sum().loc[capital].sum().sum() + self.VA.groupby(level=3).sum().loc[capital].sum().sum()
                IM_S = -self.results['VA_'+ str(sav_sen[1])].groupby(level=3).sum().loc[imports].sum().sum() + self.VA.groupby(level=3).sum().loc[imports].sum().sum() 
                    
          
                OPT.loc[i,('Saving','M kSh/FU')]=SAV
                OPT.loc[i,('Water Saving','m3/FU')]=W_S                 
                OPT.loc[i,('Emission Saving','kton/FU')]=E_S        
                OPT.loc[i,('Land Saving','kha/FU')]=L_S           
                OPT.loc[i,('Workforce Saving','M kSh/FU')]=F_S                             
                OPT.loc[i,('Import Saving','M kSh/FU')] = IM_S
                OPT.loc[i,('Capital Saving','M kSh/FU')] = C_S
                
                OPT.loc[i,('Water Total Impact','m3/FU')] = W_I + self.UL * W_S
                OPT.loc[i,('Emission Total Impact','kton/FU')] = E_I + self.UL * E_S
                OPT.loc[i,('Land Total Impact','kha/FU')] = L_I + self.UL * L_S
                OPT.loc[i,('Import Total Impact','M kSh/FU')] = IM_I + self.UL * IM_S
                OPT.loc[i,('Workforce Total Impact','M kSh/FU')] = F_I + self.UL * F_S
                OPT.loc[i,('Capital Total Impact','M kSh/FU')] = C_I + self.UL * C_S      

                OPT.loc[i,('PROI','M kSh/FU')] = SAV / INV 
                OPT.loc[i,('PPBT','years')] = INV / SAV   
                
        if inv_sen[0]=='sensitivity' and sav_sen[0]=='sensitivity':
            
            raise ValueError ("Only one senseitivty parameter can be analyzed!")

                
        self.OPT = OPT        
        save_dir = r'Optimization\ ' + sce_name + '.xlsx'
        with pd.ExcelWriter(save_dir) as writer:
            OPT.to_excel(writer)
            
        
    def optimize(self,scenario):
        import cvxpy as cp
        import numpy as np
        import pandas as pd
        
        VA_const = self.VA.sum(axis=1).values.reshape(len(self.VA),1)
        
        shares = self.Y.values / self.Y.sum().values
        
        va = self.results['va_'+ str(scenario)].values
        z  = self.results['z_' + str(scenario)].values
        
        
        x = cp.Variable(shares.shape,nonneg=True)
        
        VA = va @ x
        
        L = np.identity(len(z))-z
        Y  = L @ x 
        
        obj = cp.atoms.affine.sum.sum(Y)
        
        
        
        objective= cp.Maximize(obj)
        
        Y_const = cp.atoms.affine.binary_operators.multiply(shares,obj)
        
        Y_const_2 = Y_const + z @ x - x
        
        constraints = [VA-VA_const<=0 ,Y_const_2 <= 0]
        
        problem = cp.Problem(objective,constraints)
        
        result = problem.solve(verbose=True)
        

        self.Y_opt = pd.DataFrame(Y.value,index=self.Y.index,columns = self.Y.columns)
        self.X_opt = pd.DataFrame(x.value,index=self.X.index,columns = self.X.columns)     
        
        

###################################  ###################################      
        # Sensitivity Module
###################################  ###################################    


        
        
        
    def sensitivity (self,parameter,aggregat=True,add_dict=True):

        
        import pandas as pd
        import numpy as np
        
        print('Only one parameter can be changed for the sensitivity analysis. The parameter should be identified in the excel file.\n')
        print('To run the sensitvity function, user needs to run the shock function before.\n')
        # Why? because there is not only one change. So. it is necessary to have the other changes then make a sensitivity analysis only in one parameter!
        

        
        inp = pd.read_excel(self.sh_path,sheet_name = parameter , index_col=[0], header =[0]) 
            
        indeces = list(inp.index)
        headers = list(inp.columns)
        
        # To find the invoice in which sensitivity needs to be done!
        a=1 # This parameter shows if a sensitivity parametere is identified or not.
        for  i in indeces:
            if inp.loc[i,"Sensistivity"]=='Yes':
                a=1
                break
            else:
                a=0
                
        if a==0:
            raise ValueError('No sensitivity is identified. To identify a sensitivity analysis, the user needs to chechk the input excel file')                
                
        # depending on the parameter that we want to have a sensitivity analysis, the code will be differenert
        # general parameters:
                # sen_min: Minimum value for the sensitivity
                # sen_max: Maximum value for the sensitivity
                # sen_step: sensitivity intervals

        
        sen_min = inp.loc[i,'Min']
        sen_max = inp.loc[i,'Max']
        sen_step = inp.loc[i,'Step']
        
        self.sen_min = sen_min
        self.sen_max = sen_max
        
        
        if parameter == 'Z':
            
            # for the Z matrix:
            # par_0: level_row
            # par_1: row
            # par_2: level_col
            # par_3: col
            # par_4: type
            # par_5: Aggregated
            
            
            par_0 = inp.loc[i,'level_row']
            par_1 = inp.loc[i,'row']            
            par_2 = inp.loc[i,'level_col']            
            par_3 = inp.loc[i,'col']            
            par_4 = inp.loc[i,'type']  
            par_5 = inp.loc[i,'Aggregated']
            
            self.sen_par = '{}, {}: {} , {}: {}.'.format('Z',par_0,par_1,par_2,par_3)
            
            # To rearrange the indeces or columns
            
            
            # to save the sensitivity results, we need to build a dataframe
            
            # Make a copy of the matrix which is going to be changed.
            

            
            if par_5 == 'No':
                
                if par_4 == 'Absolute': 
                    
                    my_Z = self.Z_c.copy()
                    my_z = self.z_c.copy()
                    # Calculating the first step to form the dataframes
                    my_Z.loc[(par_0,par_1),(par_2,par_3)] = self.Z.loc[(par_0,par_1),(par_2,par_3)].values + sen_min
                    
                    my_z0 = pd.DataFrame(my_Z.values @ np.linalg.inv (self.X.values * np.identity(len(self.X))),index = self.Z.index , columns = self.Z.columns)
                    my_z.loc[(par_0,par_1),(par_2,par_3)]  = my_z0.loc[(par_0,par_1),(par_2,par_3)].values
                    # BIG QUESTION
                    l_s = np.linalg.inv(np.identity(len(my_z))-my_z) 
                    X_s_0 = pd.DataFrame(l_s @ self.Y_c.values,index=self.X.index,columns=[str(sen_min)])
                    
                    VA_s_0 = pd.DataFrame(self.va_c.values @ (X_s_0.values  * np.identity(len(X_s_0.values))),index = self.VA_ind,columns =  self.Z.columns) 
                    VA_s_0 = pd.concat([VA_s_0],keys=[str(sen_min)], names=['Scenario'])
                    
                    S_s_0  = pd.DataFrame(self.s_c.values @ (X_s_0.values * np.identity(len(X_s_0.values))),index=self.S.index,columns = self.S.columns)
                    S_s_0  = pd.concat([S_s_0],keys=[str(sen_min)],names=['Scenario'])
                    

                    

                    j = sen_min + sen_step
                    
                    while (j<=sen_max):
                        
                        my_Z.loc[(par_0,par_1),(par_2,par_3)] =  self.Z.loc[(par_0,par_1),(par_2,par_3)].values + j
                        my_z0 = pd.DataFrame(my_Z.values @ np.linalg.inv (self.X.values * np.identity(len(self.X))),index = self.Z.index , columns = self.Z.columns)
                        my_z.loc[(par_0,par_1),(par_2,par_3)]  = my_z0.loc[(par_0,par_1),(par_2,par_3)].values
                        
                        l_s = np.linalg.inv(np.identity(len(my_z))-my_z)
                        
                        X_s = pd.DataFrame(l_s @ self.Y_c.values,index=self.X.index,columns=[str(round(j,15))])
                        
                        X_s_0 = pd.concat([X_s_0,X_s],axis=1)
                        
                        VA_s = pd.DataFrame(self.va_c.values @ (X_s.values * np.identity(len(X_s.values))),index = self.VA_ind,columns =  self.Z.columns) 
                        
                        VA_s = pd.concat([VA_s],keys=[str(round(j,15))], names=['Scenario'])
                        
                        VA_s_0 = pd.concat([VA_s_0,VA_s])

                        S_s    = pd.DataFrame(self.s_c.values @ (X_s.values * np.identity(len(X_s.values))),index=self.S.index,columns = self.S.columns)
                        
                        S_s    = pd.concat([S_s],keys=[str(round(j,15))],names=['Scenario'])
                        S_s_0  = pd.concat([S_s_0,S_s])


                        
                        j = j + sen_step
                
                    self.anam = my_z 
                    self.X_s = X_s_0
                    self.VA_s = VA_s_0
                    self.S_s = S_s_0
                    
                if par_4 == 'Percentage': 
                    
                    my_z = self.z_c.copy()
                    my_z.loc[(par_0,par_1),(par_2,par_3)] = self.z.loc[(par_0,par_1),(par_2,par_3)].values * ( 1 +  sen_min )
                    
                    l_s = np.linalg.inv(np.identity(len(my_z))-my_z) 
                    X_s_0 = pd.DataFrame(l_s @ self.Y_c.values,index=self.X.index,columns=[str(sen_min)])
                    
                    VA_s_0 = pd.DataFrame(self.va_c.values @ (X_s_0.values  * np.identity(len(X_s_0.values))),index = self.VA_ind,columns =  self.Z.columns) 
                    VA_s_0 = pd.concat([VA_s_0],keys=[str(sen_min)], names=['Scenario'])
                    
                    S_s_0  = pd.DataFrame(self.s_c.values @ (X_s_0.values * np.identity(len(X_s_0.values))),index=self.S.index,columns = self.S.columns)
                    S_s_0  = pd.concat([S_s_0],keys=[str(sen_min)],names=['Scenario'])
                    

                    j = sen_min + sen_step
                    
                    while (j<=sen_max):
                        
                        my_z.loc[(par_0,par_1),(par_2,par_3)] = self.z.loc[(par_0,par_1),(par_2,par_3)].values * ( 1 +  j )
                                                
                        l_s = np.linalg.inv(np.identity(len(my_z))-my_z)
                        X_s = pd.DataFrame(l_s @ self.Y_c.values,index=self.X.index,columns=[str(round(j,15))])
                        
                        X_s_0 = pd.concat([X_s_0,X_s],axis=1)
                        
                        VA_s = pd.DataFrame(self.va_c.values @ (X_s.values * np.identity(len(X_s.values))),index = self.VA_ind,columns =  self.Z.columns) 
                        
                        VA_s = pd.concat([VA_s],keys=[str(round(j,15))], names=['Scenario'])                        
                        VA_s_0 = pd.concat([VA_s_0,VA_s])

                        S_s    = pd.DataFrame(self.s_c.values @ (X_s.values * np.identity(len(X_s.values))),index=self.S.index,columns = self.S.columns)     
                        S_s    = pd.concat([S_s],keys=[str(round(j,15))],names=['Scenario'])
                        S_s_0  = pd.concat([S_s_0,S_s])

                        j = j + sen_step
                                           
                    self.X_s = X_s_0
                    self.VA_s = VA_s_0
                    self.S_s = S_s_0


        if parameter == 'Y':
            

            

            
            # for the Y matrix:
            # par_0: level_row
            # par_1: row
            # par_2: column

            
            
            par_0 = 'Commodities'
            par_1 = inp.loc[i,'row']  
            par_2 = 'Total final demand'
            
            self.sen_par = '{}, {}.'.format('Y',par_1)            
            # to save the sensitivity results, we need to build a dataframe
            
            # Make a copy of the matrix which is going to be changed.

            my_Y = self.Y_c.copy()


            my_Y.loc[(par_0,par_1),par_2] =  self.Y.loc[(par_0,par_1),par_2].values + sen_min 

            
            
            X_s_0 = pd.DataFrame(self.l_c @ my_Y.values,index=self.X.index,columns=[str(sen_min)])
            
            VA_s_0 = pd.DataFrame(self.va_c.values @ (X_s_0.values  * np.identity(len(X_s_0.values))),index = self.VA_ind,columns =  self.Z.columns)
            
            VA_s_0 = pd.concat([VA_s_0],keys=[str(sen_min)], names=['Scenario'])
            
            S_s_0  = pd.DataFrame(self.s_c.values @ (X_s_0.values * np.identity(len(X_s_0.values))),index=self.S.index,columns = self.S.columns)
            S_s_0  = pd.concat([S_s_0],keys=[str(sen_min)],names=['Scenario'])            
            
            j = sen_min + sen_step
            
            while (j<=sen_max):


                my_Y.loc[(par_0,par_1),par_2] = self.Y.loc[(par_0,par_1),par_2].values + j 

                
                X_s = pd.DataFrame(self.l_c @ my_Y.values,index=self.X.index,columns=[str(round(j,15))])
                
                X_s_0 = pd.concat([X_s_0,X_s],axis=1)
                
                VA_s = pd.DataFrame(self.va_c.values @ (X_s.values * np.identity(len(X_s.values))),index = self.VA_ind,columns =  self.Z.columns)            
                VA_s = pd.concat([VA_s],keys=[str(round(j,15))], names=['Scenario'])                       
                VA_s_0 = pd.concat([VA_s_0,VA_s])  

                S_s    = pd.DataFrame(self.s_c.values @ (X_s.values * np.identity(len(X_s.values))),index=self.S.index,columns = self.S.columns)                        
                S_s    = pd.concat([S_s],keys=[str(round(j,15))],names=['Scenario'])
                S_s_0  = pd.concat([S_s_0,S_s])    
                
                j = j + sen_step
    
            self.Y_s = my_Y
            self.X_s = X_s_0
            self.VA_s = VA_s_0
            self.S_s  = S_s_0
        
   
        
        if parameter == 'VA':
            
            # for the VA matrix:
            # par_0: level_row
            # par_1: row
            # par_2: level_col
            # par_3: col
            # par_4: type
            # par_5: Aggregated
            
            
            par_0 = inp.loc[i,'level_row']
            par_1 = inp.loc[i,'row']            
            par_2 = inp.loc[i,'level_col']            
            par_3 = inp.loc[i,'col']            
            par_4 = inp.loc[i,'type']  
            par_5 = inp.loc[i,'Aggregated']  
            
            # to save the sensitivity results, we need to build a dataframe
            
            # Make a copy of the matrix which is going to be changed.
            

            
            if par_5 == 'No':
                
                if par_4 == 'Absolute': 
                    
                    my_VA = self.VA_c.copy()
                    
                    # Calculating the first step to form the dataframes
                    my_VA.loc[(par_0,par_1),(par_2,par_3)] = self.VA.loc[(par_0,par_1),(par_2,par_3)].values + sen_min
                    
                    my_va = pd.DataFrame(my_VA.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.VA.index, columns=self.VA.columns)
                    
                    # BIG QUESTION
                    
                    VA_s_0 = pd.DataFrame(my_va.values @ (self.X_c.values  * np.identity(len(X_s_0.values))),index = self.VA_ind,columns =  self.Z.columns) 
                    VA_s_0 = pd.concat([VA_s_0],keys=[str(sen_min)], names=['Scenario'])
                    
                    X_s_0 = pd.DataFrame(self.X_c,index=self.X.index,columns=[str(sen_min)])
                    
                    S_s_0  = pd.DataFrame(self.S_c.values,index=self.S.index,columns = self.S.columns)
                    S_s_0  = pd.concat([S_s_0],keys=[str(sen_min)],names=['Scenario'])      
                    
                    j = sen_min + sen_step
                    
                    while (j<=sen_max):
                        
                        my_VA.loc[(par_0,par_1),(par_2,par_3)] = self.VA.loc[(par_0,par_1),(par_2,par_3)].values + j
                        
                        my_va = pd.DataFrame(my_VA.values @ np.linalg.inv(self.X.values  * np.identity(len(self.X))), index=self.VA.index, columns=self.VA.columns)
                        
                        VA_s = pd.DataFrame(my_va.values @ (self.X_c.values * np.identity(len(self.X_c.values))),index = self.VA_ind,columns =  self.Z.columns) 
                        
                        VA_s = pd.concat([VA_s],keys=[str(j)], names=['Scenario'])
                        
                        VA_s_0 = pd.concat([VA_s_0,VA_s])

                        X_s = pd.DataFrame(self.X_c.values,index=self.X.index,columns=[str(round(j,15))])
                
                        X_s_0 = pd.concat([X_s_0,X_s],axis=1)

                        S_s    = pd.DataFrame(self.S_c.values,index=self.S.index,columns = self.S.columns)                        
                        S_s    = pd.concat([S_s_0],keys=[str(round(j,15))],names=['Scenario'])
                        S_s_0  = pd.concat([S_s_0,S_s])  
                        
                        j = j + sen_step
                

                    self.VA_s = VA_s_0
                    self.X_s  = X_s_0
                    self.S_s  = S_s_0
                    
                if par_4 == 'Percentage': 
                    
                    my_va = self.va_c.copy()
                    
                    # Calculating the first step to form the dataframes
                    my_va.loc[(par_0,par_1),(par_2,par_3)] = self.va.loc[(par_0,par_1),(par_2,par_3)].values + sen_min
                    
                    VA_s_0 = pd.DataFrame(my_va.values @ (self.X_c.values  * np.identity(len(X_s_0.values))),index = self.VA_ind,columns =  self.Z.columns) 
                    VA_s_0 = pd.concat([VA_s_0],keys=[str(sen_min)], names=['Scenario'])    
                    
                    S_s_0  = pd.DataFrame(self.S_c.values,index=self.S.index,columns = self.S.columns)
                    S_s_0  = pd.concat([S_s_0],keys=[str(sen_min)],names=['Scenario'])

                    
                    X_s_0 = pd.DataFrame(self.X_c,index=self.X.index,columns=[str(sen_min)])  
                    
                    
                    j = sen_min + sen_step
                    
                    while (j<=sen_max):
                        
                        my_va.loc[(par_0,par_1),(par_2,par_3)] = self.va.loc[(par_0,par_1),(par_2,par_3)].values + j                       

                        VA_s = pd.DataFrame(my_va.values @ (self.X_c.values * np.identity(len(self.X_c.values))),index = self.VA_ind,columns =  self.Z.columns) 
                        
                        VA_s = pd.concat([VA_s],keys=[str(j)], names=['Scenario'])
                        
                        VA_s_0 = pd.concat([VA_s_0,VA_s])
                        
                        X_s = pd.DataFrame(self.X_c.values,index=self.X.index,columns=[str(round(j,15))])
                
                        X_s_0 = pd.concat([X_s_0,X_s],axis=1)
                        
                        S_s    = pd.DataFrame(self.S_c.values,index=self.S.index,columns = self.S.columns)                        
                        S_s    = pd.concat([S_s],keys=[str(round(j,15))],names=['Scenario'])
                        S_s_0  = pd.concat([S_s_0,S_s])                          


                        j = j + sen_step
                

                    self.VA_s = VA_s_0
                    self.X_s  = X_s_0
                    self.S_s  = S_s_0
                    
        if add_dict:
            
            self.S_s_agg = self.S_s.groupby(level=[0,4],sort = False).sum().groupby(axis = 1 , level=[0,4],sort = False).sum()
            
            # self.X_s  = pd.concat([self.X_s],keys=[self.sen_par],names=['Parameter'],axis=1)
            # self.VA_s = pd.concat([self.VA_s],keys=[self.sen_par],names=['Parameter'],axis=0) 
            # self.S_s_agg = pd.concat([self.S_s_agg],keys=[self.sen_par],names=['Parameter'],axis=0) 
            
            
            self.results['X_s_' + str(self.s_counter)] = self.X_s
            self.results['VA_s_' + str(self.s_counter)] = self.VA_s
            self.results['S_s_agg_' + str(self.s_counter)] = self.S_s_agg

            
            self.s_counter += 1
            
            
   
        
        
        
        
        
        
        
