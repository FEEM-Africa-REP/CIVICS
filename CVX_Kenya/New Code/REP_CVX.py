# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 11:13:45 2020

@author: Mohammad Amin Tahavori
"""
class C_SUT:
    
    def __init__(self,path,unit):
        
        from functions.version import __version__
        from warnings import filterwarnings
        from functions.data_read import database
        from functions.check import unit_check
        from functions.io_calculation import cal_coef
        from functions.indexer import indeces
        from functions.aggregation import aggregate

        print(__version__)
        
        # Check if the unit is correct or not
        self.m_unit = unit_check(unit)
        
        # Ignoring the warnings 
        filterwarnings("ignore") 
        
        # Reading the Database
        self.SUT,self.U,self.V,self.Z,self.S,self.Y,self.VA,self.X = database (path)
        
        # Calculating the baseline coefficients
        self.z,self.s,self.va,self.l,self.p = cal_coef (self.Z,self.S,self.VA,self.X)
        
        # Building aggregated results for the baseline
        self.X_agg,self.Y_agg,self.VA_agg,self.S_agg,self.Z_agg = aggregate(self.X,self.Y,self.VA,self.S,self.Z)
        
        # Getting indeces
        self.indeces = indeces (self.S,self.Z,self.VA,self.X)
        
        # All the information needs to be stored in every step because it will be used in some other functions
        self.results = {'Z':self.Z, 'Y':self.Y,'X':self.X,'VA':self.VA,'p':self.p,'S':self.S,'va':self.va,'z':self.z \
                        ,'Z_agg':self.Z_agg, 'Y_agg':self.Y_agg,'X_agg':self.X_agg,'VA_agg':self.VA_agg,'S_agg':self.S_agg}
        
        # A counter for saving the results in a dictionary
        self.counter = 1 
        
        
    def shock_calc (self,path,Y=False, VA=False, Z=False, S=False,save=True):
        
        import functions.shock_io as sh
        from functions.io_calculation import cal_flows
        from functions.aggregation import aggregate
        
        # Taking a copy of all matrices to have both changed and unchanged ones
        self.Y_c   = self.Y.copy()
        self.va_c  = self.va.copy()
        self.s_c   = self.s.copy()
        self.z_c   = self.z.copy()
        
        # check the type of the shock
        if Y:   self.Y_c  = sh.Y_shock  (path,self.Y_c)                      
        if Z:   self.z_c  = sh.Z_shock  (path,self.z_c,self.Z.copy(),self.X.copy())
        if VA:  self.va_c = sh.VA_shock (path,self.va_c,self.VA.copy(),self.X.copy())
        if S:   self.s_c  = sh.S_shock  (path,self.s_c,self.S.copy(),self.X.copy())
        
        # Calculating the shock result
        self.l_c,self.X_c,self.VA_c,self.S_c,self.Z_c,self.p_c = cal_flows(self.z_c,self.Y_c,self.va_c,self.s_c,self.indeces)        

        # Aggregation of the results
        self.X_c_agg,self.Y_c_agg,self.VA_c_agg,self.S_c_agg,self.Z_c_agg = aggregate(self.X_c,self.Y_c,self.VA_c,self.S_c,self.Z_c)
        
        # Saving all the new matrices in the results dictionary.
        if save:
            self.results['Z_'  + str(self.counter)]= self.Z_c
            self.results['X_'  + str(self.counter)]= self.X_c
            self.results['VA_' + str(self.counter)]= self.VA_c
            self.results['p_'  + str(self.counter)]= self.p_c
            self.results['Y_'  + str(self.counter)]= self.Y_c
            self.results['va_' + str(self.counter)]= self.va_c
            self.results['z_'  + str(self.counter)]= self.z_c
            self.results['S_'  + str(self.counter)]= self.S_c
            
            self.results['Z_agg'  + str(self.counter)]= self.Z_c_agg
            self.results['X_agg'  + str(self.counter)]= self.X_c_agg
            self.results['VA_agg' + str(self.counter)]= self.VA_c_agg
            self.results['Y_agg'  + str(self.counter)]= self.Y_c_agg
            self.results['S_agg'  + str(self.counter)]= self.S_c_agg
            
            self.counter += 1
        
    def plot_dx (self,aggregated=True,unit='default',level=None,kind='Absolute',
                fig_format='png',title_font=15,style='ggplot',figsize=(10, 6),
                directory='my_graphs',ranshow=(0,0),title='default',color = 'rainbow'):
        
        from functions.plots import dx
        
        # Check if the shock result exist or not
        try: self.X_c          
        except: raise ValueError('To run the plot function, there should be an implemented shock.')
        
        # To check the input to the plot function in the aggregated level or disaggregated
        if aggregated:
            X_c,X = self.X_c_agg,self.X_agg    
        else:
            X_c,X = self.X_c_agg,self.X_agg
            
        self.a = dx(X_c,X,style,unit,self.m_unit,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color)



     