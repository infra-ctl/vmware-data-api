#!/usr/bin/env python

import logging
import socket
import time
import os
import argparse

from sheets.google_sheet_manager import GoogleSheetManager
from vmware.vmware_manager import VMwareManager
from config import TIMEOUT_IN_SEC
from logs import logs

socket.setdefaulttimeout(TIMEOUT_IN_SEC)

def extend_parser(service_instance):
    parser = service_instance.parser 
    parser.add_custom_argument('-sid', '--sheetid', required=True,
                               action='store', help='Sheet ID for connecting to Worksheet')
    parser.add_custom_argument('-sn', '--sheetname', required=True,
                               action='store', help='Name of Worksheet')
    parser.add_custom_argument('-sk', '--sheetkeypath', required=True,
                               action='store', help='Path of json key authentication')
    return parser


def main():
     
    logs()
    
    try:    
        vm_manager = VMwareManager()
        parser = extend_parser(vm_manager)
        args = parser.get_args()
        vm_manager.connect_instance(args)
    except Exception as e:
        logging.exception("Failed to connection with vCenter")


    try:
        SHEET_NAME = args.sheetname
        SHEET_ID = args.sheetid
        CREDS_FILE = args.sheetkeypath

        gs_manager = GoogleSheetManager(CREDS_FILE, SHEET_ID, SHEET_NAME)
        gs_manager.clear_sheet()
        gs_manager.titles([
            "Host", "Nombre", "Sistema Operativo", "Estado", 
            "IP address", "MAC address", "Descripción", 
            "Memoria RAM (MB)", "Almacenamiento (GB)",
            "Uptime", "Ruta de disco (VMware)"
        ])
    except Exception as e:
        logging.exception("Error initializing Google Sheet Manager")
        return -1

    try:

        vm_manager = VMwareManager()
        parser = extend_parser(vm_manager)
        args = parser.get_args()

        vm_manager.connect_instance(args)

        vms = vm_manager.get_vms()

        gs_manager.colour_data(vm_manager.vms_per_host())

        for vm in vms:
            try:
                gs_manager.append_data([
                    vm_manager.get_esxi(vm),
                    vm_manager.get_vmname(vm),
                    vm_manager.get_osname(vm),
                    vm_manager.get_powerstate(vm),
                    vm_manager.get_ip(vm),
                    vm_manager.get_mac(vm),
                    vm_manager.get_annotation(vm),
                    vm_manager.get_memspace(vm),
                    vm_manager.get_diskspace(vm),
                    vm_manager.get_boottime(vm),
                    vm_manager.get_pathname(vm),
                ])

                time.sleep(2)

            except Exception as e:
                logging.exception(f"Failed to append data for VM: {vm.summary.config.name}")
                return -1 

    except Exception as e:
        logging.exception("Failed to process virtual machines")
        return -1

    socket.setdefaulttimeout(None)
    return 0


# Start program
if __name__ == "__main__":
    main()

