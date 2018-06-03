# -*- coding: utf-8 -8-

from openpyxl import load_workbook
from openpyxl import Workbook
import datetime

def combine():
	wb = load_workbook('courses.xlsx')
	ws1 = wb[wb.sheetnames[0]]
	ws2 = wb[wb.sheetnames[1]]
	ws3 = wb.create_sheet(title='combined')
	titles = [x.value for x in ws1['B']]
	w3 = wb.copy_worksheet('students')
	for i in ws2.rows:
		_ = ws3.cell(column = 4, row = titles.index(i[1].value)+1, value = i[2].value )
	wb.save()

def split():
	pass

if __name__ == '__main__':
	combine()