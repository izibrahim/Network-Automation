'''
Create TENANT/Context/BD in ACI using APIs
'''

import sys
import os
from acitoolkit import Credentials, Session, Tenant, AppProfile, BridgeDomain, EPG
import acitoolkit.acitoolkit as aci
import colored
'''
Input from the USER, Tenant Name,Context,Bridge Domain,Application Profile, epg
it will create Tenant Name,Context,Bridge Domain,Application Profile, epg and add epg in bridge domain
'''

import os

# System call

newTenant = input("Enter TENANT Name : ")
newContext = input("Enter Context Name : ")

newBD = input("Enter BD Name : ")
app_pro = input("Enter App Profile : ")
epg_group_1 = input("Enter EPG 1 : ")
epg_group_2 = input("Enter EPG 2 : ")
subnet_add  = input('Add Subnet to BD: ')
add_contract = input('Enter Contract :  ')
epg_pro = input("Enter Provider EPG Name : ")
epg_cus = input("Enter Provider EPG Cusomer  : ")

tenant = aci.Tenant(newTenant)
context = aci.Context(newContext, tenant)
bd = aci.BridgeDomain(newBD, tenant)
app_profile = aci.AppProfile(app_pro, tenant)
epg_1 = aci.EPG(epg_group_1, app_profile)
epg_2 = aci.EPG(epg_group_2, app_profile)
bd.add_context(context)
#bd.add_subnet('10.0.0.1')
#x = '10.1.1.1/24'
sub1 = aci.Subnet('sub1', bd)
sub1.set_addr(subnet_add)
bd.add_subnet(sub1)
bd.add_tag('Python API Call')
epg_1.add_bd(bd)
epg_2.add_bd(bd)
#epg.consume(contract)
contract = aci.Contract(add_contract, tenant)

#epg_1.consume(contract)

icmp_entry = aci.FilterEntry('icmpentry',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='unspecified',
                         dToPort='unspecified',
                         etherT='ip',
                         prot='icmp',
                         sFromPort='unspecified',
                         sToPort='unspecified',
                         tcpRules='unspecified',
                         parent=contract)


if epg_pro == epg_group_1:
    epg_1.provide(contract)
if epg_pro == epg_group_2:
    epg_2.provide(contract)
if epg_cus == epg_group_2:
    epg_1.consume(contract)
if epg_cus == epg_group_2:
    epg_2.consume(contract)
epg_1_port = input('Phy Port for EPG-1 must be add in 1/101/1/18 format : ')
a,b,c,d = epg_1_port.split('/')
epg_2_port = input('Phy Port for EPG-2 must be add in 1/101/1/18 format : ')
e,f,g,h = epg_2_port.split('/')
# Create the physical interface objects representing the physical ethernet ports
first_intf = aci.Interface('eth', a, b, c, d)
second_intf = aci.Interface('eth', e,f,g,h)

vlan_for_epg_1 = input('Phy vlan for epg 1 : ')
vlan_for_epg_2 = input('Phy vlan for epg 2 : ')
# Create a VLAN interface and attach to each physical interface
# vlan5-on-eth1-101-1-18
interfaceLA = f'vlan{vlan_for_epg_1}-on-eth{a}-{b}-{c}-{d}'
interfaceLB = f'vlan{vlan_for_epg_2}-on-eth{e}-{f}-{g}-{h}'

first_vlan_intf = aci.L2Interface(interfaceLA, 'vlan', vlan_for_epg_1)
first_vlan_intf.attach(first_intf)

second_vlan_intf = aci.L2Interface(interfaceLB, 'vlan', vlan_for_epg_2)
second_vlan_intf.attach(second_intf)

# Attach the EPGs to the VLAN interfaces
epg_1.attach(first_vlan_intf)
epg_2.attach(second_vlan_intf)

APIC_URL = 'https://10.10.20.14'
USERNAME = 'admin'
PASSWORD = 'C1sco12345'

session = aci.Session(APIC_URL, USERNAME, PASSWORD)
resp = session.login()


resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json()) # this call will push the new tenant to ACI
print(resp)

gettenants = aci.Tenant.get(session)
for gettenants in gettenants:
    print(gettenants.name) # checking the Tenant list

print('='*20,'Context ')


getContext = aci.Context.get(session)
for getContext in getContext:
    print(getContext.name) # checking the Tenant list
