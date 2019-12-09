from io import StringIO, BytesIO
import re
from tempfile import NamedTemporaryFile
import random, string
import os

import pandas as pd

import pikepdf
from PyPDF2 import PdfFileReader
from openpyxl import Workbook
from openpyxl.styles import Font, Color, colors
from openpyxl.writer.excel import save_virtual_workbook


#pattern to match our text of choice
regex1 = r'(C.+ Name)(.+)(M.+ Number)(\d+)(E\w+ Address)(.+)(D[ a-zA-Z]+Statement)(.+)(S.+ Period)(.+ - \d{2} \w+ \d{4})'
regex = r'(\w{10})(\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2})(.+?)(Completed)(.*?\.\d{2})(.*?\.\d{2})'

def random_str(length=8):
	s = ''
	for i in range(length):
		s += random.choice(string.ascii_letters + string.digits)

	return s


def extract_from_pdf(file, password):
	"""
	Extract the contents of a pdf file to text
	"""
	content = pikepdf.open(file, password=password)
	inmemory_file = BytesIO()
	content.save(inmemory_file)
	pdf_reader = PdfFileReader(inmemory_file)
	num_pages = pdf_reader.getNumPages()

	extracted_data = StringIO()
	for page in range(num_pages):
		extracted_data.writelines(pdf_reader.getPage(page).extractText())

	return num_pages, extracted_data


def parse_mpesa_content(file):
	file.seek(0)

	lines = file.read()
	matches = re.compile(regex).findall(lines)
	matches2 = re.compile(regex1).findall(lines)

	fb = Font(name='Calibri', color=colors.BLACK, bold=True, size=11, underline='single')
	i = 0

    #creating the spreadheet
	book = Workbook()
	# grab the active worksheet
	sheet = book.active

	#excel styling 2
	ft = Font(name='Calibri', color=colors.BLUE, bold=True, size=11, underline='single')

	sheet['A1'] = 'RECEIPT NO'
	sheet['B1'] = 'COMPLETION TIME'
	sheet['C1'] = 'DETAILS'
	sheet['D1'] = 'TRANSACTION STATUS'
	sheet['E1'] = 'PAID IN(+)/WITHDRAWN(-)'
	sheet['F1'] = 'BALANCE'

	a1 = sheet['A1']
	b1 = sheet['B1']
	c1 = sheet['C1']
	d1 = sheet['D1']
	e1 = sheet['E1']
	f1 = sheet['F1']

	a1.font = ft
	b1.font = ft
	c1.font = ft
	d1.font = ft
	e1.font = ft
	f1.font = ft


	#adding every match to the excel file
	while i < len(matches):
	    # print(matches[i])
	    sheet.append(matches[i])
	    i = i + 1

	filename = random_str()
	book.save(filename)
	f = open(filename, 'rb')
	file = BytesIO(f.read())
	f.close()
	os.remove(filename)
	return file

def filter(file, filter_string):
	df = pd.read_excel(file)
	df = df[df.DETAILS == filter_string]

	output_file = BytesIO()
	df.to_excel(output_file)

	return output_file
