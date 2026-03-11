import time
import smbus3 as smbus

import ezo_i2c as atlas

bus_id = 0
ezo_address = 0x69

with smbus.SMBus(bus_id) as bus:
     co2 = atlas.EzoCO2(bus, ezo_address)

     print(' looking for EZO device on bus {}, address 0x{:x}. ctrl-c to cancel'.format(bus_id, co2.address))
     while co2.device_id is None:
          print('.')
          time.sleep(1)
          
     print('found:')

     co2.set_find() # turn on Atlas find led
     print(co2.device_id, co2.firmware_version)
     print(co2.name)
     print(co2.voltage, co2.last_restart)

     if 'CO2' not in co2.device_id:
         raise ValueError('device type at address 0x{:x} is {}. expected CO2.'.format(co2.address, co2.device_id))

     co2.temperature_enable(False)  # include temperature in reading string
     while True:
         co2.update()
         # print('{}{}, {}degC, {}volts'.format(co2.value, co2.units, co2.degc, co2.voltage))
         print('{}{}'.format(co2.value, co2.units))

         time.sleep(1)
