import pandas as pd
from utils.from_sftp import *
from utils.sheet_formatting import *

def check_reg(input_fp, output_fp, lino_col_name):
    awarxe = awarxe_from_sftp()
    input = pd.read_excel(input_fp, index_col=None)

    # input and awarxe license number to upper case
    input[lino_col_name] = input[lino_col_name].str.upper().str.strip()
    awarxe['professional license number'] = awarxe['professional license number'].str.upper().str.strip()

    output = input.assign(awarxe=input[lino_col_name].isin(awarxe['professional license number']))
    output['awarxe'] = output['awarxe'].map({True:'YES' ,False:'NO'})

    writer = pd.ExcelWriter(output_fp)

    output.style.applymap(highlight_cells).to_excel(writer, index=False, sheet_name='registration', engine='xlsxwriter')

    set_col_widths(writer, output, 'registration')

    writer.close()
    print(f'{output_fp} saved')

def main():
    in_fp = input('input file path? ex: data/test.xlsx\n')
    out_fp = input('output file path? ex: data/pharmq.xlsx\n')
    if out_fp == '':
        out_fp = 'data/pharmq.xlsx'
    li_col = input('license number column name? ex: License #\n')
    if li_col == '':
        li_col = 'License #'
    check_reg(input_fp=in_fp, output_fp=out_fp, lino_col_name=li_col)

if __name__ == "__main__":
    main()