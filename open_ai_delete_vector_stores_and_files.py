import os
from datetime import datetime

import openai

client = openai.Client(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.files.list(purpose="assistants")
files = list(response.data)
for selected_file in files:
    client.files.delete(selected_file.id)
    print(f"File deleted: {selected_file.filename}")

vector_stores = client.beta.vector_stores.list()
for selected_vector_store in vector_stores.data:
    client.beta.vector_stores.delete(selected_vector_store.id)
    print(f"Vector store deleted: {selected_vector_store.id}")