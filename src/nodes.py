import os
from colorama import Fore, Style
from .agents import Agents
from .tools.GmailTools import GmailToolsClass
from .state import GraphState, Email


class Nodes:
    def __init__(self, llm):
        self.agents = Agents(llm)
        self.gmail_tools = GmailToolsClass()

    def load_new_emails(self, state: GraphState) -> GraphState:
        """
        Loads new emails from Gmail and updates the state.

        @param state: The current state of the graph.
        @return: Updated state with new emails.
        """
        print(Fore.YELLOW + "Loading new emails...\n" + Style.RESET_ALL)
        recent_emails = self.gmail_tools.fetch_recent_emails()
        # Only keep received emails
        emails = [Email(**email) for email in recent_emails if (os.environ['MY_EMAIL'] not in email['sender'])]
        return {**state, "emails": emails}

    def check_new_emails(self, state: GraphState) -> str:
        """
        Checks if there are new emails to process.

        @param state: The current state of the graph.
        @return: 'process' if there are new emails, 'empty' otherwise.
        """
        if len(state['emails']) == 0:
            print(Fore.RED + "No new emails" + Style.RESET_ALL)
            return "empty"
        else:
            print(Fore.GREEN + "New emails to process" + Style.RESET_ALL)
            return "process"

    def categorize_email(self, state: GraphState) -> GraphState:
        """
        Categorizes the current email using the categorize_email agent.

        @param state: The current state of the graph.
        @return: Updated state with email category.
        """
        print(Fore.YELLOW + "Checking email category...\n" + Style.RESET_ALL)
        current_email = state["emails"][-1]
        category_result = self.agents.categorize_email.invoke({"email": current_email.body})
        print(Fore.MAGENTA + "Email category:" + Style.RESET_ALL, category_result["category"])
        return {
            **state, 
            "email_category": category_result["category"],
            "current_email": current_email
        }

    def route_email_based_on_category(self, state: GraphState) -> str:
        """
        Routes the email based on its category.

        @param state: The current state of the graph.
        @return: 'product related' or 'not product related' based on the email category.
        """
        print(Fore.YELLOW + "Routing email based on category...\n" + Style.RESET_ALL)
        category = state["email_category"]
        if category == "product_enquiry":
            return "product related"
        else:
            return "not product related"

    def construct_rag_questions(self, state: GraphState) -> GraphState:
        """
        Constructs RAG questions based on the email content.

        @param state: The current state of the graph.
        @return: Updated state with RAG questions.
        """
        print(Fore.YELLOW + "Designing RAG query...\n" + Style.RESET_ALL)
        email_content = state["current_email"].body
        query_result = self.agents.design_rag_query.invoke({"email": email_content})
        return {**state, "rag_questions": query_result["query"]}

    def retrieve_from_rag(self, state: GraphState) -> GraphState:
        """
        Retrieves information from internal knowledge based on RAG questions.

        @param state: The current state of the graph.
        @return: Updated state with retrieved information.
        """
        print(Fore.YELLOW + "Retrieving information from internal knowledge...\n" + Style.RESET_ALL)
        queries = state["rag_questions"]
        final_answer = ""
        for query in queries:
            rag_result = self.agents.retrieve_docs.invoke(query)
            final_answer += query + "\n" + rag_result + "\n\n"
        return {**state, "retrieved_documents": final_answer}

    def write_draft_email(self, state: GraphState) -> GraphState:
        """
        Writes a draft email based on the current email and retrieved information.

        @param state: The current state of the graph.
        @return: Updated state with generated email and trial count.
        """
        print(Fore.YELLOW + "Writing draft email...\n" + Style.RESET_ALL)
        draft_result = self.agents.write_draft_email.invoke({
            "email": state["current_email"].body,
            "subject": state["current_email"].subject,
            "category": state["email_category"],
            "informations": state["retrieved_documents"]
        })
        email = draft_result["email"]
        trials = state.get('trials', 0) + 1
        return {
            **state, 
            "generated_email": email, 
            "trials": trials
        }

    def verify_generated_email(self, state: GraphState) -> GraphState:
        """
        Verifies the generated email using the verify_email agent.

        @param state: The current state of the graph.
        @return: Updated state with email review.
        """
        print(Fore.YELLOW + "Verifying generated email...\n" + Style.RESET_ALL)
        verify_result = self.agents.verify_email.invoke({
            "initial_email": state["current_email"].body,
            "category": state["email_category"],
            "generated_email": state["generated_email"],
            "informations": state["retrieved_documents"]
        })
        review = verify_result["review"]
        return {**state, "review": review}

    def must_rewrite(self, state: GraphState) -> str:
        """
        Determines if the email needs to be rewritten based on the review and trial count.

        @param state: The current state of the graph.
        @return: 'send' if email is good, 'stop' if max trials reached, 'rewrite' otherwise.
        """
        review = state["review"]
        if review == "send":
            print(Fore.GREEN + "Email is good, ready to be sent!!!" + Style.RESET_ALL)
            state["emails"].pop()
            return "send"
        elif state["trials"] >= 3:
            print(Fore.RED + "Email is not good, we reached max trials must stop!!!" + Style.RESET_ALL)
            state["emails"].pop()
            return "stop"
        else:
            print(Fore.RED + "Email is not good, must rewrite it..." + Style.RESET_ALL)
            return "rewrite"

    def create_draft_response(self, state: GraphState) -> GraphState:
        """
        Creates a draft response in Gmail.

        @param state: The current state of the graph.
        @return: Updated state with reset trial count.
        """
        print(Fore.YELLOW + "Creating draft email...\n" + Style.RESET_ALL)
        self.gmail_tools.create_draft_reply(
            state["current_email"].id,
            state["current_email"].sender,
            f"Re: {state['current_email'].subject}",
            state["generated_email"]
        )
        return {"trials": 0}

    def send_email_response(self, state: GraphState) -> GraphState:
        """
        Sends the email response directly using Gmail.

        @param state: The current state of the graph.
        @return: Updated state with reset trial count.
        """
        print(Fore.YELLOW + "Sending email...\n" + Style.RESET_ALL)
        self.gmail_tools.send_reply(
            state["current_email"].id,
            state["current_email"].sender,
            f"Re: {state['current_email'].subject}",
            state["generated_email"]
        )
        return {"trials": 0}