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
        self.indeces = indeces(self.S,self.Z,self.VA)
        
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
        
        if Y:
            self.Y_c = sh.Y_shock (path,self.Y_c)
            
        if Z:
            print(1)
        

        


        