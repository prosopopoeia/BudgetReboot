

class simpleMath():
    
    def addington():
        return 4
        
    def f_avg(aggregate, count):
        return aggregate / count
        

class testy:
    def tess():
        return 'success'    
        
        
class pdfConverter:

    def convert_pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        coder = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr,  laparams=laparams)
        fp = open(path, 'rb')
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
        print(text)
        return text    
