import pandas as pd
from utils.sheet_formatting import *

def mm(output_fp):
    # here we will combine the lookup files and the matches and manual files
    mm_matches = pd.read_csv('data/mm_matches_combined.csv', index_col=None)
    mm_manual = pd.read_csv('data/mm_manual.csv', index_col=None)

    mm_combined = pd.concat([mm_matches, mm_manual])

    # read and combine files 1.csv, 2.csv, 3.csv, 4.csv, 5.csv, 6.csv
    lookups = pd.DataFrame()
    for n in range(1, 7):
        lookups = pd.concat([lookups, pd.read_csv(f'data/{n}.csv', delimiter='|', index_col=None)])

    # group by DEA Number and sum of totallookups
    lookups = lookups[['dea_number', 'totallookups']].groupby('dea_number').sum()

    # merge mm_combined and lookups
    mm_combined = mm_combined.merge(lookups[['totallookups']], 
        left_on='DEA Number', right_index=True, how='left')

    # if totallookups is null, set to 0
    mm_combined['totallookups'] = mm_combined['totallookups'].fillna(0)

    # add columns
    mm_combined['Lookups/Count'] = mm_combined['totallookups'] / mm_combined['Application Count']
    mm_combined['>=20'] = mm_combined['Application Count'] >= 20
    mm_combined['<80% Lookups'] = mm_combined['Lookups/Count'] < 0.8
    mm_combined['test'] = mm_combined['>=20'] & mm_combined['<80% Lookups']
    mm_combined['>=20'] = mm_combined['>=20'].map({True: 'YES', False: 'NO'})
    mm_combined['<80% Lookups'] = mm_combined['<80% Lookups'].map({True: 'YES', False: 'NO'})
    mm_combined['test'] = mm_combined['test'].map({True: 'YES', False: 'NO'})

    mm_combined = mm_combined.sort_values(by=['test', 'Application Count'], ascending=False)

    writer = pd.ExcelWriter(output_fp)
    mm_combined.reset_index(drop=True).style.applymap(highlight_cells).to_excel(writer, index=False, sheet_name='mm audit', engine='xlsxwriter')

    set_col_widths(writer, mm_combined, 'mm audit')

    writer.save()
    print(f'{output_fp} saved')

def main():
    out_fp = input('output file path? ex: ~/Downloads/mmq.xlsx\n')
    if out_fp == '':
        out_fp = '~/Downloads/mmq.xlsx'
    mm(out_fp)

if __name__ == '__main__':
    main()