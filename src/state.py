from pydantic import BaseModel, Field
from typing import List, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class Email(BaseModel):
    id: str = Field(..., description="Unique identifier of the email")
    threadId: str = Field(..., description="Thread identifier of the email")
    messageId: str = Field(..., description="Message identifier of the email")
    references: str = Field(..., description="References of the email")
    sender: str = Field(..., description="Email address of the sender")
    subject: str = Field(..., description="Subject line of the email")
    body: str = Field(..., description="Body content of the email")
    
class GraphState(TypedDict):
    emails: List[Email]
    current_email: Email
    email_category: str
    generated_email: str
    rag_queries: List[str]
    retrieved_documents: str
    writer_messages: Annotated[list, add_messages]
    sendable: bool
    trials: int