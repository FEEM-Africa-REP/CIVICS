# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:57:05 2020

@author: negar
"""

class c_sut:
    def __init__(self,path):
        self.path=path
        import pandas as pd
        import numpy as np
        SUT=pd.read_excel('Kenya_2014_SAM_0.xlsx',sheet_name='Sheet1',index_col=[0,1,2,3],header=[0,1,2,3])
        Z=SUT.loc[['commodity','industry'],['commodity','industry']]
        F=SUT.loc[['commodity','industry'],'final demand']
        INV=SUT.loc[['commodity','industry'],'investment']
        EXP=SUT.loc[['commodity','industry'],'export']
        IMP=SUT.loc['import',['commodity','industry']]
        VA=SUT.loc[['value added0','value added1','taxes','investment','extra taxes'],['commodity','industry']]
    
        x_p=F.sum(axis=1)+INV.sum(axis=1)+EXP.sum(axis=1)+Z.sum(axis=1)

        self.A=Z.values@np.linalg.inv(x_p.values*np.identity(len(x_p)))
        self.imp=IMP.values@np.linalg.inv(x_p.values*np.identity(len(x_p)))
        self.va=VA.values@np.linalg.inv(x_p.values*np.identity(len(x_p)))
        
        
        
        
            
    def parse(self):
        
        
        import pandas as pd
        import numpy as np
        
        SUT=pd.read_excel('Kenya_2014_SAM_0.xlsx',sheet_name='Sheet1',index_col=[0,1,2,3],header=[0,1,2,3])
        
        self.Z=SUT.loc[['commodity','industry'],['commodity','industry']]
        
        #This is the local final demand
        self.F=SUT.loc[['commodity','industry'],'final demand']
        
        self.INV=SUT.loc[['commodity','industry'],'investment']
        
        self.EXP=SUT.loc[['commodity','industry'],'export']
        
        self.IMP=SUT.loc['import',['commodity','industry']]
        
        self.VA=SUT.loc[['value added0','value added1','taxes','investment','extra taxes'],['commodity','industry']]
        
        self.L=np.linalg.inv(np.identity(len(self.A))-self.A)
    
    def calc_all(self):
        
        import pandas as pd
        import numpy as np
        
        self.Y=pd.DataFrame(self.F.sum(axis=1)+self.INV.sum(axis=1)+self.EXP.sum(axis=1),index=self.Z.index,columns=['total final demand'])
        self.x=self.L@self.Y
        self.VA=self.va@(self.x*np.identity(len(self.x)))
        self.IMP=self.imp@(self.x*np.identity(len(self.x)))
              
        #%%
negar=c_sut(r'F:\FEEM\input_output\kenya_sut\Kenya_2014_SAM_0.xlsx')
#%%
negar.parse()
#%%
negar.calc_all()
#%%
Y_old=negar.Y
x_old=negar.x
VA_old=negar.VA
IMP_old=negar.IMP
#%%

negar.F.loc[('commodity','Maize (home consumed)'),('Coast 0 Rural')]=negar.F.loc[('commodity','Maize (home consumed)'),('Coast 0 Rural')].values*80000
#%%
negar.calc_all()
#%%
Y_new=negar.Y
x_new=negar.x
VA_new=negar.VA
IMP_new=negar.IMP
#%%

        
       
        
        
    