#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:56:29 2022

Here we implement the OH process


@author: juan
"""

import numpy as np


def Ornstein_Uhlenbeck(theta:callable,
                       x0:float,
                       mu:float,
                       sigma:float,
                       T:float,
                       N:int):

    
    h=T/N
    t=0
    x=np.zeros(N+1)
    x[0]=x0
    
    for i in range(N):
        x[i+1]=x[i]+h*theta(t)*(mu-x[i])+sigma*h**0.5*np.random.standard_normal()
        t+=h
    return x


if __name__=='__main__':
    
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 22})
    theta1=lambda t: 4
    theta2=lambda t: 16
    x0=2
    sigma=1
    mu=0.1
    T=10
    N=1000
    G1=Ornstein_Uhlenbeck(theta1, x0, mu, sigma, T, N)
    G2=Ornstein_Uhlenbeck(theta2, x0, mu, sigma, T, N)
    time=np.linspace(0,T,N+1)
    
    plt.figure(figsize=(18,9))
    plt.subplot(121)
    plt.plot(time,G1,label=r'$\theta$='+str(theta1(1))+r', $\mu=$'+str(mu)+
             r', $\sigma=$'+str(sigma))
    plt.plot(time,G2,label=r'$\theta$='+str(theta2(1))+r', $\mu=$'+str(mu)+
             r', $\sigma=$'+str(sigma))
    plt.hlines(mu, 0, T,'k', label=r'$\mu$')
    plt.title('OU process')
    plt.legend()
    plt.subplot(122)

    plt.plot(time,np.exp(G1),label=r'$\theta$='+str(theta1(1))+r', $\mu=$'+str(mu)+
             r', $\sigma=$'+str(sigma))
    plt.plot(time,np.exp(G2),label=r'$\theta$='+str(theta2(1))+r', $\mu=$'+str(mu)+
             r', $\sigma=$'+str(sigma))
    plt.hlines(np.exp(mu),0 , T,'k',  label=r'$\mu$')
    plt.title(' Exp OU process')
    plt.legend()    
    
    
    
    
   
    
    
    
    
    
    


