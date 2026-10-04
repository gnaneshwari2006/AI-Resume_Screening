from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_docx_text(file):
    document = Document(file)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text


def extract_text(file):
    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf_text(file)
    elif file_name.endswith(".docx"):
        return extract_docx_text(file)

    return ""
