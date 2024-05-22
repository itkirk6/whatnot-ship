import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

cwd = os.getcwd()

import printpdf
prefix, suffix = printpdf.page_path.split(".")

downloads_path = os.path.join("C:\\Users", "User", "Downloads")

def process_pdf(file_path):
    time.sleep(1)
    file_path = os.path.join(downloads_path, file_path)
    printpdf.extract_pdf(file_path)
    printpdf.print_image(printpdf.image_path, printpdf.image_printer)
    
    filtered_files = [file for file in os.listdir(cwd) if file.startswith(prefix) and file.endswith(suffix)]
    
    for file in filtered_files:
        printpdf.print_image(file, printpdf.page_printer)
        os.remove(file)
    
    

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.pdf'):
            print(f"New PDF file detected: {event.src_path}")
            process_pdf(event.src_path)
            
            
def monitor_folder(folder):
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    monitor_folder(downloads_path)
    