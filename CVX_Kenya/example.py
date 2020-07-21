# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 14:02:39 2020

@author: Amin


#################### HOW TO USE THE MODEL ############################
"""
#1. Import the the mode and database

import REP_CVX as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%%
# Now You can have access to all the information You want.
"""
LIST OF THE PARAMETERS:
    1. X : production
    2. V : supply matrix
    3. U : use matrix
    4. Z : technical coefficient matrix
    5. VA: value added matrix
    6. S : satellite account matrix
    7. Y : final demand
    
Note: all the coefficients have the same index but with small letters.
Note: all the information after the shock will have the same index + _c
"""
# For example:

X = kenya.X     # Production
VA = kenya.VA   # Value added
#%%
"""
Implementing a shock:
    
    In order to implement a shock, you just need to fill an excel file with
    a precise format and shape.
    
    After that, you need to call a function to impelent the shock.
    
Note: for every single shock, the shock will be implemented regarding the baseline

FUNCTION:
    shock(path,Y,S,VA,Z)
    
    path = specifies the path of the excel file
    
    all the other parameters shows that if you want to implement a shock on the 
    specific matrix or not. For example:
        Y = True means that the shock will be implemented in final demand
    default situation is False meaning that if you do not make the differenet 
    parameters True, the code will take it False(no shock will be impelemted)
    
Now suppose that we want to impelement a shock on the final demand:
"""
# Now the shock is implemented
kenya.shock(path = r'Database\Shock_pulp.xlsx' , VA = True )

# in the next step we need to calculate all the other information after shock.
# for this reason, we just need to run the following function:
kenya.calc_all()
#%%
"""
Storing results in a dictionary:
    You can save the results in every step into a dictionary so you can track
    all the results step by step. The results will be saved on a parameter named:
        database
The following fucntion should be used.
"""
kenya.add_dict()
#%%
"""
Aggregation of the results:
    As the number of the sectors and commodities are high, data can be aggregated running the following function
Note: all the result will have the same index as befor + _agg
"""
kenya.aggregate()

X_agg = kenya.X_agg
X_c_agg = kenya.X_c_agg
#%%
"""
Implementing a shock:
    
    In order to implement a shock, you just need to fill an excel file with
    a precise format and shape.
    
    After that, you need to call a function to impelent the shock.
    
Note: for every single shock, the shock will be implemented regarding the baseline

FUNCTION:
    shock(path,Y,S,VA,Z)
    
    path = specifies the path of the excel file
    
    all the other parameters shows that if you want to implement a shock on the 
    specific matrix or not. For example:
        Y = True means that the shock will be implemented in final demand
    default situation is False meaning that if you do not make the differenet 
    parameters True, the code will take it False(no shock will be impelemted)
    
Now suppose that we want to impelement a shock on the final demand:
"""
# Now the shock is implemented
kenya.shock(path = r'Database\Shock_pulp.xlsx' , VA = True )

# in the next step we need to calculate all the other information after shock.
# for this reason, we just need to run the following function:
kenya.calc_all()
#%%
"""
Storing results in a dictionary:
    You can save the results in every step into a dictionary so you can track
    all the results step by step. The results will be saved on a parameter named:
        database
The following fucntion should be used.
"""
kenya.add_dict()
#%%
"""
Visualizing Results:
    
    all the parameters can be visualized easily.
    
    1. plot_dx = plotting the change of production. Parameters are:
        aggregation --> a.True: aggregated results will be represented b.False: complete results will be shown
        Kind --> 'bar' 
        Unit -->  a.'M KSH': monetary values in Million Kenyan Shelings , b. 'M USD': monetary values in Million US Dollars 
        stacked --> True 
        level --> a. None: both activities and commodities, b. Activities , c. Commoditites
        
    2. plot_dv = plotting the change of value added. Parameters are:
        aggregation --> a.True: aggregated results will be represented b.False: complete results will be shown
        Kind --> 'bar' 
        Unit -->  a.'M KSH': monetary values in Million Kenyan Shelings , b. 'M USD': monetary values in Million US Dollars 
        stacked --> True 
        level --> a. None: both activities and commodities, b. Activities , c. Commoditites   
        drop --> a.'unused': remove unused from the results, b.None: keep all the information

    3. plot_dp = plotting the change of prices. Parameters are:
        aggregation --> a.True: aggregated results will be represented b.False: complete results will be shown
        level --> a. None: both activities and commodities, b. Activities , c. Commoditites   

"""
kenya.plot_dv()
kenya.plot_dx()
kenya.plot_dp()
#%%
"""
Saving Results in form of excel files:
    
    for this purpose, you can use the function of: Save_all. Parameters are:
        1. path: specifies the path you want to save the results
        2. level: a. None: both baseline and shock , b. baseline, c. shock
        3. drop: a. None: saving all the results, b. 'unused: remove the unused results'
"""
kenya.Save_all(path=r'C:\Users\Amin\Documents\GitHub\My Kenya\kenya_sut\Result')
#%%
"""
At the end, you can have a database of results :-)
    
"""
database = kenya.results
#%%
import cvxpy as opt
#%%












