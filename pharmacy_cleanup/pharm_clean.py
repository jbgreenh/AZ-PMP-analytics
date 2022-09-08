import pandas as pd
from datetime import date

ddr = pd.read_csv('data/delinquent_dispenser_request.csv', index_col=None)
igov = pd.read_csv('data/igov_pharmacy.csv', index_col=None)
mp = pd.read_csv('data/manage_pharmacies.csv', index_col=None)

ddr = ddr[ddr['Days Delinquent'] >= 20]
ddr = pd.merge(ddr, mp[['DEA', 'Pharmacy License Number']], on='DEA', how='left')
ddr = pd.merge(ddr, igov[['License/Permit #', 'Status']], 
    left_on='Pharmacy License Number', right_on='License/Permit #', how='left').drop(columns=['License/Permit #'])
ddr.sort_values(['Status', 'Pharmacy License Number'], ascending=False, inplace=True)

#get today's date as a string
today = date.today().strftime("%m/%d/%Y")
ddr['Date List Pulled'] = today

#rearrange columns
ddr = ddr[['Pharmacy Name', 'Pharmacy Address', 'Pharmacy License Number', 'DEA', 'Status', 'Days Delinquent', 
    'Last Compliant', 'Date List Pulled', 'Primary Email', 'Primary Phone']]

ddr.to_clipboard(index=False)
print('copied to clipboard')