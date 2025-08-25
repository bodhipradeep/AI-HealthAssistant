from langchain.document_loaders import PyPDFLoader

def medical_report(pdf_path: str) -> str:
    try:
        pdf = PyPDFLoader(pdf_path)
        load = pdf.load()
        return load[0].page_content
    except Exception:
        return "Report not uploaded"