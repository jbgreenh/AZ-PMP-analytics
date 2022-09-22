import pandas as pd

deas = pd.read_csv('data/az_pharmacy_deas.csv', index_col=None)
manage_pharmacies = pd.read_csv('data/manage_pharmacies.csv', index_col=None)
igov = pd.read_csv('data/igov_pharmacy.csv', index_col=None)
submits = pd.read_csv('data/submits.csv', index_col=None)

# check for pharmacists in deas but not in manage_pharmacies
deas_not_in_mp = deas[~deas['DEA Number'].isin(manage_pharmacies['DEA'])]

# get DEAs and submission numbers from compliance dashboard
submits = submits[['Dea Number', 'Measure Values']]
submits.rename(columns={'Measure Values': 'Submissions'}, inplace=True)
submits = submits.groupby('Dea Number').sum()
submits = submits[~submits.index.str.isnumeric()]
submits.index = submits.index.str.upper()

# add status and email from igov to deas_not_in_mp
deas_not_in_mp = deas_not_in_mp.merge(igov[['License/Permit #', 'Status', 'Email']], 
        left_on='State License Number', right_on='License/Permit #', how='left').drop(columns=['License/Permit #'])
deas_not_in_mp = deas_not_in_mp[['DEA Number', 'Name', 'State License Number','Address 1', 'Address 2', 'Address 3', 'City', 'State',
       'Zip Code', 'Status', 'Email']]

# add submission numbers to deas_not_in_mp
deas_not_in_mp = deas_not_in_mp.merge(submits, left_on='DEA Number', right_index=True, how='left')
deas_not_in_mp.to_clipboard(index=False)
print('DEAs not in clearinhouse list copied to clipboard')
