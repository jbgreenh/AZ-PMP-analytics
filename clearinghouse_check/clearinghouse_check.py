import pandas as pd

deas = pd.read_csv('data/az_pharmacy_deas.csv', index_col=None)
ch = pd.read_csv('data/clearinghouse.csv', index_col=None)
igov = pd.read_csv('data/igov_pharmacy.csv', index_col=None)

# check for pharmacists in deas but not in clearinghouse
deas_not_in_ch = deas[~deas['DEA Number'].isin(ch['DEA'])]

# add status and email from igov to deas_not_in_ch
deas_not_in_ch = deas_not_in_ch.merge(igov[['License/Permit #', 'Status', 'Email']], 
        left_on='State License Number', right_on='License/Permit #', how='left').drop(columns=['License/Permit #'])
deas_not_in_ch = deas_not_in_ch[['DEA Number', 'Name', 'State License Number','Address 1', 'Address 2', 'Address 3', 'City', 'State',
       'Zip Code', 'Status', 'Email']]
deas_not_in_ch.to_clipboard(index=False)
print('DEAs not in clearinhouse list copied to clipboard')
