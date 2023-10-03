import sys
import polars as pl

def az_deas(p):
    # widths and names according to the file format specifications provided by the DEA
    dea_widths = [9, 1, 16, 8, 40, 40, 40, 40, 33, 2, 5, 2, 1, 8, 10, 20, 20]
    dea_names = [
        'DEA Number', 'Business Activity Code', 'Drug Schedules', 'Expiration Date', 'Name', 
        'Additional Company Info', 'Address 1', 'Address 2', 'City', 'State', 'Zip Code', 'Business Activity Sub Code',
        'Payment Indicator', 'Activity', 'Degree', 'State License Number', 'State CS License Number'
        ]
    slice_tuples = []
    offset = 0

    for w in dea_widths:
        slice_tuples.append((offset, w))
        offset += w

    # using unit seperator '\x1F' to trick pyarrow into only making one col, unlikely to make it's way into this latin-1 file
    deas = pl.read_csv('data/cs_active.txt', encoding='latin-1', has_header=False, new_columns=['full_str'], use_pyarrow=True, separator='\x1F')

    deas = (
        deas
        .with_columns(
            [pl.col('full_str').str.slice(slice_tuple[0], slice_tuple[1]).str.strip_chars().alias(col) for slice_tuple, col in zip(slice_tuples, dea_names)]
        )
        .drop('full_str')
    )

    if p == 'pharm':
        deas_pharm = (
            deas
            .filter(
                (pl.col('State') == 'AZ') &
                (pl.col('Business Activity Code') == 'A')
            )
        )
        print(deas_pharm)
        deas_pharm.write_csv('data/az_pharmacy_deas.csv')
        print('updated data/az_pharmacy_deas.csv')
    elif p == 'presc':
        deas_presc = (
            deas
            .filter(
                (pl.col('State') == 'AZ') &
                ((pl.col('Business Activity Code') == 'C') | (pl.col('Business Activity Code') == 'M'))
            )
        )
        print(deas_presc)
        deas_presc.write_csv('data/az_prescriber_deas.csv')
        print('updated data/az_prescriber_deas.csv')
    elif p == 'az':
        deas_az = (
            deas
            .filter(
                (pl.col('State') == 'AZ')
            )
        )
        print(deas_az)
        deas_az.write_csv('data/az_deas.csv')
        print('updated data/az_deas.csv')
    elif p == 'all':
        print(deas)
        deas.write_csv('data/deas.csv')
        print('updated data/deas.csv')

def main():
    # command line
    if len(sys.argv) != 2 or (sys.argv[1] not in ['pharm', 'presc', 'az', 'all']):
        print('please follow one of the below formats')
        print('python deas.py presc')
        print('python deas.py pharm')
        print('python deas.py az')
        print('python deas.py all')
    else:
        az_deas(sys.argv[1])

if __name__ == '__main__':
    main()