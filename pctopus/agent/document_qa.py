from typing import Optional, Dict, Any
from pctopus.llm.base import BaseLLM
from pctopus.reader.document_reader import DocumentReader

class DocumentQAAgent:
    """Agent for answering questions based on document content."""

    DEFAULT_SYSTEM_INSTRUCTION = """
    Use the provided context to answer the question. 
    If you cannot find the answer from the provided context, say "I cannot find the answer in the provided context."
    """

    def __init__(self, llm: BaseLLM):
        """Initialize the QA agent.

        Args:
            llm: Langauge model to use 
        """
        self.llm = llm
        self.reader = DocumentReader()

    def ask(self,
            document_path: str,
            question: str,
            system_message: Optional[str] = DEFAULT_SYSTEM_INSTRUCTION,
            model: str = "gpt-3.5-turbo") -> str:
            """Ask a question about a document based on its text content.

            Args:
                document_path: Path to the document to analyze
                question: User's question
                system_message: Optional system instruction for the LLM. By default, it uses the `DEFAULT_SYSTEM_INSTRUCTION` 
                model: Model to use (default: gpt-3.5-turbo)
            
            Returns:
                The agent's response as a string
            """
            try:
                document_content = self.reader.read(document_path)

                question_with_context = f"""
                Context: {document_content}
                Question: {question}
                """

                response = self.llm.ask(
                    prompt=question_with_context,
                    system_message=system_message,
                    model=model
                )
                return response

            except Exception as e:
                raise Exception(f"Error processing the document: {str(e)}")
