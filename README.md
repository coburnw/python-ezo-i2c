# python-ezo-i2c
Python library to ease access to the Atlas Scientific EZO Sensor line.
Developed and tested on a Raspberry Pi Zero W using the smbus2 or
smbus3 library for underlying i2c communication. Includes a wrapper
for the EZO-CO2 sensor.

## Install
 * activate an environment
 * ``pip install smbus3``
 * ``git clone https://github.com/coburnw/python-ezo-i2c.git``
 * ``cd python-ezo-i2c``
 * ``pip install -e .``

If pip complains about installing editable, you may need to upgrade your pip.

## Usage
```python
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
```
## Dependencies
 * Uses smbus2 or smbus3
 
## Notes
 * Developed on a Raspberry Pi Zero W.
 * minimal testing.
 * It appears the EZO devices use I2C clock stretching as the RPI BCM2835 bug had to be addressed
   by masking the msb of each received databyte.  How that might impact other masters is unclear.
 * Be aware that all timing is handled by the library.  
   