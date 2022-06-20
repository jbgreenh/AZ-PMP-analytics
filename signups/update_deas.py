import pandas as pd

dea_widths = [9, 1, 2, 40, 40, 40, 40, 33, 2, 9, 8, 8, 12, 3, 9, 13, 15, 15]
dea_names = [
    'DEA Number', 'Business Activity Code', 'Business Activity Sub Code', 'Name', 
    'Address 1', 'Address 2', 'Address 3', 'City', 'State', 'Zip Code', 'Date of Original Registration',
    'Expiration Date', 'Drug Schedules', 'Degree', 'SSN', 'Tax ID', 'State License Number', 'State CS License Number'
    ]

print('try reading deas')
deas = pd.read_fwf('data/cs_active.txt', widths=dea_widths, names=dea_names, encoding='latin-1')
deas = deas[(deas['Business Activity Code'] == 'C') | (deas['Business Activity Code'] == 'M')]
deas = deas[deas['State'] == 'AZ']
deas.to_csv('data/az_prescriber_deas.csv', index=False)
print('updated data/az_prescriber_deas.csv')