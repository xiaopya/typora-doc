#coding: utf-8
import argparse
from pdf2docx import Converter
pdf_file = r'I:\python相关\wks-main2\wks-main\绿色环保作文300字10篇.pdf'
docx_file = r'I:\python相关\wks-main2\wks-main\test.docx'
cv = Converter(pdf_file)
cv.convert(docx_file, start=0, end=None)
cv.close()
