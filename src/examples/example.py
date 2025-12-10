import time
import smbus3 as smbus

import ezo_i2c as atlas
   
with smbus.SMBus(1) as bus:
     co2 = atlas.EzoCO2(bus, 0x69)

     co2.set_find()
      
     print(co2.device_id, co2.firmware_version)
     print(co2.name)
     print(co2.voltage, co2.last_restart)

     if 'CO2' not in co2.device_id:
         raise ValueError('device type at address 0x{:x} is {}. expected CO2.'.format(co2.address, co2.device_id))

     co2.temperature_enable(True)  # include temperature in reading string
     while True:
         co2.update()
         print('{}{}, {}degC, {}volts'.format(co2.value, co2.units, co2.degc, co2.voltage))

         time.sleep(1)
