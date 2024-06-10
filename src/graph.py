from langgraph.graph import END, StateGraph
from .state import GraphState
from .nodes import Nodes

class Workflow():
    def __init__(self, llm, retriever):
        # initiate graph state & nodes
        workflow = StateGraph(GraphState)
        nodes = Nodes(llm, retriever)

        # define all graph nodes
        workflow.add_node("load_new_emails", nodes.load_new_emails)
        workflow.add_node("categorize_email", nodes.categorize_email)
        workflow.add_node("construct_rag_questions", nodes.construct_rag_questions)
        workflow.add_node("retrieve_from_rag", nodes.retrieve_from_rag)
        workflow.add_node("write_draft_email", nodes.write_draft_email)
        workflow.add_node("verify_generated_email", nodes.verify_generated_email)
        workflow.add_node("send_email", nodes.send_email)

        # load new email
        workflow.set_entry_point("load_new_emails")

        # chech if there are email to process
        workflow.add_conditional_edges(
            "load_new_emails",
            nodes.check_new_emails,
            {
                "process": "categorize_email",
                "empty": END
            }
        )

        # recheck for new emails after awaiting
        # workflow.add_edge("wait_next_run", "load_new_emails")

        # route email based on category
        workflow.add_conditional_edges(
            "categorize_email",
            nodes.route_email_based_on_category,
            {
                "product related": "construct_rag_questions",
                "not product related": "write_draft_email",
            }
        )

        # pass constructed query to RAG chain to get informations
        workflow.add_edge("construct_rag_questions", "retrieve_from_rag")
        # give information to writer agent to create draft email
        workflow.add_edge("retrieve_from_rag", "write_draft_email")
        # verify the create draft email
        workflow.add_edge("write_draft_email", "verify_generated_email")
        # check if email is sendable or not, if not rewrite the email
        workflow.add_conditional_edges(
            "verify_generated_email",
            nodes.must_rewrite,
            {
                "send": "send_email",
                "rewrite": "write_draft_email",
                "stop": "categorize_email"
            }
        )

        # check if there are still emails to be processed
        workflow.add_conditional_edges(
            "send_email",
            nodes.check_new_emails,
            {
                "process": "categorize_email",
                "empty": END
            }
        )

        # Compile
        self.app = workflow.compile()