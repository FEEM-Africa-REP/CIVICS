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
        import numpy as np
        
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
        
        self.Y   = pd.DataFrame(self.F.sum(axis=1)+ self.EXP.sum(axis=1)+ self.INV.sum(axis=1),index = self.F.index,columns = ['Total final demand'])
        self.x   = pd.DataFrame(self.L @ self.Y.values,index = self.Z.index,columns = ['Total Production'])
        self.VA  = pd.DataFrame(self.va.values @ (self.x.values  * np.identity(len(self.x))),index = self.VA_ind,columns =  self.Z.columns)
        self.IMP = pd.DataFrame(self.imp.values @ (self.x.values  * np.identity(len(self.x))),index = self.IMP_ind,columns =  self.Z.columns)
        self.E   = pd.DataFrame(self.e @ (self.x.values * np.identity(len(self.x))),index = self.E_ind , columns = self.Z.columns)
        
        # Aggregating Results
        # Aggregation of x Matrix
        com_pr = self.x.loc['commodity']
        com_pr.index = com_pr.index.get_level_values(3)
        com_pr = com_pr.groupby(axis=0,level=0).sum()
        
        ind_pr = self.x.loc['industry']
        ind_pr.index = ind_pr.index.get_level_values(3)
        ind_pr = ind_pr.groupby(axis=0,level=0).sum()
        
        cmdt = []
        for i in range(len(com_pr)):
            cmdt.append('commodity')
        
        inds = []
        for i in range(len(ind_pr)):
            inds.append('industry')    
            
        new_x = pd.concat([com_pr,ind_pr],axis = 0)
        new_x_index = [cmdt+inds,com_pr.index.to_list() + ind_pr.index.to_list()]
        new_x.index = new_x_index
        
        self.x_agg = new_x


        # Aggregation of VA Matrix
        com_va = self.VA['commodity']
        com_va.columns = com_va.T.index.get_level_values(3)
        com_va = com_va.groupby(axis=1,level=0).sum()
        
        ind_va = self.VA['industry']
        ind_va.columns = ind_va.T.index.get_level_values(3)
        ind_va = ind_va.groupby(axis=1,level=0).sum()
        

        new_va = pd.concat([com_va,ind_va],axis = 1)
        new_va.columns = new_x_index
        
        self.VA_agg = new_va
    

        # Aggregation of IMP Matrix
        com_im = self.IMP['commodity']
        com_im.columns = com_im.T.index.get_level_values(3)
        com_im = com_im.groupby(axis=1,level=0).sum()
        
        ind_im = self.IMP['industry']
        ind_im.columns = ind_im.T.index.get_level_values(3)
        ind_im = ind_im.groupby(axis=1,level=0).sum()
        

        new_im = pd.concat([com_im,ind_im],axis = 1)
        new_im.columns = new_x_index
        
        self.IMP_agg = new_im      
      

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    