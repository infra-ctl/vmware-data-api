import logging
import re
from samples.tools import service_instance, cli
from pyVmomi import vim

class VMwareManager:
    def __init__(self):
        self.parser = cli.Parser()
         

    def connect_instance(self, args):
        self.args = args
        self.si = service_instance.connect(self.args)

        try:
            self.content = self.si.RetrieveContent()
        except Exception as e:
            logging.exception("Failed to connect to service instance")
            return -1


    def get_vms(self):
        content = self.content
        container_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

        self.vm_list = container_view.view
        vms = VMwareManager.__sorted_vms(self.vm_list)

        return vms

    def get_hosts(self):
        content = self.content
        host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
        self.hosts = host_view.view

        return self.hosts


    def vms_per_host(self):
        hosts = sorted(self.get_hosts(), key=lambda host: host.name)
        vms_in_hosts =  {}

        for host in hosts:
            vms_in_hosts[host.name] = len(host.vm)

        return vms_in_hosts


    @staticmethod
    def __sorted_vms(vms):
        return sorted(vms, key=lambda vm: vm.summary.runtime.host.name)

    
    @staticmethod
    def get_esxi(vm):
        ip_host = vm.summary.runtime.host.name
        num_esxi = ip_host.split(".")[-1]

        return f"ESXi - {num_esxi}"

    @staticmethod
    def get_powerstate(vm):
        power_state = vm.runtime.powerState
        
        return "ON" if power_state == "poweredOn" else "OFF"

    @staticmethod
    def get_vmname(vm):
        summary = vm.summary
        vmname = summary.config.name
        
        return vmname

    @staticmethod 
    def get_osname(vm):
        summary = vm.summary
        os = summary.config.guestFullName
        
        return os

    @staticmethod
    def get_mac(vm):
        hardware = vm.config.hardware.device
        mac_addresses = [d.macAddress for d in hardware if hasattr(d, "macAddress")]
        
        return ", ".join(mac_addresses)

    @staticmethod
    def get_ip(vm):
        guest = vm.guest
        
        if guest:
            list_addresses = []
            network = guest.net
            
            for nic in network:
                ip_config = nic.ipConfig
                if ip_config:
                    addresses = ip_config.ipAddress
                    for addr in addresses:
                        if ":" not in addr.ipAddress:
                            format_address = f"{addr.ipAddress}/{addr.prefixLength}"
                            list_addresses.append(format_address)

            list_addresses_str = ",".join(list_addresses)

            if list_addresses_str:
                return list_addresses_str
            else:
                return "None"

    @staticmethod
    def get_vmtools(vm):
        guest = vm.guest
        
        return guest.toolsStatus if guest and guest.toolsStatus else "None"

    @staticmethod
    def get_boottime(vm):
        summary = vm.summary
        
        return summary.runtime.bootTime.strftime("%d/%m/%Y %H:%M") if summary.runtime.bootTime else "None"

    @staticmethod
    def get_annotation(vm):
        annotation = vm.summary.config.annotation
        
        return annotation if annotation else ""

    @staticmethod
    def get_diskspace(vm):
        summary = vm.summary
        
        return "{:.2f}".format(summary.storage.committed / (1024 ** 3))

    @staticmethod
    def get_memspace(vm):
        summary = vm.summary
        mem = "{:.2f}".format(summary.config.memorySizeMB / (1024))
        
        return mem

    @staticmethod
    def get_pathname(vm):
        summary = vm.summary
        pathname = summary.config.vmPathName
        
        return pathname
        
