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
        from functions.utility import indeces
        from functions.aggregation import aggregate
        from functions.utility import dict_maker

        print(__version__)
        
        self.main_path = path
        
        # Check if the unit is correct or not
        self.m_unit = unit_check(unit)
        
        # Ignoring the warnings 
        filterwarnings("ignore") 
        
        # Reading the Database
        self.SUT,self.U,self.V,self.Z,self.S,self.Y,self.VA,self.X = database (path)
        
        # Calculating the baseline coefficients
        self.z,self.s,self.va,self.l,self.p = cal_coef (self.Z,self.S,self.VA,self.X)
        
        # Building aggregated results for the baseline
        self.X_agg,self.Y_agg,self.VA_agg,self.S_agg,self.Z_agg,self.p_agg = aggregate(self.X,self.Y,self.VA,self.S,self.Z,self.p)
        
        # Getting indeces
        self.indeces = indeces (self.S,self.Z,self.VA,self.X)
        
        # All the information needs to be stored in every step because it will be used in some other functions
        self.results = {}
        self.results['baseline']= dict_maker(self.Z,self.X,self.VA,self.p,self.Y,self.va,
                                                self.z,self.s,self.Z_agg,self.X_agg,self.VA_agg,self.Y_agg,self.S_agg,self.p_agg)
            
        # In order to identify the sensitivity scenario, the information will be stored in the following dictionary
        self.sens_info = {}
        
        
        # A counter for saving the results in a dictionary
        self.counter   = 1 
        self.s_counter = 1
        self.i_counter = 1
        
        
    def shock_calc (self,path,Y=False, VA=False, Z=False, S=False,save=True):
        
        import functions.shock_io as sh
        from functions.io_calculation import cal_flows
        from functions.aggregation import aggregate
        from functions.utility import dict_maker
        
        self.sh_path = path
        # Taking a copy of all matrices to have both changed and unchanged ones
        self.Y_c   = self.Y.copy()
        self.va_c  = self.va.copy()
        self.s_c   = self.s.copy()
        self.z_c   = self.z.copy()
        
        # check the type of the shock
        if Y:   self.Y_c  = sh.Y_shock  (path,self.Y_c.copy())                      
        if Z:   self.z_c  = sh.Z_shock  (path,self.z_c.copy(),self.Z.copy(),self.X.copy())
        if VA:  self.va_c = sh.VA_shock (path,self.va_c.copy(),self.VA.copy(),self.X.copy())
        if S:   self.s_c  = sh.S_shock  (path,self.s_c.copy(),self.S.copy(),self.X.copy())
        
        # Calculating the shock result
        self.l_c,self.X_c,self.VA_c,self.S_c,self.Z_c,self.p_c = cal_flows(self.z_c,self.Y_c,self.va_c,self.s_c,self.indeces)        

        # Aggregation of the results
        self.X_c_agg,self.Y_c_agg,self.VA_c_agg,self.S_c_agg,self.Z_c_agg,self.p_c_agg = aggregate(self.X_c,self.Y_c,self.VA_c,self.S_c,self.Z_c,self.p_c)
        
        # Saving all the new matrices in the results dictionary.
        if save:
            self.results['shock_{}'.format(self.counter)]= dict_maker(self.Z_c,self.X_c,self.VA_c,self.p_c,self.Y_c,self.va_c,
                                                self.z_c,self.s_c,self.Z_c_agg,self.X_c_agg,self.VA_c_agg,self.Y_c_agg,self.S_c_agg,self.p_c_agg)
            self.counter += 1
            
        
    def plot_dx (self,aggregated=True,unit='default',level=None,kind='Absolute',
                fig_format='png',title_font=15,style='ggplot',figsize=(10, 6),
                directory='my_graphs',ranshow=(0,0),title='default',color = 'rainbow', drop=None,save_excel=True):
        
        from functions.plots import delta_xv
        

        # Check if the shock result exist or not
        try: self.X_c          
        except: raise ValueError('To run the plot function, there should be an implemented shock.')
        
        # To check the input to the plot function in the aggregated level or disaggregated
        if aggregated:
            X_c,X = self.X_c_agg,self.X_agg    
        else:
            X_c,X = self.X_c,self.X
            
        delta_xv(X_c,X,style,unit,self.m_unit,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,'X',drop,save_excel)


    def plot_dv(self,aggregated=True,unit='default',level=None,kind='Absolute',
                fig_format='png',title_font=15,style='ggplot',figsize=(10, 6),
                directory='my_graphs',ranshow=(0,0),title='default',color = 'terrain', drop= None,save_excel=True):
        
        from functions.plots import delta_xv
        
        # Check if the shock result exist or not
        try: self.X_c          
        except: raise ValueError('To run the plot function, there should be an implemented shock.')
        
        # To check the input to the plot function in the aggregated level or disaggregated
        if aggregated:   VA_c,VA = self.VA_c_agg,self.VA_agg    
        else:            VA_c,VA = self.VA_c,self.VA
            
        delta_xv(VA_c,VA,style,unit,self.m_unit,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,'VA',drop,save_excel)        
        
        
    def plot_ds(self,indicator,aggregated=True,detail=True,unit='default',
                level='Activities',kind='Absolute',fig_format='png',title_font=15,
                style='ggplot',figsize=(10, 6),directory='my_graphs',ranshow=(0,0)
                ,title='default',color = 'terrain', drop= None):
        
        from functions.plots import delta_s
        
        # Check if the shock result exist or not
        try: self.X_c          
        except: raise ValueError('To run the plot function, there should be an implemented shock.')        

        # To check the input to the plot function in the aggregated level or disaggregated
        if aggregated and not detail: S_c,S = self.S_c_agg,self.S_agg 
        else: S_c,S = self.S_c,self.S
        
        
        
        delta_s(S_c,S,style,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,indicator,detail,self.indeces)        
        

    def plot_dp(self,unit='default',level=None,fig_format='png',title_font=15,
                style='ggplot',figsize=(10, 6),directory='my_graphs',title='default',color = 'terrain',aggregated=False):
        
        from functions.plots import delta_p
        
        # Check if the shock result exist or not
        try: self.X_c
        except: raise ValueError('To run the plot function, there should be an implemented shock.')
        
        if aggregated: 
            p_c,p = self.p_c_agg,self.p_agg, 
            print('For the aggregated results, the mean of the price of aggregated invoices are represented')
        else: p_c,p = self.p_c,self.p
        
        delta_p(p_c,p,style,level,title,title_font,figsize,directory,fig_format,color)



    def multi_shock(self,path,Y=False,VA=False,Z=False,S=False,save=True):
        
        import glob
        from functions.utility import dict_maker
        
        if not Y and not VA and not Z and not S:
            raise ValueError('At lest one of the arguments should be \'True\' ')
        
        
        files = [f for f in glob.glob(path + "**/*.xlsx", recursive=True)]
    
              
        for i in files:
            self.shock_calc(path=r'{}'.format(i),Y=Y,VA=VA,Z=Z,S=S,save=False)
            
            if save:
                self.results['shock_{}'.format(self.counter)]= dict_maker(self.Z_c,self.X_c,self.VA_c,self.p_c,self.Y_c,self.va_c,
                                                    self.z_c,self.s_c,self.Z_c_agg,self.X_c_agg,self.VA_c_agg,self.Y_c_agg,self.S_c_agg,self.p_c_agg)
                self.counter += 1
                
        print("Warning: \n all the shock variables are equal to the last sensitivity file: \'{}\' ".format(i))
        
    def sensitivity(self,path):

        from functions.data_read import sens_info
        from functions.utility import dict_maker
        import functions.shock_io as sh
        from functions.io_calculation import cal_flows
        from functions.aggregation import aggregate
        import glob
        
        directs,sensitivity_info = sens_info (path)
        i=0
        self.a = sensitivity_info
        for file in directs:
            excels = [f for f in glob.glob(file + "**/*.xlsx", recursive=True)]
            self.results['sensitivity_{}'.format(self.s_counter)]={'information':sensitivity_info[str(i)]}
            
            # Check the affected matrices in every shock
            mat_list = sensitivity_info[str(i)]['matrices']
            
            print('Sensitivity {}. Affected Matrices: {}'.format(i+1,mat_list))
            i+=1
            
            for excel in excels:

                # Taking a copy of all matrices to have both changed and unchanged ones
                Y_c   = self.Y.copy()
                va_c  = self.va.copy()
                s_c   = self.s.copy()
                z_c   = self.z.copy()
                
                # check the type of the shock
                if 'Y' in mat_list : Y_c  = sh.Y_shock  (path,Y_c.copy())                      
                if 'Z' in mat_list : z_c  = sh.Z_shock  (path,z_c.copy(),self.Z.copy(),self.X.copy())
                if 'VA' in mat_list : va_c = sh.VA_shock (path,va_c.copy(),self.VA.copy(),self.X.copy())
                if 'S' in mat_list : s_c  = sh.S_shock  (path,s_c.copy(),self.S.copy(),self.X.copy())
                
                # Calculating the shock result
                l_c,X_c,VA_c,S_c,Z_c,p_c = cal_flows(z_c,Y_c,va_c,s_c,self.indeces)        
        
                # Aggregation of the results
                X_c_agg,Y_c_agg,VA_c_agg,S_c_agg,Z_c_agg,p_c_agg = aggregate(X_c,Y_c,VA_c,S_c,Z_c,p_c)
                
                
                value = str(excel).replace(".xlsx","").replace('{}\case_'.format(file), "")
                self.results['sensitivity_{}'.format(self.s_counter)][value]=\
                    dict_maker(Z_c,X_c,VA_c,p_c,Y_c,va_c,
                               z_c,s_c,Z_c_agg,X_c_agg,VA_c_agg,
                               Y_c_agg,S_c_agg,p_c_agg)
            
            self.s_counter+=1
                                                                   
        
    def impact(self,p_life,saving_sce,invest_sce,imports=['Import'],w_ext=['Water'], em_ext=['CO2'], land=['Land'], labour=['Labor - Skilled','Labor - Semi Skilled','Labor - Unskilled'],capital=['Capital - Machines']):
        from functions.impact import impact_assessment
        
        self.impact = impact_assessment(invest_sce,saving_sce,self.results,p_life,w_ext,em_ext,land,labour,capital,imports)
                
        self.results['Impact_{}'.format(self.i_counter)]=self.impact
        self.i_counter += 1
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        