from src.helper import  text_split , load_pdf
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder
from langchain.retrievers import PineconeHybridSearchRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings
data =  load_pdf("data/")

text_chunk = text_split(data)

pc = Pinecone(
        api_key=""
    )
index_name1 = "sarthi"
if index_name1 not in pc.list_indexes().names():
    pc.create_index(
            name=index_name1,
            dimension=384,
            metric='dotproduct',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
index = pc.Index(index_name1)
bm25encoder = BM25Encoder().default()
bm25encoder.fit([t.page_content for t in text_chunk])
bm25encoder.dump("bm25encoder_values.json")
bm25_encoder = BM25Encoder().load("bm25encoder_values.json")
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
retreiver = PineconeHybridSearchRetriever(embeddings=embedding , sparse_encoder=bm25_encoder , index=index)