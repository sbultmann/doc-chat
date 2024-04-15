
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

##load OPENAI_API_KEY from .env
load_dotenv()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=100)

"""from langchain.embeddings import HuggingFaceBgeEmbeddings

model_name = "intfloat/multilingual-e5-large"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
"""
llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.3, max_tokens=4096)
embeddings = OpenAIEmbeddings()

#Prompt tempalte used for query
template = """You are a helpful writing assistent.
Answer as extensive as possible. 
Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Return answer formatted as Mardown.
Context: {context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain

