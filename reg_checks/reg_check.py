import pandas as pd
from utils.sheet_formatting import *

def check_reg(input_fn, output_fn, dea_col_name):
    awarxe = pd.read_excel('data/awarxe.xlsx', skiprows=1, index_col=None)
    input = pd.read_excel(input_fn, index_col=None)

    output = input.assign(awarxe=input[dea_col_name].isin(awarxe['DEA Number']))
    output['awarxe'] = output['awarxe'].map({True:'YES' ,False:'NO'})

    writer = pd.ExcelWriter(output_fn)

    output.style.applymap(highlight_cells).to_excel(writer, index=False, sheet_name='registration', engine='xlsxwriter')

    set_col_widths(writer, output, 'registration')

    writer.save()
    print(f'{output_fn} saved')

def main():
    in_fn = input('input file name? ex: data/test.xlsx\n')
    out_fn = input('output file name? ex: ~/Downloads/avpq.xlsx\n')
    dea_col = input('dea number column name? ex: DEA Number\n')
    check_reg(input_fn=in_fn, output_fn=out_fn, dea_col_name=dea_col)

if __name__ == "__main__":
    main()