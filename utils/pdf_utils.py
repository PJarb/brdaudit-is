from pypdf import PdfReader
import tempfile

def extract_pdf_to_text(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        reader = PdfReader(tmp.name)

    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text
