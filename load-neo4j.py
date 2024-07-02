import os

from langchain_text_splitters import HTMLHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Neo4jVector

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
]

url = "bolt://localhost:7687"
username = "neo4j"
password = "Neo4jNeo4j"

# loop over all files in the directory ./scraper/data
for filename in os.listdir('./scraper/data'):
    with open(f'./scraper/data/{filename}', 'r', encoding='utf-8') as file:
        html_string = file.read()
        html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        html_header_splits = html_splitter.split_text(html_string)
        db = Neo4jVector.from_documents(
            html_header_splits, OpenAIEmbeddings(), url=url, username=username, password=password
        )
