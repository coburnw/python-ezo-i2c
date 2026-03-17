import time
import cmd
import subprocess

import smbus3 as smbus
import ezo_i2c as atlas

# specify bus and our device address
i2c_bus_number = 1

class Shell(cmd.Cmd):
    intro = 'phorp scanner'
    prompt = 'scan: '

    def __init__(self, smbus, *kwargs):
        super().__init__(*kwargs)

        self.smbus = None
        self.address = None
        self.ezo = self.ezo_attach(smbus, 0x69)
        
        self.start_addr = 0x60
        self.end_addr = 0x6f
        self.address_list = range(self.start_addr, self.end_addr+1)
        
        return

    def ezo_attach(self, smbus, address):
        self.address = address
        self.smbus = smbus
        ezo = atlas.EzoI2C(self.smbus, address)

        return ezo
    
    @property
    def prompt(self):
        return 'ezo(0x{:x}): '.format(self.address)
    
    def emptyline(self):
        self.do_scan(None)
        
        return False

    def do_scan(self, arg):
        ''' scan i2c bus for devices '''
        results = subprocess.run(['i2cdetect', '-y', '1'])
        # print(results)

        print()
        self.validate_address('0x0')

        print()
        
        return False
        
    def do_address(self, arg):
        ''' select device by i2c address '''
        address = self.validate_address(arg)
        
        if address:
            self.ezo = self.ezo_attach(self.smbus, address)
            
        return False

    def validate_address(self, addr):
        addr = addr.strip().lower()
        address = None
        
        if '0x' not in addr:
            print(' address must be in hexadecimal notation such as 0x60, or 0x6a')
        elif int(addr, 16) not in self.address_list:
            print(' address must be between 0x{:x} and 0x{:x} inclusive'.format(self.start_addr, self.end_addr))
        else:
            address = int(addr, 16)
        
        return address
    
    def do_find(self, arg):
        ''' flash led of device at selected address'''
        self.ezo.set_find()
        
        return False

    def do_info(self, arg):
        ''' get selected devices info'''
        print(self.ezo.get_info())

        return False

    def do_status(self, arg):
        ''' get selected devices status'''
        print(self.ezo.get_status())

        return False

    def do_name(self, arg):
        ''' get/set selected device name'''
        name = arg.strip()
        
        if len(name) > 0:
            self.ezo.set_name(arg)
            
        print(self.ezo.get_name())

        return False
    
    def do_move(self, arg):
        ''' move the selected device to new i2c address'''
        address = self.validate_address(arg)
        if address:
            print('ezo device at address 0x{:x} will be moved to address 0x{:x}'.format(self.address, address))
            self.address = self.ezo.set_address(address)
            
        return False

    def do_lock(self, arg):
        ''' lock mode of selected device to i2c only'''
        pass

    def do_exit(self, arg):
        ''' exit'''
        return True

        
if __name__ == '__main__':
    
    with smbus.SMBus(i2c_bus_number) as smbus:
        shell = Shell(smbus)

        shell.cmdloop()
