import pandas as pd
from openpyxl.styles import PatternFill

def highlight_cells(val: str):
    '''highlight cells based on YES or NO'''
    match val:
        case 'NO':
            color = '#ffcccb'   # light red
        case 'YES':
            color = '#d2f8d2'   # light green
        case _:
            color = 'transparent'

    return 'background-color: {}'.format(color)

def set_col_widths(writer: pd.ExcelWriter, df: pd.DataFrame, sheet_name: str):
    '''set column width based on max length in column'''    
    for col in df:
        col_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
        col_i = df.columns.get_loc(col)
        writer.sheets[sheet_name].set_column(col_i, col_i, col_len)

def set_col_widths_openpyxl(writer: pd.ExcelWriter, df: pd.DataFrame, sheet_name: str):
    '''set column width based on max length in column'''
    for col in df:
        col_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
        col_i = df.columns.get_loc(col)
        col_i = chr(ord('A') + col_i)
        writer.sheets[sheet_name].column_dimensions[col_i].width = col_len