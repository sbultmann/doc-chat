from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

##load OPENAI_API_KEY from .env
load_dotenv()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)


llm = ChatOpenAI(model_name="gpt-4", temperature=0.3, max_tokens=4095)
embeddings = OpenAIEmbeddings()