class Assistant():
    # brain of the chatbot
    def __init__(
        self,
        system_prompt,
        llm,
        message_history=None,
        vector_store=None,
        employee_information=None
    ):
        self.system_prompt = system_prompt
        self.llm = llm
        self.message_history = message_history or []
        self.vector_store = vector_store
        self.employee_information = employee_information

        self.chain = self._get_conversation_chain()

    def get_response(self, user_input):
        return self.chain.stream({"user_input": user_input})

    def _get_conversation_chain(self):

        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough

        prompt = ChatPromptTemplate(
            # Defines the message structure given to the LLM
            [
                ("system", self.system_prompt),
                MessagesPlaceholder("conversation_history"),
                ("human", "{user_input}")
            ]
        )

        # Store the LLM Reference
        llm = self.llm

        # Define the Output Parser
        output_parser = StrOutputParser()

        # Build the Chain
        # Think of it as a dataflow pipeline, where each step processes and passes data to the next:
        # User Input ───▶ Context Dictionary ───▶ Prompt ───▶ LLM ───▶ Output Parser ───▶ Final Response

        chain = (
            {
                # Uses your vector DB retriever to fetch policy chunks based on the question.
                "retrieved_policy_information": (
                    lambda x: self.vector_store.as_retriever().invoke(
                        x["user_input"] if isinstance(x, dict) else x
                    )
                    if self.vector_store else None
                ),
                # A small function that injects employee info (so the model can personalize answers).
                "employee_information": lambda x: self.employee_information,
                # Passes the raw user input directly into the prompt.
                "user_input": RunnablePassthrough(),
                # Injects the ongoing chat history.
                "conversation_history": lambda x: self.message_history,
            }  # Each of these entries fills a {placeholder} in your SYSTEM_PROMPT or prompt template.
            | prompt
            | llm
            | output_parser
        )
        return chain
