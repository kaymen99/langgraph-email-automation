from pprint import pprint
from colorama import Fore, Style
from src.graph import Workflow
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load all env variables
load_dotenv()

llm = ChatGroq(model_name="llama3-70b-8192", temperature=0.8)

print(Fore.YELLOW + "Loading embedding model from HuggingFace" + Style.RESET_ALL)
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

print(Fore.YELLOW + "Loading local vector store" + Style.RESET_ALL)
new_vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = new_vector_store.as_retriever()

workflow = Workflow(llm, retriever)
app = workflow.app

# Run the agent
print(Fore.GREEN + "Starting workflow..." + Style.RESET_ALL)
for output in app.stream({}):
    for key, value in output.items():
        pprint(Fore.CYAN + f"Finished running: {key}:" + Style.RESET_ALL)


