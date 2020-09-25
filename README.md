# REP_CVX
**R**esearch **E**mpowerment **P**artnership **C**omprehens**IV**e & **I**ntegrated **C**ountry **S**tudy

---
## Dscription
REP_CVX is a python module developed by REP research group in Fondazione Eni Enrico Mattei for CIVICS Kenya Project with to aim to provide an open-source tool for performing **Input-Output** analysis based on the **Supply and Use Framework**.

The module uses excel files as the input data and the outputs are in form of plots, excel files and binary files.

Main features:

    *Performing the Input-Output Calculations based on the supply and use framework
    *Shock implementation
    *Sensitivity Analysis on every specific shock implementation
    *Policy impact assessment
    *Visualizing results and generating reports
    
    
    
---
### Where to find it
The full source code is available on **Github** at : http://github.com - automatic!

To use the code, copy it in your site-packages directory: 

    e.g. anaconda3\Lib\site-packages
    
 ---
 ### Quickstart
 ##### Note:
 
 4 examples of the kenya study (refer to paper) are provided in (link bede be file tuye github).
 
To Use it:
``` python
import REP_CVX 

case = REP_CVX.C_SUT(path='Path of your Supply and Use Table according to the structure',unit='Representing the unit of measure of the monetary values of the table')
```
 
