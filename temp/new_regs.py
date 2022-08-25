import pandas as pd

awarxe = pd.read_excel('data/awarxe.xls', skiprows=1, index_col=None)
awarxe = awarxe[awarxe['Role Category'] == 'pharmacist']
before = awarxe[awarxe['Registration Review Date'] < '2021-11-21']
after = awarxe[awarxe['Registration Review Date'] >= '2021-11-21']
print(f'Before: {before.shape[0]}')
print(f'After: {after.shape[0]}')
print(f'Total: {awarxe.shape[0]}')
ttl = before.shape[0] + after.shape[0]
print(f'percent change: {(ttl - before.shape[0]) / before.shape[0] * 100}')
print(awarxe['Role Title'].unique())