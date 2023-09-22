
import numpy as np
import time 
import math

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
        #these 3 attributes are the main attributes.
        self._temperature = temperature#(C)
        self._pressure = pressure#(Pa)
        self._humidity = humidity#(%) value between [0,100]
        
        #first celerity and density is not known and will be determined
        #later by their repective method 
        self.celerity_ = math.nan
        self.density_ = math.nan      
        
        #Other air properties:
        self.saturation_vapor_pressure =  math.nan#Saturation water vapor pressure
        self.enhancement_factor =  math.nan #Enhancement factor
        self.mole_fraction_vapor =  math.nan #Mole fraction of water vapor in air
        self.compressibility_factor =  math.nan #Compressibility factor
        self.mole_fraction_C02 =  math.nan#Mole fraction of carbon-dioxide in air
        
        
        self.calculation()

    def calculation(self):
        """ 
        This method computes severall air properties. The air properties are
        transformed into attributes.
        """
        t = self.temperature 
        T = t+273.15
        
       
        self.saturation_vapor_pressure = np.exp(Air.a_i0[0]*T**2+Air.a_i0[1]*T+Air.a_i0[2]+Air.a_i0[3]*T**-1)
            
        self.enhancement_factor = Air.a_i1[0]+Air.a_i1[1]*self.pressure+Air.a_i1[2]*t
        
        self.mole_fraction_vapor = self.humidity/100*self.saturation_vapor_pressure/self.pressure*self.enhancement_factor
        
        self.compressibility_factor = 1-self.pressure/T*(Air.a_i2[0]+Air.a_i2[1]*t\
            +Air.a_i2[2]*t**2+(Air.a_i2[3]+Air.a_i2[4]*t)*self.mole_fraction_vapor\
                +(Air.a_i2[5]+Air.a_i2[6]*t)*self.mole_fraction_vapor**2) \
        +(self.pressure/T)**2*(Air.a_i2[7]+Air.a_i2[8]*self.mole_fraction_vapor**2)
        
        
        self.mole_fraction_C02 = 0.0004#recommanded laboratory value
        

        
    def density(self):
        """ 
        This method compute the air density. Air density becomes an attribute. 
        If the attribute exist the last value of the object density is directly 
        returned.
        """
        if math.isnan(self.density_):
            T = self.temperature+273.15
            #Density of air
            self.density_ = (3.48349+1.44*(self.mole_fraction_C02-0.0004))*1E-3*self.pressure/(self.compressibility_factor*T)*(1-0.3780*self.mole_fraction_vapor)
                        
        return self.density_
        
        
    def celerity(self):
        """ 
        This method compute the air celerity. Air celerity becomes an attribute. 
        If the attribute exist the last value of the object density is directly 
        returned.
        """     
        if math.isnan(self.celerity_):
            t = self.temperature   
  
            self.celerity_ = Air.a_i3[0]+Air.a_i3[1]*t\
                +(Air.a_i3[3]+Air.a_i3[4]*t+Air.a_i3[5]*t**2)*self.mole_fraction_vapor\
                +(Air.a_i3[6]+Air.a_i3[7]*t+Air.a_i3[8]*t**2)*self.pressure\
                +(Air.a_i3[9]+Air.a_i3[10]*t+Air.a_i3[11]*t**2)*self.mole_fraction_C02\
                +Air.a_i3[12]*self.mole_fraction_vapor**2+Air.a_i3[13]*self.pressure**2\
                +Air.a_i3[14]*self.mole_fraction_C02+Air.a_i3[15]*self.mole_fraction_vapor*self.pressure*self.mole_fraction_C02
           
        return self.celerity_
    
    
    # property
    def _setmainattributes(attr):
        """ 
        When a main attribute: temperature, pressure or humidity is changer,
        the celerity and denisity are computed.
        """          
        def set_any(self, value):
            #change the value of the corresponding attribute
            setattr(self, attr, value)
            
            #compute the new
            self.calculation()
            
            #reset celerity_ and density_
            self.celerity_ = math.nan
            self.density_ = math.nan
                
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
