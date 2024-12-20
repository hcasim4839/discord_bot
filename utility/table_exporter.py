'''
File is for various tables that can be used to display information
'''
from table2ascii import table2ascii
#import pandas as pd

def create_single_col_ascii_table(amt_of_rows:int, row_list:list, column_width = None, cell_alignment_list = None, header_list = None):
    table = None
    table_body = []
    print(f'{amt_of_rows=}')
    print(f'{row_list=}')
    for index in range(amt_of_rows):
        new_row_data = [row_list[index]]
        table_body.append(new_row_data)
    
    print(f'{table_body=}')
    table = table2ascii(body=table_body,header=header_list, cell_padding=2)
    return table


#def create_pd_dataframe(data:list[str], columns:list)->pd.DataFrame:
#    df = pd.DataFrame(data='',columns= [])
#    return df

#def export_pd_dataframe_to_img(dataframe:pd.DataFrame):
#    return None

