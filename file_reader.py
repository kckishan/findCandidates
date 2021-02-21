from PyPDF2 import PdfFileReader
import re
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def process_text(text):
    # replace newline with space
    text = text.replace("\n", " ")
    # convert to lowercase
    text = text.lower()

    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = [t for t in word_tokenize(text) if t not in ENGLISH_STOP_WORDS]

    return " ".join(text)


def resume_reader(resume_file):
    with open(resume_file, 'rb') as pdfObject:
        resumeReader = PdfFileReader(pdfObject)

        resume_text = ""
        name = resumeReader.getDocumentInfo().author
        for i in range(resumeReader.numPages):
            pageObj = resumeReader.getPage(0)
            resume_text += pageObj.extractText()

    return name, process_text(resume_text)


def jobdesc_reader(descr_file):
    with open(descr_file, 'r') as f:
        descr = f.readlines()

    descr = "".join(descr)
    return process_text(descr)
