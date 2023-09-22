# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import time 
class Air:
    """        
    The air properties are calculated following Rasmussen (1997).
                 
    Rasmussen, K (1997). "Calculation method for the physical properties of
    air used in the calibration of microphones: A proposal for a unified 
    calculation procedure to be used among European metrology laboratories,"
    Report PL-11b, Department of Acoustic Technology, Technical University
    of Denmark.    
    """ 
    #Appendix A: (a_i0=the first column of the table )
    a_i0 = [1.2378847E-5, -1.9121316E-2, 33.93711047, -6.3431645E3]
    a_i1 = [1.00062,3.14E-5, 5.6E-7]
    a_i2 = [1.58123E-6, -2.9331E-8, 1.1043E-10, 5.707E-6, -2.051E-8, 1.9898E-4, -2.376E-6, 1.83E-11, -0.765E-8]
    a_i3 = [331.5024, 0.603055, -0.000528, 51.471935, 0.1495874, -0.000782, -1.82E-7, 3.73E-8, -2.93E-10, -85.20931, -0.228525, 5.91E-5, -2.835149, -2.15E-13, 29.179762, 0.000486]
    a_i4= [1.400822, -1.75E-5, -1.73E-7, -0.0873629, -0.0001665, -3.26E-6, 2.047E-8, -1.26E-10, 5.939E-14, -0.1199717, -0.0008693, 1.979E-6, -0.01104, -3.478E-16, 0.0450616, 1.82E-6 ]
    a_i5 = [84.986, 7.0, 113.157, -1, -3.7501E-3, -100.015 ]
    a_i6 = [60.054, 1.846, 2.0E-6, 40, -1.775E-4]
    a_i7 = [0.251625, -9.2525E-5, 2.1334E-7,-1.0043E-10,0.12477, -2.283E-5, 1.267E-7, 0.0116, 4.61E-6, 1.74E-8]
    def __init__(self,temperature=20,pressure=101325,humidity=0 ):
        """  
        Properties: 
        - temperature: air temperature in Celcius
        - pressure: atmospheric pressure in Pascal
        - humidity: relative air humidity in %
        
        """
        self._temperature = temperature#(C)
        self._pressure = pressure#(Pa)
        self._humidity = humidity#(%) value between [0,100]
        
        self.calculation()

    def calculation(self):
        """ 
        This method computes severall air properties. The air properties are
        transformed into attributes.
        """
        t = self.temperature 
        T = t+273.15
        
        #Saturation water vapor pressure
        psv = np.exp(Air.a_i0[0]*T**2+Air.a_i0[1]*T+Air.a_i0[2]+Air.a_i0[3]*T**-1)
        #Enhancement factor    
        ef = Air.a_i1[0]+Air.a_i1[1]*self.pressure+Air.a_i1[2]*t
        #Mole fraction of water vapor in air
        xw = self.humidity/100*psv/self.pressure*ef
        #Compressibility factor
        Cf = 1-self.pressure/T*(Air.a_i2[0]+Air.a_i2[1]*t+Air.a_i2[2]*t**2+(Air.a_i2[3]+Air.a_i2[4]*t)*xw+(Air.a_i2[5]+Air.a_i2[6]*t)*xw**2) \
        +(self.pressure/T)**2*(Air.a_i2[7]+Air.a_i2[8]*xw**2)
        #Mole fraction of carbon-dioxide in air
        xc = 0.0004#recommanded laboratory value
        
        setattr(self,'psv',psv)
        setattr(self,'ef',ef)
        setattr(self,'xw',xw)
        setattr(self,'Cf',Cf)
        setattr(self,'xc',xc)
        
    def density(self):
        """ 
        This method compute the air density. Air density becomes an attribute. 
        If the attribute exist the last value of the object density is directly 
        returned.
        """
        if not(hasattr(self,'rho0')):
            T = self.temperature+273.15
            #Density of air
            rho0 = (3.48349+1.44*(self.xc-0.0004))*1E-3*self.pressure/(self.Cf*T)*(1-0.3780*self.xw)
            setattr(self,'rho0',rho0)
            
        return self.rho0
        
        
    def celerity(self):
        """ 
        This method compute the air celerity. Air celerity becomes an attribute. 
        If the attribute exist the last value of the object density is directly 
        returned.
        """     
        if not(hasattr(self,'c0')):
            t = self.temperature   
  
            c0 = Air.a_i3[0]+Air.a_i3[1]*t+(Air.a_i3[3]+Air.a_i3[4]*t+Air.a_i3[5]*t**2)*self.xw+(Air.a_i3[6]+Air.a_i3[7]*t+Air.a_i3[8]*t**2)*self.pressure\
                +(Air.a_i3[9]+Air.a_i3[10]*t+Air.a_i3[11]*t**2)*self.xc+Air.a_i3[12]*self.xw**2+Air.a_i3[13]*self.pressure**2+Air.a_i3[14]*self.xc+Air.a_i3[15]*self.xw*self.pressure*self.xc
            setattr(self,'c0',c0)
        return self.c0
    
    # property
    def _setmainattributes(attr):
        """ 
        When a main attribute: temperature, pressure or humidity is changer,
        the celerity and denisity are computed.
        """          
        def set_any(self, value):
            setattr(self, attr, value)
    #(self,new_temperature,name):
      #  setattr(self,name,new_temperature)
            self.calculation()
            if hasattr(self,'c0'):
                del self.c0
                self.celerity()       
            if hasattr(self,'rho0'):
                del self.rho0
                self.density()
        return set_any

    temperature = property(fget = lambda self: self._temperature, fset=_setmainattributes("_temperature"))
    pressure = property(fget = lambda self: self._pressure, fset=_setmainattributes("_pressure"))
    humidity = property(fget = lambda self: self._humidity, fset=_setmainattributes("_humidity"))

#various test
t = time.time()
air = Air(humidity=0    )
# do stuff
print(" creation time {:.10f}" .format(time.time()-t))

print(air.pressure)
print(air.density())
print(air.celerity())
print(air.celerity())
t = time.time()
air.temperature =10
print(" {:.10f}" .format(time.time()-t))
print(air.celerity())
