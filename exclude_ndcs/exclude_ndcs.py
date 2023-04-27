import pandas as pd

excluded_ndcs = pd.read_csv('data/excluded_ndcs.csv', index_col=None, low_memory=False, dtype=object)
antagonists = pd.read_csv('data/opiate_antagonists.csv', index_col=None, low_memory=False, dtype=object)

# get the ndc numbers that are not already on the list
new_ndcs = pd.merge(excluded_ndcs, antagonists, on='NDC', how='right', indicator=True)
new_ndcs = new_ndcs.query('_merge == "right_only"')
new_ndcs = new_ndcs.drop(columns=['_merge', 'drug'])
new_ndcs = new_ndcs.rename(columns={'Generic Name':'drug'})
new_ndcs.to_clipboard(index=False)
print('new_ndcs copied to clipboard, please input exclusion list in awarxe')

# update the list
new_file = pd.concat([excluded_ndcs, new_ndcs], axis=0, ignore_index=True)
new_file.to_csv('data/excluded_ndcs.csv', index=False)
print('data/excluded_ndcs.csv updated')