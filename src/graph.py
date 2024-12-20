from langgraph.graph import END, StateGraph
from .state import GraphState
from .nodes import Nodes

class Workflow():
    def __init__(self):
        # initiate graph state & nodes
        workflow = StateGraph(GraphState)
        nodes = Nodes()

        # define all graph nodes
        workflow.add_node("load_new_emails", nodes.load_new_emails)
        workflow.add_node("is_email_inbox_empty", nodes.is_email_inbox_empty)
        workflow.add_node("categorize_email", nodes.categorize_email)
        workflow.add_node("construct_rag_queries", nodes.construct_rag_queries)
        workflow.add_node("retrieve_from_rag", nodes.retrieve_from_rag)
        workflow.add_node("email_writer", nodes.write_draft_email)
        workflow.add_node("email_proofreader", nodes.verify_generated_email)
        workflow.add_node("send_email", nodes.create_draft_response)
        workflow.add_node("skip_unrelated_email", nodes.skip_unrelated_email)

        # load new email
        workflow.set_entry_point("load_new_emails")

        # chech if there are email to process
        workflow.add_edge("load_new_emails", "is_email_inbox_empty")
        workflow.add_conditional_edges(
            "is_email_inbox_empty",
            nodes.check_new_emails,
            {
                "process": "categorize_email",
                "empty": END
            }
        )

        # route email based on category
        workflow.add_conditional_edges(
            "categorize_email",
            nodes.route_email_based_on_category,
            {
                "product related": "construct_rag_queries",
                "not product related": "email_writer",
                "unrelated": "skip_unrelated_email"
            }
        )

        # pass constructed query to RAG chain to get informations
        workflow.add_edge("construct_rag_queries", "retrieve_from_rag")
        # give information to writer agent to create draft email
        workflow.add_edge("retrieve_from_rag", "email_writer")
        # verify the create draft email
        workflow.add_edge("email_writer", "email_proofreader")
        # check if email is sendable or not, if not rewrite the email
        workflow.add_conditional_edges(
            "email_proofreader",
            nodes.must_rewrite,
            {
                "send": "send_email",
                "rewrite": "email_writer",
                "stop": "categorize_email"
            }
        )

        # check if there are still emails to be processed
        workflow.add_edge("send_email", "is_email_inbox_empty")
        workflow.add_edge("skip_unrelated_email", "is_email_inbox_empty" )

        # Compile
        self.app = workflow.compile()