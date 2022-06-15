from operator import index
import pandas as pd

ddr = pd.read_csv('delinquent_dispenser_request.csv', index_col=None)
igov = pd.read_csv('list_request.csv', index_col=None)
mp = pd.read_csv('manage_pharmacies.csv', index_col=None)

ddr = ddr[ddr['Days Delinquent'] >= 20]
ddr = pd.merge(ddr,mp[['DEA', 'Pharmacy License Number']], on='DEA', how='left')
ddr = pd.merge(ddr,igov[['License/Permit #', 'Status']], left_on='Pharmacy License Number', right_on='License/Permit #', how='left').drop(['License/Permit #'], axis=1)
ddr.sort_values(['Status', 'Pharmacy License Number'], ascending=False, inplace=True)

ddr.to_clipboard(index=False)
print('copied to clipboard')
