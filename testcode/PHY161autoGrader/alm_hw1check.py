
# coding: utf-8

# In[66]:

import pandas as pd
import sys

#xdata = np.linspace(0.01,10.,200)
#ydata = xdata**1.15

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if( len(sys.argv) < 2):
    print "No cmd line arg for dummy txt save data\n"
    sys.exit()
dumfile = str(sys.argv[1])
print ("Dummy file passed: "+dumfile)

def alm_llsquares(xd, yd):
    xm = xd.mean()
    ym = yd.mean()
    
    m = np.sum( (xd-xm)*(yd-ym) ) / np.sum( (xd-xm)**2 )
    b = ym - m*xm
    
    return (m,b) #dummy return


# In[89]:

mym, myb = alm_llsquares(xdata,ydata)
studm, studb = llsquares(xdata,ydata)
dm = np.abs(mym-studm)
db = np.abs(myb-studb)
gra1 = 0.0
com1 = str("")
if( dm < 1.e-12):
    gra1 += 2.5
else :
    com1 += " Slope off by "
    com1 += "{:.2E}".format(dm)
    com1 += "."
    
if( db < 1.e-12):
    gra1 += 2.5
else :
    com1 += " Y-int off by "
    com1 += "{:.2E}".format(db)
    com1 += "."
              


# In[90]:

#dumfile="dum4.csv"
d1=[{'Grade': gra1, 'Comment': com1}]
pd.DataFrame(data=d1).to_csv(dumfile)
#print(pd.DataFrame(data=d1))


# dum = pd.read_csv(dumfile, skipinitialspace=True)
# print(dum)
# ckey = dum.keys()[1]
# gkey = dum.keys()[2]
# gread = str(dum.get_value(0,gkey))
# cread = str(dum.get_value(0,ckey))

# In[ ]:




# In[ ]:



