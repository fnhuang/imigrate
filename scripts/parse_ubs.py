import os 
from openpyxl import load_workbook

dir_path = os.path.dirname(os.path.realpath(__file__))

wb = load_workbook(dir_path + "/../data/UBS_PricesAndEarnings_OpenData.xlsx")
ws = wb.active
print(tuple(ws.columns))