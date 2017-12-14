#!/usr/bin/python
# coding: utf-8

# In[1]:

#Relevant video:
#http://www.youtube.com/watch?v=VIt2z6zJrMs&t=1m52s

#My output from code:
#https://www.youtube.com/watch?v=E_yE2Q0ArpM

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import scipy.integrate as ing

d2r = np.pi/180.  #deg to radian
k2f = 1.68781  #knots to ft per sec
kilo=10.**3  

###--Import and basic data manipulation--####

#-Load dataset 1-#
a1 = np.loadtxt('./dumb2.dat') #My data: uses Youtube timestamp
#Source:
#https://drive.google.com/file/d/0ByW1n-WOmDAEeDlPSGc1UHpDcWs/view?usp=sharing
a1=a1.T
#index map:: 0:time[s], 1:aspd[kt], 2:alt[kft], 3:Mach#?, 4:G, 5:Ptich[deg]

a1[2]=a1[2]*kilo #convert from kiloft to ft

#Break velocity into components and convert to f/s
xv1=np.multiply(a1[1],np.cos(d2r*a1[5])*k2f)
yv1=np.multiply(a1[1],np.sin(d2r*a1[5])*k2f)


#-Load dataset 2-#
a2 = np.loadtxt('./dumb5.dat')  #from reddit.com/user/what_are_you_saying
#Original Source:
#https://drive.google.com/file/d/0B0DNIvRXrB1jeWdBYkVkZ1ByOXM/view
#reformatted source for correct pitch data:
#https://drive.google.com/file/d/0ByW1n-WOmDAEY2ZOZFZQQXdnZ0k/view?usp=sharing
a2=a2.T
#index map:: 0:time[s], 1:aspd[kt], 2:alt[ft], 3:Ptich[deg]

xv2=np.multiply(a2[1],np.cos(d2r*a2[3])*k2f)
yv2=np.multiply(a2[1],np.sin(d2r*a2[3])*k2f)

###--Numerically integrate to get position, using 2 methods
#     Simpson & CumulativeTrapezoid methods, (whoever
#     named that function didnt think about phrasing)--###

#dataset 1
n = len(a1[0])
xp11 = np.empty(n)
xp12 = np.empty(n)
yp11 = np.empty(n)
yp12 = np.empty(n)
yp12[0]=yp11[0]=xp11[0]=xp12[0]=0.
for i in range(1,n):
    xp11[i]=ing.simps(xv1[0:i],a1[0,0:i])
    yp11[i]=ing.simps(yv1[0:i],a1[0,0:i])
    
xp12=ing.cumtrapz(xv1,a1[0],initial=0.)
yp12=ing.cumtrapz(yv1,a1[0],initial=0.)

#dataset 2
n = len(a2[0])
xp21 = np.empty(n)
xp22 = np.empty(n)
yp21 = np.empty(n)
yp22 = np.empty(n)
yp22[0]=yp21[0]=xp21[0]=xp22[0]=0.
for i in range(1,n):
    xp21[i]=ing.simps(xv2[0:i],a2[0,0:i])
    yp21[i]=ing.simps(yv2[0:i],a2[0,0:i])
    
xp22=ing.cumtrapz(xv2,a2[0],initial=0.)
yp22=ing.cumtrapz(yv2,a2[0],initial=0.)


# In[2]:

###--Create idealized circular trajectory--###

#Circle trajectory parameters:
xcirc=3800   #xcenter
ycirc=13550  #ycenter
radc=3000    #radius circle
xstart=0.    #start x val
xend=10000.  #ending x val
ystart=ycirc - radc

nc=60 #data points in circle, only make multiple of 10!

#get circl points starting at bottom
def circlepts(xc,yc,r,frac):
    yret=r*np.sin((frac-0.25)*2*np.pi)+yc
    xret=r*np.cos((frac-0.25)*2*np.pi)+xc
    return (xret, yret)


xpts = np.empty(nc)
ypts = np.empty(nc)
for i in range(0,nc):    
    xpts[i], ypts[i] = circlepts(xcirc,ycirc,radc,float(i)/float(nc))
    

xlin1= np.empty(nc/10)
ylin1= np.empty(nc/10)
xlin2= np.empty(nc/10)
ylin2= np.empty(nc/10)
delx=float(xcirc-xstart)/float(nc/10)
delx2=float(xend-xcirc)/float(nc/10)
for i in range(0,nc/10):
    xlin1[i]=xstart + i*delx
    ylin1[i]=ystart
    xlin2[i]=xcirc + (i+1)*delx2
    ylin2[i]=ystart

xtraj=np.concatenate((xlin1,xpts,xlin2))
ytraj=np.concatenate((ylin1,ypts,ylin2))


# In[3]:

###--Comparison plots of data available and analysis methods--###

plt.plot(xp11,a1[2],label='1) Simps vs Alt')
plt.plot(xp12,a1[2],label='1) CumTrap vs Alt')
plt.plot(xp12,yp12+a1[2,0],label='1) CumTrap vs CumTrap')

plt.plot(xp21,a2[2],label='2) Simps vs Alt')
plt.plot(xp22,a2[2],label='2) CumTrap vs Alt')
plt.plot(xp22,yp22+a2[2,0],label='2) CumTrap vs CumTrap')

plt.plot(xtraj,ytraj,label='Idealized circular Traj')

plt.axis([0,12000,8000,20000])
plt.axis("equal")
plt.legend()
plt.show()


# In[5]:

fig, ax = plt.subplots()
plt.axis("equal") #keeps plot on a 1:1 x:y scale

plt.axis([-1000,12000,8000,20000]) #Plot ranges

xjet=xp11
yjet=a1[2]

line, = ax.plot(xjet[0:3],yjet[0:3],label='Actual Trajectory')
line2, = ax.plot(xtraj[0],ytraj[0],label='Circular Trajectory')
plt.legend() #Comment to remove legend

xlen=len(xjet)
clen=len(xtraj)

def animate(i):
    if(i < 2*xlen and (i%2)==0): #Plot the actual trajectory first
        line.set_xdata(xjet[0:i/2]) #Only go every 2 to be slower
        line.set_ydata(yjet[0:i/2])
    elif(i< (2*xlen+clen) and i > 2*xlen): #Plot the circle trajectory second
        line2.set_xdata(xtraj[0:i-2*xlen+1])
        line2.set_ydata(ytraj[0:i-2*xlen+1])
    
    return (line,line2)


# Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(yjet, mask=True))
    line.set_xdata(np.ma.array(xjet, mask=True))
    line2.set_ydata(np.ma.array(ytraj, mask=True))
    line2.set_xdata(np.ma.array(xtraj, mask=True))
    return (line, line2)

ani = animation.FuncAnimation(fig, animate, np.arange(4, (2*xlen+clen)), init_func=init,
                              interval=120, blit=False)

plt.show() #Comment to not show animation


# In[117]:

#Save file method
#ani.save(filename='test4.mpeg', writer="ffmpeg", fps=30, dpi=140, codec=None, bitrate=8000, extra_args=None, metadata=None, extra_anim=None, savefig_kwargs=None)


# In[ ]:



