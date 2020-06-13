#! python3

import enum
import re
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


class eMonth(enum.Enum):
    January     = 1
    February    = 2
    March       = 3
    April       = 4
    May         = 5
    June        = 6
    July        = 7
    August      = 8
    September   = 9
    October     = 10
    November    = 11
    December    = 12
    
class utils:

    def tessy():
        return 'success'
    
    def calculateDayOfMonth(daynum):
        return eMonth(daynum)
        
        
        
class pdfHandler:

    def pdf_to_txt(pdfpath):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        coder = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr,  laparams=laparams)
        fp = open(pdfpath, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        fp.close()
        device.close()
        text = retstr.getvalue()
        retstr.close()
        #print(text)
        return text    
        
    """take block of data and sort between seen and not seen 
     if the source is known, add entry to db
    // if the source is new, have user categorize, then add to db"""
    
    def parsePdf(pdfpath):
        pdfContents = pdfHandler.pdf_to_txt(pdfpath)
        
        entries = re.findall(r'\d\d/\d\d\s+\d+\.\d\d\s+[A-Z\s]+', pdfContents)
                
        for entry in entries:
            print(entry)
       

if __name__ == "__main__":
   pdfHandler.parsePdf('C:/Users/ngwtt/source/repos/djangoRepo/BudgetReboot/AmazingBudgetSite/tst.pdf')     
        
        