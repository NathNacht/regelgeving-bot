import os
import time
from pprint import pprint

from openai import OpenAI
from config import Config
from open_ai_vector_store_loader import get_vector_store_id_by_name


class Assistant:
    def __init__(self, client=None):
        self.client = client if client else OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def get_assistant(self):
        """
        Gets the ArcelorMittal assistant if it exists, otherwise creates it
        :return:
        """
        assistants = self.client.beta.assistants.list().data
        results = []
        for selected_assistant in assistants:
            if selected_assistant.name == Config.ASSITANT_NAME:
                results.append(selected_assistant)
        if results and len(results) > 1:
            print(f"WARNING: Multiple assistants found with name {Config.ASSITANT_NAME}")
        if results:
            return results[0]
        return self.create_assistant()

    def delete_assistants(self):
        """
        Deletes all assistants with the name Config.ASSITANT_NAME
        :return:
        """
        assistants = self.client.beta.assistants.list().data
        for selected_assistant in assistants:
            if selected_assistant.name == Config.ASSITANT_NAME:
                self.client.beta.assistants.delete(selected_assistant.id)

    def create_assistant(self):
        """
        Creates a new assistant with
        :return:
        """
        self.delete_assistants()
        vector_store_id = get_vector_store_id_by_name(Config.VECTOR_STORE_NAME, self.client)
        if not vector_store_id:
            raise Exception(f"Vector store with name {Config.VECTOR_STORE_NAME} not found. First create it, "
                            f"look in the README.md")
        assistant = self.client.beta.assistants.create(
            instructions=Config.PROMPT,
            name=Config.ASSITANT_NAME,
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
            model=Config.MODEL,
        )
        time.sleep(5)
        return assistant

if __name__ == '__main__':
    assistant = Assistant()
    assistant.delete_assistants()