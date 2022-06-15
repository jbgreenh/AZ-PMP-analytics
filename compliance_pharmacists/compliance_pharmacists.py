import pandas as pd

def highlight_YN(val):
    match val:
        case 'NO':
            color = '#ffcccb'   # light red
        case 'YES':
            color = '#d2f8d2'   # light green
        case _:
            color = 'transparent'

    return 'background-color: {}'.format(color)

awarxe = pd.read_excel('awarxe.xlsx', skiprows=1, index_col=None)
inspection_list = pd.read_csv('inspection_list.csv', index_col=None)
manage_pharmacies = pd.read_csv('manage_pharmacies.csv', index_col=None)
sched_2 = pd.read_csv('pharmacy_sched_2.csv', index_col=None)
pharmacies_igov = pd.read_csv('igov_pharmacy.csv', index_col=None)
pharmacists_igov = pd.read_csv('igov_pharmacist.csv', index_col=None)
# TODO
# pharmacist lookups
# 2 months, add them together

final_sheet = pd.merge(inspection_list, pharmacies_igov[['License/Permit #', 'Business Name', 'SubType']], 
    left_on='Permit #', right_on='License/Permit #', how='left').drop(['License/Permit #'], axis=1)

final_sheet = pd.merge(final_sheet, manage_pharmacies[['Pharmacy License Number', 'DEA']],
    left_on='Permit #', right_on='Pharmacy License Number', how='left').drop(['Pharmacy License Number'], axis=1)
final_sheet.rename(columns={'DEA':'Pharmacy DEA'}, inplace=True)

final_sheet = pd.merge(final_sheet, pharmacists_igov[['License/Permit #', 'First Name', 'Middle Name', 'Last Name', 'Status', 'Phone', 'Email']],
    left_on='License #', right_on='License/Permit #', how='left').drop(['License/Permit #'], axis=1)

final_sheet = final_sheet.assign(awarxe=final_sheet['Pharmacy DEA'].isin(awarxe['DEA Number']))
final_sheet['awarxe'] = final_sheet['awarxe'].map({True:'YES' ,False:'NO'})

# TODO
# add pharmacist lookups
# rearrange columns
# to clipboard
# ---------------
# group by and sum for new sheet
# usage sheet

print(final_sheet.columns)
