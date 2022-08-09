#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 16:22:25 2022

@author: juan
"""

import pandas as pd
import numpy as np
from getData import sentinel
#%% reads dataset
f = open("SecretString.txt", "r")
NAME_DB=f.read()
#initializes the class
db=sentinel(NAME_DB)
#gets derived gas output dataframe
MIN_BLOCK=2000000
df=db.getGasfromBlock(minBlock=MIN_BLOCK,unique=False)
base_fee=db.getParentBaseFee(MIN_BLOCK)
df=df.sort_values('height')
#%% groups by block.
dfg=df.groupby(by=['height','actor_family','method'])['gas_used'].sum()
number_of_messages_per_block=df.groupby(by='height').count()
df_per_block=df.groupby(by=['height']).sum()
G_LIMIT=10_000_000_000.
G_TARGET=10_000_000_000./2.
#%%
import matplotlib.pyplot as plt

base_fees=np.array(df.groupby(by=['height'])['parent_base_fee'].unique())
base_fees=np.concatenate(base_fees)
plt.subplot(131)
plt.plot(base_fees/1E9)
plt.subplot(132)
G_tilde=8*np.diff(base_fees)/base_fees[:-1]
plt.plot(G_tilde)
plt.subplot(133)
plt.hist(G_tilde,bins=30)
plt.tight_layout()