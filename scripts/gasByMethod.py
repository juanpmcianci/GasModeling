#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 15:02:29 2022

@author: juan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from getData import sentinel
import matplotlib
import seaborn as sn

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 12}
matplotlib.rc('font', **font)

def mergeDataframes(dfs:list,axis:str):
    dd=dfs[0]
    N=len(dfs)
    for i in range(1,N):
        dd=pd.merge(dd,dfs[i],on=axis)
    return dd


def byMethod(df:pd.DataFrame,quantity:str):
    listOfMethods=np.unique(df['method'])
    blocks=df['height'].unique()
    

    dd={'height':blocks}    
    for ll in listOfMethods:
        dd[ll]=[]
    
    
    
    for bb in blocks:
        for mm in listOfMethods:
            aux=df[df['height']==bb]
            dd[mm].append(aux[quantity][aux['method']==mm].sum())
    
    dd=pd.DataFrame(dd)
    return dd

#%%
    
MIN_BLOCK=2045000

    
SQL1='''
SELECT  "cid", "gas_fee_cap", "gas_premium", "gas_limit", "size_bytes", "nonce",
 "exit_code", "gas_used", "parent_base_fee", 
"base_fee_burn", "over_estimation_burn", "miner_penalty", "miner_tip",
"refund", "gas_refund", "gas_burned", "height", "actor_name", "actor_family"
FROM "visor"."derived_gas_outputs" 
WHERE height>
'''+str(MIN_BLOCK)
    
SQL1='''
SELECT  "cid", "gas_fee_cap", "gas_premium", "gas_limit", "gas_used", 
"parent_base_fee", "base_fee_burn", "over_estimation_burn", "gas_burned", "height"
FROM "visor"."derived_gas_outputs" 
WHERE height>'''+str(MIN_BLOCK)

SQL2='''
SELECT "cid", "value" FROM  "visor"."messages" WHERE height>'''+str(MIN_BLOCK)


SQL3='''
SELECT "cid", "method" FROM  "visor"."parsed_messages" WHERE height>'''+str(MIN_BLOCK)




f = open("SecretString.txt", "r")
NAME_DB=f.read()
#initializes the class
db=sentinel(NAME_DB)

d1=db.customSQL(SQL1)
d2=db.customSQL(SQL2)
d3=db.customSQL(SQL3)
df=mergeDataframes([d1,d2,d3], axis='cid')
df.to_csv('usage.csv')
#%%
df=df.sort_values(by='height')
valueByMethod=byMethod(df=df,quantity='value')
GasByMethod=byMethod(df=df,quantity='gas_used')
#%%
plt.figure(figsize=(16,9))
corrMatrix = GasByMethod.corr()
sn.heatmap(corrMatrix, annot=True)
plt.title('Correlation matrix, total gas used by method')
plt.savefig('corrTotalGas.png')
plt.show()
#%%
plt.figure(figsize=(16,9))
valueByMethod = valueByMethod.loc[:, (valueByMethod != 0).any(axis=0)]
corrMatrix = valueByMethod.corr()
sn.heatmap(corrMatrix, annot=True)
plt.title('Correlation matrix, FIL sent by method')
plt.savefig('corrFIL.png')
plt.show()
#%%
listOfMethods=np.unique(df['method'])
blocks=df['height'].unique()
for mm in listOfMethods:
    
    plt.figure(figsize=(16,9))
    plt.suptitle(mm)
    plt.subplot(121)
    plt.plot(blocks,GasByMethod[mm])
    plt.xlabel('blocks')
    plt.ylabel('Total gas ussage, '+mm)
    plt.subplot(122)
    plt.hist(GasByMethod[mm],bins=100)
    plt.xlabel('Total gas ussage, '+mm)

    plt.savefig('usage_method_'+mm+'.png')
    


    
    
    
    







