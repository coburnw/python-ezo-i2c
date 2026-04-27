import sys
import time
import smbus3 as smbus

import ezo_i2c as atlas

def print_options():
    print('example requires two arguments:')
    print()
    print(' python {} bus=n address=0xNN # dump ezo device readings'.format(sys.argv[0]))
    print( '   Where bus is the host i2c bus number from [0,1]')
    print( '   and address is the hexadecimal address of the device to communicate with')
    
    return
    
def get_bus_number():
     if len(sys.argv) != 3:
          print_options()
          exit()

     i2c_bus_number = None
    
     arg = sys.argv[1].strip().lower()
     key, sep, value = arg.partition('=')
     if sep == '':
          pass
     elif 'bus' not in key.lower():
          pass
     elif value not in ['0', '1']:
          pass
     else:
          i2c_bus_number = int(value)

     if i2c_bus_number is None:
          print_options()
          exit()
          
     return i2c_bus_number

def get_dev_addr():
     if len(sys.argv) != 3:
          print_options()
          exit()

     i2c_dev_addr = None
    
     arg = sys.argv[2].strip().lower()
     key, sep, value = arg.partition('=')
     if sep == '':
          pass
     elif 'addr' not in key.lower():
          pass
     elif '0x' not in value.lower():
          pass
     else:
          i2c_dev_addr = int(value, 0)

     if i2c_dev_addr is None:
          print_options()
          exit()
          
     return i2c_dev_addr 

if __name__ == '__main__':
     bus_id = get_bus_number()
     ezo_address = get_dev_addr()
     
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
               raise ValueError('device type at address 0x{:x} is {}. expected "CO2".'.format(co2.address, co2.device_id))

          co2.temperature_enable(False)  # include temperature in reading string
          while True:
               co2.update()
               # print('{}{}, {}degC, {}volts'.format(co2.value, co2.units, co2.degc, co2.voltage))
               print('{}{}, {}volts'.format(co2.value, co2.units, co2.voltage))
               # print('{}{}'.format(co2.value, co2.units))

               time.sleep(1)
