from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# load agency docs
loader = TextLoader("./data/agency.txt")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
text_chunks = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# will automaticly convert given text chunks into vector using provided embeddings
# then we will store into FAISS DB
vectorstore = FAISS.from_documents(text_chunks, embeddings)

# save localy vectorstore
vectorstore.save_local("faiss_index")