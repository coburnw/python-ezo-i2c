# ezo_i2c.py - Generic interface to Atlas Scientific's EZO Sensors.
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

import time

class EzoI2C():
    def __init__(self, smbus, ezo_address):
        self.smbus = smbus
        self.dev_addr = ezo_address

        self._device_id = None
        self._firmware_version = None
        self._name = None
        
        return

    @property
    def address(self):
        return self.dev_addr
    
    def _write(self, command):
        write_msg = self.smbus.i2c_wr(self.dev_addr, command)
        
        return write_msg
    
    def _read(self):
        ''' returns a clean string '''
        read_msg = self.smbus.i2c_rd(self.dev_addr, 31)

        response = ''
        for byte in read_msg.__bytes__():
            # mask any msb's that may have been glitched by raspberry pi's BCM2835
            c = str(chr(byte & 0x7f))
            # remove status byte and any terminating nulls
            if c.isprintable():
               response += c
            
        # print(response, read_msg.__repr__())
        
        return response

    def _request(self, command, delay):
        write_msg = self._write(command)
        time.sleep(delay)
        response = self._read()
        
        return response

    def set_find(self):
        response = self._write('find')
        time.sleep(0.3)
        
        return
    
    def get_info(self):
        response = self._request('I', 0.3).split(',')

        if len(response) != 3:
            response = None
        elif response[0] != '?I':
            response = None
        else:
            response.pop(0)

        return response

    def get_name(self):
        response = self._request('Name,?', 0.3).split(',')
        
        if len(response) not in [1,2]:
            response = None
        elif response[0] != '?NAME':
            response = None
        else:
            response.pop(0)
            if len(response) == 0:
                response.append('')
        
        return response

    def set_name(self, name):
        if len(name) > 16:
            name = name[:16]

        name = name.replace(' ', '_')
        cmd = 'Name,{}'.format(name)

        self._write(cmd)
        time.sleep(0.3)
        
        return
            
    def get_status(self):
        response = self._request('status', 0.3).split(',')

        if len(response) != 3:
            response = None
        elif response[0] != '?STATUS':
            response = None
        else:
            response.pop(0)
            
        return response

    def get_output(self):
        response = self._request('o,?', 0.3).split(',')

        if len(response) not in [2,3]:
            response = None
        elif response[0] != '?O':
            response = None
        else:
            response.pop(0)
            
        return response

    def set_output(self, parameter, enabled):
        enabled = int(enabled)

        if enabled not in [0,1]:
            raise ValueError('enabled parameter must be True/False, 1/0')
        
        cmd = 'O,{},{}'.format(parameter, int(enabled))

        self._write(cmd)
        time.sleep(0.3)
        
        return

    def get_reading(self):
        response = self._request('r', 1.0).split(',')
            
        return response

    @property
    def device_id(self):
        if self._device_id is None or self._firmware_version is None:
            info = self.get_info()
            if info is None:
                self._device_id = None
                self._firmware_version = None
            else:
                self._device_id = info[0]
                self._firmware_version = info[1]

        return self._device_id

    @property
    def firmware_version(self):
        if self._firmware_version is None:
            ignore = self.device_id
            
        return self._firmware_version

    @property
    def name(self):
        if self._name is None:
            name = self.get_name()
            self._name = name[0]
                
        name = self._name
        
        if name is None:
            name = ''
            
        return name

    @name.setter
    def name(self, value):
        self._name = None        
        self.set_name(value)
        
        return
    
    @property
    def last_restart(self):
        status = self.get_status()
        
        if not status:
            self._last_restart = None
            self._voltage = None
        else:
            self._last_restart = status[0]
            self._voltage = status[1]
            
        return self._last_restart

    @property
    def voltage(self):
        ignore = self.last_restart
        
        return self._voltage

    
