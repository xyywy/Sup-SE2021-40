# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import scipy.ndimage
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from obspy.io.segy.segy import _read_segy

from matplotlib import collections

from mpl_toolkits.axes_grid1 import make_axes_locatable

#import matplotlib.pyplot as pylab
import matplotlib.style
import matplotlib as mpl


#这个应该是原始的追踪型RMOpicker的设计。最初的构想。是给定一个起始点，starting time，然后依照NRM field的原理进行追踪。但是发现，一切都错了。因为NRM是从origin 到 ref的过程。所以，从origin到ref的矢量矫正才有效。所以，给定的starting time不会有任何作用。即便是能track到rmo，也是因为smooth比较强烈，然后弄出的巧合。那应该怎么办呢。1. 在生成NRM的时候，讲Origin和Ref调换位置，然后一切就能按照原始构想做成了。2. 将NRM场进行自矫正，然后进行accumulative summation，然后在给定的任何的starting time，就可以从一条直线上，取到所有的RMO的picks的值。所以，在我们的出版物里，我们暂时将错纠错，虽然我们还没有比较accumulative的RMO和原始构想的RMO的区别有多大，但是视觉上看，差别很小。所以，就说是，采用方法1得来的。
#################################STYLE#############################

mpl.style.use('default')

mpl.rcParams['font.size'] = 6
mpl.rcParams['lines.linewidth'] = 0.2
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['lines.markersize'] = np.sqrt(0.5)
mpl.rcParams['scatter.marker'] = "v"
#mpl.rcParams['figure.figsize'] = 5, 5
#mpl.rcParams['image.aspect'] = "equal"

######################DEFINE PATH AND MAIN OBJECTS##############
ip1 = _read_segy(r'./inputdata_withavo/3D_SYN_SO190_313_41.sgy', headonly=True)
ip2 = _read_segy(r'./inputdata_withavo/3D_DISPLACE_SO190_313_OPS.sgy', headonly=True)
ip3 = _read_segy(r'./inputdata_withavo/3D_SYN_FLAT_SO190_313_41.sgy', headonly=True)
ip4 = _read_segy(r'./inputdata_withavo/3D_CPICKS_SO190_313_41.sgy', headonly=True)


print(ip1)
#fig,ax1,ax2 = plt.subplots()
dt = 2e-3
y = np.linspace(0.,500.,2501)

fig,((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharey='all', sharex='all')
#fig,((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharey=False, sharex=False)


#ax1_off.get_shared_x_axes().join(ax1_off, ax3_off, ax2_off,ax4_off,)



#####################DISPLACEMENT############################
ip2_seis = np.stack(t.data for t in ip2.traces)*1
ip2_seis = scipy.signal.resample(ip2_seis,500,axis=1)


vm = np.percentile(ip2_seis, 100)

#fig,ax2 = plt.subplots()

print(ip2_seis.shape)

vm = np.percentile(ip2_seis, 100)


disimage = ax2.imshow(ip2_seis.T, cmap="bwr", vmin=-6, vmax=6, aspect="auto")
ax2.set_xlim(0,41)

t2 = ax2.text(0.03,0.93,'(b) NRM Displacement Field', transform=ax2.transAxes)
t2.set_bbox(dict(facecolor='white', alpha=1, edgecolor='white'))

'''
cbaxes = fig.add_axes([0.92, 0.53, 0.015, 0.35]) 
cb = plt.colorbar(disimage, cax = cbaxes,  label='NRM Time Shift [ms / trace]')  
#here we use a tricky method to customize a new axe according to the global fractin position
#and append the colorbar to the new axe. fraction spatial position have to be tested. 
'''


###############################RMOCPICKS########################
'''
ip4_seis = np.stack(t.data for t in ip4.traces)*0.0002
ip4_seis = scipy.signal.resample(ip4_seis,1050,axis=1)

vm = np.percentile(ip4_seis, 99)

#fig,ax2 = plt.subplots()

print(ip4_seis.shape)

vm = np.percentile(ip4_seis, 99)

#ax2.plot()

ax4.imshow(ip4_seis.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto')

#ax2.colorbar()

'''

###########################WIGGLESOF3dSYN##################



one_trace = ip1.traces[1]

#offsets = [1., 2., 3., 4.]
offsets = np.linspace(0.,40.,41)

for offset in offsets:

    one_trace = ip1.traces[int(offset)]
    ampl=offset + one_trace.data*0.00006
   
    ax1.plot(ampl,y,'k-', linewidth=0.2)
    
    ax1.fill_betweenx(y,offset,ampl,where=(ampl>offset),color='k',linewidth=0.1)

    
    ax1.set_ylim(500,0)
    ax1.set_xlim(-0.5,40.5)
    #ax1.imshow(ip2_seis.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto')
    #if offset == float(70):
    #    break
     
t1 = ax1.text(0.03,0.93,'(a) Synthetic Gather', transform=ax1.transAxes)
t1.set_bbox(dict(facecolor='white', alpha=1, edgecolor='white'))


############################WIGGLE_FLAT############################
one_trace_2 = ip3.traces[1]
#offsets = np.linspace(1,71,71)
#offsets = np.linspace(0.,70.,71)


for offset in offsets:

    one_trace_2 = ip3.traces[int(offset)]
    
    ampl_2=offset + one_trace_2.data*0.00006
    #ampl_2 = scipy.signal.resample(ampl_2,5250,axis=0)
    ax3.plot(ampl_2,y,'k-')
    
    ax3.fill_betweenx(y,offset,ampl_2,where=(ampl_2>offset),color='k',linewidth=0.1)
    #ax3.fill_betweenx(y,offset,ampl_2,where=(ampl_2>offset),color='k')
    
#    ax3.set_ylim(130,30)
#    ax3.set_xlim(15,25)
    ax3.set_ylim(500,0)
    ax3.set_xlim(-0.5,40.5)
    
t3 = ax3.text(0.03,0.93,'(c) Flattened Synthetic Gather', transform=ax3.transAxes)
t3.set_bbox(dict(facecolor='white', alpha=1, edgecolor='white'))
#####################picker design#################################

matrix = ip2_seis * -1.00


#####################first hori#############################
ns = np.arange(0,41)
starttime = 126
overall = np.array([])
y3 = np.arange(0,41)

for n in ns:
    disvalue = matrix[n, int(starttime)]
    starttime = disvalue + starttime
    overall = np.append (overall, [starttime])
    #if n == 71:
    #    break


#y3 = np.arange(0,71)

ax4.scatter(y3, overall,label='RMO_Pick_1')

#####################second hori#############################
ns = np.arange(0,41)
starttime = 204
overall = np.array([])

for n in ns:
    disvalue = matrix[n, int(starttime)]
    starttime = disvalue + starttime
    overall = np.append (overall, [starttime])
    #if n == 71:
    #    break


y3 = np.arange(0,41)

ax4.scatter(y3, overall,label='RMO_Pick_2')


#####################third hori#############################
ns = np.arange(0,41)
starttime = 256
overall = np.array([])

for n in ns:
    disvalue = matrix[n, int(starttime)]
    starttime = disvalue + starttime
    overall = np.append (overall, [starttime])
    #if n == 71:
    #    break


#y3 = np.arange(0,71)

ax4.scatter(y3, overall,label='RMO_Pick_3')

#####################fourth hori#############################
ns = np.arange(0,41)
starttime = 366
overall = np.array([])

for n in ns:
    disvalue = matrix[n, int(starttime)]
    starttime = disvalue + starttime
    overall = np.append (overall, [starttime])
    #if n == 71:
    #    break


#y3 = np.arange(0,71)

ax4.scatter(y3, overall, label='RMO_Pick_4')
plt.legend(fontsize=5, loc='lower left',frameon=False, ncol=2)

t4 = ax4.text(0.03,0.93,'(d) NRM Residual Depth Error', transform=ax4.transAxes)
t4.set_bbox(dict(facecolor='white', alpha=1, edgecolor='white'))
########################OFFSET_AXE_TWINY###################################


ax1_off = ax1.twiny()      #TWIN THE X AXE As offsetdomain
ax2_off = ax2.twiny()      #TWIN THE X AXE As offsetdomain
ax3_off = ax3.twiny()      #TWIN THE X AXE As offsetdomain
ax4_off = ax4.twiny()      #TWIN THE X AXE As offsetdomain


oldticks = ax1.get_xticks()

newticks = []
for X in oldticks:
    newticks.append(X * 0.1)


#intnewticks = [int(i) for i in newticks] #I dont know why we have this int module. 


ax1_off.set_xticks(oldticks)
ax1_off.set_xbound(ax1.get_xbound())
ax1_off.set_xticklabels(newticks)

ax2_off.set_xticks(oldticks)
ax2_off.set_xbound(ax1.get_xbound())
ax2_off.set_xticklabels(newticks)

ax3_off.set_xticks(oldticks)
ax3_off.set_xbound(ax1.get_xbound())
ax3_off.set_xticklabels(newticks)

ax4_off.set_xticks(oldticks)
ax4_off.set_xbound(ax1.get_xbound())
ax4_off.set_xticklabels(newticks)


ax3_off.set_xticklabels([]) #set the twin axe lable to nothing
ax4_off.set_xticklabels([]) #set the twin axe lable to nothing

ax1.set_ylabel('Depth [km]')
ax3.set_ylabel('Depth [km]')

ax1_off.set_xlabel('Offset [km]')
ax2_off.set_xlabel('Offset [km]')

ax3.set_xlabel('Trace Number')
ax4.set_xlabel('Trace Number')
#################### Y axis MOD ''''''''''''''''''''''''''
oldyticks = ax1.get_yticks()

newyticks = []
for X in oldyticks:
    newyticks.append(X * 0.001 + 3)

ax1.set_yticks(oldyticks)
ax1.set_ybound(ax1.get_ybound())
ax1.set_yticklabels(newyticks)
####################NRM COLOR BAR###########################################

cbaxes = fig.add_axes([0.92, 0.53, 0.015, 0.35]) 
cb = plt.colorbar(disimage, cax = cbaxes, label='NRM DEPTH ERROR [m / trace]')


#here we use a tricky method to customize a new axe according to the global fractin position
#and append the colorbar to the new axe. fraction spatial position have to be tested. 

###########################LETS_SHOW#########################################

#plt.show()

plt.savefig("NRM_syn.pdf", dpi=500)
plt.savefig("NRM_syn.png", dpi=500)
            
            
            
            
            
'''

decon_seis = np.stack(t.data for t in decon.traces)

#print(decon_seis.shape)

vm = np.percentile(decon_seis, 99)

#print("The 99th percentile is
{:.0f}; the max amplitude is
{:.0f}".format(vm, decon_seis.max()))

plt.imshow(decon_seis.T, cmap="Greys", vmin=-vm, vmax=vm, aspect='auto')

plt.figure(figsize=(18,6))

plt.imshow(decon_seis.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto')

plt.colorbar()

plt.show()



ax = plt.subplots()

ip1_seis = np.stack(t.data for t in ip1.traces)

#print(decon_seis.shape)

vm = np.percentile(ip1_seis, 99)

#print("The 99th percentile is
{:.0f}; the max amplitude is
{:.0f}".format(vm, ip1_seis.max()))

ax.fill_betweenx(ip1_seis.T,ip1.traces,ip1_seis,where=(ip1_seis>ip1.traces),color='k')

plt.imshow(ip1_seis.T, cmap="Greys", vmin=-vm, vmax=vm, aspect='auto')

plt.figure(figsize=(18,6))

plt.imshow(ip1_seis.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto')

plt.ylabel('time (s)')

plt.xlabel('trace')

plt.colorbar()

plt.show()



ip2_seis = np.stack(t.data for t in ip2.traces)

#print(decon_seis.shape)

vm = np.percentile(ip2_seis, 99)

#print("The 99th percentile is
{:.0f}; the max amplitude is
{:.0f}".format(vm, ip2_seis.max()))

plt.imshow(ip2_seis.T, cmap="Greys", vmin=-vm, vmax=vm, aspect='auto')

plt.figure(figsize=(18,6))

plt.imshow(ip2_seis.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto')

plt.colorbar()

plt.show()

'''
