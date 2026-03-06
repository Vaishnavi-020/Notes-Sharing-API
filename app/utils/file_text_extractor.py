from pypdf import PdfReader
from docx import Document
import os

def extract_text(file_path:str):
    extension=os.path.splitext(file_path)[1].lower()
    if extension==".pdf":
        return extract_pdf(file_path)
    elif extension==".docx":
        return extract_docx(file_path)
    else:
        return ""
    
def extract_pdf(file_path):
    reader=PdfReader(file_path)
    text=""
    for page in reader.pages:
        page_text=page.extract_text()
        if page_text:
            text+=page_text
    return text

def extract_docx(file_path):
    doc=Document(file_path)
    text=""
    for para in doc.paragraphs:
        text+=para.text+"\n"
    return text
