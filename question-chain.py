from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI

graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="Neo4jNeo4j",
)

chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0.1),
    graph=graph,
    verbose=True,
)

result = chain.invoke({"query": "What kind of materials does arcelormittal produce?"})

print(result)