from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen.canvas import Canvas
from io import BytesIO
from pathlib import Path

# Set input and output paths
old_path = ("./Modulo covid - modificabile .pdf")
new_path = ("./Modulo covid aggiornato.pdf")

# Read pdf
old_pdf = PdfFileReader(old_path)

# Create new content
packet = BytesIO()
canvas = Canvas(packet)
canvas.drawString(100, 100, "Hello world")
canvas.save()

# Move to the beginning of the StringIO buffer
packet.seek(0)

# Read new content
new_content = PdfFileReader(packet)

# Create new pdf
new_pdf = PdfFileWriter()

# Add new content to old pdf
page = old_pdf.getPage(0)
page.mergePage(new_content.getPage(0))
new_pdf.addPage(page)

with Path(new_path).open(mode="wb") as output_file:
    new_pdf.write(output_file)


