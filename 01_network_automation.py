from threading import Thread
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException, ConnectionClosedException
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import pprint
import time
from datetime import date 
import threading 
import sys


devices = []


def connect_to_node(device):
    driver = get_network_driver('ios')
    device = driver(hostname=device, username='admin', password='admin')
    try:
        device.open()
        print("Connection successful!")
        facts = device.get_facts()
        bgp = device.get_bgp_neighbors()
        env = device.get_environment()
        inft = device.get_interfaces()
        intf_ip = device.get_interfaces_ip()
        lldp = device.get_lldp_neighbors()
        mac = device.get_mac_address_table()
        ntp = device.get_ntp_servers()
        vlan = device.get_vlans()
        live_ = device.is_alive()
        all_facts = {
                **facts,
                **bgp,
                **env,
                **inft,
                **intf_ip,
                **lldp,
                'mac_address_table': mac,  # mac is a list, not a dict
                **ntp,
                **vlan,
                **live_}
        pprint.pprint(all_facts)
    except ConnectionException as e:
        print(f"NAPALM Connection Error: {e}")
    except NetmikoTimeoutException:
        print("Connection timed out - device unreachable or SSH not enabled")
    except NetmikoAuthenticationException:
        print("Authentication failed - check username/password")
    except ConnectionRefusedError:
        print("Connection refused - SSH service may not be running")
    except ConnectionClosedException:
        print("Connection was closed unexpectedly")
    except OSError as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__} - {e}")
    finally:
        try:
            device.close()
            print("Connection closed")
        except:
            pass


def main():
 #   start_time = datetime.now() ##### Checking the start time of the Script
    while True:
        s = input("Enter Device Name : ")
        if s:
            devices.append(s)
        else:
            break
    for a_device in devices: ##################### Starting Multitasking
        my_thread = threading.Thread(target=connect_to_node, args=(a_device,)) #Starting Multitasking
        time.sleep(6) ############## adding sleep timer to avoid the Netmiko session issues
        my_thread.start() ##### Starting the start the thread

    main_thread = threading.current_thread() #### getting the current thread
    for some_thread in threading.enumerate(): ####### join the thread
        if some_thread != main_thread: ####### join the thread
            print(some_thread) ####### join the thread
            some_thread.join() ####### join the thread
    else:
        print("Task Completed : ")


if __name__ == "__main__":
    main()
