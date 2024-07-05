```mermaid
  graph TD;
      website scraper-->./data/website;
      jobs scraper-->./data/jobs;
      ./data/website-->vector store loader;
      ./data/jobs-->vector store loader;
      vector store loader-->OpenAi VectorStore;
      OpenAi VectorStore-->OpenAi Assistant;
      OpenAi Assistant-->Streamlit;
```