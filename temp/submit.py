import pandas as pd

submits = pd.read_csv('data/submits.csv', index_col=None)

submits = submits[['Dea Number', 'Measure Values']]
submits = submits.groupby('Dea Number').sum()
submits = submits[~submits.index.str.isnumeric()]
submits.index = submits.index.str.upper()

submits.to_clipboard()
print('copied to clipboard')