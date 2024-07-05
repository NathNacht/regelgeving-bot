# Project Overview
```mermaid
graph TD;
    A[Main Website] --> B[Scrapy Sitemap Spider];
    A2[Job Website] --> B2[Scrapy Spider];
    B --> C[Website Folder];
    B2 --> C2[Job Folder];
    C --> D[Vector Store Loader];
    C2 --> D;
    D --> E[OpenAI VectorStore];
    E --> F[Streamlit App];
    F --> G[OpenAI Assistant];
    G -.-> E;
    G --> H[🤖 Chat 🤖];
```
## Tree Structure
```
.
├── app.py  # streamlit app
├── assitant.py  # openai assistant
├── config.py
├── open_ai_delete_vector_stores_and_files.py  # deletes all vector stores
├── open_ai_vector_store_loader.py  # loads all vector stores
├── README.md
├── requirements.txt
└── scraper
    ├── data
    │   ├── website  # all website data
    │   └── jobs  # all job data
    ├── scraper
    │   ├── settings.py
    │   └── spiders
    │       ├── arcelormittal-jobs.py  # crawls jobs
    │       └── arcelormittal-website.py  # crawls website
    ├── scrapy.cfg
    └── utils.py  # scrapy utils
```