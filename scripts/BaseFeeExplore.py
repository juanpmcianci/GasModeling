#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 11:41:46 2022

@author: juan
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#%%
# reads dataset
df=pd.read_csv('message_gas_economy.csv')
#gets it indexed by block height
df=df.sort_values(by='height')
df=df.set_index('height')
diffBase=np.concatenate([[0.],np.diff(df['base_fee'])])
G_tilde=8*diffBase/df['base_fee']
G_tt=df['gas_fill_ratio']-1
plt.plot(G_tilde)
plt.plot(G_tt)
plt.show()
#%%
plt.plot(G_tt[:-1],np.exp(df['base_fee_change_log'][1:]),'.')
#%%
def autocorrelation(x):
    from numpy.fft import ifftshift
    from scipy.fftpack import fft, ifft
    xp = ifftshift((x - np.average(x))/np.std(x))
    n, = xp.shape
    xp = np.r_[xp[:n//2], np.zeros_like(xp), xp[n//2:]]
    f = fft(xp)
    p = np.absolute(f)**2
    pi = ifft(p)
    return np.real(pi)[:n//2]/(np.arange(n//2)[::-1]+n//2)

from statsmodels.graphics.tsaplots import plot_acf
plot_acf(np.array(df['base_fee'])[:1000])
# # Gets G tilde, given by 
# #
# #   8(b_{t+1}-b_t)/b_{t}=tilde{G}
# #
# #%%
# diffBase=np.concatenate([[0.],np.diff(df['base_fee'])])
# G_tilde=8*diffBase/df['base_fee']

# # let's look at it:
# plt.plot(G_tilde)
# plt.hlines(-1,0,len(G_tilde),'r')
# plt.hlines(1,0,len(G_tilde),'r')
# plt.show()
# plt.hist(G_tilde,bins=100)
# plt.tight_layout()
# plt.show()    
