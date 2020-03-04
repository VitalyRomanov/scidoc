from PyPDF2 import PdfFileReader
import sys

filename = sys.argv[1]

with open(filename, 'rb') as f:
    pdf = PdfFileReader(f)
    info = pdf.getDocumentInfo()
    number_of_pages = pdf.getNumPages()

    print(info)

    all_text = ""

    for page_num in range(number_of_pages):
        page = pdf.getPage(1)
        text = page.extractText()

        all_text += text

    print(all_text)