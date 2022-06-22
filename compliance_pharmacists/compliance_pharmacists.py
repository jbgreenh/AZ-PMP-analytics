import sys
import pandas as pd

def run_it():
    awarxe = pd.read_excel('data/awarxe.xlsx', skiprows=1, index_col=None)
    inspection_list = pd.read_csv('data/inspection_list.csv', index_col=None)
    manage_pharmacies = pd.read_csv('data/manage_pharmacies.csv', index_col=None)
    sched_2 = pd.read_csv('data/pharmacy_sched_2.csv', index_col=None)
    pharmacies_igov = pd.read_csv('data/igov_pharmacy.csv', index_col=None)
    pharmacists_igov = pd.read_csv('data/igov_pharmacist.csv', index_col=None)

    lookups_mo_1 = pd.read_csv('data/lookups_mo_1.csv', sep='|', index_col=None)
    lookups_mo_2 = pd.read_csv('data/lookups_mo_2.csv', sep='|', index_col=None)
    lookups = pd.concat([lookups_mo_1, lookups_mo_2])
    lookups = lookups[['prof_lic', 'totallookups']].groupby('prof_lic', as_index=False).sum()

    # license and DEA numbers to uppercase for matching
    final_sheet = inspection_list
    final_sheet['License #'] = final_sheet['License #'].str.upper()
    final_sheet['Permit #'] = final_sheet['Permit #'].str.upper()
    pharmacies_igov['License/Permit #'] = pharmacies_igov['License/Permit #'].str.upper()
    pharmacists_igov['License/Permit #'] = pharmacists_igov['License/Permit #'].str.upper()
    manage_pharmacies['Pharmacy License Number'] = manage_pharmacies['Pharmacy License Number'].str.upper()
    awarxe['Professional License Number'] = awarxe['Professional License Number'].str.upper()
    lookups['prof_lic'] = lookups['prof_lic'].str.upper()

    # igov pharmacy: add business name and subtype
    final_sheet = pd.merge(inspection_list, pharmacies_igov[['License/Permit #', 'Business Name', 'SubType']], 
        left_on='Permit #', right_on='License/Permit #', how='left').drop(['License/Permit #'], axis=1)

    # manage pharmacies: add pharmacy DEA
    final_sheet = pd.merge(final_sheet, manage_pharmacies[['Pharmacy License Number', 'DEA']],
        left_on='Permit #', right_on='Pharmacy License Number', how='left').drop(['Pharmacy License Number'], axis=1)
    final_sheet.rename(columns={'DEA':'PharmacyDEA'}, inplace=True)

    # igov pharmacist: add name, status, phone, and email
    final_sheet = pd.merge(final_sheet, pharmacists_igov[['License/Permit #', 'First Name', 'Middle Name', 'Last Name', 'Status', 'Phone', 'Email']],
        left_on='License #', right_on='License/Permit #', how='left').drop(['License/Permit #'], axis=1)

    # awarxe: check registration and add review date
    final_sheet = final_sheet.assign(awarxe=final_sheet['License #'].isin(awarxe['Professional License Number']))
    final_sheet['awarxe'] = final_sheet['awarxe'].map({True:'YES' ,False:'NO'})
    final_sheet = pd.merge(final_sheet, awarxe[['Professional License Number', 'Registration Review Date']],
        left_on='License #', right_on='Professional License Number', how='left').drop('Professional License Number', axis=1)

    # add lookups
    final_sheet = pd.merge(final_sheet, lookups, left_on="License #", right_on='prof_lic', how='left').drop('prof_lic', axis=1)
    final_sheet.rename(columns={'totallookups':'lookups in date range'}, inplace=True)

    # rearrange columns
    final_sheet = final_sheet[['awarxe', 'Registration Review Date', 'lookups in date range',
        'SubType', 'Business Name', 'Permit #', 'License #', 'Last Insp',
        'Date Range', 'Notes', 'PharmacyDEA', 'First Name', 'Middle Name',
        'Last Name', 'Status', 'Phone', 'Email']]

    # sort by awarxe
    final_sheet.sort_values(['awarxe'], inplace=True)

    # usage table
    usage = final_sheet[['Permit #', 'lookups in date range']].groupby('Permit #', as_index=False).sum()
    usage = pd.merge(usage, final_sheet[['Permit #', 'PharmacyDEA', 'Business Name', 'SubType', 'Date Range', 'Notes']], how='left')
    usage = pd.merge(usage, sched_2, left_on='PharmacyDEA', right_on='Pharmacy DEA', how='left').drop('Pharmacy DEA', axis=1)
    usage.rename(columns={'Prescription Count':'pharmacy sched 2'}, inplace=True)
    usage = usage[['Permit #', 'PharmacyDEA', 'Business Name', 'SubType',
        'lookups in date range', 'pharmacy sched 2', 'Date Range',
        'Notes']]
    usage = usage.drop_duplicates()
    usage.sort_values(['lookups in date range', 'pharmacy sched 2'], ascending=[True, False], inplace=True)
    return(final_sheet, usage)

def main():
    # command line
    if len(sys.argv) != 2 or (sys.argv[1] != 'reg' and sys.argv[1] != 'use'):
        print('please follow one of the below formats')
        print('reg: python3.10 compliance_pharmacists.py reg')
        print('use: python3.10 compliance_pharmacists.py use')
    elif sys.argv[1] == 'reg':
        run_it()[0].to_clipboard(index=False)
        print('copied reg to clipoard')
    else:
        run_it()[1].to_clipboard(index=False)
        print('copied use to clipboard')

if __name__ == "__main__":
    main()    
