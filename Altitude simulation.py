#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 11:23:34 2018

@author: johnvdk
"""

import matplotlib.pyplot as plt

R = 8.31
g = 9.81
m = 28.9/1000
y = 1.4
dz = 0.1
I = 100000
P_0 = 101000
T = 273 + 15
Alt = [0]
Pvals = [P_0]


for x in range (1,I+1):
    Pi = Pvals[x-1]
    if (Pi > 101000/2.718):
        Pvals.append(Pi - m*g/(R*T)*Pi*dz)
        T = T - m*g/R*(1-1/y)*dz
        Alt.append(x*dz)
    else:
        break

print(Alt[-1])
plt.plot(Alt[:], Pvals[:], 'r')
plt.xlabel('Altitude (m)')
plt.ylabel('Pressure (Pa)')