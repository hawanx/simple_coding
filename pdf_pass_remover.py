from pypdf import PdfReader, PdfWriter

input_pdf = ""

password = ""

reader = PdfReader(input_pdf)

if reader.is_encrypted:
    reader.decrypt(password)

writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

with open(input_pdf, "wb") as f:
    writer.write(f)

print("Password removed successfully!")