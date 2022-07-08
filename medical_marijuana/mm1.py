import pandas as pd

def trim_string(astring, trailing):
    '''trim trailing characters from a string'''
    thelen = len(trailing)
    if astring[-thelen:] == trailing:
        return astring[:-thelen]
    return astring

def main():
    awarxe = pd.read_excel('data/awarxe.xlsx', skiprows=1, index_col=None)
    awarxe = awarxe[~awarxe['DEA Number'].isnull()]
    awarxe = awarxe[['Last Name', 'Professional License Number', 'DEA Number']]
    awarxe['Last Name'] = awarxe['Last Name'].str.upper()

    mm = pd.read_csv('data/mm_audit.csv', index_col=None)
    mm['Physician Name'] = mm['Physician Name'].str.upper()

    old = pd.read_excel('data/old_mm.xlsx', index_col=None)
    old = old[['Physician ID', 'DEA Number']]

    deg_for_trimming = [' DO', ' MD', ' PA', ' NP', ' ND']   # add degrees with a leading space to be trimmed as needed

    for deg in deg_for_trimming:
        awarxe['Last Name'] = awarxe['Last Name'].apply(lambda x: trim_string(x, deg))
        awarxe['Last Name'] = awarxe['Last Name'].apply(lambda x: trim_string(x, ','))
        mm['Physician Name'] = mm['Physician Name'].apply(lambda x: trim_string(x, deg))
        mm['Physician Name'] = mm['Physician Name'].apply(lambda x: trim_string(x, ','))

    # check the old file for matches on physician id
    mm = mm.merge(old[['Physician ID', 'DEA Number']], left_on='Physician Id', right_on='Physician ID', how='left').drop('Physician ID', axis=1)
    mm_old_match = mm[~mm['DEA Number'].isnull()]
    mm_no_old_match = mm[mm['DEA Number'].isnull()].drop('DEA Number', axis=1)

    awarxe['awarxe_code'] = awarxe['Last Name'].str[-3:] + awarxe['Professional License Number'].str[-4:]
    mm_no_old_match['mm_code'] = mm_no_old_match['Physician Name'].str[-3:] + mm_no_old_match['License Number'].str[-4:]
    mm_no_old_match = mm_no_old_match.merge(awarxe[['awarxe_code', 'DEA Number']], 
        left_on='mm_code', right_on='awarxe_code', how='left').drop(['awarxe_code', 'mm_code'], axis=1)
    mm_code_match = mm_no_old_match[~mm_no_old_match['DEA Number'].isnull()]
    mm_match_neither = mm_no_old_match[mm_no_old_match['DEA Number'].isnull()]
    mm_match_neither = mm_match_neither.sort_values(by='Application Count', ascending=False)

    mm_matches_combined = pd.concat([mm_old_match, mm_code_match])

    mm_matches_combined.to_csv('data/mm_matches_combined.csv', index=False)
    mm_match_neither.to_clipboard(index=False)
    print('generated data/mm_matches_combined.csv')
    print('copied mm_match_neither to clipboard')

if __name__ == '__main__':
    main()