import re ######################################### Import Regular Expression library
import xlsxwriter  ######################################### Import xlsxwriter library for Excel
from netmiko import ConnectHandler #############################Netwmiko library
from getpass import getpass #################################Secure password library to hide pasword
from threading import Thread ######################################## multitasking library ############################## Pandas library
from collections import OrderedDict
import time
from datetime import date ############################### Date Time library
import threading ################threading library
from datetime import datetime
import sys


dict = {}
ip_address = []
interface_add = []
status_add = []
protocol_add = []
node_name = []
super_list = [] ################## to record all the router sh ip int br command


def show_version(a_device):
    device = {'host':a_device, 'username':"admin",'password':'C1sco12345','device_type':"cisco_xr"}
    net_conn = ConnectHandler(**device) ##### Netmiko
    output_cmd =net_conn.send_command_timing("show version ",delay_factor=2)
    print(output_cmd)
    output_showIP =net_conn.send_command_timing("show ip int br ",strip_command=False ,normalize=True,strip_prompt=False)
    print(output_showIP,file=open(a_device,'a'))
    cmd = net_conn.disconnect()
    ### disconnect from router otherwise Multitasking will not work

devices = []
#########################multitasking
def main():
    start_time = datetime.now() ##### Checking the start time of the Script
    while True:
        s = input("Enter Device Name : ")
        if s:
            devices.append(s)
        else:
            break
    for a_device in devices: ##################### Starting Multitasking
        my_thread = threading.Thread(target=show_version, args=(a_device,)) #Starting Multitasking
        time.sleep(6) ############## adding sleep timer to avoid the Netmiko session issues
        my_thread.start() ##### Starting the start the thread

    main_thread = threading.currentThread() #### gettig the current thread
    for some_thread in threading.enumerate(): ####### join the thread
        if some_thread != main_thread: ####### join the thread
            print(some_thread) ####### join the thread
            some_thread.join() ####### join the thread
    else:
        print("Task Completed : ")


if __name__ == "__main__":
    main()


'''
IOS XR device
conn = manager.connect(
    host="sbx-iosxr-mgmt.cisco.com",
    username="admin",
    password='C1sco12345',
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False,
    port=10000,
    timeout=60,
)
'''


#https://pbpython.com/pandas-list-dict.html
#https://xlsxwriter.readthedocs.io/example_pandas_conditional.html
