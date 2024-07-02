import os
from pprint import pprint

from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings


db = Neo4jVector.from_existing_graph(
    embedding=OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY')),
    url="bolt://localhost:7687",
    username="neo4j",
    password="Neo4jNeo4j",
    embedding_node_property="embedding",
    text_node_properties=["text"],
    node_label="Chunk",
)

query = "What kind of materials does arcelormittal produce?"
docs_with_score = db.similarity_search_with_score(query=query, k=10)
pprint(docs_with_score)

def question_answer_workflow_with_langchain(index_name, query):
    try:
        print(f"\nQuestion/Answer workflow with LangChain\n\tQuery: {query}\n")

        neo4j_vector = initialize_neo4j_vector(neo4j_credentials, index_name)

        # Initialize and execute the QA workflow
        qa_workflow = initialize_qa_workflow(
            neo4j_vector, neo4j_credentials["openai_api_secret_key"]
        )

        qa_results = execute_qa_workflow(
            neo4j_vector, qa_workflow, query, neo4j_credentials["openai_api_secret_key"]
        )
        print(qa_results["answer"])

        # Close the Neo4j connection
        neo4j_vector._driver.close()

    except Exception as e:
        print(f"\n\tAn unexpected error occurred: {e}")