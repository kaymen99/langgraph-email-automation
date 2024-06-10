from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from .prompts import *

class Agents():
    def __init__(self, llm, retriever):
        # QA assistant chat
        qa_prompt = ChatPromptTemplate.from_template(qa_prompt_template)
        self.retrieve_docs = (
            {"context": retriever, "question": RunnablePassthrough()}
            | qa_prompt
            | llm
            | StrOutputParser()
        )

        # Categorize email chain
        category_prompt = PromptTemplate(
            template=categorize_email_prompt_template, 
            input_variables=["email"]
            )
        self.categorize_email = category_prompt | llm | JsonOutputParser()

        # Used to design queries for RAG retrieval
        query_prompt = PromptTemplate(
            template=rag_query_prompt_template, 
            input_variables=["email"]
            )
        self.design_rag_query = query_prompt | llm | JsonOutputParser()

        # Used to write a draft email based on category and related informations
        draft_prompt = PromptTemplate(
            template=draft_email_prompt_template, 
            input_variables=["category", "email", "informations"]
            )
        self.write_draft_email = draft_prompt | llm | JsonOutputParser()

        # Verify the generated email
        verify_prompt = PromptTemplate(
            template=verify_email_prompt_template, 
            input_variables=["category", "initial_email", "generated_email", "informations"]
            )
        self.verify_email = verify_prompt | llm | JsonOutputParser()