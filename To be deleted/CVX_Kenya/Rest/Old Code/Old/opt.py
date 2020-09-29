# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:15:35 2020

@author: Amin
"""

# Short Example on final demand optimization:
import civivs_sut as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')

kenya.shock(path = r'Database\Shock.xlsx' , Z = True )
kenya.calc_all()
kenya.add_dict()
results = kenya.results
kenya.optimize(scenario=1)
X_opt =kenya.X_opt

#%%
import cvxpy as cp
import numpy as np
import pandas as pd

VA_const = results['VA'].sum(axis=1).values.reshape(len(results['VA']),1)

shares = results['Y'].values / results['Y'].sum().values
#%%

va = results['va_1'].values
z  = results['z_1'].values


x = cp.Variable(shares.shape,nonneg=True)

VA = va @ x

L = np.identity(len(z))-z
Y  = L @ x 

obj = cp.atoms.affine.sum.sum(Y)



objective= cp.Maximize(obj)

Y_const = cp.atoms.affine.binary_operators.multiply(shares,obj)

constraints = [VA == VA_const,Y>=Y_const,Y>=0]

problem = cp.Problem(objective,constraints)

result = problem.solve(verbose=True)

Y_old = kenya.Y
X_old = kenya.X
new_Y = pd.DataFrame(Y.value,index=Y_old.index,columns = Y_old.columns)
new_X = pd.DataFrame(x.value,index=X_old.index,columns = X_old.columns)

my_VA = VA.value



#%%

delta_x = new_X - X_old
delta_Y = new_Y - Y_old
delta_VA = VA_const - my_VA
#%%
shares_1 =new_Y.values / new_Y.sum().values
