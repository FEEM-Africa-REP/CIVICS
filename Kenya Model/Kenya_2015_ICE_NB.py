# KENYA as it is in 2015

import calliope
import Graphs as gg

calliope.set_log_level('INFO')
model = calliope.Model('model.yaml')
model.run()

model.to_csv(r'C:\Users\stevo\Dropbox (FEEM)\REP\CIVICS Kenya\Energy Model\Kenya_Operation_2015 - BioExperiments\Gasificator+ICE\Nairobi\Results')

gg.Dispatch_reg(model,'bio_coffee_pp','NBOR')
gg.Dispatch_sys(model,'bio_coffee_pp')