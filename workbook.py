import openpyxl as xl
import os

def write_excel(json_data):
    wb = xl.Workbook()
    dest_filename = 'size_data.xlsx'
    ws = wb.active
    ws.title = 'данные размеров рыб'
    for key in json_data:
        filename = [os.path.basename(key)]
        sizes = json_data[key]['cm_lengths']
        filename += sizes
        ws.append(filename)
    wb.save(filename = dest_filename)