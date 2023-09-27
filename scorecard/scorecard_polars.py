import datetime
import polars as pl
import pandas as pd
from utils.from_sftp import *

def scorecard():
    '''takes a string of the form YYYYMM and returns a scorecard row as a dataframe'''

    # get last month
    today = datetime.datetime.now()
    last_month = today.replace(day=1) - datetime.timedelta(days=1)
    m_y_str = last_month.strftime('%b-%y')
    m_y = last_month.strftime('%Y%m')

    print(f'getting {m_y} patient request data')
    lookups = (
        pl.from_pandas(from_sftp(f'/Monthly/Patient_Requests_REPORTAE_48/AZ_PtReqByProfile_{m_y}/Prescriber.csv'))
        .select('dea_number','totallookups')
    )

    print(f'getting {m_y} dispensations data')
    disps = (
        pl.from_pandas(from_sftp(f'/Monthly/REPORTAE_47/Dispensations/AZ_Dispensations_{m_y}.csv'))
        .filter(pl.col('state') == 'AZ')
        .select('dea_number')
        .join(lookups, on='dea_number', how='left')
        .group_by('dea_number')
        .sum()
    )

    n = disps.shape[0]
    n_lookups = disps.filter(pl.col('totallookups') > 0).shape[0]
    n_lookups_per = (n_lookups / n) * 100
    n_lookups_str = f'{round(n_lookups_per, 2)}'
    df_lookups = pd.DataFrame({'n_prescribers': [n], 'n_lookups': [n_lookups], '%': [n_lookups_str]})

    print(f'getting {m_y} ob dispensations data')
    ob_disps = (
        pl.from_pandas(from_sftp(f'/Monthly/REPORTAE_47/Dispensations/AZ_Dispensations_{m_y}_opioid_benzo.csv'))
        .filter(pl.col('state') == 'AZ')
        .select('dea_number')
        .join(lookups, on='dea_number', how='left')
        .group_by('dea_number')
        .sum()
    )

    ob_n = ob_disps.shape[0]
    ob_n_lookups = ob_disps.filter(pl.col('totallookups') > 0).shape[0]
    ob_n_lookups_per = (ob_n_lookups / ob_n) * 100
    ob_n_lookups_str = f'{round(ob_n_lookups_per, 2)}'
    ob_df_lookups = pd.DataFrame({'ob_n_prescribers': [ob_n], 'ob_n_lookups': [ob_n_lookups], 'ob_%': [ob_n_lookups_str]})

    date_col = pd.DataFrame({'date': [m_y_str]})
    combined = pd.concat([date_col, df_lookups, ob_df_lookups], axis=1)
    combined.to_clipboard(index=False, header=False)
    print('new row copied to clipboard')
    print(combined)

def main():
    scorecard()

if __name__ == '__main__':
    main() 