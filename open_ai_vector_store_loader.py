import os
from pprint import pprint

from openai import OpenAI


def get_vector_store_id_by_name(name: str, client=None):
    if not client:
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    vector_stores = client.beta.vector_stores.list()
    for selected_vector_store in vector_stores.data:
        if selected_vector_store.name == name:
            return selected_vector_store.id
    return None


def upload_files_to_vector_store(directory_paths: list, vector_store_name: str, client=None):
    if not client:
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    vector_store = get_vector_store_id_by_name(vector_store_name, client)
    if not vector_store:
        print(f"Vector store with name {vector_store_name} not found. Creating new vector store.")
        vector_store = client.beta.vector_stores.create(name=vector_store_name)

    # List all the files in the directory
    file_paths = []
    for directory_path in directory_paths:
        file_paths.extend([os.path.join(directory_path, filename) for filename in os.listdir(directory_path)])

    file_streams = []
    for path in file_paths:
        f = open(path, "rb")
        print(f"Opening file {path} for upload")
        file_streams.append(f)

    # Use the upload and poll SDK helper to upload the files
    for file_stream in file_streams:
        print(f"Uploading file {file_stream}")
        file_stream = [file_stream]
        try:
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_stream
            )
            pprint(file_batch)
        except Exception as e:
            print(f"Error uploading batch: {e}")

    return vector_store


if __name__ == '__main__':
    vector_store = upload_files_to_vector_store(["./scraper/data/website", "./scraper/data/jobs"], "ArcelorMittal")
    print(f"uploaded all documents to {vector_store.id}")