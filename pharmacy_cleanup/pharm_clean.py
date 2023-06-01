import pandas as pd
import numpy as np
from datetime import date

ddr = pd.read_csv('data/delinquent_dispenser_request.csv', index_col=None)
igov = pd.read_csv('data/igov_pharmacy.csv', index_col=None)
mp = pd.read_csv('data/manage_pharmacies.csv', index_col=None)

ddr = ddr[ddr['Days Delinquent'] >= 21]
ddr['DEA'] = ddr['DEA'].str.upper().str.strip()
mp['DEA'] = mp['DEA'].str.upper().str.strip()

ddr = pd.merge(ddr, mp[['DEA', 'Pharmacy License Number']], on='DEA', how='left')
ddr['Pharmacy License Number'] = ddr['Pharmacy License Number'].str.upper().str.strip()
igov['License/Permit #'] = igov['License/Permit #'].str.upper().str.strip()
ddr = pd.merge(ddr, igov[['License/Permit #', 'Status', 'Business Name', 'Street Address', 'Apt/Suite #', 'City', 'State', 'Zip', 'Email', 'Phone']], 
    left_on='Pharmacy License Number', right_on='License/Permit #', how='left').drop(columns=['License/Permit #'])
ddr.sort_values(['Status', 'Pharmacy License Number', 'Days Delinquent'], ascending=False, inplace=True)

# favor info from igov over manage pharmacies and add apt/suite # if available
ddr['Street Address'] = np.where(ddr['Apt/Suite #'].isna(), ddr['Street Address'], 
    ddr['Street Address'].str.cat(ddr['Apt/Suite #'].astype(str), sep=', '))
ddr['Street Address'] = ddr['Street Address'].fillna(ddr['Pharmacy Address'])
ddr['Business Name'] = ddr['Business Name'].fillna(ddr['Pharmacy Name'])

ddr.rename(columns={'Primary Email': 'awarxe_email'}, inplace=True)
ddr.rename(columns={'Email': 'igov_email'}, inplace=True)
ddr.rename(columns={'Primary Phone': 'awarxe_phone'}, inplace=True)
ddr.rename(columns={'Phone': 'igov_phone'}, inplace=True)

# convert last compliant date
ddr['Last Compliant'] = pd.to_datetime(ddr['Last Compliant'])
ddr['Last Compliant'] = ddr['Last Compliant'].dt.strftime('%m/%d/%Y')

# get today's date as a string
today = date.today().strftime("%m-%d-%Y")
ddr['Date List Pulled'] = today

# rearrange columns
ddr = ddr[['Business Name', 'Street Address', 'City', 'State', 'Zip', 'Pharmacy License Number', 'DEA', 'Status', 'Days Delinquent', 
    'Last Compliant', 'Date List Pulled', 'awarxe_email', 'igov_email', 'awarxe_phone', 'igov_phone']]

ddr.to_clipboard(index=False)
print('copied to clipboard')