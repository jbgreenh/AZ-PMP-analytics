import pandas as pd
pd.options.display.max_columns = 999

# widths and names according to the file format specifications provided by the DEA
dea_widths = [9, 1, 16, 8, 40, 40, 40, 40, 33, 2, 5, 2, 1, 8, 10, 20, 20]
dea_names = [
    'DEA Number', 'Business Activity Code', 'Drug Schedules', 'Expiration Date', 'Name', 
    'Additional Company Info', 'Address 1', 'Address 2', 'City', 'State', 'Zip Code', 'Business Activity Sub Code',
    'Payment Indicator', 'Activity', 'Degree', 'State License Number', 'State CS License Number'
    ]

print('trying to read deas')
deas = pd.read_fwf('data/cs_active.txt', widths=dea_widths, names=dea_names, encoding='latin-1')
deas = deas[(deas['Business Activity Code'] == 'A')]
deas = deas[deas['State'] == 'AZ']
print(deas.head())
deas.to_csv('data/az_pharmacy_deas.csv', index=False)
print('updated data/az_pharmacy_deas.csv')