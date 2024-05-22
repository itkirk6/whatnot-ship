import PyPDF2
#import io
from PIL import Image, ImageWin
import win32print
import win32ui
#import win32con
from pdf2image import convert_from_path
import os

image_printer = "Zebra ZP 500 (ZPL) (Copy 1)"
page_printer = "Warehouse Printer (M404n)"


pdf_path = 'your_pdf_file.pdf'
image_path = 'extracted_image.png'
page_path = 'extracted_page.png'

cwd = os.getcwd()
poppler_path = os.path.join(cwd, "poppler-24.02.0", "Library", "bin")


PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111
# don't touch this



def extract_pdf(pdf_path):       
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        
        total_pages = len(reader.pages)
        
        images = convert_from_path(pdf_path, first_page=1, last_page=(total_pages - 1), poppler_path=poppler_path)
        for i in range(len(images)):
            images[i].save(page_path.split(".")[0] + f"_{i}." + page_path.split(".")[1], 'JPEG')
        
        #now, extract the image from the second page
        page = reader.pages[total_pages - 1]  # Page numbering starts from 0

        try:
            xObject = page['/Resources']['/XObject'].get_object()
        except KeyError:
            print("No objects found.")
            return None

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].get_data()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"

                image = Image.frombytes(mode, size, data)
                image.save(image_path)  # Save the image to a file



def print_image(image_path, printer_name):
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)

    bmp = Image.open(image_path)

    hDC.StartDoc(image_path)
    hDC.StartPage()

    dib = ImageWin.Dib(bmp)
    dib.draw(hDC.GetHandleOutput(), (0,0,printer_size[0],printer_size[1]))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()
    
    



#extract_pdf(pdf_path)
#print_image(image_path, image_printer)
#print_image(page_path, page_printer)
