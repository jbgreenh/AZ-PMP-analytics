import pandas as pd
import paramiko
import json

def from_sftp(remote_tail: str) -> pd.DataFrame:
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
    client.connect(host, username=username, password=password, port=port)

    sftp = client.open_sftp()
    remote_file = sftp.open(remote_path)
    remote_file.prefetch()
    df = pd.read_csv(remote_file, index_col=None, sep='|')
    remote_file.close()
    sftp.close()
    client.close()

    return df
