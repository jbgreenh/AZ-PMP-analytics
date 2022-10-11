import pandas as pd
from utils.from_sftp import *

df = from_sftp('/Monthly/Patient_Requests_REPORTAE_48/AZ_PtReqByProfile_202209/Prescriber.csv')
df.to_clipboard(index=False)