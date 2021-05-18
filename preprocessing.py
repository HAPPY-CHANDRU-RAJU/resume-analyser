from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io, os, sys, json, time
import re, string, unicodedata
import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

resume_scarpped = 0

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def convert_to_html(case,fname, pages=None):
    if not pages: pagenums = set();
    else:         pagenums = set(pages);      
    manager = PDFResourceManager() 
    codec = 'utf-8'
    caching = True
      
    if case == 'HTML' :
        output = io.BytesIO()
        converter = HTMLConverter(manager, output, laparams=LAParams())
 
    interpreter = PDFPageInterpreter(manager, converter)   
    infile = open(fname, 'rb')
 
    for page in PDFPage.get_pages(infile, pagenums,caching=caching, check_extractable=True):
        interpreter.process_page(page)
 
    convertedPDF = output.getvalue()  
 
    infile.close(); converter.close(); output.close()
    return convertedPDF

def lexical_analysis(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    return words

def convert_to_json():
    resume_scarpped = 0
    ids = 399
    for filename in os.listdir(os.getcwd()+"/html-data"):
        ids = ids+1
        with open(os.path.join(os.getcwd()+"/html-data/"+filename),"r", errors='ignore') as rf:
            processed_doc_name = filename[:-5]+"html"
            
            sample = rf.read()

            #beautifulsoup to remove HTML tags
            sample = strip_html(sample)
            sample = sample.strip().lower()
            sample = sample.split("\n")

            #lexical analysis
            sample = lexical_analysis(sample)
            words = list(map(str,sample))

            datas = []
            for w in words[1:]:
                
                #Removal Words
                if w not in ["","•","page 1","resume generator","1 of 1","http://nitish.site/resume-generator/"]: 
                    datas.append(w)

                    # Email Regrex
                    if re.findall('\S+@\S+', w): 
                        lst = re.findall('\S+@\S+', w)

            Did = "1HCR21EG{}".format(ids) #id generator

            #json for resume data
            resume_json = {
                "id": Did,
                "name": datas[0].strip().upper(),
                "mail": lst[0],
                "data": datas,
              }

            file_name = filename[:-5]
            file_name = ''.join(file_name.split())
            file_name = file_name.replace("/", "")
            with open(os.path.join(os.getcwd()+"/processed/"+file_name + ".json"), "w") as output_file:
                json.dump(resume_json, output_file, indent = 2, ensure_ascii = False)

            resume_scarpped += 1
    return resume_scarpped


print("----------------------------------RESUME-------------------------------------------")

fileNAMEs = "resume"
filePDF = "data"
fileHTML = "processed"

if not os.path.isdir(os.path.join(os.getcwd(), filePDF)):
        os.mkdir(filePDF)

if not os.path.isdir(os.path.join(os.getcwd(), fileHTML)):
        os.mkdir(fileHTML)

for filelist in os.listdir(os.getcwd()+"/data"):
    with open(os.path.join(os.getcwd()+"/data/"+filelist),"r", errors='ignore') as rf:
        fileHTML = filelist[:-3]+"html"
        convertedPDF = convert_to_html('HTML', os.path.join(os.getcwd()+"/data/"+filelist), pages=None)
        fileConverted = open(os.path.join(os.getcwd()+"/html-data/"+fileHTML), "wb")
        fileConverted.write(convertedPDF)
        fileConverted.close()

vocabulary = []
resume_no_scarpped = convert_to_json()

print("Successfully")
