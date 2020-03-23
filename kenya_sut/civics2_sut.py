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
        
        sut = pd.read_excel(self.path,index_col = [0,1,2,3,4] , header = [0,1,2,3,4])
        Z=sut.loc[['commodity','industry'],['commodity','industry']] 
        F=sut.loc[['commodity','industry'],'final demand']
        INV=sut.loc[['commodity','industry'],'investment']
        EXP=sut.loc[['commodity','industry'],'export']
        IMP = sut.loc['import', ['commodity','industry']]
        VA = sut.loc[['value added0','value added1','taxes','investment','extra taxes'],['commodity','industry']]
        x_p   = F.sum(axis=1)+INV.sum(axis=1)+EXP.sum(axis=1)+Z.sum(axis=1)
        E = sut.loc['environment',['commodity','industry']]
        
        self.VA_ind = VA.index
        self.IMP_ind = IMP.index
        self.E_ind = E.index


        

     
        self.A = pd.DataFrame(Z.values @ np.linalg.inv(x_p.values  * np.identity(len(x_p))),index=Z.index,columns=Z.columns)
        self.imp = pd.DataFrame(IMP.values @ np.linalg.inv(x_p.values  * np.identity(len(x_p))),index=IMP.index,columns=IMP.columns)
        self.va = pd.DataFrame(VA.values @ np.linalg.inv(x_p.values  * np.identity(len(x_p))),index=VA.index,columns=VA.columns)
        self.e = pd.DataFrame(E.values @ np.linalg.inv(x_p.values  * np.identity(len(x_p))),index=E.index,columns=E.columns)
       
        
    def parse(self):
        
        import pandas as pd
        import numpy as np
        
        sut = pd.read_excel(self.path,index_col = [0,1,2,3,4] , header = [0,1,2,3,4])
        self.Z = sut.loc[['commodity','industry'],['commodity','industry']]
        # local final demand
        self.F   = sut.loc[['commodity','industry'],'final demand']
        # exports
        self.EXP = sut.loc[['commodity','industry'],'export']
        # investments
        self.INV = sut.loc[['commodity','industry'],'investment']
        # Import on final demand 
        self.IMP_fd = sut.loc['import','final demand']
        self.IMP_inv = sut.loc['import','investment']

        self.L = np.linalg.inv(np.identity(len(self.A)) - self.A)
   
        

                

    def plot_dx(self, old_x,new_x,level=False,Type='bar'):
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots()
        
        dx = new_x-old_x
        
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
        
        
        
        
            
    def calc_all(self):        
        import pandas as pd
        import numpy as np
        
        self.Y   = pd.DataFrame(self.F.sum(axis=1)+ self.EXP.sum(axis=1)+ self.INV.sum(axis=1),index = self.F.index,columns = ['Total final demand'])
        self.x   = pd.DataFrame(self.L @ self.Y.values,index = self.Z.index,columns = ['Total Production'])
        self.VA  = pd.DataFrame(self.va @ (self.x.values  * np.identity(len(self.x))),index = self.VA_ind,columns =  self.Z.columns)
        self.IMP = pd.DataFrame(self.imp @ (self.x.values  * np.identity(len(self.x))),index = self.IMP_ind,columns =  self.Z.columns)
        self.E   = pd.DataFrame(self.e @ (self.x.values * np.identity(len(self.x))),index = self.E_ind , columns = self.Z.columns)
        
        # Aggregating Results
#        com_pr = self.x.loc['commodity']
#        com_pr.index = com_pr.index.get_level_values(3)
#        com_pr = com_pr.groupby(axis=0,level=0).sum()
#        
#        ind_pr = self.x.loc['industry']
#        ind_pr.index = ind_pr.index.get_level_values(3)
#        ind_pr = ind_pr.groupby(axis=0,level=0).sum()
#        
#        cmdt = []
#        for i in range(len(com_pr)):
#            cmdt.append('commodity')
#        
#        inds = []
#        for i in range(len(ind_pr)):
#            inds.append('industry')    
#            
#        new_x = pd.concat([com_pr,ind_pr],axis = 0)
#        new_x_index = [cmdt+inds,com_pr.index + ind_pr.index]
#        new_x.index = new_x_index
#        
#        self.x_agg = new_x


    

#%%        
negar=C_SUT(r'F:\FEEM\input_output\kenya_sut\Kenya_2014_SAM_0 (2).xlsx')
#%%
negar.parse()
#%%
negar.calc_all()
#%%
Y_old=negar.Y
x_old=negar.x
VA_old=negar.VA
IMP_old=negar.IMP
INV_old=negar.INV
A_old=negar.A
#%%
# Implementing the shock: Pulping machine
# Investment
# 1. Metals and machines (commodity)
Num_machine = 500
Mach_inv = 0.155  #MSh (we transfer it from kilo shillings to million shillings)
negar.INV.loc[('commodity','Metals and machines (commodity)'),('General investment saving')] = \
    negar.INV.loc[('commodity','Metals and machines (commodity)'),('General investment saving')].values + Mach_inv * Num_machine
    
#2. Transport
Trs_cost = 5/1000.0  #MSh
negar.INV.loc[('commodity','Transport (commodity)'),'General investment saving'] = \
    negar.INV.loc[('commodity','Transport (commodity)'),'General investment saving'].values + Trs_cost * Num_machine
    #%%
#Matrix of Technical Coefficients
# Use side
#  a)coffe commodity into high rainfall (increase in productivity)
prod_coef=0.98
negar.A.loc[('commodity','Coffee (commodity)'),('industry','High Rainfall (commercial production)')] = \
      negar.A.loc[('commodity','Coffee (commodity)'),('industry','High Rainfall (commercial production)')].values*prod_coef
      #%%
#  b)Use of diesel (petroleum commodity)
diesel_coef=0.01 #MSh
negar.A.loc[('commodity','Petroleum (commodity)'),('industry','High Rainfall (commercial production)')] = \
      negar.A.loc[('commodity','Petroleum (commodity)'),('industry','High Rainfall (commercial production)')].values+diesel_coef*Num_machine
      #%%
#value added
# Unskilled labour reduction
lab_coef=0.7
negar.va.loc[('value added0','Unskilled labour 0 High Rainfall'),('industry','High Rainfall (commercial production)')] = \
    negar.va.loc[('value added0','Unskilled labour 0 High Rainfall'),('industry','High Rainfall (commercial production)')].values*lab_coef
    #%%
#environmental effect
#water footprint reduction
WFN_coef=0.15
negar.e.loc[('WaterFootprintNetwork','WFN: Total water footprint (Mm3/yr) - Blue'),('industry','High Rainfall (commercial production)')] = \
    negar.e.loc[('WaterFootprintNetwork','WFN: Total water footprint (Mm3/yr) - Blue'),('industry','High Rainfall (commercial production)')].values*WFN_coef
#%%
negar.calc_all()
#%%
Y_new=negar.Y
x_new=negar.x
VA_new=negar.VA
IMP_new=negar.IMP
INV_new=negar.INV
A_new=negar.A
#%%
#Impelementing the shock: Shading tree Managment    
    

      
      

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    