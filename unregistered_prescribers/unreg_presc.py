import pandas as pd
from utils.from_sftp import *
from utils.sheet_formatting import *

def main():
    awarxe = awarxe_from_sftp()
    boards = pd.read_csv('data/boards.csv', index_col=None)
    exclude_degs = pd.read_csv('data/exclude_degs.csv', index_col=None)
    az_presc_deas = pd.read_csv('data/az_prescriber_deas.csv', index_col=None)

    az_presc_deas['DEA Number'] = az_presc_deas['DEA Number'].str.upper().str.strip()
    awarxe['dea number'] = awarxe['dea number'].str.upper().str.strip()
    az_presc_q = az_presc_deas.assign(awarxe=az_presc_deas['DEA Number'].isin(awarxe['dea number']))
    az_presc_q['awarxe'] = az_presc_q['awarxe'].map({True:'YES' ,False:'NO'})
    az_presc_q = az_presc_q[az_presc_q['awarxe'] == 'NO']

    # drop ')' '(' and '.' from Name
    pattern = '|'.join(['\(', '\)', '\.'])
    az_presc_q['Name'] = az_presc_q['Name'].str.replace(pattern, '', regex=True)

    az_presc_q['deg'] = az_presc_q['Name'].apply(lambda x: x.split(' ')[-1])

    def final_deg(row):
        if len(row['deg']) > 1 and row['deg'] not in exclude_degs['deg'].values:
            return row['deg']
        else:
            return row['Degree']

    az_presc_q['final_deg'] = az_presc_q.apply(lambda row: final_deg(row), axis=1)

    az_presc_q = az_presc_q.drop(columns=['Degree', 'deg'])
    az_presc_q = az_presc_q[az_presc_q['final_deg'].notnull()]
    az_presc_q = az_presc_q.rename(columns={'final_deg':'Degree'})

    az_presc_q = az_presc_q.merge(boards, how='left', left_on='Degree', right_on='degree')

    az_presc_q = az_presc_q[['awarxe', 'DEA Number', 'Name', 'Additional Company Info', 'Address 1', 'Address 2', 'City', 'State', 'Zip Code', 'degree', 'State License Number', 'board']]

    board_counts = az_presc_q['board'].value_counts().reset_index()
    board_counts = board_counts.rename(columns={'index':'board', 'board':'NOs'})
    board_counts = board_counts[board_counts['board'] != 'Veterinary']
    board_counts = board_counts[board_counts['board'] != 'Homeopathic']

    total_row = pd.DataFrame({'board':['Total'], 'NOs':board_counts['NOs'].sum()})
    board_counts = pd.concat([board_counts, total_row])

    dental = az_presc_q[az_presc_q['board'] == 'Dental']
    medical = az_presc_q[az_presc_q['board'] == 'Medical']
    naturopath = az_presc_q[az_presc_q['board'] == 'Naturopathic']
    nursing = az_presc_q[az_presc_q['board'] == 'Nursing']
    optometry = az_presc_q[az_presc_q['board'] == 'Optometry']
    osteopathic = az_presc_q[az_presc_q['board'] == 'Osteopathic']
    physician_assistants = az_presc_q[az_presc_q['board'] == 'Physician Assistants']
    podiatry = az_presc_q[az_presc_q['board'] == 'Podiatry']

    writer = pd.ExcelWriter('data/unregistered_prescribers.xlsx')
    tabs = {'Counts':board_counts, 'Dental':dental, 'Medical':medical, 'Naturopathic':naturopath, 'Nursing':nursing, 'Optometry':optometry, 
        'Osteopathic':osteopathic, 'Physician Assistants':physician_assistants, 'Podiatry':podiatry}

    for n, d in tabs.items():
        if n == 'Counts':
            d.to_excel(writer, index=False, sheet_name=n, engine='xlsxwriter')
        else:
            d.drop(columns=['board']).style.applymap(highlight_cells).to_excel(writer, index=False, sheet_name=n, engine='xlsxwriter')
        set_col_widths(writer, d, n)

    writer.close()
    print('data/unregistered_prescribers.xlsx saved')

if __name__ == '__main__':
    main()