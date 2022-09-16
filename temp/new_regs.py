import pandas as pd

awarxe = pd.read_excel('data/awarxe.xls', skiprows=1, index_col=None)
awarxe = awarxe[awarxe['Role Category'] == 'pharmacist']

ba_date = '2021-11-21'

before = awarxe[awarxe['Registration Review Date'] < ba_date]
after = awarxe[awarxe['Registration Review Date'] >= ba_date]
ttl = awarxe.shape[0]
print(f'Before: {before.shape[0]}')
print(f'After: {after.shape[0]}')
print(f'Total: {ttl}')
print(f'percent change: {(ttl - before.shape[0]) / before.shape[0] * 100}')
print(awarxe['Role Title'].unique())