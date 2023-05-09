from bs4 import BeautifulSoup
import xlwt

workbook = xlwt.Workbook(encoding = "utf-8")
worksheet = workbook.add_sheet("sheet1")
for i in range(0, 9):
    for j in range(0, i+1):
        worksheet.write(i, j ,i*j)

workbook.save("test1.xls")

