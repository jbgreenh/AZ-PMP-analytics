import pandas as pd
from utils.sheet_formatting import *

def check_reg(input_fp, output_fp, dea_col_name):
    awarxe = pd.read_excel('data/awarxe.xlsx', skiprows=1, index_col=None)
    input = pd.read_excel(input_fp, index_col=None)

    output = input.assign(awarxe=input[dea_col_name].isin(awarxe['DEA Number']))
    output['awarxe'] = output['awarxe'].map({True:'YES' ,False:'NO'})

    writer = pd.ExcelWriter(output_fp)

    output.style.applymap(highlight_cells).to_excel(writer, index=False, sheet_name='registration', engine='xlsxwriter')

    set_col_widths(writer, output, 'registration')

    writer.save()
    print(f'{output_fp} saved')

def main():
    in_fp = input('input file path? ex: data/test.xlsx\n')
    out_fp = input('output file path? ex: ~/Downloads/prescq.xlsx\n')
    if out_fp == '':
        out_fp = '~/Downloads/prescq.xlsx'
    dea_col = input('dea number column name? ex: DEA Number\n')
    if dea_col == '':
        dea_col = 'DEA Number'
    check_reg(input_fp=in_fp, output_fp=out_fp, dea_col_name=dea_col)

if __name__ == "__main__":
    main()