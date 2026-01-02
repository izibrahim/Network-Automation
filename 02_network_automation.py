from threading import Thread
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException, ConnectionClosedException
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import pprint
import time
from datetime import date 
import threading 
import sys
from tabulate import tabulate


devices = []


def connect_to_node(hostname):
    driver = get_network_driver('ios')
    device = driver(hostname=hostname, username='admin', password='admin')
    try:
        device.open()
        print(f"\n{'='*80}")
        print(f"  CONNECTION SUCCESSFUL TO: {hostname}")
        print('='*80)
        
        # Gather all data
        facts = device.get_facts()
        bgp = device.get_bgp_neighbors()
        env = device.get_environment()
        interfaces = device.get_interfaces()
        intf_ip = device.get_interfaces_ip()
        
        # ===== DEVICE INFO TABLE =====
        uptime_seconds = facts.get('uptime', 0)
        uptime_str = f"{uptime_seconds:.0f} sec ({uptime_seconds/3600:.1f} hrs / {uptime_seconds/86400:.1f} days)"
        
        device_info = [
            ["Hostname", facts.get('hostname', 'N/A')],
            ["FQDN", facts.get('fqdn', 'N/A')],
            ["Vendor", facts.get('vendor', 'N/A')],
            ["Model", facts.get('model', 'N/A')],
            ["OS Version", facts.get('os_version', 'N/A')],
            ["Serial Number", facts.get('serial_number', 'N/A')],
            ["Uptime", uptime_str],
        ]
        print("\n📋 DEVICE INFO")
        print(tabulate(device_info, headers=["Property", "Value"], tablefmt="pretty"))
        
        # ===== CPU & MEMORY TABLE =====
        cpu_mem_data = []
        cpu_info = env.get('cpu', {})
        for cpu_id, cpu_data in cpu_info.items():
            usage = cpu_data.get('%usage', 'N/A')
            cpu_mem_data.append([f"CPU {cpu_id}", f"{usage}%"])
        
        memory = env.get('memory', {})
        used_ram = memory.get('used_ram', 0)
        available_ram = memory.get('available_ram', 0)
        total_ram = used_ram + available_ram
        if total_ram > 0:
            mem_percent = (used_ram / total_ram) * 100
            cpu_mem_data.append(["Memory Used", f"{used_ram / (1024**2):.1f} MB"])
            cpu_mem_data.append(["Memory Total", f"{total_ram / (1024**2):.1f} MB"])
            cpu_mem_data.append(["Memory %", f"{mem_percent:.1f}%"])
        
        print("\n💻 CPU & MEMORY")
        print(tabulate(cpu_mem_data, headers=["Resource", "Value"], tablefmt="pretty"))
        
        # ===== INTERFACES TABLE =====
        intf_table = []
        for intf_name in facts.get('interface_list', []):
            intf_data = interfaces.get(intf_name, {})
            status = "✅ UP" if intf_data.get('is_up') else "❌ DOWN"
            mac = intf_data.get('mac_address', 'N/A')
            
            # Get IP address
            ip_info = intf_ip.get(intf_name, {}).get('ipv4', {})
            if ip_info:
                ip_addr = list(ip_info.keys())[0]
                prefix = ip_info[ip_addr].get('prefix_length', '')
                ip_str = f"{ip_addr}/{prefix}"
            else:
                ip_str = "N/A"
            
            intf_table.append([intf_name, status, ip_str, mac])
        
        print("\n🔌 INTERFACES")
        print(tabulate(intf_table, headers=["Interface", "Status", "IP Address", "MAC Address"], tablefmt="pretty"))
        
        # ===== BGP NEIGHBORS TABLE =====
        global_bgp = bgp.get('global', {})
        router_id = global_bgp.get('router_id', 'N/A')
        
        print(f"\n🌐 BGP NEIGHBORS (Router ID: {router_id})")
        
        peers = global_bgp.get('peers', {})
        if peers:
            bgp_table = []
            for peer_ip, peer_data in peers.items():
                remote_as = peer_data.get('remote_as', 'N/A')
                state = "✅ UP" if peer_data.get('is_up') else "❌ DOWN"
                uptime = peer_data.get('uptime', -1)
                uptime_str = str(uptime) if uptime >= 0 else "N/A"
                
                # Get prefix counts
                addr_families = peer_data.get('address_family', {})
                for af_name, af_data in addr_families.items():
                    rx = af_data.get('received_prefixes', 0)
                    tx = af_data.get('sent_prefixes', 0)
                    prefix_str = f"{rx}/{tx}" if rx >= 0 else "N/A"
                
                bgp_table.append([peer_ip, remote_as, state, uptime_str, prefix_str])
            
            print(tabulate(bgp_table, headers=["Neighbor", "Remote AS", "State", "Uptime (sec)", "Prefixes Rx/Tx"], tablefmt="pretty"))
        else:
            print("  No BGP neighbors configured")
        
        print(f"\n{'='*80}\n")
        
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
