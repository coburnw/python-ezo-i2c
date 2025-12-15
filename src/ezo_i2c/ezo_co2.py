# ezo_co2.py - Interface to Atlas Scientific's EZO-CO2 sensor.
#
# Copyright (c) 2025 Coburn Wightman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#

import ezo_i2c as ezo

class EzoCO2(ezo.EzoI2C):
    def __init__(self, modbus, ezo_address):
        super().__init__(modbus, ezo_address)

        self._reading_format = None
        self._ppm = None
        self._degc = None
        
        return

    def update(self):
        if not self._reading_format:
            self.load_reading_format()

        if not self._reading_format:
            self._reading = None
        else:
            self._reading = self.get_reading()

        return

    def load_reading_format(self):
        reading_format = self.get_output()
        
        if not reading_format:
            reading_format = None
        elif 'PPM' not in reading_format:
            reading_format = None
        elif len(reading_format) == 2 and 'T' not in reading_format:
            reading_format = None

        self._reading_format = reading_format

        return

    @property
    def value(self):
        if not self._reading_format:
            result = None
        elif not self._reading:
            result = None
        else:
            try:
                i = self._reading_format.index('PPM')
                result = float(self._reading[i])
            except ValueError:
                result = None
            except IndexError:
                result = None
        
        return result

    @property
    def units(self):
        return 'ppm'
    
    @property
    def degc(self):
        if not self._reading_format:
            result = None
        elif not self._reading:
            result = None
        else:
            try:
                i = self._reading_format.index('T')
                result = float(self._reading[i])
            except ValueError:
                result = None
            except IndexError:
                result = None
            
        return result

    def temperature_enable(self, state=True):
        self._reading_format = None
        self.set_output('t', state)

        return

    
if __name__ == '__main__':
    import time
    import smbus3 as SMBus    
    
    with SMBus.SMBus(1) as bus:
        co2 = EzoCO2(bus, 0x69)

        co2.set_find()
        co2.temperature_enable(True)
        
        print(co2.device_id, co2.firmware_version)
        print(co2.name)
        print(co2.voltage, co2.last_restart)

        if 'CO2' not in co2.device_id:
            raise ValueError('device type at address 0x{:x} is {}. expected CO2.'.format(co2.address, co2.device_id))

        if len(co2.name) == 0:
            print('setting name')
            co2.name = 'test_name'
        
        while True:
            co2.update()
            print('{}{}, {}degC, {}volts'.format(co2.value, co2.units, co2.degc, co2.voltage))

            time.sleep(5)
            
