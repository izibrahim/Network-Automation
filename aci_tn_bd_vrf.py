import sys
import acitoolkit.acitoolkit as aci
from acitoolkit import Session, Node, ExternalSwitch
import re
print('='*40)
'''
Dicover the Physical Topology
'''

from netmiko import ConnectHandler
from getpass import getpass


APIC_URL = '10.10.20.14'
USERNAME = 'admin'
PASSWORD = 'C1sco12345'

device = {'host':APIC_URL, 'username':USERNAME,'password':PASSWORD,'device_type':'hp_procurve'} ##### Netwmiko connecting to NCM
net_conn = ConnectHandler(**device) ##### Netmiko
output1 =net_conn.send_command_timing("terminal len 0",delay_factor=2)
show_bd =net_conn.send_command_timing("show bridge-domain",delay_factor=2) #

bd_list = show_bd.splitlines()

#bd_list = show_bd.splitlines()

for bd in bd_list:
    if bd.startswith(" Tenant      Interface"):
        pass
    elif bd.startswith(" ----"):
        pass
    else:
        r1 =  re.search(r".+Multi Destination",bd)
        if r1:
            bd_to_list = r1.group(0).split()
            print("Tenant =",bd_to_list[0]," || Bridge Domain = ",bd_to_list[1]," || VRF = ",bd_to_list[4])
