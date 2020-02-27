#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[15]:


data=pd.read_csv("./medianRent.csv", encoding='utf-8')
data.head()


# In[16]:


a=pd.DataFrame(data['quarter'].str.split('-',expand=True).values, columns=['year','q'])


# In[17]:


data=pd.concat([data,a],axis=1,ignore_index=False)


# In[18]:


data['median_rent']=pd.to_numeric(data['median_rent'],errors='coerce').fillna(0)
#data['median_rent'].replace({'na':int(0)})


# In[19]:


town_unique=data['town'].unique()
year_unique=data['year'].unique()
flat_unique=data['flat_type'].unique()
quarter_unique=['Q1','Q2', 'Q3', 'Q4']


# In[20]:


import panel.widgets as pnw
import panel as pn
#pn.extension()
from matplotlib.figure import Figure 

#print (list(data['flat_type'].unique()))


# In[21]:


#variable  = pnw.RadioButtonGroup(name='Room_Type', value='EXEC', 
#                                 options=list(data['flat_type'].unique()))
#window  = pnw.IntSlider(name='window', value=2019, start=2005, end=2019, step=1)
#print(type([variable.value]), variable.value,[variable.value], len(variable.options), variable.options[:],variable.options[1])
#print([window.value], type([window.value]))

def find_output(variable, window):
    year=[window]
    r_type=variable
    return mpl_plot(year,r_type,variable)
    
    
def mpl_plot(year,r_type,variable):
    fig2,ax2=plt.subplots(figsize=(12,8))
    fig2.subplots_adjust(bottom=0.4)
  
    #Increase space for x axis labels: subplots_adjust will do it. 
    #You can play with the bottom keyword to get a good placement of the bottom of the plot
    #fig.subplots_adjust(bottom=0.2)
    
    ax2.tick_params(axis="y", labelsize=12)
    barWidth=0.2
    town_count=0
    #print(r_type, type(r_type))
    for i in year:
        #for q in quarter_unique:
            for s in [variable]:
                #print('s',s)
                for t in  town_unique:#['ANG MO KIO','BEDOK','BISHAN', 'BUKIT BATOK','BUKIT MERAH']:
                    
                    
                    mr=data[(data['year']==str(i)) & (data['town']==str(t)) & (data['flat_type']==str(s))]
                    #print (mr)

                    #print ('start barWidth', barWidth)

                    barWidth=1+barWidth

                    #print ('barWidth + town_count:',barWidth)
                    qCol=np.arange(len(quarter_unique))
                    qCol1=[0.2*x+barWidth for x in qCol]

                    #print (qCol1)

                    l1=ax2.bar(qCol1[0],mr[mr['q']==quarter_unique[0]]['median_rent'],0.2,color='#ff0000',label='1st Quarter')
                    l2=ax2.bar(qCol1[1],mr[mr['q']==quarter_unique[1]]['median_rent'],0.2,color='#A9A9A9',label='2nd Quarter')
                    l3=ax2.bar(qCol1[2],mr[mr['q']==quarter_unique[2]]['median_rent'],0.2,color='#080000',label='3rd Quarter')
                    l4=ax2.bar(qCol1[3],mr[mr['q']==quarter_unique[3]]['median_rent'],0.2,color='#0000FF',label='4th Quarter')


                    ax2.set_xticks(np.arange(len(town_unique))+1.45)
                    ax2.set_xticklabels(town_unique,{'fontsize':10},rotation=90,)


                    #print(barWidth)
                    #print('town_count', town_count)
    ax2.set_ylabel('$/month',{'fontsize':12},rotation=90,)
    fig2.legend([l1, l2, l3, l4],     # The line objects
                           labels=quarter_unique,   # The labels for each line
                           fontsize=8, 
                           loc="center right",   # Position of legend
                           bbox_to_anchor=(1,0.5), #A 2-tuple (x, y) places the corner of the 
                                                   #legend specified by loc at x, y.(based on proportion to fig size)
                           borderaxespad=0,    # Small spacing around legend box
                           title="Median Rental\nBy Quarter",  # Title for the legend
                           title_fontsize=10
                           )
    fig2.suptitle('Median Rental By Year And Town For Year {} \n  {} '.format(year,r_type), fontsize=18)
    plt.close()
    return fig2
    #fig2.suptitle(t,fontsize) - add a centered title to the figure
#find_output(variable,window)


# In[22]:


variable  = pnw.RadioButtonGroup(name='Room_Type', value='EXEC', 
                                 options=list(data['flat_type'].unique()))
window  = pnw.IntSlider(name='Year', value=2019, start=2005, end=2019, step=1)
print(type([variable.value]), variable.value,[variable.value], len(variable.options), variable.options[:],variable.options[1])
print([window.value], type([window.value]))


# In[23]:



@pn.depends(variable, window)
def response_output(variable, window):
     return find_output(variable, window)

widgets_show   = pn.Column("<br>\n# <font size='3'>Flat Type</font>", variable, window)
print(widgets_show)


# In[24]:


median_rent = pn.Row(response_output, widgets_show)

median_rent.show()


# In[ ]:




