import pandas as pd

# read necessary tables
deas = pd.read_csv('data/az_prescriber_deas.csv', index_col=None)
awarxe = pd.read_excel('data/awarxe.xlsx', skiprows=1, index_col=None)
az_dispensations = pd.read_csv('data/az_dispensations.csv', sep='|', index_col=None)
exclude_dvm = pd.read_csv('data/exclude_dvm.csv', index_col=None)
city_county_lkup = pd.read_csv('data/lookup_city_county.csv', index_col=None)
typo_city = pd.read_csv('data/lookup_mispelled_city.csv', index_col=None)

# TODO

# case fix

# city fix

# link stuff up

# generate file