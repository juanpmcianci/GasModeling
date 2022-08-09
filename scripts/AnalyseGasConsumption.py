#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 18:21:21 2022

@author: juan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..utils.getData import sentinel
import matplotlib
font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 12}
matplotlib.rc('font', **font)
#%%
def getGtilde(base_fee):
    N=len(base_fee)
    block_array=[base_fee['height'].iloc[0]]
    G_tilde_array=[]
    base_fee_array=[base_fee['parent_base_fee'].iloc[0]]
    for n in range(1,N):
        if base_fee['height'].iloc[n]-base_fee['height'].iloc[n-1]==1:
            block_array.append(base_fee['height'].iloc[n])
            bfn=base_fee['parent_base_fee'].iloc[n]
            bfn_=base_fee['parent_base_fee'].iloc[n-1]
            Gt=8*(bfn-bfn_)/bfn_
            G_tilde_array.append(Gt)
            base_fee_array.append(bfn)
            
    block_array=np.array(block_array)[:-1]
    G_tilde_array=np.array(G_tilde_array)
    base_fee_array=np.array(base_fee_array)[:-1]
    return block_array, G_tilde_array,base_fee_array
        

f = open("SecretString.txt", "r")
NAME_DB=f.read()
#initializes the class
db=sentinel(NAME_DB)
MIN_BLOCK=1900000
#gets base fee and sorts dataframe
base_fee=db.getParentBaseFee(MIN_BLOCK)
base_fee=base_fee.sort_values('height')
base_fee.set_index('height')
MAX_BLOCK=base_fee.index[-1]
blocks,G_tilde,base_fees=getGtilde(base_fee)
#%%
#gets derived gas output dataframe
G_TARGET=5_000_000_000
G_MAX=10_000_000_000
G=G_tilde*G_TARGET+G_TARGET
# presents some prelimnary plots:    
plt.figure(figsize=(18,9))
plt.subplot(221)
plt.plot(blocks,base_fees/1E9) # to convert from attoFIL to nanoFIL
plt.title('Base fee (nanoFIL) vs block number')
plt.xlabel('block number')
plt.ylabel(r'$b_t$')
plt.subplot(222)
plt.plot(blocks,G_tilde)
plt.title('Normalized gas consumption vs block number')
plt.xlabel('block number')
plt.ylabel(r'$\tilde{G}_t$')
plt.subplot(223)
plt.hist(G_tilde,bins=100,density=True)
plt.title('Histogram normalized gas consumption')
plt.xlabel(r'$\tilde{G}_t$')
plt.tight_layout()
#Gas usage
G=G_tilde*G_TARGET+G_TARGET
plt.subplot(224)
plt.plot(blocks,G)
plt.title('Gas consumption vs block number')
plt.xlabel('block number')
plt.ylabel(r'${G}_t$')
plt.tight_layout()
plt.savefig('gasConsumption.png')
#%%
THRESHOLD=0.95
peaks=(G_tilde>THRESHOLD)
valleys=-1*(G_tilde<-THRESHOLD)

plt.figure(figsize=(18,9))
plt.subplot(221)
plt.plot(blocks[-5000:],peaks[-5000:])
plt.xlabel('block number')
plt.title(' High demand peak (Gas above '+str(THRESHOLD)+')')
plt.subplot(222)
plt.plot(blocks,valleys)
plt.title(' low demand valley (Gas below -'+str(THRESHOLD)+')')
plt.xlabel('block number')
plt.subplot(223)
plt.title(r'$\tilde{G}_{t}-\tilde{G}_{t-1}$')
plt.xlabel('block number')
plt.plot(np.diff(G_tilde))
plt.subplot(224)
plt.title(r'Histogram $\tilde{G}_{t}-\tilde{G}_{t-1}$')
plt.xlabel('block number')
plt.hist(np.diff(G_tilde),bins=100,density=True)
plt.tight_layout()
plt.savefig('gasPeaks.png')

#%%
def timeBetweenPeaks(G,blocks,M,high=True):
    if high:
        peaks=G>M
    else:
        peaks=G<-M
    blockWithPeak=blocks[peaks]
    timeBetween=np.diff(blockWithPeak)
    return timeBetween
#%%

timeHighUse=timeBetweenPeaks(G_tilde, blocks, THRESHOLD)
timelowUse=timeBetweenPeaks(G_tilde, blocks, THRESHOLD,high=False)
# looks at the time between events
plt.hist(timeHighUse,bins=100,density=True,label='Histogram')
# uses an MLE to fit the poisson distr, which just has \lambda=mean(obs)
lam=1./np.mean(timeHighUse)
dens=lambda x:lam*np.exp(-lam*x)
xx=np.arange(1,150)
plt.title('Time between two high-ussage peaks')
plt.plot(xx,dens(xx),label=r'Exp($\lambda$), $\lambda$='+str(round(lam,3)))
plt.xlabel('number of blocks')
plt.ylabel('density')
plt.savefig('gasPeaksHistogram.png')
plt.legend()

    
    
    

    
    







