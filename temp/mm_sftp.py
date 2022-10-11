import datetime
import pandas as pd
from utils.from_sftp import *

# read and combine files for six months of lookups
year = datetime.datetime.now().year
month = datetime.datetime.now().month
start, end = 0, 0
if month < 7:
    year = year - 1
    start, end = 7, 12
else:
    start, end = 1, 6
    
path_mid = '/Monthly/Patient_Requests_REPORTAE_48/AZ_PtReqByProfile_'

lookups = pd.DataFrame()
for n in range(start, end + 1):
    if n < 10:
        n = f'0{n}'
    lookups = pd.concat([lookups, from_sftp(f'{path_mid}{year}{n}/Prescriber.csv')])

# ask in future to adjust data retention policy to 12 months