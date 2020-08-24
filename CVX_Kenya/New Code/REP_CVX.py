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
        from functions.units import unit_check
        from functions.io_calculation import cal_coef
        from functions.indexer import indeces
        

        
        
        print(__version__)
        
        # Check if the unit is correct or not
        self.m_unit = unit_check(unit)
        
        # Ignoring the warnings caused by 
        filterwarnings("ignore") 
        
        # Reading the Data Base
        self.SUT,self.U,self.V,self.Z,self.S,self.Y,self.VA,self.X = database(path)
        
        # Calculating the baseline coefficients
        self.z,self.s,self.va,self.l,self.p = cal_coef (self.Z,self.S,self.VA,self.X)
        
        # Getting indeces
        self.indeces = indeces(self.S,self.Z,self.VA,self.X)
        
        # All the information needs to be stored in every step because it will be used in some other functions
        self.results = {'Z':self.Z, 'Y':self.Y,'X':self.X,'VA':self.VA,'p':self.p,'va':self.va,'z':self.z}
        
        # A counter for saving the results in a dictionary
        self.counter = 1 
        
        
    def shock (self,path,Y=False, VA=False, Z=False, S=False):
        
        import functions.shock_io as sh
        
        # Taking a copy of all matrices to have both changed and unchanged ones
        self.Y_c   = self.Y.copy()
        self.va_c  = self.va.copy()
        self.s_c   = self.s.copy()
        self.z_c   = self.z.copy()
        
        # check the type of the code
        if Y:
            self.Y_c  = sh.Y_shock (path,self.Y_c)
            
        if Z:
            self.z_c  = sh.Z_shock (path,self.z_c,self.Z.copy(),self.X.copy())
            
        if VA:
            self.va_c = sh.VA_shock (path,self.va_c,self.VA.copy(),self.X.copy())
        

    def calc_all(self,save=True):
        
        from functions.io_calculation import cal_flows
        
        try:
            # Calculating the shock result
            self.l_c,self.X_c,self.VA_c,self.S_c,self.Z_c,self.p_c = cal_flows(self.z_c,self.Y_c,self.va_c,self.s_c,self.indeces)
        except:
            raise ValueError('To run /calc_all/ function, a shock needs to be implemented.')
         
        # Saving all the new matrices in the results dictionary.
        if save:
            self.results['Z_' + str(self.counter)]= self.Z_c
            self.results['X_' + str(self.counter)]= self.X_c
            self.results['VA_'+ str(self.counter)]= self.VA_c
            self.results['p_' + str(self.counter)]= self.p_c
            self.results['Y_' + str(self.counter)]= self.Y_c
            self.results['va_' + str(self.counter)]= self.va_c
            self.results['z_' + str(self.counter)]= self.z_c
            self.results['S_' + str(self.counter)]= self.S_c   
            
            self.counter += 1

        