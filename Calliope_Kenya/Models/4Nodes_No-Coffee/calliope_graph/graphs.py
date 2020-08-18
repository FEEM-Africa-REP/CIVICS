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
    
    
def disp (nodes,fig_format,unit,conversion,style,date_format,title_font,production,imports,exports,figsize,demand,colors,names,rotate):
    
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    from calliope_graph.graphs import style_check  
    from calliope_graph.matrixmaker import prod_imp_exp
    
    style = style_check(style)
    
    
    for i in nodes:
        plt.style.use(style)
        data = prod_imp_exp(production,imports,exports,nodes)
        
        fig,(ax) = plt.subplots(1,figsize=figsize)
        ax.margins(x=0)
        ax.margins(y=0.1)
        
        
        # Drawing demand line
        plt.plot(demand[i].index,demand[i].values/conversion,'black',alpha=0.5, linestyle = '--', label ='Demand',linewidth=3)
        
        # Drawing positivie numbers
        plt.stackplot(data[0].index,data[0].values.T/conversion,colors=colors[data[0].columns],labels=names[data[0].columns])
        
        # Drawing negative numbers
        plt.stackplot(data[1].index,data[1].values.T/conversion,colors=colors[data[1].columns],labels=names[data[1].columns])
        
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
        plt.savefig('{}_dispatch.{}'.format(i,fig_format), dpi=fig.dpi,bbox_inches='tight')
        plt.show()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        