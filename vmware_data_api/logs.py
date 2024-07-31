import logging 
import os 

def logs():
    
    current_dir = os.getcwd()
    logs_dir = os.path.join(current_dir, '.logs')
    os.makedirs(logs_dir, exist_ok=True)

    log_name = 'backup'

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        filename=f'{logs_dir}/{log_name}.log'
    )