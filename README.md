```mermaid
  graph TD;
      arcelormittal-website scraper-->./scraper/data/website;
      crawl arcelormittal-jobs scraper-->./scraper/data/jobs;
      ./scraper/data/website-->open_ai_vector_store_loader.py;
      ./scraper/data/jobs-->open_ai_vector_store_loader.py;
      open_ai_vector_store_loader.py-->OpenAi VectorStore;
      OpenAi VectorStore-->OpenAi Assistant;
      OpenAi Assistant-->Streamlit;
```