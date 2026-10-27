import time

from colorama import Fore, Style
from dotenv import load_dotenv

from src.graph import Workflow

# Load all env variables
load_dotenv()

config = {"recursion_limit": 100}
poll_interval_seconds = 300



workflow = Workflow()
app = workflow.app


def run_workflow() -> None:
    initial_state = {
        "emails": [],
        "current_email": {
            "id": "",
            "threadId": "",
            "messageId": "",
            "references": "",
            "sender": "",
            "subject": "",
            "body": "",
        },
        "email_category": "",
        "generated_email": "",
        "rag_queries": [],
        "retrieved_documents": "",
        "writer_messages": [],
        "sendable": False,
        "trials": 0,
    }

    print(Fore.GREEN + "Checking inbox for new emails..." + Style.RESET_ALL)
    for output in app.stream(initial_state, config):
        for key in output:
            print(Fore.CYAN + f"Finished running: {key}:" + Style.RESET_ALL)


if __name__ == "__main__":
    print(
        Fore.GREEN
        + "Starting email polling loop. Press Ctrl+C to stop."
        + Style.RESET_ALL
    )
    try:
        while True:
            run_workflow()
            print(
                Fore.YELLOW
                + "Waiting 5 minutes before the next inbox check..."
                + Style.RESET_ALL
            )
            time.sleep(poll_interval_seconds)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nEmail polling stopped." + Style.RESET_ALL)
