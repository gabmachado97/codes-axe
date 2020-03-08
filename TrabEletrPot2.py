# -*- coding: utf-8 -*-
"""
Created on Mon May 27 08:34:08 2019

@author: Gabriel Machado
"""
from __future__ import division #Python 2.x
from sympy.solvers import solve
from sympy import Symbol

#Ganho Estático
def GanhoEstatico(Vo, Vi):
       D = Symbol('D')
       return solve((D/(1-D)) - (Vo/Vi), D)

#Indutor   
def Indutor(P, Vi, D, delta_Il, fs):
       Il_md = P/(D*Vi)
       return ((Vi*D)/(delta_Il*Il_md*fs))
       
#Capacitor
def Capacitor(P, Vo, D, delta_Vo, fs):
       Ic = P/Vo
       return ((Ic*D)/(delta_Vo*Vo*fs))

#Dados Fornecidos
Vi = 90 #[V]
Vo = 60 #[V]
P  = 180 #[W]
fs = 20000 #[Hz]
delta_Vo = 0.01 # [1%]
delta_Il = 0.1


D = GanhoEstatico(Vo,Vi)[0]

L = Indutor(P, Vi, D, delta_Il, fs)

C = Capacitor(P, Vo, D, delta_Vo, fs)

R = (Vo**2)/P

print(L,C,D,R)