# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:28:11 2019

@author: Gabriel Machado
"""

from __future__ import division #Python 2.x
import numpy as np
import math

class ProjetoEletromagnetico(object):
       def __init__(self, L, Ipico, Ief, Bmax, Jmax, Kw, fs):
              self.L = L
              self.Ipico = Ipico
              self.Ief = Ief
              self.Bmax = Bmax
              self.Jmax = Jmax
              self.Kw = Kw
              self.fs = fs
              
       def nucleo(self):
              return (10**4)*(self.L*self.Ipico*self.Ief)/(self.Bmax*self.Jmax*self.Kw) #[Minimo em cm^4]
       
       def espirras(self, Ae):
              return (self.L*self.Ipico)/(self.Bmax*Ae)
              
       def entreferro(self,N, uo, Ae):
              return ((N**2)*uo*Ae*10**(-2))/self.L
       
       def condutores(self):
              delta = 7.5/(np.sqrt(self.fs)) #Profundidade de penetração da corrente
              diametro = 2*delta #Diametro máximo
              return delta, diametro
              
       def condutores_paralelo(self, Sfio):
              S = self.Ief/self.Jmax #Seção mínima
              Nfios = S/Sfio #Quantidade de fios
              return S, Nfios
       
       def carretel(self, N, Nfios, Sfio, Aw):
              Afio = N*Nfios*Sfio #Área de condutores
              kw = Afio/Aw
              return kw
       
       def perdas_nucleo(self, deltaI, Vnucleo):
              kh = 4*(10**(-5))
              kf = 4*(10**(-10))
              deltaB = self.Bmax*deltaI/self.Ipico
              return (deltaB**2.4)*(kh*fs + kf*(self.fs**2))*Vnucleo

       def perdas_cobre(self, l, N, Nfios):
              ro = 2.21*(10**(-8))/100 #Slide convertido para ohm/cm
              R = ro*l*N/Nfios #Eq.(23) Ivo Barbi
              return R*(self.Ief**2)
              
if __name__ == '__main__':     
         
       Vi     = 90 #[V]
       P      = 180 #[W]
       D      = 0.4 
       L      = 0.0036 #[H]
       C      = 0.0001 #[F]
       Jmax   = 450 #[A/cm²]
       Bmax   = 0.25 #[T]
       Kw     = 0.5
       fs     = 20000 #[Hz]
       delta_Il = 0.1
       Ipico  = 5.2551927
       Imin   = 4.75
       Ief    = 5.0179468
       uo     = 4*np.pi*10**(-7)

       PE = ProjetoEletromagnetico(L, Ipico, Ief, Bmax, Jmax, Kw, fs)

       AeAw = PE.nucleo()
       print("Núcleo: %f cm4" %AeAw)

       #Modelo NEE-65/33/26
       Ae = 532/100 #cm²
       Aw = (4.42 - 1.93)*2.2 #Datasheet (Lext-Lmeio)*h
       print("AeAw Real: %f cm4" %(Ae*Aw))
       N = math.ceil(PE.espirras(Ae/10000)) #->para m²
       print("N: %f" %N)

       Lentf = PE.entreferro(N, uo, Ae)
       print("Ientf: %f cm" %Lentf)

       _, Dmax = PE.condutores()
       print("Diâmetro máximo condutor: %f mm" %(Dmax*10))
       
       #Bitola escolhida: 20 AWG / 0.813mm
       Sfio = np.pi*(0.813/(10*2))**2 #cm²
       _, Nfios = PE.condutores_paralelo(Sfio)
       Nfios = math.ceil(Nfios)
       print("Quantidade de fios: %f" %Nfios)
       
       kw = PE.carretel(N, Nfios, Sfio, Aw)
       print("Fator de ocupação: %f" %kw)
       
       #Perdas
       dI      = Ipico-Imin
       Vnucleo = 6.65*2.7*3.22*2 #cm³
       Pnucleo = PE.perdas_nucleo(dI, Vnucleo)
       
       Perimetro_nucleo = (2*1.93)+(2*2.7)
       comp_enrolamento = Perimetro_nucleo*N/kw
       print(comp_enrolamento)
       Pcobre = PE.perdas_cobre(comp_enrolamento, N, Nfios)
       print(Pnucleo, Pcobre)
      