import pandas as pd
from utils.sheet_formatting import *

def signups(out_fp):
    '''generate an excel file at out_fp with Totals and County Lists tabs'''
    # read necessary tables
    deas = pd.read_csv('data/az_prescriber_deas.csv', index_col=None)
    awarxe = pd.read_excel('data/awarxe.xlsx', skiprows=1, index_col=None)
    dispensations = pd.read_csv('data/az_dispensations.csv', sep='|')
    exclude_dvm = pd.read_csv('data/exclude_dvm.csv', index_col=None)
    city_county_lkup = pd.read_csv('data/lookup_city_county.csv', index_col=None)
    typo_city_lkup = pd.read_csv('data/lookup_mispelled_city.csv', index_col=None)

    dispensations['state'] = dispensations['state'].str.upper()

    # create az_pro_info from dispensations and DEA list
    az_dispensations = dispensations[(dispensations['state'] == 'AZ') | (dispensations['state'] == 'ARIZONA')]
    az_dispensations = az_dispensations.drop(az_dispensations.dropna(subset=['dea_suffix']).index)
    pro_info_sum = az_dispensations[['dea_number', 'rx_count']].groupby('dea_number', as_index=False).sum()
    az_pro_info = pd.merge(pro_info_sum, deas[['DEA Number', 'Name', 'Address 1', 'Address 2', 'Address 3', 'City', 'State', 'Zip Code']], 
        left_on='dea_number', right_on='DEA Number', how='inner').drop(columns=['DEA Number'])

    # fix typos in city and add county
    # TODO add report of unmatched typos
    az_pro_info.rename(columns={'City':'pi_city'}, inplace=True)
    az_pro_info['pi_city'] = az_pro_info['pi_city'].str.upper()
    az_pro_info = pd.merge(az_pro_info, typo_city_lkup[['CityError', 'City']], 
        left_on='pi_city', right_on='CityError', how='left')
    az_pro_info['fixed_city'] = az_pro_info['City'].fillna(az_pro_info['pi_city'])
    az_pro_info = az_pro_info.drop(columns=['pi_city','CityError','City'])
    az_pro_info.rename(columns={'fixed_city':'City'}, inplace=True)
    az_pro_info = pd.merge(az_pro_info, city_county_lkup[['City', 'County']], how='left')

    # keep only prescribers with a county
    az_pro_info = az_pro_info[az_pro_info['County'].notna()]

    # update exclude_dvm
    vets = az_pro_info[az_pro_info['Name'].str.contains('DVM|VMD')]
    vets = vets[['dea_number']]
    vets.rename(columns={'dea_number':'DEA'}, inplace=True)
    new_vets = vets.merge(exclude_dvm, how='left', indicator=True)
    new_vets = new_vets[new_vets['_merge'] == 'left_only'][['DEA']]
    new_exclude_dvm = pd.concat([exclude_dvm, new_vets])
    new_exclude_dvm.to_csv('data/exclude_dvm.csv', index=False)

    # drop vets from list
    az_pro_info = az_pro_info.merge(new_exclude_dvm, left_on='dea_number', right_on='DEA', how='left', indicator=True)
    az_pro_info = az_pro_info[az_pro_info['_merge'] == 'left_only'].drop(columns=['DEA', '_merge'])

    # drop hospital style names
    az_pro_info = az_pro_info[~az_pro_info['Name'].str.contains('CENTER|HOSPITAL|SCOTTSDALE|MEDICAL|REGIONAL')]

    # check registration in awarxe
    az_pro_info = az_pro_info.assign(awarxe=az_pro_info['dea_number'].isin(awarxe['DEA Number']))
    az_pro_info['awarxe'] = az_pro_info['awarxe'].map({True:'YES' ,False:'NO'})
    az_pro_info.drop_duplicates(subset="dea_number", keep='first', inplace=True)

    # rearrange and sort the table
    az_pro_info = az_pro_info[['awarxe', 'County', 'Name', 'Address 1', 'Address 2', 'Address 3', 'City', 'State', 'Zip Code']]
    az_pro_info.sort_values(['County'], inplace=True)
    az_pro_info.rename(columns={'awarxe':'AWARxE Account?', 'Name':'Prescriber Name'}, inplace=True)

    # make the totals table
    yeses = az_pro_info[['County', 'AWARxE Account?']]
    yeses = yeses[yeses['AWARxE Account?'] == 'YES']
    yeses = yeses.groupby('County', as_index=False).count()
    county_count = az_pro_info[['County']].value_counts().reset_index(name='county_total')
    totals = pd.merge(yeses, county_count, on='County', how='inner')
    sums_row = pd.DataFrame([['Total', totals['AWARxE Account?'].sum(), totals['county_total'].sum()]], columns=totals.columns)
    totals = pd.concat([totals, sums_row])
    totals['percent'] = (totals['AWARxE Account?'] / totals['county_total']) * 100
    totals = totals.round({'percent':2})
    totals.rename(columns={'AWARxE Account?':'Number of PMP Registrants1', 
        'county_total':'Number of Controlled Substance (II-IV) Prescribers (last 12 months)2',
        'percent':'Percentage3'}, inplace=True)

    # write to output_fp
    writer = pd.ExcelWriter(out_fp)

    totals.to_excel(writer, index=False, sheet_name='Totals', engine='xlsxwriter')
    az_pro_info.style.applymap(highlight_cells).to_excel(writer, index=False, sheet_name='County Lists', engine='xlsxwriter')
    set_col_widths(writer, totals, 'Totals')
    set_col_widths(writer, az_pro_info, 'County Lists')

    # get delegate users in casa grande
    awarxe_delegates = awarxe[awarxe['Role Title'].str.contains('Delegate') | awarxe['Role Title'].str.contains('Technician')]
    awarxe_delegates = awarxe_delegates[awarxe_delegates['City'].str.upper() == 'CASA GRANDE']
    awarxe_delegates_presc = awarxe_delegates[awarxe_delegates['Role Title'].str.contains('Presc')]
    awarxe_delegates_pharm = awarxe_delegates[awarxe_delegates['Role Title'].str.contains('Pharm')]
    print(f'number of CG prescriber delegates: {len(awarxe_delegates_presc)}')
    print(f'number of CG pharmacist delegates: {len(awarxe_delegates_pharm)}')

    writer.save()
    print(f'{out_fp} saved')

def main():
    out_fp = '~/Downloads/monthly_signups.xlsx' # ~/Downloads/
    signups(out_fp)

if __name__ == "__main__":
    main()

# TODO
# cover page
# formatting

# for adding images: https://xlsxwriter.readthedocs.io/example_images.html