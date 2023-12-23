from pypdf import PdfReader

reader = PdfReader("Vaani_Pathariya_Resume.pdf")

for i in range(len(reader.pages)):
  page = reader.pages[i]
  print(page.extract_text())