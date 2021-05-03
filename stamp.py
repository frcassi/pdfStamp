from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen.canvas import Canvas
from io import BytesIO
from pathlib import Path
from reportlab.lib.units import cm
import os

parent_path = r"C:\Users\feder\OneDrive\Scout\!Branco\2020-2021\Moduli attività"
path = parent_path + "\\" + "Moduli compilati genitori"
new_base_path = parent_path + "\\" + "Moduli compilati genitori stamped"

# Set strings to be written
fields = [
    {
        'name':'location',
        'pos_x':3.65*cm,
        'pos_y':13.6*cm,
        'page':1,
        'font_size':13
    },
    {
        'name':'location_co',
        'pos_x':8.65*cm,
        'pos_y':13.6*cm,
        'page':1,
        'font_size':13
    },
    {
        'name':'date',
        'pos_x':16.45*cm,
        'pos_y':14.5*cm,
        'page':1,
        'font_size':13
    },
    {
        'name':'sig_loc_date',
        'pos_x':3.4*cm,
        'pos_y':3.2*cm,
        'page':2,
        'font_size':13
    }
]
values = { 
    'location':'Pontedecimo',
    'location_co':'Ricreatorio',
    'date':'03/05/2021',
    'sig_loc_date':'Genova, 03/05/2021'
    }

def stamp_pdf(old_base_path, filename):
    # Set input and output paths
    #old_path = ("./Modulo covid - modificabile .pdf")
    #new_path = ("./Modulo covid aggiornato.pdf")
    #new_path = old_path.split(".")[0] + " stamped.pdf"
    old_path = str(os.path.join(old_base_path, filename))
    new_path = str(os.path.join(new_base_path, filename))

    # Read pdf
    old_pdf = PdfFileReader(old_path)
    num_pages = old_pdf.getNumPages()

    # Create new content
    packet = BytesIO()
    canvas = Canvas(packet)

    for page_num in range(1, num_pages+1):
        for field in fields:
            if(field['page']==page_num):
                canvas.setFontSize(field['font_size'])
                value = values[field['name']]
                canvas.drawString(field['pos_x'], field['pos_y'], value)
        canvas.showPage()

    canvas.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)

    # Read new content
    new_content = PdfFileReader(packet)

    # Create new pdf
    new_pdf = PdfFileWriter()

    # Add new content to old pdf
    for page_num in range(num_pages):
        page = old_pdf.getPage(page_num)
        page.mergePage(new_content.getPage(page_num))
        new_pdf.addPage(page)

    with Path(new_path).open(mode="wb") as output_file:
        new_pdf.write(output_file)
    
    print(new_path)

if not os.path.isdir(new_base_path):
    os.mkdir(new_base_path)

for filename in os.listdir(path):
    if filename.endswith(".pdf"):
        stamp_pdf(path, filename)
    else:
        print("Not stamped:" + str(os.path.join(path, filename)))
        continue
