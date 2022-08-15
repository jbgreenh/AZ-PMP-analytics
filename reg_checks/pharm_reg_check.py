import pandas as pd
from utils.sheet_formatting import *

def check_reg(input_fp, output_fp, lino_col_name):
    awarxe = pd.read_excel('data/awarxe.xls', skiprows=1, index_col=None)
    input = pd.read_excel(input_fp, index_col=None)

    # input and awarxe license number to upper case
    input[lino_col_name] = input[lino_col_name].str.upper()
    input[lino_col_name] = input[lino_col_name].str.strip()
    awarxe['Professional License Number'] = awarxe['Professional License Number'].str.upper()
    awarxe['Professional License Number'] = awarxe['Professional License Number'].str.strip()

    output = input.assign(awarxe=input[lino_col_name].isin(awarxe['Professional License Number']))
    output['awarxe'] = output['awarxe'].map({True:'YES' ,False:'NO'})

    writer = pd.ExcelWriter(output_fp)

    output.style.applymap(highlight_cells).to_excel(writer, index=False, sheet_name='registration', engine='xlsxwriter')

    set_col_widths(writer, output, 'registration')

    writer.save()
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