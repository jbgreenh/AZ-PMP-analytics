import pandas as pd
import datetime
import pyperclip
from utils.sheet_formatting import *

naloxone = pd.read_csv('data/naloxone.csv', index_col=None)

total_naloxone = naloxone['Prescription Count'].sum()

naloxone = pd.concat([naloxone, pd.DataFrame([total_naloxone], columns=['Prescription Count'])])
total_naloxone_str = '{:,}'.format(total_naloxone)

today = datetime.datetime.now().strftime('%m%d%Y')
tod = 'Morning' if datetime.datetime.now().hour < 12 else 'Afternoon'

fp = input('enter path to folder for export: ex: data/\n')
if not fp:
    fp = 'data/'
output_fp = f'{fp}naloxone_{today}.xlsx'
writer = pd.ExcelWriter(output_fp)

naloxone.to_excel(writer, index=False, sheet_name='naloxone', engine='xlsxwriter')
set_col_widths(writer, naloxone, 'naloxone')
writer.save()
print(f'naloxone data exported to {output_fp}')
print(f'{total_naloxone = }')
pyperclip.copy(f'Good {tod} DHS Team-\n\nWe are now up to {total_naloxone_str} doses of naloxone dispensed.')
print('email body copied to clipboard')


