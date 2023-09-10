from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA




from config import text_splitter, embeddings, QA_CHAIN_PROMPT, llm

def pdf_to_text(pdf_path):
    # Step 1: Convert PDF to images
    images = convert_from_path(pdf_path)

    with open('./docs/uploaded_file.txt', 'w') as f:  # Open the text file in write mode
        for i, image in enumerate(images):
            # Save pages as images in the pdf
            image_file = f'./tmp/page{i}.jpg'
            image.save(image_file, 'JPEG')
            # Step 2: Use OCR to extract text from images
            text = pytesseract.image_to_string(image_file)
            f.write(text + '\n')  # Write the text to the file and add a newline for each page

def load_txt_data(uploaded_file):
    with open('./docs/uploaded_file.txt', 'w') as f:
        f.write(uploaded_file.getvalue().decode())
    return 0

def load_pdf_data(uploaded_file):
    with open('./docs/uploaded_file.pdf', 'wb') as f:
        f.write(uploaded_file.getbuffer())
    """pdf = PdfReader('./docs/uploaded_file.pdf')
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    pdf_to_text('./docs/uploaded_file.pdf')"""
    return 0

def process_document(type):
    if type == "text/plain":
        loader = TextLoader('./docs/uploaded_file.txt').load()
    elif type == "application/pdf":
        loader = PyPDFLoader("./docs/uploaded_file.pdf").load()
    splits = text_splitter.split_documents(loader)
    
    return splits

def process_query(index):
    fetch_k=index._collection.count()
    k = 1+int(fetch_k*0.1)
    if k > 10:
        k = 10
    print(f'vector DB loaded. fetch_k: {fetch_k}, k: {k}')
    qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=index.as_retriever(search_type="mmr",search_kwargs={'k': k, 'fetch_k': fetch_k}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
    return qa_chain