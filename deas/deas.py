import sys
import pandas as pd
pd.options.display.max_columns = 999

def az_deas(p):
    # widths and names according to the file format specifications provided by the DEA
    dea_widths = [9, 1, 16, 8, 40, 40, 40, 40, 33, 2, 5, 2, 1, 8, 10, 20, 20]
    dea_names = [
        'DEA Number', 'Business Activity Code', 'Drug Schedules', 'Expiration Date', 'Name', 
        'Additional Company Info', 'Address 1', 'Address 2', 'City', 'State', 'Zip Code', 'Business Activity Sub Code',
        'Payment Indicator', 'Activity', 'Degree', 'State License Number', 'State CS License Number'
        ]
        
    print('trying to read deas')
    deas = pd.read_fwf('data/cs_active.txt', widths=dea_widths, names=dea_names, encoding='latin-1')
    deas_az = deas[deas['State'] == 'AZ']

    if p == 'pharm':
        deas_az = deas_az[(deas_az['Business Activity Code'] == 'A')]
        print(deas_az.head())
        deas_az.to_csv('data/az_pharmacy_deas.csv', index=False)
        print('updated data/az_pharmacy_deas.csv')
    elif p == 'presc':
        deas_az = deas_az[(deas_az['Business Activity Code'] == 'C') | (deas_az['Business Activity Code'] == 'M')]
        print(deas_az.head())
        deas_az.to_csv('data/az_prescriber_deas.csv', index=False)
        print('updated data/az_prescriber_deas.csv')
    elif p == 'az':
        print(deas_az.head())
        deas_az.to_csv('data/az_deas.csv', index=False)
        print('updated data/az_deas.csv')
    elif p == 'all':
        print(deas.head())
        deas.to_csv('data/deas.csv', index=False)
        print('updated data/deas.csv')

def main():
    # command line
    if len(sys.argv) != 2 or (sys.argv[1] not in ['pharm', 'presc', 'az', 'all']):
        print('please follow one of the below formats')
        print('python deas.py presc')
        print('python deas.py pharm')
        print('python deas.py az')
        print('python deas.py all')
    else:
        az_deas(sys.argv[1])

if __name__ == '__main__':
    main()