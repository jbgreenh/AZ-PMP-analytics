from operator import index
import pandas as pd

INPUT_FN = 'tests/test.xlsx'
OUTPUT_FN = '~/Downloads/testq.xlsx' # ~/Downloads/
DEA_COL_NAME = 'DEA#'

def highlight_cells(val):
    match val:
        case 'NO':
            color = '#ffcccb'   # light red
        case 'YES':
            color = '#d2f8d2'   # light green
        case _:
            color = 'transparent'

    return 'background-color: {}'.format(color)

awarxe = pd.read_excel('awarxe.xlsx', skiprows=1, index_col=None)
input = pd.read_excel(INPUT_FN, index_col=None)

output = input.assign(awarxe=input[DEA_COL_NAME].isin(awarxe['DEA Number']))
output['awarxe'] = output['awarxe'].map({True:'YES' ,False:'NO'})

writer = pd.ExcelWriter(OUTPUT_FN)

output.style.applymap(highlight_cells).to_excel(writer, index=False, sheet_name='registration', engine='xlsxwriter')

# set column width based on max length in column
for col in output:
    col_len = max(output[col].astype(str).map(len).max(), len(col)) + 2
    col_i = output.columns.get_loc(col)
    writer.sheets['registration'].set_column(col_i, col_i, col_len)

writer.save()
print(f'{OUTPUT_FN} saved')