# -*- coding: utf-8 -*-
'''
REP_CVX - A python module for automating SU-IO calculations and generating reports
==============================================================================

The classes and tools in this module should work with any Supply and Use table following the structure defined in the tutorial.

The main class of the module "C_CUT" :
The calss has multiple typical tools for input-output analysis:
    1. Calculating all the matrices of flows and coefficients from a given database
    2. Implementing shocks 
    3. Sensitivity Analysis on the shocks
    4. Policy impact assesment
    5. Visualizing results and generating reports
    
Data storage
------------
xlsx files together is used for storing data. In addition,
the "C_SUT" with all data can also be pickled (binary).


----
Dependencies:

- pandas
- matplotlib
- seaborn
- pymrio
- pickle

:Authors:   Mohammad Amin Tahavori,
            Nicolo Gulinucci,
            Negar Namazifard

:license: 

'''
class C_SUT:
    
    ''' C_SUT Class

    The class reads the given database in form of an excel file and built all 
    pandas DataFrames of the flows and coefficients of the IO system. 

    Notes
    -----
        1. The attributes and extension dictionary entries are pandas.DataFrame
        with an MultiIndex.  This index must have the specified level names.
        
        2. Capital letters represent the flows and the same letter in small case
        represents the coefficients.
        
        3. Every variable with "_c" represents the values after the last shock 
        implemented.
        
        4. Every variable with "_agg" represents the aggregated variable with
        the same name.

    Attributes
    ----------
    Z : pandas.DataFrame
        Supply and Use flows of activities and commodities
        MultiIndex with levels and aggregatedn and disaggregated names
      
    U,V : pandas.DataFrame
        Use and Supply Matrices
        MultiIndex with levels and aggregatedn and disaggregated names   
        for U: [index=Commodities,columns=Activities]
        for V: [index=Activities,columns=Commodities]
        
    Y : pandas.DataFrame
        final demand with MultiIndex similar to Z matrix
        
    S : pandas.DataFrame
        satellite account
        MultiIndex with levels and aggregatedn and disaggregated names

    VA : pandas.DataFrame
        Economic factor flows
        MultiIndex with levels and aggregatedn and disaggregated names
        
    X : pandas.DataFrame
        Total production of Activities and Commodities
        MultiIndex with levels and aggregatedn and disaggregated names 
        
    l : pandas.DataFrame
        Leontief, MultiTndex as Z

    p : pandas.DataFrame
        price index  
        
    Arguments
    ----------
    path :  the path of the database excel file.
    
    unit :  represepnts the main unit of the flows in the table. This will be 
            used for the unit conversions.    
    
    ''' 
    
    def __init__(self,path,unit):
        
        '''  
        path :  string
            the path of the database excel file.
                
        unit :  string
            represepnts the main unit of the flows in the table. This will be 
                used for the unit conversions. 
        '''                          
        
        from functions.version import __version__
        from warnings import filterwarnings
        from functions.data_read import database
        from functions.check import unit_check
        from functions.io_calculation import cal_coef
        from functions.utility import indeces
        from functions.aggregation import aggregate
        from functions.utility import dict_maker

        # Printing the version and the information of the module
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
        self.counter   = 1      # Shock Counter
        self.s_counter = 1      # Sensitivity Counter
        self.i_counter = 1      # Impact Assessment Couter
        
        
    def shock_calc (self,path,Y=False, VA=False, Z=False, S=False,save=True):
        
        '''  
        shock_calc:
            This function is used to implement a shock
            The shock should be defined through an excel file which is described
            in detail in the tutorial.
            
        As a shock can be implemented in different steps or on differnet matrices
        the user should identify that which matrix of shock excel file should
        be implemented by calling the function.
            
        Arguments
        ----------
        path :  string
            the path of the shock excel file.
                
        Y  :  boolean
            True: Final demand shock
            
        Z  :  boolean  
            True: Technical change shock
             
        VA :  boolean
            True: Economic factor change shock

        S  :  boolean
            True: Satellite account shock  
        
        save: boolean
            True: Saving the results in a dictionary. 
        
        -----------------------------------------------------------------------
        Note: It is suggested to keep "save" always "True". In this way, all the
                information can be stored and used easily.
        -----------------------------------------------------------------------
        
        '''            
        import functions.shock_io as sh
        from functions.io_calculation import cal_flows
        from functions.aggregation import aggregate
        from functions.utility import dict_maker
    
        # There should be at least one shock!
        if not Y and not VA and not Z and not S:
            raise ValueError('At lest one of the arguments should be \'True\' ')
            
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
        '''  
        plot_dx:
            This function is used to plot delta_x between the baseline and the
            last shock implemented
            
        Arguments
        ----------
        aggregated  :  boolean
            True: Showing aggregated results of production
            
        unit  :  string
            default: the unit will be equal the the main unit in the database
            or the user can choose the unit among the acceptable units.
             
        level :  string
            None: Both Activities and Commodities will be represented
            Activities: Activities level
            Commodities: Commodities level

        kind  :  string
            Absolute: Absolute change
            Percentage: Relative change
            
        title:  string
            The user can choose a specific title otherwise the default title
            will be used.
            
        fig_format: string
            To save the plot
                    'png','svg'
        
        title_font:  float
            size of title font
        
        style: string
            Plot style
        
        figsize: tuple
            Figure size
        
        directory: string
            the directory to save the results
        
        ranshow: tuple
            it represents the range of the values to be shown:
                    (Max value,Min value)
                    
        color: colormap:string  , colors:list 
            could be colormap or a list of colors
        
        drop: list
            To drop specific categories from the data
               
        save_excel: boolean
                    If True, the results will be saved also in form of excel file
                    in the same directory
             
        ''' 
        
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
        '''  
        plot_dv:
            This function is used to plot delta_VA between the baseline and the
            last shock implemented
            
        Arguments
        ----------
        aggregated  :  boolean
            True: Showing aggregated results of production
            
        unit  :  string
            default: the unit will be equal the the main unit in the database
            or the user can choose the unit among the acceptable units.
             
        level :  string
            None: Both Activities and Commodities will be represented
            Activities: Activities level
            Commodities: Commodities level

        kind  :  string
            Absolute: Absolute change
            Percentage: Relative change
            
        title: string
            The user can choose a specific title otherwise the default title
            will be used.
            
        fig_format: string
            To save the plot
                    'png','svg'
        
        title_font: float
            size of title font
        
        style: string
            Plot style
        
        figsize: tuple
            Figure size
        
        directory: string
            the directory to save the results
        
        ranshow: tuple
            it represents the range of the values to be shown:
                    (Max value,Min value)
                    
        color: colormap:string  , colors:list 
            could be colormap or a list of colors
        
        drop: list
            To drop specific categories from the data
               
        save_excel: booelan
                    If True, the results will be saved also in form of excel file
                    in the same directory     
        '''        
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
                ,title='default',color = 'terrain', drop= None,save_excel=True):
        '''  
        plot_dv:
            This function is used to plot delta_VA between the baseline and the
            last shock implemented
            
        Arguments
        ----------
        indicator: string
            defines the specfic indicator to be ploted such as:
                water consumption, CO2 and ....
                
                NOTE: the indicator name should be the corresponding name of 
                the imported database
                
        aggregated  :  booelan
            True: Showing aggregated results of economic factor use
        
        detail: boolean
            True: shows different levels of the a specific indicator if
            presents in the database
            
        unit  :  string
            default: the unit will be equal the the main unit in the database
            or the user can choose the unit among the acceptable units.
             
        level :  string
            None: Both Activities and Commodities will be represented
            Activities: Activities level
            Commodities: Commodities level

        kind  :  string
            Absolute: Absolute change
            Percentage: Relative change
            
        
        fig_format: string
            To save the plot
                    'png','svg'
        
        title_font: float
            size of title font
        
        style: string
            Plot style
        
        figsize: tuple
            Figure size
        
        directory: string
            the directory to save the results
        
        ranshow: tuple
            it represents the range of the values to be shown:
                    (Max value,Min value)
                    
        color: colormap:string  , colors:list 
            could be colormap or a list of colors
        
        drop: list
            To drop specific categories from the data
               
        save_excel: boolean
                    If True, the results will be saved also in form of excel file
                    in the same directory     
        '''         
        from functions.plots import delta_s
        
        # Check if the shock result exist or not
        try: self.X_c          
        except: raise ValueError('To run the plot function, there should be an implemented shock.')        

        # To check the input to the plot function in the aggregated level or disaggregated
        if aggregated and not detail: S_c,S = self.S_c_agg,self.S_agg 
        else: S_c,S = self.S_c,self.S
        
        delta_s(S_c,S,style,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,indicator,detail,self.indeces,save_excel)        
        

    def plot_dp(self,unit='default',level=None,fig_format='png',title_font=15,
                style='ggplot',figsize=(10, 6),directory='my_graphs',title='default',color = 'terrain',aggregated=False,save_excel=True):
        '''  
        plot_dp:
            This function is used to plot change in the price ratio between the baseline and the
            last shock implemented
            
        Arguments
        ----------
        aggregated  :  
            True: Showing aggregated results of price index as the average between the aggregated invoices
             
        level :  
            None: Both Activities and Commodities will be represented
            Activities: Activities level
            Commodities: Commodities level
            
        title:
            The user can choose a specific title otherwise the default title
            will be used.
            
        fig_format: 
            To save the plot
                    'png','svg'
        
        title_font: 
            size of title font
        
        style: 
            Plot style
        
        figsize:
            Figure size
        
        directory: 
            the directory to save the results
                    
        color: 
            could be colormap or a list of colors
               
        save_excel: 
                    If True, the results will be saved also in form of excel file
                    in the same directory     
        '''          
        from functions.plots import delta_p
        
        # Check if the shock result exist or not
        try: self.X_c
        except: raise ValueError('To run the plot function, there should be an implemented shock.')
        
        if aggregated: 
            p_c,p = self.p_c_agg,self.p_agg, 
            print('For the aggregated results, the mean of the price of aggregated invoices are represented')
        else: p_c,p = self.p_c,self.p
        
        delta_p(p_c,p,style,level,title,title_font,figsize,directory,fig_format,color,save_excel)



    def multi_shock(self,path,Y=False,VA=False,Z=False,S=False,save=True):
        
        '''
        multi_shock:
            This function can be used to implement multiple shocks at the same time
        Arguments
        ----------
        path:
            Defines the folder in which all the shocks exist not a single shock
            excel file.
        
        Y  :  boolean
            True: Final demand shock
            
        Z  :  boolean
            True: Technical change shock
             
        VA :  boolean
            True: Economic factor change shock

        S  :  boolean
            True: Satellite account shock  
        
        save: boolean
            True: Saving the results in a dictionary. 
        
        -----------------------------------------------------------------------
        Note: It is suggested to keep "save" always "True". In this way, all the
                information can be stored and used easily.
        -----------------------------------------------------------------------
        '''
        
        import glob
        from functions.utility import dict_maker
        
        # There should be at least one shock to be implemented!
        if not Y and not VA and not Z and not S:
            raise ValueError('At lest one of the arguments should be \'True\' ')
        
        # Taking all the excel files in the given path and store the directory
        files = [f for f in glob.glob(path + "**/*.xlsx", recursive=True)]
    
        # taking all the excel files detected in loop and implement the shock    
        for i in files:
            # Calling the shock_calc for every excel file
            self.shock_calc(path=r'{}'.format(i),Y=Y,VA=VA,Z=Z,S=S,save=False)
            
            # Saving all the results in the results dictionary
            if save:
                self.results['shock_{}'.format(self.counter)]= dict_maker(self.Z_c,self.X_c,self.VA_c,self.p_c,self.Y_c,self.va_c,
                                                    self.z_c,self.s_c,self.Z_c_agg,self.X_c_agg,self.VA_c_agg,self.Y_c_agg,self.S_c_agg,self.p_c_agg)
                self.counter += 1
                
        print("Warning: \n all the shock variables are equal to the last sensitivity file: \'{}\' ".format(i))
        
    def sensitivity(self,path):

        from functions.data_read import sens_info
        from functions.utility import dict_maker
        from functions.utility import value_from_excel
        import functions.shock_io as sh
        from functions.io_calculation import cal_flows
        from functions.aggregation import aggregate
        import glob
        
        '''
        sensitivity:
            This function can be used for sensitivity analysis on a parameter
            
        Arguments
        ----------
        path:  string
            Defines the path of an excel file, in which the shock is identified
            according to the example in the tutorial.
        '''    
        
        # Given the path, sens_info is called to take all the information of
        # sensitivity such as the directory, paramaters, type of the shock and so on.
        directs,sensitivity_info = sens_info (path)
        
        i=0     # Counter for the number of sensitivities in every shock

        # For every set of sensitivities, a folder is created by the code 
        # Which contains all the whole shock related to the specific sensitivity
        
        for file in directs:
            
            # In every folder all the excels should be taken
            excels = [f for f in glob.glob(file + "**/*.xlsx", recursive=True)]
            
            # Storing the main information of the sensitivity in the results dictionary
            self.results['sensitivity_{}'.format(self.s_counter)]={'information':sensitivity_info[str(i)]}
            
            # Check the affected matrices in every shock inserted in the excel file
            mat_list = sensitivity_info[str(i)]['matrices']
            
            # Printing the information related to the every set of sensitivities
            print('Sensitivity {}. Affected Matrices: {}'.format(i+1,mat_list))
            i+=1
            
            # Implementing all the excel files taken in the previous step for
            # every set of sensitivities
            for excel in excels:
                
                value_from_excel(excel)
                # Taking a copy of all matrices to have both changed and unchanged ones
                Y_c   = self.Y.copy()
                va_c  = self.va.copy()
                s_c   = self.s.copy()
                z_c   = self.z.copy()
                
                # check the type of the shock and calling the function
                if 'Y' in mat_list  : Y_c  = sh.Y_shock  (excel,Y_c.copy())                      
                if 'Z' in mat_list  : z_c  = sh.Z_shock  (excel,z_c.copy(),self.Z.copy(),self.X.copy())
                if 'VA' in mat_list : va_c = sh.VA_shock (excel,va_c.copy(),self.VA.copy(),self.X.copy())
                if 'S' in mat_list  : s_c  = sh.S_shock  (excel,s_c.copy(),self.S.copy(),self.X.copy())
                

                # Calculating the shock result
                l_c,X_c,VA_c,S_c,Z_c,p_c = cal_flows(z_c,Y_c,va_c,s_c,self.indeces)        

                # Aggregation of the results
                X_c_agg,Y_c_agg,VA_c_agg,S_c_agg,Z_c_agg,p_c_agg = aggregate(X_c,Y_c,VA_c,S_c,Z_c,p_c)
                
                # Taking the name of excel file and removing .xlsx to use it 
                # for indexing the stored data related to sensitivities in
                # results dictionaries
                value = str(excel).replace(".xlsx","").replace('{}\case_'.format(file), "")
                
                # Storing the data in results dictionary
                self.results['sensitivity_{}'.format(self.s_counter)][value]=\
                    dict_maker(Z_c,X_c,VA_c,p_c,Y_c,va_c,
                               z_c,s_c,Z_c_agg,X_c_agg,VA_c_agg,
                               Y_c_agg,S_c_agg,p_c_agg)
            
            self.s_counter+=1
                                                                   
        
    def impact(self,p_life,saving_sce,invest_sce,imports=['Import'],w_ext=['Water'], em_ext=['CO2'], land=['Land'], labour=['Labor - Skilled','Labor - Semi Skilled','Labor - Unskilled'],capital=['Capital - Machines']):
        
        '''
        impact:
            This function can be used for the impact assessment analysis of an
            implemented policy
         
         Arguments   
        ----------
        p_life: float
            Project lifetime in terms of Years
        
        saving_sce  : list
            it represents the non-investment steps of the project
            [number of the scneario,type of scenario]
            example:
                saving_sce = [1,'se']
                
                'se': represnets that the information should be taken from sensitivites
                  1 : shows that the first sensitivity should be taken
            Note: 'se' == sensitivity , 'sh' == shock
        
        invest_sce: list
            it represents the investment steps of the project
            similar to saving_sce
            
        imports  :  list
            Represents the category of 'imports' in the imported database
             
        w_ext :  list
            Represents the category of 'water use' in the imported database

        em_ext  :  list
            Represents the category of 'emissions' in the imported database
             
        land :  list
            Represents the category of 'land' use in the imported database
            
        labour  :  list
            Represents the category of 'labour' in the imported database
             
        capital :  list
            Represents the category of 'capital' use in the imported database            
        
        
        -----------------------------------------------------------------------
        Note: To add new indicators, the user can modify the indicators
        through functions.impact.impact_assessment accoring to the function
        guide
        -----------------------------------------------------------------------
        '''
        
        from functions.impact import impact_assessment
        
        # calculating the impacts using the impact_assessment function
        self.impact = impact_assessment(invest_sce,saving_sce,self.results,p_life,w_ext,em_ext,land,labour,capital,imports)
        
        # Saving the results of impcat assessment
        self.results['impact_{}'.format(self.i_counter)]=self.impact
        self.i_counter += 1
        
        
        
    def obj_save(self,file_name):
        
        '''
        obj_save:
            This function can be used to save the whole object in a binary file
         
         Arguments   
        ----------
        file_name: string
            Specifies the name of the file to store the object.
        ''' 
        
        import pickle 
        
        with open(file_name, 'wb') as config_dictionary_file:
            pickle.dump(self,config_dictionary_file)
        
        
        
        
        
        
        
        
        
        
        
        
        