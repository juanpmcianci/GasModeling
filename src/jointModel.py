#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 17:16:46 2022

Here we implement the joint gas model:

@author: juan
"""



import numpy as np


def GasOneStep(n:int,
                  X:np.ndarray,
                  h:float,
                  s:float,
                  b_tn_plus_half:float,
                  bStar:float,
                  m:np.ndarray,
                  Gamma:np.ndarray):

    dim=np.size(X)
    #Xp=X+h*s*np.abs(b_tn_plus_half-bStar)*(m-X)+h**0.5*Gamma@np.random.standard_normal(dim)
    Xp=X+h*s*(m-X)+h**0.5*Gamma@np.random.standard_normal(dim)

    return Xp    
    




def baseFeeHalfStep(n:int,
                    b:float,
                    h:float,
                    cFun:callable,
                    G:float):
    '''
    

    Parameters
    ----------
    n : int
        DESCRIPTION.
    b : float
        DESCRIPTION.
    h : float
        DESCRIPTION.
    cFun : callable
        DESCRIPTION.
    G : float
        DESCRIPTION.
    GStar : float
        DESCRIPTION.

    Returns
    -------
    bh : TYPE
        DESCRIPTION.

    '''
    
    
    
    
    
    tn=n*h
    c=cFun(tn)
    bh=b+0.5*h*b*c*G
    return bh



def runJointModel(T,N,x0,b0,m,c,s,gamma,BStar):
    '''
    

    Parameters
    ----------
    T : TYPE
        DESCRIPTION.
    N : TYPE
        DESCRIPTION.
    x0 : TYPE
        DESCRIPTION.
    b0 : TYPE
        DESCRIPTION.
    m : TYPE
        DESCRIPTION.
    c : TYPE
        DESCRIPTION.
    s : TYPE
        DESCRIPTION.
    gamma : TYPE
        DESCRIPTION.
    GStar : TYPE
        DESCRIPTION.
    BStar : TYPE
        DESCRIPTION.

    Returns
    -------
    b : TYPE
        DESCRIPTION.
    x : TYPE
        DESCRIPTION.

    '''
    h=T/N
    dim=np.size(x0)
    x=np.zeros((N+1,dim))
    b=np.zeros(N+1)
    x[0]=x0
    b[0]=b0
    bh=[]
    #starts main loop
    for n in range(N):
        
        #takes a half-step of b
        b_half=baseFeeHalfStep(n=n,
                            b=b[n],
                            h=h,
                            cFun=c,
                            G=np.sum(x[n,:]))
        bh.append(b_half)
        
        # takes full step of log gas
        x[n+1]=GasOneStep(n=n,
                          X=x[n],
                          h=h,
                          s=s,
                          b_tn_plus_half=b_half,
                          bStar=BStar,
                          m=m,
                          Gamma=Gamma)
        

        #takes last half step of base fee
        b[n+1]=baseFeeHalfStep(n=n+1,
                            b=b[n],
                            h=h,
                            cFun=c,
                            G=np.sum(x[n+1,:]))
        
    return b,x
    
    


if __name__=='__main__':
    #tests the joint dynamic. Here we preallocate some data
    import matplotlib.pyplot as plt
    T=10
    N=1000  
    dim=1
    x0=np.zeros(dim)
    b0=0.1 #nanoFIL
    B_STAR=0.1 #nanoFIL
    c=lambda x: 0.125
    s=5
    Gamma=0.05*np.eye(dim)
    m=x0
    
    base_fee,gas=runJointModel(T=T,
                                   N=N,
                                   x0=x0,
                                   b0=b0,
                                   m=m,
                                   c=c,
                                   s=s,
                                   gamma=Gamma,
                                   BStar=B_STAR)

    
    times=np.linspace(0,T,N+1)
    plt.plot(times,gas)
    plt.title('Gas consumption')
    plt.show()
    
    
    plt.plot(times,base_fee)
    plt.title('base fee')
    plt.show()
    
    plt.plot(gas,base_fee,'.')
    plt.title('base fee vs gas')
    plt.show()
    

    
    
            



    


