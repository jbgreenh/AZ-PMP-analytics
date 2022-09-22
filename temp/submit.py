import pandas as pd

submits = pd.read_csv('data/submits.csv', sep='\t', index_col=None)
manage_pharmacies = pd.read_csv('data/manage_pharmacies.csv', index_col=None)

not_mp = submits[~submits['Dea Number'].isin(manage_pharmacies['DEA'])]
not_mp = not_mp.sort_values(by=['Dispensary Name', 'License Number'])
not_mp = not_mp.drop_duplicates(subset=['Dea Number'])

not_mp.to_clipboard(index=False)