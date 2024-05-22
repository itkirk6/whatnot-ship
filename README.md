
# whatnot-ship

This program is simple! use python to automatically ship whatnot orders to their desired printer when you download them.

# Setup

You will need to modify the printpdf.py file. Two variables at the top, 

```
image_printer = ""
page_printer = ""
```

You will need to fill this text in with the name of your printers. The image printer prints the label (which gets sent as just s 6x4 image, that's why I'm using a zebra label printer), and the page_printer prints the packing slip(s).
To see the name of all connected printers in python, type:
``` python
import win32print
win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
```
Paste the name of your desired printer into the printpdf.py file.

# Operation
Run the whatnot_ship.py file. This will continue to run and monitor your downloads folder for any pdfs that are newly downloaded.