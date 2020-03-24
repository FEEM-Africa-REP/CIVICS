########### Pulping Machine Shock ##############


import civivs_sut as cvx
#%%        
negar=cvx.C_SUT(r'Database\Kenya_2014_SAM.xlsx')
#%%
negar.parse()
#%%
negar.calc_all()
#%%
Y_old=negar.Y
x_old=negar.x
VA_old=negar.VA
IMP_old=negar.IMP
INV_old=negar.INV
A_old=negar.A
x_agg_old = negar.x_agg
VA_agg = negar.VA_agg

#%%
# Implementing the shock: Pulping machine
# Investment
# 1. Metals and machines (commodity)
Num_machine = 500
Mach_inv = 0.155  #MSh (we transfer it from kilo shillings to million shillings)
negar.INV.loc[('commodity','Metals and machines (commodity)'),('General investment saving')] = \
    negar.INV.loc[('commodity','Metals and machines (commodity)'),('General investment saving')].values + Mach_inv * Num_machine
    
#2. Transport
Trs_cost = 5/1000.0  #MSh
negar.INV.loc[('commodity','Transport (commodity)'),'General investment saving'] = \
    negar.INV.loc[('commodity','Transport (commodity)'),'General investment saving'].values + Trs_cost * Num_machine
    #%%
#Matrix of Technical Coefficients
# Use side
#  a)coffe commodity into high rainfall (increase in productivity)
prod_coef=0.98
negar.A.loc[('commodity','Coffee (commodity)'),('industry','High Rainfall (commercial production)')] = \
      negar.A.loc[('commodity','Coffee (commodity)'),('industry','High Rainfall (commercial production)')].values*prod_coef
      #%%
#  b)Use of diesel (petroleum commodity)
diesel_coef=0.01 #MSh
negar.A.loc[('commodity','Petroleum (commodity)'),('industry','High Rainfall (commercial production)')] = \
      negar.A.loc[('commodity','Petroleum (commodity)'),('industry','High Rainfall (commercial production)')].values+diesel_coef*Num_machine
      #%%
#value added
# Unskilled labour reduction
lab_coef=0.7
negar.va.loc[('value added0','Unskilled labour 0 High Rainfall'),('industry','High Rainfall (commercial production)')] = \
    negar.va.loc[('value added0','Unskilled labour 0 High Rainfall'),('industry','High Rainfall (commercial production)')].values*lab_coef
    #%%
#environmental effect
#water footprint reduction
WFN_coef=0.15
negar.e.loc[('WaterFootprintNetwork','WFN: Total water footprint (Mm3/yr) - Blue'),('industry','High Rainfall (commercial production)')] = \
    negar.e.loc[('WaterFootprintNetwork','WFN: Total water footprint (Mm3/yr) - Blue'),('industry','High Rainfall (commercial production)')].values*WFN_coef
#%%
negar.calc_all()
#%%
Y_new=negar.Y
x_new=negar.x
VA_new=negar.VA
IMP_new=negar.IMP
INV_new=negar.INV
A_new=negar.A
x_agg_new = negar.x_agg
VA_agg_new = negar.VA_agg
#%%
#Impelementing the shock: Shading tree Managment    
negar.plot_dx(x_agg_old,x_agg_new,level=False,Type='bar')   
negar.plot_dv(VA_agg.loc['taxes'],VA_agg_new.loc['taxes'],level='commodity',Type='bar') 
      
      

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    