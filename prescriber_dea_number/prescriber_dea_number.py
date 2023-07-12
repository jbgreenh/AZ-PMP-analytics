import pandas as pd

dsr = pd.read_csv('data/dsr.csv', index_col=None)
deas = pd.read_csv('../deas/data/deas.csv', index_col=None, low_memory=False)

all_presc = deas.query('`Business Activity Code` == "C" or `Business Activity Code` == "M"')

presc_info = all_presc[['DEA Number', 'Name', 'State License Number']].copy()
presc_info = presc_info.rename(columns={'Name':'dea_name'})

dsr = dsr.drop(columns=['Pharmacy License Number', 'Status', 'igov_email', 'igov_phone', 'City', 'State', 'Zip'])

dsr_presc = presc_info.merge(dsr, how='right', left_on='DEA Number', right_on='DEA').drop(columns=['DEA'])
dsr_presc.to_clipboard(index=False)
print('prescriber details copied to clipboard')