import sys
import acitoolkit.acitoolkit as aci
from acitoolkit import Session, Node, ExternalSwitch
print('='*40)
'''
Dicover the Physical Topology
'''
APIC_URL = 'https://10.10.20.14'
USERNAME = 'admin'
PASSWORD = 'C1sco12345'

session = aci.Session(APIC_URL, USERNAME, PASSWORD)
RESP = session.login()

device_ = 0

node = Node
getPhy = node.get(session)
for getPhy in getPhy:
    print(device_,' : ',getPhy,"IP Address => ",getPhy.ipAddress)
    device_ = device_ + 1
    #print(dir(getPhy))
print('='*40)
