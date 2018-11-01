#!/usr/bin/env python
'''
@author: Sandro Melo

'''
import os
try:
    import pyowm
except:
    print('Big problem -> Not found modulo pyowm!',sys.exc_info()[0])
    print('This script was write to Python 3')
    sys.exit(0)

#mykey="a97e4c2f53f23fbb1ca98c3ac20288ca"
#city="dublin"

mykey=os.environ['OPENWEATHER_API_KEY']
city=os.environ['CITY_NAME']

def func_weather():
    owm = pyowm.OWM(mykey) 
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    wind = str(w.get_wind())                  
    desc = str(w.get_status())                  
    temperatura = w.get_temperature(unit='celsius') 
    temp2 = str(temperatura.get('temp','0'))
    humi = str(w.get_humidity())
    print('source=openweathrmap, ' + 'city=' + '\"' + city + '\", ' 'description=' + desc + ' temp=' + temp2 + ', ' + ' humidity=' + humi)
func_weather() 

