import subprocess
import logging
import os 

ip = os.getenv("VCENTER_IP")
user = os.getenv("VCENTER_USERNAME")
password = f"\'{os.getenv('VCENTER_PASSWORD')}\'"
sheet_id = os.getenv("GSHEET_ID")
sheet_name = os.getenv("GSHEET_NAME")
sheet_key_path = os.getenv("GSHEET_KEY_PATH")

command = f"python3 vmware_data_api/main.py --host {ip} --user {user} --password {password} --sheetid {sheet_id} --sheetname {sheet_name} --sheetkeypath {sheet_key_path} -nossl"
try:
    subprocess.run(command, shell=True)
except:
    logging.exception("Error al ejecutar el script")
