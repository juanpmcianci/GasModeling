#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 11:17:06 2022

This module is used to get the relevant data from the 
sentinel database.

Needs: SQLAlchemy and pandas
pip install SQLAlchemy==1.3.7
It also needs a connection string to the sentinel DB, which im storing locally
as a txt file. You'll need to provide this. 

@author: JP, juan.madrigalcianci@protocol.ai
"""

import sqlalchemy as sqa
import pandas.io.sql as psql



class sentinel:
    '''
    class to connect to the sentinel database.
    '''
    def __init__(self,connString):
     try:
         self.connection =sqa.create_engine(connString).connect()
         print('connected to sentinel')
     except:
         print ("Error while connecting")
    
        
    def getDB(self,dbName:str,minBlock=None):
        '''
        Connects to one of the datasets from sentinel

        Parameters
        ----------
        dbName : str
            name of the dataset. see here: 
            https://lilium.sh/data/models/#messages.
        MinBlock, int, optional
            minimum block to get the extraction
        
        Returns
        -------
        df : pandas.DataFrame
            pandas dataframe containing the requested dataset

        '''

   
        print('fetching '+dbName+' ...')
        SQL=''' SELECT * FROM  "visor"."'''+dbName+'''"''' 
        df=psql.read_sql(SQL, self.connection)
        return df
    
    def customSQL(self,SQL):
        print('performing custom query...')
        df=psql.read_sql(SQL, self.connection)
        print('done!')
        return df
        
    
    def getGasfromBlock(self,minBlock:int,unique:bool=False):
        '''
        Connects to the serived_gas_outputs dataset starting from minBlock to
        the current block. 

        Parameters
        ----------
        minBlock : int
            Smallest block to get the info from. Daset starts at block 806639.
        unique : bool, optional
            Set to True if only interested in the info on minBlock.
            The default is False.

        Returns
        -------
        df : pandas.DataFrame
            pandas dataframe containing the requested dataset

        '''

        if unique:
            tail='where height='+str(minBlock)
            print('''fetching derived_gas_output database at block ''' 
                  +str(minBlock)+ ' ...')
        else:
            tail='where height>'+str(minBlock)
            print('''fetching derived_gas_output database from block ''' 
                  +str(minBlock)+ ' ...')
        SQL='''
        SELECT  "gas_fee_cap", "gas_premium", "gas_limit", "size_bytes", "nonce",
        "method", "state_root", "exit_code", "gas_used", "parent_base_fee", 
        "base_fee_burn", "over_estimation_burn", "miner_penalty", "miner_tip",
        "refund", "gas_refund", "gas_burned", "height", "actor_name", "actor_family"
        FROM "visor"."derived_gas_outputs" '''+str(tail)
        df=psql.read_sql(SQL, self.connection)
        print('done')
        return df
        
    def getParentBaseFee(self,minBlock):
        '''
        Connects to the serived_gas_outputs dataset starting, and outputs the parent base fee
        of each block. 

        Parameters
        ----------
        minBlock : int
            Smallest block to get the info from. Daset starts at block 806639.

        Returns
        -------
        df : pandas.DataFrame
            pandas dataframe containing the requested dataset

        '''
        print('''fetching parent_base_fee database  from block ''' 
                  +str(minBlock)+ ' ...')
        SQL='''
        SELECT DISTINCT parent_base_fee, height 
        FROM "visor"."derived_gas_outputs" 
        WHERE height>
        '''+str(minBlock)
        df=psql.read_sql(SQL, self.connection)
        print('done')
        return df                




    
if __name__=='__main__':
    import time
    # reads the connection string stored as a text file in 
    # SecretString.txt
    f = open("SecretString.txt", "r")
    NAME_DB=f.read()
    
    #initializes the class
    db=sentinel(NAME_DB)
    #gets derived gas output dataframe
    MIN_BLOCK=2044500
    t0=time.time()
    #df=db.getGasfromBlock(minBlock=MIN_BLOCK,unique=False)
    tf=time.time()-t0
    print('request time '+str(tf) +'seconds')    
    


    
