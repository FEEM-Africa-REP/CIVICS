import REP_CVX

kenya = REP_CVX.C_SUT(path = r'Database\Kenya_2014_SAM.xlsx', unit='M KSH', name='Shading Trees')
#%% Investment impact
kenya.shock_calc(path=r'Shading Trees\Shading Trees.xlsx', Y=True)

kenya.plot_dx()
kenya.plot_dv(level='Activities', drop='unused')
kenya.plot_dv(level='Commodities', drop='unused')
kenya.plot_ds(indicator='CO2')
kenya.plot_ds(indicator='Water', color=['Blue','Green','Gray'])
kenya.plot_ds(indicator='Energy', color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
kenya.plot_ds(indicator='FAO Land')
#%% Operation impact
kenya.shock_calc(path=r'Shading Trees\Shading Trees.xlsx', Z=True, VA=True, S=True)

kenya.plot_dx(level='Commodities', unit='K USD')
kenya.plot_dv(level='Activities', drop='unused', unit='K USD')
kenya.plot_dv(level='Commodities', drop='unused')
kenya.plot_ds(indicator='CO2')
kenya.plot_ds(indicator='Water', color=['Blue','Green','Gray'])
kenya.plot_ds(indicator='Energy', color=['darkgreen','black','orange','aqua','royalblue','gold','peru','yellow','palegreen'])
kenya.plot_ds(indicator='FAO Land')
#%% Sensitivity analysis
kenya.sensitivity(path=r'Shading Trees\Shading Trees.xlsx')

kenya.plot_sens(variable='VA', sc_num=1)
kenya.plot_sens(variable='VA', sc_num=2)
#%% Impact assessment
kenya.impact_assess(p_life=20, saving_sce=['sh',2], invest_sce=['sh',1])
kenya.impact_assess(p_life=20, saving_sce=['se',2], invest_sce=['sh',1])
kenya.impact_assess(p_life=20, saving_sce=['sh',2], invest_sce=['se',1])
#%% Storing all the results
results = kenya.results