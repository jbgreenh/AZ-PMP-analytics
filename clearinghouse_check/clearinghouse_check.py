import pandas as pd

deas = pd.read_csv('data/az_pharmacy_deas.csv', index_col=None)
manage_pharmacies = pd.read_csv('data/manage_pharmacies.csv', index_col=None)
igov = pd.read_csv('data/igov_pharmacy.csv', index_col=None)
submits = pd.read_csv('data/submits.csv', sep='\t', encoding='utf-16',index_col=None)

# check for pharmacists in deas but not in manage_pharmacies
deas_not_in_mp = deas[~deas['DEA Number'].isin(manage_pharmacies['DEA'])]

# group by DEA and count number of submissions
submits = submits[['DEA Number']]
submits = submits.groupby('DEA Number').size().reset_index(name='Submissions')

submits = submits[~submits['DEA Number'].str.isnumeric()]
submits['DEA Number'] = submits['DEA Number'].str.upper()

# add status and email from igov to deas_not_in_mp
deas_not_in_mp = deas_not_in_mp.merge(igov[['License/Permit #', 'Status', 'Email']], 
        left_on='State License Number', right_on='License/Permit #', how='left').drop(columns=['License/Permit #'])

deas_not_in_mp = deas_not_in_mp[['DEA Number', 'Name', 'State License Number','Additional Company Info', 'Address 1', 'Address 2', 'City', 'State',
       'Zip Code', 'Status', 'Email']]

# add submission numbers to deas_not_in_mp
deas_not_in_mp = deas_not_in_mp.merge(submits, on='DEA Number', how='left')
deas_not_in_mp.to_clipboard(index=False)
print('DEAs not in manage pharmacies copied to clipboard')
