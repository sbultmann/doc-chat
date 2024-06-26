from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.llms import OpenAI


# Wrap our vectorstore
#llm_compression = OpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, max_tokens=11000)


from config import text_splitter, embeddings, QA_CHAIN_PROMPT, llm

compressor = LLMChainExtractor.from_llm(llm)

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
    with open(f'./docs/{uploaded_file.name}.txt', 'w') as f:
        f.write(uploaded_file.getvalue().decode())
    return 0

def load_pdf_data(uploaded_file):
    with open(f'./docs/{uploaded_file.name}.pdf', 'wb') as f:
        f.write(uploaded_file.getbuffer())
    """pdf = PdfReader('./docs/uploaded_file.pdf')
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    pdf_to_text('./docs/uploaded_file.pdf')"""
    return 0

def process_document(type, uploaded_file):
    if type == "text/plain":
        loader = TextLoader(f'./docs/{uploaded_file.name}.txt').load()
    elif type == "application/pdf":
        loader = PyPDFLoader(f"./docs/{uploaded_file.name}.pdf").load()
    splits = text_splitter.split_documents(loader)
    
    return splits

def process_query(index):
    fetch_k=index._collection.count()
    k = 1+int(fetch_k*0.1)
    if k > 11:
        k = 11
        fetch_k = 110
    print(f'vector DB loaded. fetch_k: {fetch_k}, k: {k}')
    qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=index.as_retriever(search_type="mmr",search_kwargs={'k': k, 'fetch_k': fetch_k}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
    return qa_chain

def process_query2(index):
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=index.as_retriever(search_kwargs={'k': 20})
    )
    qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=compression_retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
    return qa_chain

