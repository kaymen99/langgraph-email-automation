import os, re
from colorama import Fore, Style
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft
from langchain_community.tools.gmail.search import GmailSearch
from .agents import Agents

class Nodes:
    """
    The graph consists on the following nodes:
      * Load new emails
      * Categorize email
      * Design RAG queries
      * Retrieve from RAG
      * Write draft email
      * Verify generated email
    """

    def __init__(self, llm, retriever):
        """
        Initialize the Nodes class with language model and retriever.

        @param llm: The language model to be used for generating responses.
        @param retriever: The retriever to be used for fetching relevant information.
        """
        self.agents = Agents(llm, retriever)
        self.gmail = GmailToolkit()

    def load_new_emails(self, state):
        """
        Load new emails from the Gmail account.

        @param state: The current state of the application.
        @return: Updated state with new emails and viewed email IDs.
        """
        print(Fore.YELLOW + "Loading new emails...\n" + Style.RESET_ALL)
        search = GmailSearch(api_resource=self.gmail.api_resource)
        emails = search('newer_than:1d')
        viewed_emails = state['viewed_emails_ids'] if state['viewed_emails_ids'] else []
        thread = []
        new_emails = []
        for email in emails:
            if (email['id'] not in viewed_emails) and (email['threadId'] not in thread) and (os.environ['MY_EMAIL'] not in email['sender']):
                sender = re.search(r'<([^>]+)>', email["sender"]).group(1)
                thread.append(email['threadId'])
                new_emails.append(
                    {
                    "id": email['id'],
                    "threadId": email['threadId'],
                    "snippet": email['snippet'],
                    "sender": sender
                    }
                )
        viewed_emails.extend([email['id'] for email in emails])
        return {
            **state,
            "emails": new_emails,
            "viewed_emails_ids": viewed_emails
        }

    def check_new_emails(self, state):
        """
        Check if there are new emails to process.

        @param state: The current state of the application.
        @return: "empty" if no new emails, otherwise "process".
        """
        print(Fore.CYAN + str(state['emails']) + Style.RESET_ALL)
        if len(state['emails']) == 0:
            print(Fore.RED + "No new emails" + Style.RESET_ALL)
            return "empty"
        else:
            print(Fore.GREEN + "New emails to process" + Style.RESET_ALL)
            return "process"

    # def wait_next_run(self, state):
    #     print("Processed all emails, waiting for next run!!!")
    #     time.sleep(3600)
    #     return state

    def categorize_email(self, state):
        """
        Categorize the current email.

        @param state: The current state of the application.
        @return: Updated state with email category and sender information.
        """
        print(Fore.YELLOW + "Checking email category...\n" + Style.RESET_ALL)
        emails = state["emails"]
        current_email = emails[-1]
        category_result = self.agents.categorize_email.invoke({"email": current_email})
        print(Fore.MAGENTA + "Email category:" + Style.RESET_ALL, category_result["category"])
        return {
            **state, 
            "email_category": category_result["category"],
            "email_sender": current_email["sender"]
        }

    def route_email_based_on_category(self, state):
        """
        Route the email based on its category.

        @param state: The current state of the application.
        @return: "product related" if the category is product or price enquiry, otherwise "not product related".
        """
        print(Fore.YELLOW + "Routing email based on category...\n" + Style.RESET_ALL)
        category = state["email_category"]
        if category == "product_enquiry":
            return "product related"
        else:
            return "not product related"

    def construct_rag_questions(self, state):
        """
        Design RAG (Retrieval-Augmented Generation) queries based on the email.

        @param state: The current state of the application.
        @return: Updated state with RAG questions.
        """
        print(Fore.YELLOW + "Designing RAG query...\n" + Style.RESET_ALL)
        emails = state["emails"]
        current_email = emails[-1]
        query_result = self.agents.design_rag_query.invoke({"email": current_email})
        return {**state, "rag_questions": query_result["query"]}

    def retrieve_from_rag(self, state):
        """
        Retrieve information from internal knowledge based on RAG queries.

        @param state: The current state of the application.
        @return: Updated state with retrieved information.
        """
        print(Fore.YELLOW + "Retrieving information from internal knowledge...\n" + Style.RESET_ALL)
        queries = state["rag_questions"]
        final_answer = ""
        for query in queries:
            rag_result = self.agents.retrieve_docs.invoke(query)
            final_answer += query + "\n" + rag_result + "\n\n"
        return {**state, "retrieved_infos": final_answer}

    def write_draft_email(self, state):
        """
        Write a draft email based on the retrieved information and email category.

        @param state: The current state of the application.
        @return: Updated state with the generated email, subject, and number of trials.
        """
        print(Fore.YELLOW + "Writing draft email...\n" + Style.RESET_ALL)
        emails = state["emails"]
        current_email = emails[-1]
        draft_result = self.agents.write_draft_email.invoke({
            "email": current_email,
            "category": state["email_category"],
            "informations": state["retrieved_infos"]
        })
        email = draft_result["email"]
        subject = draft_result["subject"]
        if state['trials'] is None:
            state['trials'] = 0
        trials = int(state['trials'])
        trials += 1
        return {
            **state, 
            "email_subject": subject, 
            "generated_email": email, 
            "trials": trials
        }

    def verify_generated_email(self, state):
        """
        Verify the generated email.

        @param state: The current state of the application.
        @return: Updated state with the review result.
        """
        print(Fore.YELLOW + "Verifying generated email...\n" + Style.RESET_ALL)
        emails = state["emails"]
        current_email = emails[-1]
        verify_result = self.agents.verify_email.invoke({
            "initial_email": current_email,
            "category": state["email_category"],
            "generated_email": state["generated_email"],
            "informations": state["retrieved_infos"]
        })
        review = verify_result["review"]
        return {**state, "review": review}

    def must_rewrite(self, state):
        """
        Determine if the email must be rewritten based on the review result.

        @param state: The current state of the application.
        @return: "send" if the email is ready to be sent, "stop" if max trials reached, otherwise "rewrite".
        """
        review = state["review"]
        if review == "send":
            print(Fore.GREEN + "Email is good, ready to be sent!!!" + Style.RESET_ALL)
            # remove processed email
            state["emails"].pop()
            return "send"
        elif state["trials"] >= 3:
            print(Fore.RED + "Email is not good, we reached max trials must stop!!!" + Style.RESET_ALL)
            # remove processed email
            state["emails"].pop()
            return "stop"
        else:
            print(Fore.RED + "Email is not good, must rewrite it..." + Style.RESET_ALL)
            return "rewrite"

    def send_email(self, state):
        """
        Send the generated email.

        @param state: The current state of the application.
        @return: The updated state after sending the email.
        """
        print(Fore.YELLOW + "Sending email...\n" + Style.RESET_ALL)
        # send email
        draft = GmailCreateDraft(api_resource=self.gmail.api_resource)
        result = draft({
            'to': [state["email_sender"]],
            'subject': state["email_subject"],
            'message': state["generated_email"]
        })
        return state
