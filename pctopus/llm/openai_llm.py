import os
from typing import Optional, List, Dict, Any
import openai
from dotenv import load_dotenv
from pctopus.llm.base import BaseLLM

class OpenAILLM(BaseLLM):
    """Class for interacting with OpenAI Large Language Models"""

    def __init__(self):
        """Initializes the OpenAI LLM client"""
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')

        self.client = openai.OpenAI(api_key = api_key)

    def ask(self,
            prompt: str,
            system_message: Optional[str] = None,
            model: str = "gpt-3.5-turbo") -> str:
        """Method to get response from an OpenAI LLM. 

        Args:
            prompt: The prompt to the LLM, which includes user's message and context
            system_message: Optional system message to control the LLM's behavior
            model: The model to use (default: gpt-3.5-turbo)

        Returns:
            The model's response as a string
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )

        return response.choices[0].message.content

    