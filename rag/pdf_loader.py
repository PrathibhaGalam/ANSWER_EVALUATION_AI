from PyPDF2 import PdfReader


def load_pdfs(uploaded_files):

    texts = []

    for file in uploaded_files:
        pdf = PdfReader(file)
        text = ""

        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content

        texts.append({
            "filename": file.name,
            "text": text
        })

    return texts