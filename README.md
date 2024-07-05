```mermaid
graph TD;
    website_scraper-->data_website;
    jobs_scraper-->data_jobs;
    data_website-->vector_store_loader;
    data_jobs-->vector_store_loader;
    vector_store_loader-->OpenAi_VectorStore;
    OpenAi_VectorStore-->OpenAi_Assistant;
    OpenAi_Assistant-->Streamlit;
```