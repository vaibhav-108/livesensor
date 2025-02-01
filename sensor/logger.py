import logging
import os
from datetime import datetime


Log_file= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_S')}.log"
Log_path= os.path.join(os.getcwd(),"logs",Log_file)
os.makedirs(Log_path,exist_ok=True)

Log_File_Path= os.path.join(Log_path,Log_file)

logging.basicConfig(
    filename=Log_File_Path, 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')



