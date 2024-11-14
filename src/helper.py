
from langchain.document_loaders import PyPDFLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf(data):
    loader = DirectoryLoader(data , 
                             glob="*.pdf",
                             loader_cls=PyPDFLoader)
    document = loader.load()

    return document



def text_split(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500 , chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(data)
    return text_chunks
