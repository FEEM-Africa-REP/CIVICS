# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 13:53:42 2020

@author: Amin
"""
def style_check(style):
    
    styles = ['defualt','classic','Solarize_Light2','_classic_test','bmh',
              'dark_background','fast','fivethirtyeight','ggplot','grayscale',
              'seaborn','seaborn-bright','seaborn-colorblind','seaborn-dark',
              'seaborn-dark-palette','seaborn-darkgrid','seaborn-deep',
              'seaborn-muted','seaborn-notebook','seaborn-paper',
              'seaborn-pastel','seaborn-poster','seaborn-talk','seaborn-ticks',
              'seaborn-white','seaborn-whitegrid','tableau-colorblind10']
    
    if style not in styles:
        
        raise ValueError ('{} is not correct. Acceptable styles are : \n {} \n For more information: https://matplotlib.org/3.1.1/gallery/style_sheets/style_sheets_reference.html'.format(style,styles))
        
    return style
    
    
def disp (nodes,fig_format,unit,conversion,style,date_format,title_font,production,imports,exports,figsize,demand,colors,names,rotate,average,sp_techs,sp_nodes,directory):
    
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib import gridspec
    
    from calliope_graph.graphs import style_check  
    from calliope_graph.matrixmaker import prod_imp_exp
    
    style = style_check(style)
    plt.style.use(style)
    
    if average == 'weekly':
        av = '1w'
    elif average == 'daily':
        av = '1d'
    elif average == 'monthly':
        av = '1m'
    elif average == 'hourly':
        av = '1h'
    elif average == 'yearly':
        av = '1y'
            
    else:
        raise ValueError ('Incorrect average type.\n Average can be one of the followings: {},{},{},{} and {}'.format('hourly','daily','weekly','monthly','yearly'))
    
    for i in nodes:
        
        data = prod_imp_exp(production,imports,exports,i)
        


        demand[i] = demand[i].resample(av).mean()
        data0     = data[0].resample(av).mean()
        data1     = data[1].resample(av).mean()
        

        
        
        if sp_techs!= None and i in sp_nodes:
            

                
            fig, (axs) = plt.subplots(2, figsize=figsize,sharex=True)
            gs = gridspec.GridSpec(2, 1,height_ratios=[3,1]) 
            
            axs[1] = plt.subplot(gs[1])
            axs[0] = plt.subplot(gs[0],sharex=axs[1])
            
            plt.setp(axs[0].get_xticklabels(), visible=False)
               
            
            axs[0].margins(x=0)
            axs[0].margins(y=0.1)

            axs[1].margins(x=0)
            axs[1].margins(y=0.1)
            
            axs[0].plot(demand[i].index,demand[i].values*conversion,'black',alpha=0.5, linestyle = '--', label ='Demand',linewidth=3)
                
            # Drawing positivie numbers
            axs[0].stackplot(data0.index,data0.values.T*conversion,colors=colors[data0.columns],labels=names[data0.columns])
                
            # Drawing negative numbers
            axs[0].stackplot(data1.index,data1.values.T*conversion,colors=colors[data1.columns],labels=names[data1.columns])                
                
            axs[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,frameon=True)
                
            axs[1].stackplot(data0.index,data0[sp_techs].values.T*conversion,colors=colors[sp_techs])
            
            # xticks properties
            xfmt = mdates.DateFormatter(date_format)
            axs[1].xaxis.set_major_formatter(xfmt)
            axs[1].tick_params(axis='x', rotation=rotate)



        else:
            
            fig,(ax) = plt.subplots(1,figsize=figsize)
            ax.margins(x=0)
            ax.margins(y=0.1)
            
            # Drawing demand line
            plt.plot(demand[i].index,demand[i].values*conversion,'black',alpha=0.5, linestyle = '--', label ='Demand',linewidth=3)
            
            # Drawing positivie numbers
            plt.stackplot(data0.index,data0.values.T*conversion,colors=colors[data0.columns],labels=names[data0.columns])
            
            # Drawing negative numbers
            plt.stackplot(data1.index,data1.values.T*conversion,colors=colors[data1.columns],labels=names[data1.columns])
            
            # Legend properties
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,frameon=True)
            
            
            # xticks properties
            xfmt = mdates.DateFormatter(date_format)
            ax.xaxis.set_major_formatter(xfmt)
            plt.xticks(rotation=rotate)
        
            # labels
            plt.xlabel('Date')
            plt.ylabel(unit)
            
        # Title
        plt.title('{} Dispatch'.format(i),fontsize=title_font)
        
        
        # saving 
        try:
            plt.savefig('{}\{}_{}_dispatch.{}'.format(directory,i,average,fig_format), dpi=fig.dpi,bbox_inches='tight')
            plt.show()
        except:
            plt.show()
        


        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        