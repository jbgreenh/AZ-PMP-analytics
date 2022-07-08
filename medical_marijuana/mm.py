import pandas as pd

def trim_string(astring, trailing):
    '''trim trailing characters from a string'''
    thelen = len(trailing)
    if astring[-thelen:] == trailing:
        return astring[:-thelen]
    return astring

awarxe = pd.read_excel('data/awarxe.xlsx', skiprows=1, index_col=None)
awarxe = awarxe[~awarxe['DEA Number'].isnull()]
awarxe = awarxe[['Last Name', 'Professional License Number', 'DEA Number']]
awarxe['Last Name'] = awarxe['Last Name'].str.upper()

deg_for_trimming = [', DO', ', MD', ', PA', ', NP']   # add degrees to be trimmed as needed

for deg in deg_for_trimming:
    awarxe['Last Name'] = awarxe['Last Name'].apply(lambda x: trim_string(x, deg))

awarxe['awarxe_code'] = awarxe['Last Name'].str[-3:] + awarxe['Professional License Number'].str[-4:]

awarxe.to_csv('~/Downloads/test_awarxe.csv', index=False)

