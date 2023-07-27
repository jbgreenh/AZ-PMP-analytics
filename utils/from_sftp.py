import pandas as pd
import datetime
import paramiko
import json

def from_sftp(remote_tail: str, sep: str='|') -> pd.DataFrame:
    '''read a file from an sftp server and return a pandas dataframe'''
    with open('../config.json') as f:
        config = json.load(f)['sftp']
    host = config['host']
    port = config['port']
    username = config['username']
    password = config['password']
    remote_path = config['remote_path']
    
    remote_path = f'{remote_path}{remote_tail}'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password, port=port, banner_timeout=200)

    sftp = client.open_sftp()
    remote_file = sftp.open(remote_path)
    remote_file.prefetch()
    df = pd.read_csv(remote_file, index_col=None, sep=sep, low_memory=False)
    remote_file.close()
    sftp.close()
    client.close()

    return df

def awarxe_from_sftp(day=None):
    '''get yesterday's date and return the most recent awarxe file'''
    if day == None:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday_year = yesterday.strftime('%Y')
        yesterday = yesterday.strftime('%Y%m%d')
    else:
        yesterday = day
        yesterday_year = day[0:4]
    
    print(f'pulling awarxe file for {yesterday}')
    tail = f'/Daily/Userex/{yesterday_year}/AZ_UserEx_{yesterday}.csv'
    return from_sftp(tail)