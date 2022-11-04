import datetime
import pandas as pd
from utils.from_sftp import *

def scorecard(m_y, ob=False):
    '''takes a string of the form YYYYMM and returns a dataframe for the scorecard'''    
    if ob:
        print(f'getting {m_y} ob data')
        df_47 = from_sftp(f'/Monthly/REPORTAE_47/Dispensations/AZ_Dispensations_{m_y}_opioid_benzo.csv')
    else:
        print(f'getting {m_y} data')
        df_47 = from_sftp(f'/Monthly/REPORTAE_47/Dispensations/AZ_Dispensations_{m_y}.csv')
    df_48 = from_sftp(f'/Monthly/Patient_Requests_REPORTAE_48/AZ_PtReqByProfile_{m_y}/Prescriber.csv')
    
    df_47 = df_47[df_47['state'] == 'AZ']
    df_47 = df_47[['dea_number']]
    df_48 = df_48[['dea_number','totallookups']]
    df_merge = pd.merge(df_47, df_48, on='dea_number', how='left')
    df_merge = df_merge.groupby(['dea_number'], as_index=False).sum()
    
    n = df_merge.shape[0]
    n_lookups = df_merge[df_merge['totallookups'] > 0].shape[0]
    n_lookups_per = n_lookups/n
    n_lookups_per = n_lookups_per * 100
    n_lookups_str = f'{round(n_lookups_per, 2)}'
    ob_str = 'ob_' if ob else ''
    
    df_lookups = pd.DataFrame({f'{ob_str}n_prescribers': [n], f'{ob_str}n_lookups': [n_lookups], f'{ob_str}%': [n_lookups_str]})
    score_ob_str = 'percent of ob prescribers with a lookup:' if ob else 'percent of cs prescribers with a lookup:'
    score_str = f'{score_ob_str} {n_lookups} / {n} = {n_lookups_str}%'
    print(score_str)
    return df_lookups

def main():
    # get last month
    today = datetime.datetime.now()
    last_month = today.replace(day=1) - datetime.timedelta(days=1)
    m_y_str = last_month.strftime('%b-%y')
    m_y = last_month.strftime('%Y%m')
    # m_y = '202211'
    # m_y_str = 'Nov-22'
    reg_scores = scorecard(m_y)
    ob_scores = scorecard(m_y, ob=True)
    
    date_col = pd.DataFrame({'date': [m_y_str]})
    combined = pd.concat([date_col, reg_scores, ob_scores], axis=1)
    combined.to_clipboard(index=False, header=False)
    print('combined copied to clipboard')

if __name__ == '__main__':
    main() 