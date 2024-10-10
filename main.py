from colorama import Fore, Style
from src.graph import Workflow
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load all env variables
load_dotenv()

llm = ChatGroq(model_name="llama-3.1-70b-versatile", temperature=0.1)
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)

# config 
config = {'recursion_limit': 100}

workflow = Workflow(llm)
app = workflow.app

initial_state = {
    "emails": [],
    "current_email": {
      "id": "",
      "sender": "",
      "subject": "",
      "body": ""
    },
    "email_category": "",
    "generated_email": "",
    "rag_questions": [],
    "retrieved_infos": "",
    "review": "",
    "trials": 0
}

# Run the automation
print(Fore.GREEN + "Starting workflow..." + Style.RESET_ALL)
for output in app.stream(initial_state, config):
    for key, value in output.items():
        print(Fore.CYAN + f"Finished running: {key}:" + Style.RESET_ALL)


