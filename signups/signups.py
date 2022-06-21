import pandas as pd

# read necessary tables
deas = pd.read_csv('data/az_prescriber_deas.csv', index_col=None)
awarxe = pd.read_excel('data/awarxe.xlsx', skiprows=1, index_col=None)
dispensations = pd.read_csv('data/az_dispensations.csv', sep='|', index_col=None)
exclude_dvm = pd.read_csv('data/exclude_dvm.csv', index_col=None)
city_county_lkup = pd.read_csv('data/lookup_city_county.csv', index_col=None)
typo_city_lkup = pd.read_csv('data/lookup_mispelled_city.csv', index_col=None)

dispensations['state'] = dispensations['state'].str.upper()

az_dispensations = dispensations[(dispensations['state'] == 'AZ') | (dispensations['state'] == 'ARIZONA')]
pro_info_sum = az_dispensations[['dea_number', 'rx_count']].groupby('dea_number', as_index=False).sum()
az_pro_info = pd.merge(pro_info_sum, deas[['DEA Number', 'Name', 'Address 1', 'Address 2', 'Address 3', 'City', 'State', 'Zip Code']], 
    left_on='dea_number', right_on='DEA Number', how='inner').drop('DEA Number', axis=1)
print(az_pro_info)  # may want to filter for AZ again, will check
# TODO

# case fix

# city fix

# link stuff up

# generate file
# for adding images: https://xlsxwriter.readthedocs.io/example_images.html