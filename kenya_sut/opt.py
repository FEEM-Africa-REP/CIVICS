# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:15:35 2020

@author: Amin
"""

# Short Example on final demand optimization:
import civivs_sut as cvx
kenya = cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')

kenya.shock(path = r'Database\Shock.xlsx' , Y = True )
kenya.calc_all()
kenya.add_dict()
kenya.shock(path = r'Database\Shock.xlsx' , Z = True )
kenya.calc_all()
kenya.add_dict()
results = kenya.results
#%%
import cvxpy as cp
#%%
VA = results['VA']
my_VA = VA.sum(axis=1)

my_Fin = results['Y']

#%%
VA = results['VA_2']
Yoo_VA = VA.sum(axis=1)

Yoo_Fin = results['Y_2']
small_va = results['va_2']
#%%

an = small_va.values @ my_Fin.values


#%%


## Findin the shares
shares = my_Fin.copy()
summ = my_Fin.sum().values
shares = shares / summ
new_z = results['z_2']
#%%
x = cp.Variable(my_Fin.shape,nonneg=True)
new_VA = small_va.values @ x  # Constraint
import numpy as np
newfd = (np.identity(len(new_z)) - new_z.values) @ x # constraint and obj

obj = newfd.atoms.affine.sum.sum()

fdconst = my_Fin.copy()
fdconst = fdconst * obj
fdconst = fdconst.values

internal = new_z.values @ x

constraints = []
constraints.append(new_VA=my_VA.values)
constraints.append(newfd=fdconst)
objective = cp.Minimize(obj)
problem = cp.Problem(objective,constraints)


